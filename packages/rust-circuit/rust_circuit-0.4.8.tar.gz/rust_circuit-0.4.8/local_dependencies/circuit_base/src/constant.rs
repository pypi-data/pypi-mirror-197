use anyhow::{bail, Result};
use base16::encode_lower;
use macro_rules_attribute::apply;
use pyo3::{
    prelude::*,
    types::{IntoPyDict, PyTuple},
};
use rr_util::{
    lru_cache::TensorCacheRrfs,
    name::Name,
    py_types::{Tensor, PY_UTILS},
    shape::{shape_as_known_result, shape_is_known},
    sv,
    tensor_db::{get_tensor_prefix, save_tensor},
    tensor_util::TorchDeviceDtypeOp,
};
use rustc_hash::FxHashMap as HashMap;
use uuid::Uuid;

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    new_rc, new_rc_unwrap,
    prelude::*,
    CachedCircuitInfo, CircuitFlags, PyCircuitBase, Shape,
};

macro_rules! circuit_node_auto_leaf_impl {
    ($uuid:literal) => {
        circuit_node_auto_impl!($uuid, no_autoname);

        fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
            vec![]
        }

        fn map_children_enumerate<F>(&self, _f: F) -> Result<Self>
        where
            F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
        {
            Ok(self.clone())
        }

        fn _replace_children(&self, _children: Vec<CircuitRc>) -> Result<Self> {
            Ok(self.clone())
        }
    };
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Array {
    #[pyo3(get)]
    pub value: Tensor,
    info: CachedCircuitInfo,
}

circuit_node_extra_impl!(Array, self_hash_default);

impl CircuitNodeComputeInfoImpl for Array {}

impl CircuitNodeHashItems for Array {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(self.value.hash().unwrap());
    }
}

impl CircuitNode for Array {
    circuit_node_auto_leaf_impl!("b2aac9d5-1bfa-4c2a-9684-e3f9ecbc1b94");
}

impl Array {
    #[apply(new_rc_unwrap)]
    pub fn try_new(value: Tensor, name: Option<Name>) -> Result<Self> {
        let value = value.hashed()?;
        let out = Self {
            info: CachedCircuitInfo::with_device_dtype(
                name,
                value.shape().clone(),
                vec![],
                value.device_dtype().into(),
            ),
            value,
        };
        out.initial_init_info()
    }
    pub fn from_hash_prefix(
        name: Option<Name>,
        hash_base16: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        if let Some(tc) = tensor_cache {
            return tc
                .get_tensor(hash_base16.to_owned())
                .map(|value| Array::new(value, name));
        }
        get_tensor_prefix(hash_base16).map(|value| Array::new(value, name))
    }

    pub fn randn(shape: Shape) -> Result<Self> {
        Self::randn_full(shape, None, TorchDeviceDtypeOp::TENSOR_DEFAULT, None)
    }

    pub fn randn_named(
        shape: Shape,
        name: Option<Name>,
        device_dtype: TorchDeviceDtypeOp,
    ) -> Result<Self> {
        Self::randn_full(shape, name, device_dtype, None)
    }
}

#[pymethods]
impl Array {
    #[new]
    #[pyo3(signature=(value, name = None))]
    fn py_new(value: Tensor, name: Option<Name>) -> Result<PyClassInitializer<Self>> {
        Ok(Array::try_new(value, name)?.into_init())
    }

    #[staticmethod]
    #[pyo3(name = "randn", signature=(
        *shape,
        name = None,
        device_dtype = TorchDeviceDtypeOp::TENSOR_DEFAULT,
        seed = None
    ))]
    pub fn randn_full(
        shape: Shape,
        name: Option<Name>,
        device_dtype: TorchDeviceDtypeOp,
        seed: Option<usize>,
    ) -> Result<Self> {
        Python::with_gil(|py| {
            if let Some(seed) = seed {
                PY_UTILS
                    .torch
                    .getattr(py, "manual_seed")
                    .unwrap()
                    .call(py, (seed,), None)
                    .unwrap();
            }

            let mut kwargs = HashMap::default();
            if let Some(dtype) = device_dtype.dtype {
                let dtype: &str = &String::from(&dtype);
                kwargs.insert("dtype", PY_UTILS.torch.getattr(py, dtype).unwrap());
            }
            if let Some(device) = device_dtype.device {
                kwargs.insert("device", device.into_py(py));
            }
            Array::try_new(
                PY_UTILS
                    .torch
                    .getattr(py, "randn")
                    .unwrap()
                    .call(
                        py,
                        (PyTuple::new(py, shape_as_known_result(&shape)?),),
                        Some(kwargs.into_py_dict(py)),
                    )
                    .unwrap()
                    .extract(py)
                    .unwrap(),
                name,
            )
        })
    }
    #[pyo3(signature=(force = false))]
    pub fn save_rrfs(&self, force: bool) -> Result<String> {
        save_tensor(self.value.clone(), force).map(|_| self.tensor_hash_base16())
    }

    pub fn tensor_hash_base16(&self) -> String {
        encode_lower(&self.value.hash().unwrap())
    }

    #[staticmethod]
    pub fn from_hash(name: Option<Name>, hash_base16: &str) -> Result<Self> {
        get_tensor_prefix(hash_base16).map(|value| Array::new(value, name))
    }

    #[staticmethod]
    #[pyo3(name = "from_hash_prefix")]
    pub fn from_hash_prefix_py(
        name: Option<Name>,
        hash_base16: &str,
        tensor_cache: Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        let mut tensor_cache = tensor_cache;
        Array::from_hash_prefix(name, hash_base16, &mut tensor_cache)
    }
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Symbol {
    #[pyo3(get)]
    pub uuid: Uuid,
    info: CachedCircuitInfo,
}

circuit_node_extra_impl!(Symbol, self_hash_default);

impl CircuitNodeComputeInfoImpl for Symbol {
    fn compute_flags(&self) -> CircuitFlags {
        self.compute_flags_default() & !CircuitFlags::IS_EXPLICITLY_COMPUTABLE
    }
}

impl CircuitNodeHashItems for Symbol {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(self.uuid.as_bytes());
        for l in &self.info.shape {
            hasher.update(&l.to_le_bytes());
        }
    }
}

impl CircuitNode for Symbol {
    circuit_node_auto_leaf_impl!("13c3ee63-76e9-4afb-8057-40309d17b458");
}

impl Symbol {
    #[apply(new_rc)]
    pub fn new(shape: Shape, uuid: Uuid, name: Option<Name>) -> (Self) {
        let out = Self {
            uuid,
            info: CachedCircuitInfo::incomplete(name, shape, vec![]).unwrap(),
        };
        out.initial_init_info().unwrap()
    }

    // HACK: currently only used for Schedule & not exported to python
    pub fn new_device_dtype_random_uuid(
        shape: Shape,
        name: Option<Name>,
        device_dtype: TorchDeviceDtypeOp,
    ) -> Self {
        Self {
            uuid: Uuid::new_v4(),
            info: CachedCircuitInfo::with_device_dtype(name, shape, vec![], device_dtype),
        }
        .initial_init_info()
        .unwrap()
    }
}

#[pymethods]
impl Symbol {
    #[new]
    fn py_new(shape: Shape, uuid: Uuid, name: Option<Name>) -> PyClassInitializer<Self> {
        Symbol::new(shape, uuid, name).into_init()
    }

    #[staticmethod]
    pub fn new_with_random_uuid(shape: Shape, name: Option<Name>) -> Self {
        Self::new(shape, Uuid::new_v4(), name)
    }
    #[staticmethod]
    pub fn new_with_none_uuid(shape: Shape, name: Option<Name>) -> Self {
        Self::new(shape, Uuid::nil(), name)
    }

    /// equality by ident is nice because we can guarantees about correct
    /// behavior even when shapes change
    pub fn ident(&self) -> (Uuid, Option<Name>) {
        (self.uuid, self.info().name)
    }
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Scalar {
    #[pyo3(get)]
    pub value: f64,
    info: CachedCircuitInfo,
}

circuit_node_extra_impl!(Scalar, self_hash_default);

impl CircuitNodeComputeInfoImpl for Scalar {}

impl CircuitNodeHashItems for Scalar {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.value.to_le_bytes());
        for l in &self.info.shape {
            hasher.update(&l.to_le_bytes());
        }
    }
}

impl CircuitNode for Scalar {
    circuit_node_auto_leaf_impl!("78a77905-8b3f-4471-bb77-255673941fef");
}

impl Scalar {
    #[apply(new_rc_unwrap)]
    pub fn try_new(value: f64, shape: Shape, name: Option<Name>) -> Result<Self> {
        if !shape_is_known(&shape) {
            bail!(ConstructError::ScalarUnknownSizes { shape, name, value })
        }

        let out = Self {
            value,
            info: CachedCircuitInfo::incomplete(name, shape, vec![])?,
        };

        out.initial_init_info()
    }
}

#[pymethods]
impl Scalar {
    #[new]
    #[pyo3(signature=(value, shape = sv![], name = None))]
    fn py_new(value: f64, shape: Shape, name: Option<Name>) -> Result<PyClassInitializer<Self>> {
        Ok(Self::try_new(value, shape, name)?.into_init())
    }

    pub fn is_zero(&self) -> bool {
        self.value == 0.
    }

    pub fn is_one(&self) -> bool {
        self.value == 1.
    }

    pub fn evolve_shape(&self, shape: Shape) -> Result<Self> {
        Self::try_new(self.value, shape, self.info().name)
    }
}
