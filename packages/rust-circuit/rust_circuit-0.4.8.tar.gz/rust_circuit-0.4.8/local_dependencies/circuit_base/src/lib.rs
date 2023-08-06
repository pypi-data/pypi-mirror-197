#![feature(let_chains)]
#![feature(if_let_guard)]
#![allow(clippy::borrow_deref_ref)]
use std::{
    collections::{BTreeMap, BTreeSet},
    fmt::Debug,
    ops::{Deref, DerefMut},
};

use anyhow::Result;
use num_bigint::BigUint;
use pyo3::{prelude::*, pyclass::CompareOp};
use rr_util::{
    eq_by_big_hash::EqByBigHash,
    name::Name,
    py_types::{
        reduction_to_ints, use_rust_comp, PyCallable, PyOpAtAxes, PySymShape, Tensor,
        PY_CIRCUIT_ITEMS,
    },
    pycall,
    rearrange_spec::{PyCountsAtAxes, RearrangeSpec},
    shape::Shape,
    tensor_util::{TensorIndex, TorchDevice, TorchDeviceDtype, TorchDeviceDtypeOp, TorchDtype},
    util::{HashBytes, HashBytesToPy, NamedAxes},
};

pub mod auto_name;
pub mod cached_circuit_properties;
pub mod circuit;
pub mod circuit_info;
pub mod circuit_node_private;
pub mod circuit_utils;
pub mod computational_node;
pub mod constant;
pub mod cumulant;
pub mod errors;
pub mod generalfunction;
pub mod module;
pub mod named_axes;
pub mod nrc;
pub mod opaque_iterative_matcher;
pub mod self_funcs;
pub mod variable_nodes;

use auto_name::OperatorPriority;
pub use circuit::*;
use circuit_node_private::*;
pub use circuit_utils::*;
pub use computational_node::{
    flat_concat, flat_concat_back, Add, Concat, Conv, Einsum, Index, Rearrange, Scatter,
};
pub use constant::{Array, Scalar, Symbol};
pub use cumulant::Cumulant;
pub use errors::ConstructError;
pub use generalfunction::{GeneralFunction, GeneralFunctionSpec};
pub use module::{Module, ModuleArgSpec, ModuleSpec};
use named_axes::set_named_axes;
use opaque_iterative_matcher::OpaqueIterativeMatcherVal;
use pyo3::{types::PyModule, wrap_pyfunction, PyResult};
use self_funcs::SELF_FUNCS;
pub use variable_nodes::{DiscreteVar, StoredCumulantVar, Tag};

use crate::{
    circuit_info::{CachedCircuitInfo, CircuitFlags},
    module::get_free_symbols,
};

pub fn register(py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    use crate::named_axes::{propagate_named_axes, set_named_axes_py};

    m.add_class::<crate::PyCircuitBase>()?;

    m.add_class::<crate::generalfunction::GeneralFunctionShapeInfo>()?;
    m.add_class::<crate::generalfunction::GeneralFunctionSimpleSpec>()?;
    m.add_function(wrap_pyfunction!(
        crate::generalfunction::get_shape_info_simple,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::generalfunction::get_shape_info_broadcast,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::generalfunction::pow, m)?)?;
    m.add_function(wrap_pyfunction!(crate::generalfunction::multinomial, m)?)?;
    crate::generalfunction::register(py, m)?;
    m.add_class::<crate::generalfunction::GeneralFunctionIndexSpec>()?;
    m.add_class::<crate::generalfunction::GeneralFunctionExplicitIndexSpec>()?;
    m.add_class::<crate::generalfunction::GeneralFunctionSetDDSpec>()?;
    m.add_class::<crate::generalfunction::GeneralFunctionPowSpec>()?;
    m.add_class::<crate::generalfunction::GeneralFunctionMultinomialSpec>()?;
    m.add_class::<crate::Einsum>()?;
    m.add_class::<crate::Array>()?;
    m.add_class::<crate::Symbol>()?;
    m.add_class::<crate::Scalar>()?;
    m.add_class::<crate::Add>()?;
    m.add_class::<crate::Rearrange>()?;
    m.add_class::<crate::Index>()?;
    m.add_class::<crate::GeneralFunction>()?;
    m.add_class::<crate::Concat>()?;
    m.add_class::<crate::Scatter>()?;
    m.add_class::<crate::Conv>()?;

    m.add_class::<crate::module::Module>()?;
    m.add_class::<crate::module::ModuleSpec>()?;
    m.add_class::<crate::module::ModuleArgSpec>()?;
    m.add_function(wrap_pyfunction!(crate::module::py_get_free_symbols, m)?)?;
    m.add_class::<crate::Tag>()?;
    m.add_class::<crate::DiscreteVar>()?;
    m.add_class::<crate::StoredCumulantVar>()?;
    m.add_class::<crate::Cumulant>()?;

    m.add_class::<crate::opaque_iterative_matcher::Finished>()?;
    m.add("FINISHED", crate::opaque_iterative_matcher::Finished)?;

    m.add_function(wrap_pyfunction!(count_nodes, m)?)?;
    m.add_function(wrap_pyfunction!(total_flops, m)?)?;
    m.add_function(wrap_pyfunction!(total_arrayconstant_size, m)?)?;

    m.add_function(wrap_pyfunction!(flat_concat, m)?)?;
    m.add_function(wrap_pyfunction!(crate::flat_concat_back, m)?)?;
    m.add_function(wrap_pyfunction!(set_named_axes_py, m)?)?;
    m.add_function(wrap_pyfunction!(propagate_named_axes, m)?)?;

    m.add_function(wrap_pyfunction!(crate::deep_map_preorder_py, m)?)?;
    m.add_function(wrap_pyfunction!(crate::deep_map_py, m)?)?;

    m.add_function(wrap_pyfunction!(crate::visit_circuit_py, m)?)?;
    m.add_function(wrap_pyfunction!(crate::all_children, m)?)?;

    m.add_function(wrap_pyfunction!(toposort_circuit, m)?)?;

    m.add_function(wrap_pyfunction!(crate::module::substitute_all_modules, m)?)?;
    m.add_function(wrap_pyfunction!(crate::module::conform_all_modules, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::module::inline_single_callsite_modules,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module::clear_module_circuit_caches,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module::get_children_with_symbolic_sizes,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module::any_children_with_symbolic_sizes,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(crate::print_circuit_type_check, m)?)?;

    Ok(())
}

#[pyclass(subclass, name = "Circuit")]
#[derive(Clone, Debug)]
pub struct PyCircuitBase(CircuitRc);

impl Deref for PyCircuitBase {
    type Target = CircuitRc;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for PyCircuitBase {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl EqByBigHash for PyCircuitBase {
    fn hash(&self) -> HashBytes {
        self.info().hash
    }
}

const DEFAULT_FANCY_VALIDATE: bool = false;
const DEFAULT_ASSERT_ANY_FOUND: bool = false;

#[pymethods]
impl PyCircuitBase {
    #[getter]
    fn shape(&self) -> PySymShape {
        PySymShape(self.info().shape.clone())
    }

    #[getter]
    fn is_constant(&self) -> bool {
        self.info().is_constant()
    }

    #[getter]
    fn is_explicitly_computable(&self) -> bool {
        self.info().is_explicitly_computable()
    }

    #[getter]
    fn can_be_sampled(&self) -> bool {
        self.info().can_be_sampled()
    }

    #[getter]
    fn no_unbound_symbols(&self) -> bool {
        get_free_symbols(&self.0).is_empty()
    }

    #[getter]
    fn use_autoname(&self) -> bool {
        self.info().use_autoname()
    }

    #[getter]
    fn name(&self) -> &str {
        Name::str_maybe_empty(self.0.info().name)
    }

    #[getter]
    fn op_name(&self) -> Option<&'static str> {
        self.0.info().name.map(|z| z.into())
    }

    fn get_autoname(&self) -> Result<Option<Name>> {
        self.0.get_autoname()
    }

    #[getter]
    fn children(&self) -> Vec<CircuitRc> {
        self.0.info().children.clone()
    }

    #[getter]
    fn non_free_children(&self) -> Vec<CircuitRc> {
        self.0.non_free_children().collect()
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self.0, &object.0, comp_op)
    }

    fn __repr__(&self) -> Result<String> {
        self.debug_repr()
    }

    #[getter]
    fn hash(&self) -> HashBytesToPy {
        self.info().hash.into()
    }

    #[getter]
    fn hash_base16(&self) -> String {
        base16::encode_lower(&self.info().hash)
    }

    fn __hash__(&self) -> u64 {
        self.first_u64()
    }

    pub fn self_flops(&self) -> BigUint {
        self.0.self_flops()
    }

    pub fn total_flops(&self) -> BigUint {
        total_flops((*self.0).crc())
    }

    pub fn print_stats(&self) {
        (SELF_FUNCS.print_circuit_stats)(&self.0)
    }

    #[pyo3(signature=(autoname_disabled=true))]
    fn with_autoname_disabled(&self, autoname_disabled: bool) -> CircuitRc {
        self.0.clone().with_autoname_disabled(autoname_disabled)
    }

    fn repr(&self, options: Option<PyObject>) -> Result<String> {
        (SELF_FUNCS.PrintOptions_repr)(options, self.0.clone())
    }

    fn print(&self, options: Option<PyObject>) -> Result<()> {
        (SELF_FUNCS.PrintOptionsBase_print)(options, &[self.0.clone()])
    }

    fn print_html(&self, options: Option<PyObject>) -> Result<()> {
        (SELF_FUNCS.PrintHtmlOptions_print)(options, &[self.0.clone()])
    }
    #[getter]
    fn numel(&self) -> BigUint {
        self.0.info().numel()
    }

    #[getter]
    fn rank(&self) -> usize {
        self.0.rank()
    }

    #[getter]
    fn ndim(&self) -> usize {
        self.rank()
    }
    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.0.child_axis_map()
    }

    fn to_py(&self) -> Result<PyObject> {
        circuit_rust_to_py(self.0.clone())
    }

    fn evaluate(&self) -> Result<Tensor> {
        evaluate(self.0.clone())
    }

    fn map_children_enumerate(&self, f: PyCallable) -> Result<CircuitRc> {
        self.0
            .map_children_enumerate(|i, child| pycall!(f, (i, child), anyhow))
    }

    fn map_children(&self, f: PyCallable) -> Result<CircuitRc> {
        self.0.map_children(|child| pycall!(f, (child,), anyhow))
    }

    fn map_child(&self, ix: usize, f: PyCallable) -> Result<CircuitRc> {
        anyhow::ensure!(
            ix < self.children_sl().len(),
            "replace_child: child index out of bounds"
        );
        let mut v = self.children();
        v[ix] = pycall!(f, (v[ix].clone(),), anyhow)?;
        self._replace_children(v)
    }

    #[getter]
    fn num_children(&self) -> usize {
        self.0.num_children()
    }

    fn total_arrayconstant_size(&self) -> BigUint {
        total_arrayconstant_size(self.0.clone())
    }
    #[getter]
    fn device_dtype(&self) -> TorchDeviceDtypeOp {
        self.0.info().device_dtype
    }
    #[getter]
    fn device(&self) -> Option<TorchDevice> {
        self.0.info().device_dtype.device
    }
    #[getter]
    fn dtype(&self) -> Option<TorchDtype> {
        self.0.info().device_dtype.dtype
    }
    #[getter]
    fn torch_dtype(&self) -> Option<PyObject> {
        self.0.info().device_dtype.get_torch_dtype()
    }

    fn get_compatible_device_dtype(&self) -> TorchDeviceDtype {
        get_compatible_dtype(self)
    }

    fn rename(&self, name: Option<Name>) -> CircuitRc {
        self.0.clone().rename(name)
    }

    fn rename_axes(&self, named_axes: NamedAxes) -> Result<CircuitRc> {
        set_named_axes(self.0.clone(), named_axes)
    }

    fn add_suffix(&self, suffix: Option<&str>) -> CircuitRc {
        self.0.clone().add_suffix(suffix)
    }

    fn visit(&self, f: PyCallable) -> Result<()> {
        visit_circuit_py(self.0.clone(), f)
    }

    fn reduce(
        &self,
        op_name: Name,
        axis: Option<PyOpAtAxes>,
        name: Option<Name>,
    ) -> Result<Circuit> {
        self.0
            .reduce(op_name, &reduction_to_ints(axis, self.rank()), name)
    }

    fn sum(&self, axis: Option<PyOpAtAxes>, name: Option<Name>) -> Result<Einsum> {
        self.0.sum(&reduction_to_ints(axis, self.rank()), name)
    }
    fn mean(
        &self,
        axis: Option<PyOpAtAxes>,
        name: Option<Name>,
        scalar_name: Option<Name>,
    ) -> Result<Einsum> {
        self.0
            .mean(&reduction_to_ints(axis, self.rank()), name, scalar_name)
    }
    fn min(&self, axis: Option<PyOpAtAxes>, name: Option<Name>) -> Result<CircuitRc> {
        Ok(self
            .0
            .min_(&reduction_to_ints(axis, self.rank()), name)?
            .rc())
    }
    fn max(&self, axis: Option<PyOpAtAxes>, name: Option<Name>) -> Result<CircuitRc> {
        Ok(self
            .0
            .max_(&reduction_to_ints(axis, self.rank()), name)?
            .rc())
    }

    fn add(&self, other: CircuitRc, name: Option<Name>) -> Result<Add> {
        self.0.add(other, name)
    }
    fn sub(&self, other: CircuitRc, name: Option<Name>) -> Result<Add> {
        self.0.sub(other, name)
    }
    fn mul(&self, other: CircuitRc, name: Option<Name>) -> Result<Einsum> {
        self.0.mul(other, name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<Name>,
        scalar_name: Option<Name>,
    ) -> Result<Einsum> {
        self.0.mul_scalar(scalar, name, scalar_name)
    }
    fn index(&self, index: TensorIndex, name: Option<Name>) -> Result<Index> {
        self.0.index(index, name)
    }
    fn expand_at_axes(
        &self,
        axes: PyOpAtAxes,
        counts: Option<PyCountsAtAxes>,
        name: Option<Name>,
    ) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.0.crc(),
            RearrangeSpec::expand_at_axes_py(self.rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: PyOpAtAxes, name: Option<Name>) -> Result<Rearrange> {
        self.expand_at_axes(axes, None, name)
    }
    fn squeeze(&self, axes: PyOpAtAxes, name: Option<Name>) -> Result<Rearrange> {
        self.0.squeeze(axes, name)
    }
    fn flatten(&self, name: Option<Name>) -> Result<Rearrange> {
        self.0.flatten(name)
    }
    fn unflatten(&self, shape: Shape, name: Option<Name>) -> Result<Rearrange> {
        self.0.unflatten(shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<Name>) -> Result<Rearrange> {
        self.0.unflatten_axis(axis, shape, name)
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<Name>) -> Result<Rearrange> {
        self.0.rearrange(spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<Name>) -> Result<Rearrange> {
        self.0.rearrange_str(string, name)
    }
    fn enforce_dtype_device(
        &self,
        device_dtype: TorchDeviceDtypeOp,
        name: Option<Name>,
    ) -> GeneralFunction {
        enforce_dtype_device(self.0.clone(), device_dtype, name)
    }
    pub fn is_irreducible_node(&self) -> bool {
        self.0.is_irreducible_node()
    }
    pub fn is_leaf(&self) -> bool {
        self.0.is_leaf()
    }
    pub fn is_leaf_constant(&self) -> bool {
        self.0.is_leaf_constant()
    }
    pub fn is_var(&self) -> bool {
        self.0.is_var()
    }
    pub fn into_irreducible_node(&self) -> Option<IrreducibleNode> {
        self.0.clone().c().into()
    }
    pub fn into_leaf(&self) -> Option<Leaf> {
        self.0.clone().c().into()
    }
    pub fn into_leaf_constant(&self) -> Option<LeafConstant> {
        self.0.clone().c().into()
    }
    pub fn into_var(&self) -> Option<Var> {
        self.0.clone().c().into()
    }
    #[pyo3(signature=(
        matcher,
        transform,
        cache_transform = true,
        cache_update = true,
        fancy_validate = DEFAULT_FANCY_VALIDATE,
        assert_any_found = DEFAULT_ASSERT_ANY_FOUND
    ))]
    pub fn update(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        transform: PyObject,
        cache_transform: bool,
        cache_update: bool,
        fancy_validate: bool,
        assert_any_found: bool,
    ) -> PyResult<CircuitRc> {
        matcher.update(
            self.0.clone(),
            transform,
            cache_transform,
            cache_update,
            fancy_validate,
            assert_any_found,
        )
    }
    #[pyo3(signature=(matcher, fancy_validate = DEFAULT_FANCY_VALIDATE))]
    pub fn get(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<BTreeSet<CircuitRc>> {
        matcher.get(self.0.clone(), fancy_validate)
    }

    #[pyo3(signature=(matcher, fancy_validate = DEFAULT_FANCY_VALIDATE))]
    pub fn get_unique_op(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<Option<CircuitRc>> {
        matcher.get_unique_op(self.0.clone(), fancy_validate)
    }

    #[pyo3(signature=(matcher, fancy_validate = DEFAULT_FANCY_VALIDATE))]
    pub fn get_unique(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<CircuitRc> {
        matcher.get_unique(self.0.clone(), fancy_validate)
    }

    pub fn get_paths(
        &self,
        matcher: OpaqueIterativeMatcherVal,
    ) -> PyResult<BTreeMap<CircuitRc, Vec<CircuitRc>>> {
        matcher.get_paths(self.0.clone())
    }
    pub fn get_all_paths(
        &self,
        matcher: OpaqueIterativeMatcherVal,
    ) -> PyResult<BTreeMap<CircuitRc, Vec<Vec<CircuitRc>>>> {
        matcher.get_all_paths(self.0.clone())
    }

    pub fn are_any_found(&self, matcher: OpaqueIterativeMatcherVal) -> PyResult<bool> {
        matcher.are_any_found(self.0.clone())
    }
}

pub fn get_compatible_dtype(circ: &Circuit) -> TorchDeviceDtype {
    circ.info().device_dtype.unwrap_or_defaults()
}

pub mod prelude {
    pub use crate::{
        errors::ConstructError, Circuit, CircuitNode, CircuitNodeAutoName, CircuitNodeUnion,
        CircuitRc,
    };
}

pub fn circuit_rust_to_py(circ: CircuitRc) -> Result<PyObject> {
    Python::with_gil(|py| Ok(PY_CIRCUIT_ITEMS.rust_to_py.call(py, (circ,), None)?))
}

/// alias for new_cast with same input, output constraint
pub fn enforce_dtype_device(
    circ: CircuitRc,
    device_dtype: TorchDeviceDtypeOp,
    name: Option<Name>,
) -> GeneralFunction {
    GeneralFunction::new_cast(circ, device_dtype, device_dtype, name).unwrap()
}
