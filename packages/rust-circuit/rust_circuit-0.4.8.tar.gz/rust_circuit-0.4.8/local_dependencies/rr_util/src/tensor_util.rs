use std::{
    cmp::{max, min},
    fmt::{self, Display},
    iter::zip,
    ops::Deref,
    str::FromStr,
};

use anyhow::{anyhow, bail, Context, Error, Result};
use itertools::izip;
use macro_rules_attribute::apply;
use pyo3::{
    exceptions,
    exceptions::PyValueError,
    ffi,
    prelude::*,
    pyclass::CompareOp,
    pymethods,
    types::{IntoPyDict, PySlice, PyTuple},
    AsPyPointer, FromPyObject, IntoPy, PyAny, PyErr, PyObject, PyResult, Python, ToPyObject,
};
use rustc_hash::FxHashMap as HashMap;
use thiserror::Error;
use uuid::uuid;

use super::py_types::ExtraPySelfOps;
use crate::{
    atr, filter_by_variant,
    lru_cache::TensorCacheRrfs,
    py_types::{use_rust_comp, Tensor, PY_UTILS},
    pycall, python_error_exception,
    shape::{Shape, Size},
    tensor_db::{get_tensor_prefix, save_tensor},
    util::HashBytes,
};

/// casts tensors whith None device/dtype to specified device/dtype
pub fn cast_tensors(tensors: &[Tensor], out_device_dtype: TorchDeviceDtype) -> Vec<Tensor> {
    tensors
        .iter()
        .map(|t| {
            if t.device_dtype() != out_device_dtype {
                pycall!(PY_UTILS.cast_tensor, (t.clone(), out_device_dtype))
            } else {
                t.clone()
            }
        })
        .collect()
}

pub fn upcast_tensor_device_dtypes(tensors: &[Tensor]) -> Vec<Tensor> {
    let device = upcast_devices_if_needed(
        &tensors
            .iter()
            .map(|z| z.device_dtype().device)
            .collect::<Vec<_>>(),
    );
    let dtype = upcast_dtypes_if_needed(
        &tensors
            .iter()
            .map(|z| z.device_dtype().dtype)
            .collect::<Vec<_>>(),
    );
    if device.is_some() || dtype.is_some() {
        return cast_tensors(
            tensors,
            TorchDeviceDtypeOp { device, dtype }.unwrap_or_defaults(),
        );
    }
    tensors.to_owned()
}

fn upcast_devices_if_needed(devices: &[TorchDevice]) -> Option<TorchDevice> {
    if devices.is_empty() || devices[1..].iter().all(|z| z == &devices[0]) {
        return None;
    }
    devices.iter().cloned().find(|z| *z != TorchDevice::Cpu)
}
fn upcast_dtypes_if_needed(dtypes: &[TorchDtype]) -> Option<TorchDtype> {
    if dtypes.is_empty() || dtypes[1..].iter().all(|z| z == &dtypes[0]) {
        return None;
    }
    dtypes.iter().cloned().find(|z| *z != TorchDtype::float64)
}

#[pyfunction]
#[pyo3(name = "upcast_tensor_devices")]
pub fn upcast_tensor_devices_py(tensors: Vec<Tensor>) -> Vec<Tensor> {
    upcast_tensor_devices(&tensors)
}
#[pyfunction]
#[pyo3(name = "upcast_tensor_device_dtypes")]
pub fn upcast_tensor_device_dtypes_py(tensors: Vec<Tensor>) -> Vec<Tensor> {
    upcast_tensor_device_dtypes(&tensors)
}

pub fn upcast_tensor_devices(tensors: &[Tensor]) -> Vec<Tensor> {
    if let Some(device) = upcast_devices_if_needed(
        &tensors
            .iter()
            .cloned()
            .map(|z| z.device_dtype().device)
            .collect::<Vec<_>>(),
    ) {
        return cast_tensors(
            tensors,
            TorchDeviceDtypeOp {
                dtype: None,
                device: Some(device),
            }
            .unwrap_or_defaults(),
        );
    }
    tensors.to_owned()
}

#[apply(python_error_exception)]
#[base_error_name(MiscInput)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum MiscInputError {
    #[error("Shapes aren't broadcastable, {shapes:?} ({e_name})")]
    NotBroadcastable { shapes: Vec<Shape> },

    #[error("GeneralFunction Index index dtype isnt i64 ({e_name})")]
    IndexDtypeNotI64 {},

    #[error("item={item}, count={count} (needed -{count} <= {item} < {count}) ({e_name})")]
    ItemOutOfBounds { item: i64, count: usize },

    #[error("Children multiple dtypes {a:?} {b:?} ({e_name})")]
    ChildrenMultipleDtypes {
        a: Option<TorchDtype>,
        b: Option<TorchDtype>,
    },

    #[error("Cast node got incompatible input, required compatibility {required:?}  actual {actual:?} ({e_name})")]
    CastIncompatibleDeviceDtype {
        required: TorchDeviceDtypeOp,
        actual: TorchDeviceDtypeOp,
    },

    #[error("Children multiple dtypes {a:?} {b:?} ({e_name})")]
    ChildrenMultipleDevices {
        a: Option<TorchDevice>,
        b: Option<TorchDevice>,
    },
}

#[apply(python_error_exception)]
#[base_error_name(Index)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum IndexError {
    #[error("Only ndim of 1 is supported for index tensors and got {ndim} (tensor: {tensor:?}) ({e_name})")]
    TensorNDimNot1 { ndim: usize, tensor: Tensor },

    #[error("Index {axis:?} out of bounds, index: {index:?} shape: {shape:?}. NB: Rust circuit slices don't saturate like Python ones do. ({e_name})")]
    IndexOutOfBounds {
        index: TensorIndex,
        shape: Shape,
        at: usize,
        axis: TensorAxisIndex,
        l: Size,
    },

    #[error("index rank too high: {index_rank} vs {node_rank} ({e_name})")]
    IndexRankTooHigh { index_rank: usize, node_rank: usize },

    #[error("slice={slice:?} ({e_name})")]
    UnsupportedSlice { slice: Slice },
}

pub fn check_canon_idxs(count: usize, ints: &[i64]) -> Result<Vec<usize>> {
    let icount = count as i64;
    ints.iter()
        .map(|&item| {
            if item >= icount || item < -icount {
                bail!(MiscInputError::ItemOutOfBounds { item, count })
            } else {
                Ok(((item + icount) % icount) as usize)
            }
        })
        .collect()
}

pub fn check_canon_axes(rank: usize, axes: &[i64]) -> Result<Vec<usize>> {
    check_canon_idxs(rank, axes).context("axis out of bounds")
}

// we could bit pack if we wanted...
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Slice {
    pub start: Option<i64>,
    pub stop: Option<i64>,
}

impl Slice {
    pub const IDENT: Slice = Slice {
        start: None,
        stop: None,
    };

    pub fn to_unsigned_loc(x: i64, l: usize) -> usize {
        if x < 0 {
            l.saturating_sub((-x) as usize)
        } else {
            // don't min with l to match Index bounds checking
            x as usize
        }
    }

    pub fn start_u(self, l: usize) -> usize {
        self.start.map_or(0, |x| Self::to_unsigned_loc(x, l))
    }

    pub fn stop_u(self, l: usize) -> usize {
        self.stop.map_or(l, |x| Self::to_unsigned_loc(x, l))
    }

    pub fn to_uslice(self, l: usize) -> USlice {
        USlice {
            start: self.start_u(l),
            stop: self.stop_u(l),
        }
    }

    fn size(self, l: Size) -> Size {
        match l.t() {
            None => match (self.start, self.stop) {
                (Some(x), Some(y)) if x >= 0 && y >= 0 => {
                    Size::known(y.checked_sub(x).unwrap().try_into().unwrap())
                }
                _ => Size::NONE,
            },
            Some(l) => Size::known(self.stop_u(l).saturating_sub(self.start_u(l))),
        }
    }

    fn canonicalize(self, l: usize) -> Self {
        Self {
            start: Some(self.start_u(l) as i64),
            stop: Some(self.stop_u(l) as i64),
        }
    }

    fn update_hash(self, hasher: &mut blake3::Hasher) {
        for op in [self.start, self.stop] {
            match op {
                Some(i) => {
                    hasher.update(&i.to_le_bytes());
                    hasher.update(&[0]);
                }
                None => {
                    hasher.update(&0_i64.to_le_bytes());
                    hasher.update(&[1]);
                }
            }
        }
    }

    pub fn is_identity(self, l: Size) -> bool {
        (self.start.is_none() && self.stop.is_none()) || (l.is_known() && self.size(l) == l)
    }
}

impl<'source> FromPyObject<'source> for Slice {
    fn extract(slice_in: &'source PyAny) -> PyResult<Self> {
        let py_slice: &PySlice = slice_in.extract()?;

        // could also use never type if that was supported : /
        let step: Option<isize> = py_slice.getattr("step").unwrap().extract()?;
        if step.is_some() {
            return Err(PyErr::new::<exceptions::PyValueError, _>(
                "step must be None!",
            ));
        }

        Ok(Slice {
            start: py_slice.getattr("start").unwrap().extract()?,
            stop: py_slice.getattr("stop").unwrap().extract()?,
        })
    }
}

impl IntoPy<PyObject> for Slice {
    fn into_py(self, py: Python<'_>) -> PyObject {
        unsafe {
            // we use unsafe + ffi because pyo3 slice doesn't support None
            let ptr = ffi::PySlice_New(
                self.start.into_py(py).as_ptr(),
                self.stop.into_py(py).as_ptr(),
                None::<i64>.into_py(py).as_ptr(),
            );
            let slice: &PySlice = py.from_owned_ptr(ptr);
            slice.into()
        }
    }
}

#[derive(PartialEq, Eq, Hash, Clone, Debug, Copy)]
pub struct USlice {
    pub start: usize,
    pub stop: usize,
}
impl USlice {
    pub fn intersection(&self, other: &USlice) -> USlice {
        let start = max(self.start, other.start);
        USlice {
            start,
            stop: max(min(self.stop, other.stop), start),
        }
    }
    pub fn union(&self, other: &USlice) -> USlice {
        USlice {
            start: min(self.start, other.start),
            stop: max(self.stop, other.stop),
        }
    }

    pub fn shrink_base(&self, new_base: &USlice) -> USlice {
        assert!(new_base.stop >= self.stop);
        assert!(self.start >= new_base.start);
        USlice {
            start: self.start - new_base.start,
            stop: self.stop - new_base.start,
        }
    }

    pub fn containing_uslice(x: &TensorAxisIndex) -> Option<USlice> {
        match x {
            TensorAxisIndex::Single(single) => Some(USlice {
                start: *single as usize,
                stop: (*single + 1) as usize,
            }),
            TensorAxisIndex::Slice(slice) => (*slice).into(),
            TensorAxisIndex::Tensor(_) => None,
        }
    }
    pub fn length(&self) -> usize {
        self.stop - self.start
    }
}

pub fn uslices_shrink_base(x: &Vec<USlice>, new_base: &Vec<USlice>) -> Vec<USlice> {
    zip(x, new_base).map(|(x, b)| x.shrink_base(b)).collect()
}

pub fn uslices_to_index(x: &Vec<USlice>) -> TensorIndex {
    TensorIndex(
        x.iter()
            .map(|x| TensorAxisIndex::Slice((*x).into()))
            .collect(),
    )
}

impl From<USlice> for Slice {
    fn from(x: USlice) -> Self {
        Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        }
    }
}

impl From<Slice> for Option<USlice> {
    fn from(slice: Slice) -> Self {
        if let Slice {
            start: Some(start),
            stop: Some(stop),
        } = slice
        {
            if start < 0 || stop < 0 {
                return None;
            }
            Some(USlice {
                start: start as usize,
                stop: stop as usize,
            })
        } else {
            None
        }
    }
}

impl From<USlice> for TensorAxisIndex {
    fn from(x: USlice) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        })
    }
}

/// Wrapper which ensures ndim <= 1
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IndexTensor(Tensor);

impl Deref for IndexTensor {
    type Target = Tensor;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl TryFrom<Tensor> for IndexTensor {
    type Error = Error;
    fn try_from(tensor: Tensor) -> Result<Self> {
        if tensor.ndim() != 1 {
            bail!(IndexError::TensorNDimNot1 {
                ndim: tensor.ndim(),
                tensor,
            });
        }
        Ok(IndexTensor(tensor))
    }
}

impl<'source> FromPyObject<'source> for IndexTensor {
    fn extract(tensor: &'source PyAny) -> PyResult<Self> {
        let tensor: Tensor = tensor.extract()?;
        tensor.try_into().map_err(Into::into)
    }
}
impl IntoPy<PyObject> for IndexTensor {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0.into_py(py)
    }
}
impl IntoPy<PyObject> for &IndexTensor {
    fn into_py(self, py: Python<'_>) -> PyObject {
        (&self.0).into_py(py)
    }
}

/// for now, doesn't support tensors with negatives
#[derive(Debug, Clone, FromPyObject, PartialEq, Eq)]
pub enum TensorAxisIndex {
    Tensor(IndexTensor), // tensor needs to come first so len 1 tensors go to tensor not single
    Single(i64),
    Slice(Slice),
}

impl TensorAxisIndex {
    pub const IDENT: TensorAxisIndex = TensorAxisIndex::Slice(Slice {
        start: None,
        stop: None,
    });

    // TODO should be cached
    pub fn tensor_canon(tensor: &IndexTensor) -> Self {
        pycall!(PY_UTILS.canon_index_tensor, (tensor,))
    }

    pub fn indices_contiguous_uslice(indices: &Vec<TensorAxisIndex>) -> Option<USlice> {
        if let Some(mut containings) = indices
            .iter()
            .map(USlice::containing_uslice)
            .collect::<Option<Vec<_>>>()
        {
            containings.sort_by(|a, b| a.start.cmp(&b.start));
            let mut result = containings[0];
            for c in &containings[1..] {
                if c.start > result.stop {
                    return None;
                }
                result.stop = max(result.stop, c.stop)
            }
            return Some(result);
        }
        None
    }

    // assumes indices canonicalized
    pub fn indices_union_and_rebased(
        indices: &Vec<TensorAxisIndex>,
        l: usize,
        device_dtype: TorchDeviceDtype,
    ) -> (TensorAxisIndex, Vec<TensorAxisIndex>) {
        if let Some(contiguous) = TensorAxisIndex::indices_contiguous_uslice(indices) {
            (
                TensorAxisIndex::Slice(contiguous.into()),
                indices
                    .iter()
                    .map(|x| x.shrink_base_uslice(&contiguous))
                    .collect(),
            )
        } else {
            // TODO probably should cache?
            pycall!(
                PY_UTILS.index_union_rebase,
                (indices.clone(), l, device_dtype.device)
            )
        }
    }

    // assumes self canonicalized
    fn offset(&self, b: i64) -> Self {
        match self {
            TensorAxisIndex::Slice(i) => {
                let i2: USlice = Into::<Option<USlice>>::into(*i).unwrap();
                TensorAxisIndex::Slice(
                    USlice {
                        start: (i2.start as i64 + b).try_into().unwrap(),
                        stop: (i2.stop as i64 + b).try_into().unwrap(),
                    }
                    .into(),
                )
            }
            TensorAxisIndex::Single(i) => {
                TensorAxisIndex::Single(TryInto::<usize>::try_into(i + b).unwrap() as i64)
            }
            TensorAxisIndex::Tensor(t) => Python::with_gil(|py| {
                TensorAxisIndex::Tensor(t.0.clone().py_add(py, b).unwrap().try_into().unwrap())
            }),
        }
    }

    // assumes self canonicalized
    pub fn shrink_base_uslice(&self, uslice: &USlice) -> Self {
        self.offset(-(uslice.start as i64))
    }

    pub fn canonicalize(&self, l: &Size) -> Self {
        match self {
            TensorAxisIndex::Single(i) if let Some(l) = l.t() => TensorAxisIndex::Single((*i + l as i64) % l as i64),
            TensorAxisIndex::Slice(sl) if let Some(l) = l.t() => TensorAxisIndex::Slice(sl.canonicalize(l)),
            TensorAxisIndex::Tensor(t) => TensorAxisIndex::tensor_canon(t),
            _ => self.clone()
        }
    }

    pub fn new_plain_slice(start: usize, stop: usize) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(start as i64),
            stop: Some(stop as i64),
        })
    }

    pub fn is_identity(&self, l: Size) -> bool {
        match self {
            TensorAxisIndex::Slice(s) => s.is_identity(l),
            _ => false, // dont bother to check tensor, if you want that canon first
        }
    }

    pub fn new_tensor_randint_seeded(
        length: usize,
        base_length: usize,
        device_dtype: TorchDeviceDtypeOp,
        seed: usize,
    ) -> Self {
        TensorAxisIndex::Tensor(pyo3::Python::with_gil(|py| {
            PY_UTILS
                .torch
                .getattr(py, "manual_seed")
                .unwrap()
                .call(py, (seed,), None)
                .unwrap();
            let mut kwargs = HashMap::default();
            if let Some(dtype) = device_dtype.dtype {
                let dtype: &str = &String::from(&dtype);
                kwargs.insert("dtype", PY_UTILS.torch.getattr(py, dtype).unwrap());
            }
            if let Some(device) = device_dtype.device {
                kwargs.insert("device", device.into_py(py));
            }
            PY_UTILS
                .torch
                .getattr(py, "randint")
                .unwrap()
                .call(
                    py,
                    (0, base_length, pyo3::types::PyTuple::new(py, vec![length])),
                    Some(kwargs.into_py_dict(py)),
                )
                .unwrap()
                .extract(py)
                .unwrap()
        }))
    }

    pub fn axis_len(&self, l: usize) -> usize {
        match self {
            TensorAxisIndex::Single(_) => 0,
            TensorAxisIndex::Slice(s) => s.to_uslice(l).length(),
            TensorAxisIndex::Tensor(t) => t.0.shape[0].unwrap(),
        }
    }
}

impl IntoPy<PyObject> for TensorAxisIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Self::Single(x) => x.into_py(py),
            Self::Tensor(x) => x.into_py(py),
            Self::Slice(x) => x.into_py(py),
        }
    }
}

// https://github.com/PyO3/pyo3/issues/1595 for why needed
impl ToPyObject for TensorAxisIndex {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub struct TensorIndex(pub Vec<TensorAxisIndex>);

// TensorIndexSync is like TensorIndex but allows tensors to have any rank
// this is for extracting these numpy-style indices
// we don't have full support for this, only used in new_synchronized_to_start
pub struct TensorIndexSync(pub TensorIndex);
impl<'source> FromPyObject<'source> for TensorIndexSync {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        Ok(TensorIndexSync(TensorIndex(
            ob.iter()?
                .map(|x| {
                    let x_unwrapped = x?;
                    let tensory: PyResult<Tensor> = x_unwrapped.extract();
                    tensory
                        .map(|z| TensorAxisIndex::Tensor(IndexTensor(z)))
                        .or_else(move |_| x_unwrapped.extract())
                })
                .collect::<PyResult<Vec<_>>>()?,
        )))
    }
}

impl Display for TensorIndex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut result = "[".to_owned();
        for (i, idx) in self.0.iter().enumerate() {
            result.push_str(&match idx {
                TensorAxisIndex::Single(i) => i.to_string(),
                TensorAxisIndex::Slice(slice) => {
                    slice.start.map(|i| i.to_string()).unwrap_or("".to_owned())
                        + ":"
                        + &slice.stop.map(|i| i.to_string()).unwrap_or("".to_owned())
                }
                TensorAxisIndex::Tensor(tensor) => {
                    "[".to_owned() + &tensor.shape()[0].to_string() + "]"
                }
            });
            if i != self.0.len() - 1 {
                result.push(',');
            }
        }
        result.push(']');
        write!(f, "{}", result)
    }
}

#[test]
fn sat_as_expected() {
    assert_eq!(1, 4usize.saturating_sub((-(-3isize)) as usize));
    assert_eq!(0, 4usize.saturating_sub((-(-5isize)) as usize));
}

impl TensorIndex {
    pub fn expand_to_shape(&self, old_shape: &[Size], new_shape: &[Size]) -> Self {
        TensorIndex(
            izip!(&self.0, new_shape, old_shape)
                .map(|(x, news, olds)| {
                    if !x.is_identity(*news) && x.is_identity(*olds) {
                        TensorAxisIndex::IDENT
                    } else {
                        x.clone()
                    }
                })
                .collect(),
        )
    }

    pub fn apply_to_shape(&self, shape: &Shape) -> Shape {
        zip(&self.0, shape)
            .filter_map(|(idx, l)| match idx {
                TensorAxisIndex::Single(_i) => None,
                TensorAxisIndex::Tensor(t) => {
                    if t.shape().is_empty() {
                        None
                    } else {
                        Some(Size::known(t.shape()[0].unwrap()))
                    }
                }
                TensorAxisIndex::Slice(sl) => Some(sl.size(*l)),
            })
            .collect()
    }

    pub fn edges_to_none(&self, shape: &Shape) -> Self {
        TensorIndex(
            zip(&self.0, shape)
                .map(|(ax, l)| match ax {
                    TensorAxisIndex::Slice(slice) if let Some(l) = l.t() => TensorAxisIndex::Slice(Slice {
                        start: if slice.start_u(l) == 0 {
                            None
                        } else {
                            slice.start
                        },
                        stop: if slice.stop_u(l) == l {
                            None
                        } else {
                            slice.stop
                        },
                    }),
                    _ => ax.clone(),
                })
                .collect(),
        )
    }

    pub fn is_identity(&self, shape: &[Size]) -> bool {
        zip(&self.0, shape).all(|(idx, &l)| idx.is_identity(l))
    }

    pub fn validate(&self, shape: &Shape) -> Result<()> {
        let get_err = |at| {
            Err(IndexError::IndexOutOfBounds {
                index: self.clone(),
                shape: shape.clone(),
                at,
                axis: self.0[at].clone(),
                l: shape[at],
            })
        };

        let check = |at: usize, i: Option<i64>, l: usize, is_slice: bool| {
            if let Some(i) = i {
                let end_b = if is_slice { l + 1 } else { l };
                if i >= end_b as i64 || i < -(l as i64) {
                    return get_err(at);
                }
            }
            Ok(())
        };

        for (at, (idx, l)) in zip(&self.0, shape).enumerate() {
            if let Some(l) = l.t() {
                match *idx {
                    TensorAxisIndex::Single(i) => check(at, Some(i), l, false)?,
                    TensorAxisIndex::Slice(Slice { start, stop }) => {
                        check(at, start, l, true)?;
                        check(at, stop, l, true)?;

                        let mod_l_idx = |x| if x < 0 { l as i64 + x } else { x };
                        let start_u: i64 = start.map_or(0, mod_l_idx);
                        let stop_u: i64 = stop.map_or(l as i64, mod_l_idx);
                        if start_u > stop_u {
                            get_err(at)?;
                        }
                    }
                    _ => (),
                }
            }
        }

        Ok(())
    }

    pub fn canonicalize(&self, shape: &Shape) -> TensorIndex {
        self.validate(shape).expect("invalid tensor index");
        TensorIndex(
            zip(&self.0, shape)
                .map(|(idx, l)| idx.canonicalize(l))
                .collect(),
        )
    }

    pub fn all_slices(&self) -> Option<Vec<Slice>> {
        let filtered = filter_by_variant!(&self.0, TensorAxisIndex, Slice, Slice).0;
        if filtered.len() == self.0.len() {
            Some(filtered)
        } else {
            None
        }
    }

    pub fn all_uslices(&self) -> Option<Vec<USlice>> {
        self.all_slices().and_then(|x| {
            let result: Vec<USlice> = x.iter().filter_map(|x| (*x).into()).collect();
            if result.len() == x.len() {
                Some(result)
            } else {
                None
            }
        })
    }

    pub fn new_single(idx: TensorAxisIndex, pos: usize, rank: usize) -> Self {
        TensorIndex(
            (0..rank)
                .map(|i| {
                    if i == pos {
                        idx.clone()
                    } else {
                        TensorAxisIndex::IDENT
                    }
                })
                .collect(),
        )
    }

    pub fn ident(rank: usize) -> Self {
        Self(vec![TensorAxisIndex::IDENT; rank])
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        for axis in self.0.iter() {
            hasher.update(&uuid!("3d14636b-a1ed-4235-91cd-5fc9e818c93d").into_bytes()); // delimit with uuid
            match axis {
                TensorAxisIndex::Single(i) => {
                    hasher.update(&i.to_le_bytes());
                }
                TensorAxisIndex::Tensor(t) => {
                    hasher.update(t.hashed().unwrap().hash().unwrap());
                }
                TensorAxisIndex::Slice(sl) => sl.update_hash(&mut hasher),
            }
        }
        hasher.finalize().into()
    }

    pub fn repr_bijection(&self, is_full_text: bool) -> Result<String> {
        let mut result = "[".to_owned();
        for (i, idx) in self.0.iter().enumerate() {
            result.push_str(&match idx {
                TensorAxisIndex::Single(i) => i.to_string(),
                TensorAxisIndex::Slice(slice) => {
                    slice.start.map(|i| i.to_string()).unwrap_or("".to_owned())
                        + ":"
                        + &slice.stop.map(|i| i.to_string()).unwrap_or("".to_owned())
                }
                TensorAxisIndex::Tensor(tensor) => {
                    if is_full_text {
                        pycall!(
                            atr!(
                                pycall!(atr!(tensor.tensor(), tolist, raw), (), raw),
                                __repr__,
                                raw
                            ),
                            ()
                        )
                    } else {
                        save_tensor((**tensor).clone(), false)?;
                        "t".to_owned()
                            + &base16::encode_lower(&tensor.hash().unwrap())[..10]
                            + &format!(" [{}]", tensor.shape()[0])
                    }
                }
            });
            if i != self.0.len() - 1 {
                result.push(',');
            }
        }
        result.push(']');
        Ok(result)
    }

    pub fn from_bijection_string(
        string: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        let er = ParseError::InvalidIndex {
            string: string.to_owned(),
        };
        Ok(TensorIndex(
            string
                .strip_prefix('[')
                .ok_or(er.clone())?
                .strip_suffix(']')
                .ok_or(er.clone())?
                .split(',')
                .map(str::trim)
                .filter(|x| !x.is_empty())
                .map(|x| -> Result<_> {
                    if let Ok(int) = parse_numeric(x) {
                        return Ok(TensorAxisIndex::Single(int));
                    }
                    if let Some(no_t) = x.strip_prefix('t') {
                        let no_t_pre_bracket = no_t.split('[').next().unwrap().trim();
                        return tensor_cache
                            .as_mut()
                            .map(|tc| tc.get_tensor(no_t_pre_bracket.to_owned()))
                            .unwrap_or_else(|| {
                                get_tensor_prefix(no_t_pre_bracket)
                                    .context("tensor hash from string")
                            })
                            .and_then(|x| {
                                Ok(TensorAxisIndex::Tensor(
                                    x.try_into()
                                        .context("index tensor loaded from disk is invalid")?,
                                ))
                            });
                    }

                    let get_slice_bound = |item: &str, name: &str| {
                        if item.is_empty() {
                            Ok(None)
                        } else {
                            parse_numeric(item)
                                .with_context(|| {
                                    format!(
                                        "failed to parse {} of slice, index string='{}'",
                                        name, string
                                    )
                                })
                                .map(Some)
                        }
                    };

                    if let [start, stop] = x.split(':').map(str::trim).collect::<Vec<_>>()[..] {
                        return Ok(TensorAxisIndex::Slice(Slice {
                            start: get_slice_bound(start, "start")?,
                            stop: get_slice_bound(stop, "stop")?,
                        }));
                    }
                    bail!(er.clone())
                })
                .collect::<Result<Vec<_>>>()?,
        ))
    }
}

impl IntoPy<PyObject> for TensorIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

pub fn compose(top: &TensorIndex, bottom: &TensorIndex) -> Option<TensorIndex> {
    let mut result: Vec<TensorAxisIndex> = vec![];
    let mut top_idx: usize = 0;
    for bottom_idx in bottom.0.iter() {
        match bottom_idx {
            TensorAxisIndex::Single(_i) => result.push(bottom_idx.clone()),
            TensorAxisIndex::Tensor(t) => {
                let top_here = top.0[top_idx].clone();
                top_idx += 1;
                Python::with_gil(|py| {
                    let indexed_tensor = (**t).clone().py_getitem(py, top_here).unwrap();
                    if indexed_tensor.ndim() == 0 {
                        result.push(TensorAxisIndex::Single(pycall!(
                            PY_UTILS.cast_int,
                            (indexed_tensor,)
                        )));
                    } else {
                        result.push(TensorAxisIndex::Tensor(indexed_tensor.try_into().unwrap()));
                    }
                })
            }
            TensorAxisIndex::Slice(slice) => {
                let start = slice.start.unwrap_or(0);
                let stop = slice.stop;
                let top_here = top.0[top_idx].clone();
                match top_here {
                    TensorAxisIndex::Single(i) => {
                        if i < 0 {
                            result.push(TensorAxisIndex::Single(stop.unwrap_or(0) + i))
                        } else {
                            result.push(TensorAxisIndex::Single(start + i))
                        }
                    }
                    TensorAxisIndex::Tensor(t) => {
                        if start < 0 {
                            return None;
                        } else {
                            Python::with_gil(|py| {
                                result.push(TensorAxisIndex::Tensor(
                                    (*t).clone().py_add(py, start).unwrap().try_into().unwrap(),
                                ))
                            })
                        }
                    }
                    TensorAxisIndex::Slice(top_slice) => {
                        let top_start = top_slice.start.unwrap_or(0);
                        let top_stop = top_slice.stop;
                        let (mut new_start, mut new_stop) =
                            (Some(start + top_start), Some(start + top_stop.unwrap_or(0)));
                        if top_start < 0 {
                            new_start = Some(stop.unwrap_or(0) + top_start);
                        }
                        if top_stop.unwrap_or(-1) < 0 {
                            if top_stop.is_none() && stop.is_none() {
                                new_stop = None;
                            } else {
                                new_stop = Some(stop.unwrap_or(0) + top_stop.unwrap_or(0));
                            }
                        }
                        // if you add negative and positive indices and get 0, you really meant "end", or None
                        if (top_stop.is_some() && top_stop.unwrap() < 0 || start < 0)
                            && new_stop == Some(0)
                        {
                            new_stop = None
                        }
                        result.push(TensorAxisIndex::Slice(Slice {
                            start: new_start,
                            stop: new_stop,
                        }))
                    }
                }
                // dbg!(top, bottom);
                top_idx += 1;
            }
        }
    }
    Some(TensorIndex(result))
}

pub fn string_escape(s: &String) -> String {
    format!("\"{}\"", s.replace('\\', r"\\").replace('"', "\\\""))
}

/// use string so you can compare fast when constructing and have full range (weird types like uint or bfloat16)
/// as opposed to PyObject torch.dtype or enum (could switch to enum)
#[pyclass]
#[derive(Copy, Clone, PartialEq, Eq, Default, PartialOrd, Ord)]
pub struct TorchDeviceDtypeOp {
    #[pyo3(get)]
    pub device: Option<TorchDevice>,
    #[pyo3(get)]
    pub dtype: Option<TorchDtype>,
}
impl std::fmt::Debug for TorchDeviceDtypeOp {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{{device:{},dtype:{}}}",
            self.device
                .map(|x| String::from(&x))
                .unwrap_or("None".to_owned()),
            self.dtype
                .map(|x| String::from(&x))
                .unwrap_or("None".to_owned())
        )
    }
}

#[pymethods]
impl TorchDeviceDtypeOp {
    #[staticmethod]
    #[pyo3(name = "default")]
    fn default_py() -> Self {
        Self::default()
    }

    #[new]
    fn new(device: Option<TorchDevice>, dtype: Option<TorchDtype>) -> Self {
        Self { device, dtype }
    }

    pub fn only_keep_floating(&self) -> Self {
        Self {
            device: self.device,
            dtype: if self.dtype.map(|x| x.is_floating_point()).unwrap_or(false) {
                self.dtype
            } else {
                None
            },
        }
    }

    pub fn __repr__(&self) -> String {
        format!(
            "TorchDeviceDtypeOp(device={}, dtype={})",
            self.device
                .as_ref()
                .map(|x| format!("\"{}\"", String::from(x)))
                .unwrap_or("None".to_owned()),
            self.dtype
                .as_ref()
                .map(|x| format!("\"{}\"", String::from(x)))
                .unwrap_or("None".to_owned())
        )
    }

    pub fn get_torch_dtype(&self) -> Option<PyObject> {
        self.dtype.map(TorchDtype::get_torch)
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }
}
macro_rules! lit_or {
    ($a:ident, $b:literal) => {
        $b
    };
    ($a:ident) => {
        stringify!($a)
    };
}
macro_rules! string_enum{
    {$name:ident,$converter:expr, ($($var:ident $(=$lit:literal)?),*)}=>{
        #[derive(Copy, Clone, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
        #[allow(non_camel_case_types)]
        pub enum $name{
            $($var,)*
        }
        impl From<&$name> for String{
            #[allow(unreachable_code)]
            fn from(value:&$name)->Self{
                match value{
                    $($name::$var=>{
                        $(return $lit.to_owned();)*
                        return stringify!($var).to_owned();
                    }),*
                }
            }
        }
        impl TryFrom<String> for $name{
            type Error = Error;
            fn try_from(value:String)->Result<$name>{
                let inp_str_str:&str = &value;
                match inp_str_str{
                    $(
                        lit_or!($var $(,$lit)?)=>Ok($name::$var),
                    )*
                    _=>Err(anyhow!("invalid value for enum {}, {}", stringify!($name), value).into())
                }
            }
        }
        impl TryFrom<&str> for $name{
            type Error = Error;
            fn try_from(value:&str)->Result<$name>{
                match value{
                    $(
                        lit_or!($var $(,$lit)?)=>Ok($name::$var),
                    )*
                    _=>Err(anyhow!("invalid value for enum {}, {}", stringify!($name), value).into())
                }
            }
        }
        impl IntoPy<PyObject> for $name {
            fn into_py(self, py: Python<'_>) -> PyObject {
                String::from(&self).into_py(py)
            }
        }
        impl<'source> FromPyObject<'source> for $name {
            fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
                let converter:Option<&dyn Fn(&pyo3::PyAny)->Option<String>> = $converter;
                let inp_str:String  = if let Some(converter) = converter{
                    circuit_obj.extract().or_else(|_e|{let thing:Option<String> = converter(circuit_obj); thing.ok_or_else(||anyhow!("dtype not string or pytorch dtype object"))}
                )
                }else{
                    circuit_obj.extract::<String>().context("string enum conversion failed")
                }?;
                let resulty:Result<$name> = inp_str.try_into();
                resulty.map_err(|e|e.into())
            }
        }
    }
}
string_enum! {
    TorchDtype,
    Some(&|obj|pycall!(PY_UTILS.maybe_dtype_to_maybe_string,(obj,))),
    (
        float16,
        bfloat16,
        float32,
        float64,
        int8,
        int16,
        int32,
        int64,
        uint8,
        bool
    )
}

impl TorchDtype {
    pub fn get_torch(self) -> PyObject {
        PY_UTILS.dtype_convert[&self].clone()
    }

    pub fn is_floating_point(self) -> bool {
        matches!(
            self,
            Self::float16 | Self::bfloat16 | Self::float32 | Self::float64
        )
    }

    // pub fn is_integral(self) -> bool {
    //     // I assume this shouldn't include bool? idk though
    //     matches!(
    //         self,
    //         Self::int8 | Self::int16 | Self::int32 | Self::int64 | Self::uint8
    //     )
    // }
    pub fn from_python(x: PyObject) -> Result<Self> {
        Python::with_gil(|py| {
            if !x
                .as_ref(py)
                .is_instance(PY_UTILS.torch.getattr(py, "dtype")?.as_ref(py))?
            {
                bail!("not torch dtype")
            }
            let s: String = x.call_method1(py, "__str__", ())?.extract(py)?;
            s[6..].to_owned().try_into()
        })
    }
}

string_enum! {
    TorchDevice,
    None,
    (
        Cpu="cpu",
        Cuda0="cuda:0",
        Cuda1="cuda:1",
        Cuda2="cuda:2",
        Cuda3="cuda:3",
        Cuda4="cuda:4",
        Cuda5="cuda:5",
        Cuda6="cuda:6",
        Cuda7="cuda:7",
        Cuda8="cuda:8",
        Cuda9="cuda:9",
        Cuda10="cuda:10",
        Cuda11="cuda:11",
        Cuda12="cuda:12",
        Cuda13="cuda:13",
        Cuda14="cuda:14",
        Cuda15="cuda:15"
    )
}

impl TorchDevice {
    pub const CUDA: TorchDevice = TorchDevice::Cuda0;

    pub fn is_cuda(&self) -> bool {
        matches!(self, |Self::Cuda0| Self::Cuda1
            | Self::Cuda2
            | Self::Cuda3
            | Self::Cuda4
            | Self::Cuda5
            | Self::Cuda6
            | Self::Cuda7
            | Self::Cuda8
            | Self::Cuda9
            | Self::Cuda10
            | Self::Cuda11
            | Self::Cuda12
            | Self::Cuda13
            | Self::Cuda14
            | Self::Cuda15)
    }
    pub fn from_python(x: PyObject) -> Result<Self> {
        Python::with_gil(|py| {
            if !x
                .as_ref(py)
                .is_instance(PY_UTILS.torch.getattr(py, "device")?.as_ref(py))?
            {
                bail!("not torch device")
            }
            let s: String = x.getattr(py, "type")?.extract(py)?;
            if &s == "cpu" {
                return Ok(TorchDevice::Cpu);
            }
            let idx: usize = atr!(x, index);
            ("cuda".to_owned() + ":" + &idx.to_string()).try_into()
        })
    }
}

#[pyclass]
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct TorchDeviceDtype {
    #[pyo3(get)]
    pub device: TorchDevice,
    #[pyo3(get)]
    pub dtype: TorchDtype,
}
impl std::fmt::Debug for TorchDeviceDtype {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{{device:{},dtype:{}}}",
            String::from(&self.device),
            String::from(&self.dtype)
        )
    }
}

#[pymethods]
impl TorchDeviceDtype {
    #[new]
    fn new(device: TorchDevice, dtype: TorchDtype) -> Self {
        Self { device, dtype }
    }

    pub fn cast_tensor(&self, tensor: Tensor) -> Tensor {
        Python::with_gil(|py| {
            PY_UTILS
                .cast_tensor
                .call(py, (tensor, *self), None)
                .unwrap()
                .extract(py)
                .unwrap()
        })
    }

    pub fn op(&self) -> TorchDeviceDtypeOp {
        (*self).into()
    }

    pub fn __repr__(&self) -> String {
        format!(
            "TorchDeviceDtype(device=\"{}\", dtype=\"{}\")",
            String::from(&self.device),
            String::from(&self.dtype),
        )
    }

    pub fn get_torch_dtype(&self) -> PyObject {
        self.dtype.get_torch()
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }
}

impl TorchDeviceDtype {
    pub fn size(&self) -> usize {
        match self.dtype {
            TorchDtype::float32 => 4,
            TorchDtype::float64 => 8,
            TorchDtype::float16 => 2,
            TorchDtype::bfloat16 => 2,
            TorchDtype::int64 => 8,
            TorchDtype::int32 => 4,
            TorchDtype::int16 => 2,
            TorchDtype::int8 => 1,
            TorchDtype::uint8 => 1,
            TorchDtype::bool => 1,
        }
    }
}

impl From<TorchDeviceDtype> for TorchDeviceDtypeOp {
    fn from(x: TorchDeviceDtype) -> Self {
        Self {
            device: Some(x.device),
            dtype: Some(x.dtype),
        }
    }
}

impl TorchDeviceDtypeOp {
    pub const NONE: Self = TorchDeviceDtypeOp {
        device: None,
        dtype: None,
    };
    pub const TENSOR_DEFAULT: Self = TorchDeviceDtypeOp {
        device: Some(TorchDevice::Cpu),
        dtype: Some(TorchDtype::float32),
    };

    pub fn combine(self, other: Self) -> Result<Self> {
        let out = Self {
            device: match (&self.device, &other.device) {
                (Some(l), Some(r)) if l != r => {
                    bail!(MiscInputError::ChildrenMultipleDevices {
                        a: self.device,
                        b: other.device,
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
            dtype: match (&self.dtype, &other.dtype) {
                (Some(l), Some(r)) if l != r => {
                    bail!(MiscInputError::ChildrenMultipleDtypes {
                        a: self.dtype,
                        b: other.dtype,
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
        };
        Ok(out)
    }

    pub fn unwrap_or_defaults(self) -> TorchDeviceDtype {
        TorchDeviceDtype {
            dtype: self.dtype.unwrap_or(TorchDtype::float64),
            device: self.device.unwrap_or(TorchDevice::Cpu),
        }
    }

    pub fn size(&self) -> usize {
        (*self).unwrap_or_defaults().size()
    }
    pub fn overwrite(&self, concrete: &TorchDeviceDtype) -> TorchDeviceDtype {
        let mut result = *concrete;
        if let Some(x) = &self.device {
            result.device = *x;
        }
        if let Some(x) = &self.dtype {
            result.dtype = *x;
        }
        result
    }
    pub fn override_other(&self, other: TorchDeviceDtypeOp) -> TorchDeviceDtypeOp {
        let mut result = other;
        if let Some(x) = &self.device {
            result.device = Some(*x);
        }
        if let Some(x) = &self.dtype {
            result.dtype = Some(*x);
        }
        result
    }
    pub fn cast_tensor(&self, tensor: Tensor) -> Tensor {
        let concrete = self.overwrite(&tensor.device_dtype());
        concrete.cast_tensor(tensor)
    }
    pub fn hash(&self, hasher: &mut blake3::Hasher) {
        if let Some(dev) = self.device {
            hasher.update(&[1, dev as u8]);
        } else {
            hasher.update(&[0, 0]);
        }
        if let Some(typ) = self.dtype {
            hasher.update(&[1, typ as u8]);
        } else {
            hasher.update(&[0, 0]);
        }
    }
}

impl Default for TorchDeviceDtype {
    fn default() -> Self {
        TorchDeviceDtypeOp::NONE.unwrap_or_defaults()
    }
}

#[apply(python_error_exception)]
#[base_error_name(Parse)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ParseError {
    #[error("Parsing number failed string='{string}', err={err_string} ({e_name})")]
    InvalidNumber { string: String, err_string: String },

    #[error("string='{string}'\nindex should look like '[1,3:5,f6d587856c8444a9]'\n({e_name})")]
    InvalidIndex { string: String },

    #[error("Expected UUID string, found '{string}'\nerr_msg={err_msg} ({e_name})")]
    InvalidUuid { string: String, err_msg: String },

    #[error("Einsum string invalid {string} {substring} ({e_name})")]
    EinsumStringInvalid { string: String, substring: String },

    #[error("Einsum string doesn't have arrow {string} ({e_name})")]
    EinsumStringNoArrow { string: String },

    #[error("factors={factors:?} string='{string}' ({e_name})")]
    FactorProductTooLarge { factors: Vec<usize>, string: String },

    #[error("i={i} >= bound={bound} ({e_name})")]
    SymbolicSizeNumberOutOfBounds { i: usize, bound: usize },
}

pub const UINT_WITH_UNDERSCORE: &str = r"\d[\d_]*";

pub fn parse_numeric<T: FromStr>(x: &str) -> Result<T, ParseError>
where
    T::Err: fmt::Display,
{
    // this allows (e.g.) stuff like 38473.___3 or -___3 which isn't allowed in rust. Seems fine to me (for now).
    (x.chars().take(1).collect::<String>()
        + &x.chars().skip(1).collect::<String>().replace('_', ""))
        .parse::<T>()
        .map_err(|e| ParseError::InvalidNumber {
            err_string: e.to_string(),
            string: x.to_owned(),
        })
}

#[test]
fn test_parse_numeric() {
    assert!(parse_numeric::<usize>("hi").is_err());
    assert!(parse_numeric::<usize>("_1").is_err());
    assert!(parse_numeric::<usize>("__2").is_err());
    assert!(parse_numeric::<usize>("_387483741").is_err());
    assert!(parse_numeric::<usize>("_38748_3741").is_err());
    assert!(parse_numeric::<f64>("_.38748_3741").is_err());
    assert!(parse_numeric::<f64>("_1.1").is_err());

    assert_eq!(parse_numeric::<usize>("38748_3741").unwrap(), 387_483_741);
    assert_eq!(
        parse_numeric::<usize>("38748_____3741").unwrap(),
        387_483_741
    );
    assert_eq!(
        parse_numeric::<usize>("3_____8748_3741").unwrap(),
        387_483_741
    );
    assert_eq!(parse_numeric::<f64>("3.38473").unwrap(), 3.38473);
    assert_eq!(parse_numeric::<f64>("3.").unwrap(), 3.);
    assert_eq!(parse_numeric::<f64>("3____.3").unwrap(), 3.3);
    assert_eq!(parse_numeric::<f64>("3.____3__").unwrap(), 3.3);
}
