use std::{
    borrow::Borrow,
    cmp::max,
    fmt::{self, Debug, Display},
    iter::zip,
    str::FromStr,
};

use anyhow::{bail, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::{exceptions::PyValueError, prelude::*, pyclass, types::PyTuple};
use smallvec::SmallVec as Sv;
use thiserror::Error;

use crate::{
    python_error_exception, sv,
    tensor_util::{parse_numeric, ParseError, UINT_WITH_UNDERSCORE},
};

pub type Shape = Sv<[Size; 4]>;

/// OpSize is a memory optimization of Option<usize> that stores a 63-bit int and one "is this none" bit
#[derive(Clone, Copy, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Size(pub u64);

static UNKNOWN_DIM_MESSAGE: &str = "found unknown dim size when concrete size expected, possibly you are trying to do an operation along a dim with unknown size, or using a rewrite that doesn't support unknown sizes? (or possibly there's a bug)";

impl Size {
    pub const SHIFT: usize = 63;
    pub const NONE: Size = Size(1 << Self::SHIFT);

    pub fn some(x: usize) -> Self {
        const _: () = assert!(std::mem::size_of::<usize>() <= std::mem::size_of::<u64>());
        assert!(Self::is_valid_some(x));
        Size(x as u64)
    }
    #[inline(always)]
    pub fn is_valid_some(x: usize) -> bool {
        x >> Self::SHIFT == 0
    }
    pub fn is_some(&self) -> bool {
        self.0 >> Self::SHIFT == 0
    }
    pub fn is_none(&self) -> bool {
        self.0 >> Self::SHIFT != 0
    }
    pub fn eq_if_known(self, other: Size) -> bool {
        self.is_none() || other.is_none() || self.unwrap() == other.unwrap()
    }
    pub fn eq_and_known(self, other: Size) -> bool {
        self.is_known() && other.is_known() && self.eq(&other)
    }
    pub fn is(self, x: usize) -> bool {
        self.is_some() && self.unwrap() == x
    }
    pub fn is_if_known(self, x: usize) -> bool {
        !self.is_some() || self.unwrap() == x
    }
    pub fn known(x: usize) -> Self {
        Self::some(x)
    }
    pub fn is_known(self) -> bool {
        self.is_some()
    }
    pub fn unwrap(self) -> usize {
        assert!(self.is_known(), "{}", UNKNOWN_DIM_MESSAGE);
        self.0 as usize
    }
    pub fn unwrap_or(self, x: usize) -> usize {
        if self.is_none() {
            x
        } else {
            self.0 as usize
        }
    }
    pub fn unwrap_err(self) -> Result<usize> {
        if !self.is_known() {
            bail!(UNKNOWN_DIM_MESSAGE)
        }
        Ok(self.unwrap())
    }
    pub fn map<F>(self, f: F) -> Self
    where
        F: FnOnce(usize) -> usize,
    {
        if self.is_none() {
            Size::NONE
        } else {
            Size::known(f(self.0 as usize))
        }
    }
    pub fn combine_with<F>(self, other: Size, f: F) -> Self
    where
        F: FnOnce(usize, usize) -> usize,
    {
        match (self.t(), other.t()) {
            (Some(x), Some(y)) => Self::known(f(x, y)),
            _ => Self::NONE,
        }
    }
    pub fn t(self) -> Option<usize> {
        self.into()
    }
    pub fn to_le_bytes(&self) -> [u8; 8] {
        self.0.to_le_bytes()
    }
    pub fn join_with<F>(&self, other: &Size, f: F) -> Result<Self>
    where
        F: FnOnce(usize, usize) -> Result<usize>,
    {
        Ok(match (self.t(), other.t()) {
            (Some(a), Some(b)) => Size::known(f(a, b)?),
            (None, _) => *other,
            (_, None) => *self,
        })
    }
    pub fn join_eq<F>(&self, other: &Size, err: F) -> Result<Self>
    where
        F: FnOnce() -> anyhow::Error,
    {
        Ok(match (self.t(), other.t()) {
            (Some(a), Some(b)) => Size::known(if a == b { a } else { bail!(err()) }),
            (None, _) => *other,
            (_, None) => *self,
        })
    }
}

static MAYBE_SYMBOLIC_SIZE: Lazy<String> = Lazy::new(|| format!(r"{}s?", UINT_WITH_UNDERSCORE));
// still parse old symbolic sizes for back compat, convert then to unknown
pub static SIZE_MATCH: Lazy<String> =
    Lazy::new(|| format!(r"(?:\?|(?:{d}\s*\*\s*)*{d})", d = *MAYBE_SYMBOLIC_SIZE));

#[pyfunction]
pub fn symbolic_sizes() -> Vec<Size> {
    vec![Size::NONE; 256]
}

impl FromStr for Size {
    type Err = ParseError;
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        let parse_item = |x: &str| -> Result<_, _> {
            let x = x.trim();
            let out = if x.ends_with('s') {
                let mut chars = x.chars().collect::<Vec<_>>();
                chars.pop(); // drop last
                parse_numeric::<usize>(&chars.into_iter().collect::<String>())?;
                (true, 0)
            } else {
                (false, parse_numeric(x)?)
            };
            Ok(out)
        };

        if s == "?" {
            return Ok(Size::NONE);
        }

        let all_sizes = if s.contains('*') {
            s.split('*').map(parse_item).collect()
        } else {
            parse_item(s).map(|x| vec![x])
        };
        let all_sizes = all_sizes?;
        if all_sizes.iter().any(|(a, _)| *a) {
            Ok(Size::NONE)
        } else {
            return Ok(Size::known(all_sizes.iter().map(|(_, b)| b).product()));
        }
    }
}

#[pyclass(name = "Size", module = "rust_circuit")]
#[derive(Clone, Debug)]
pub struct PySize(pub Size);

#[pymethods]
impl PySize {
    fn __str__(&self) -> String {
        self.0.to_string()
    }
    fn __repr__(&self) -> String {
        self.0.to_string()
    }
    fn __richcmp__(&self, other: &PyAny, cmp: pyo3::basic::CompareOp) -> bool {
        if let Ok(o) = other.extract::<Size>() {
            cmp.matches(self.0.cmp(&o))
        } else {
            false
        }
    }
    #[staticmethod]
    fn known(x: usize) -> Self {
        PySize(Size::known(x))
    }
    #[classattr]
    #[pyo3(name = "NONE")]
    fn none() -> Self {
        PySize(Size::NONE)
    }
}

impl<'source> FromPyObject<'source> for Size {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        if ob.is_none() {
            Ok(Size::NONE)
        } else if let Ok(x) = ob.extract::<PySize>() {
            Ok(x.0)
        } else {
            Ok(Size::known(ob.extract()?))
        }
    }
}

impl IntoPy<PyObject> for Size {
    fn into_py(self, py: Python<'_>) -> PyObject {
        static PY_NONE_SZ: Lazy<PyObject> =
            Lazy::new(|| Python::with_gil(|py| PySize(Size::NONE).into_py(py)));
        match self.t() {
            None => PY_NONE_SZ.clone(),
            // None => py.None(),
            Some(x) => x.into_py(py),
        }
    }
}

macro_rules! arith_op {
    ($self:ty, $trait:ty, $m:ident, $rhs:ty) => {
        impl $trait for $self {
            type Output = Size;
            fn $m(self, rhs: $rhs) -> Size {
                self.map(|x| x.$m(rhs))
            }
        }
    };
}
macro_rules! arith_combine_op {
    ($self:ty, $trait:ty, $m:ident) => {
        impl $trait for $self {
            type Output = Size;
            fn $m(self, rhs: Size) -> Size {
                self.combine_with(rhs, |x, y| x.$m(y))
            }
        }
    };
}
macro_rules! mk_arith {
    ($trait_size:ty, $trait_usize:ty, $m: ident) => {
        arith_op!(Size, $trait_usize, $m, usize);
        arith_op!(&Size, $trait_usize, $m, usize);
        arith_combine_op!(Size, $trait_size, $m);
        arith_combine_op!(&Size, $trait_size, $m);
    };
}

mk_arith!(std::ops::Sub<Size>, std::ops::Sub<usize>, sub);
mk_arith!(std::ops::Add<Size>, std::ops::Add<usize>, add);
mk_arith!(std::ops::Div<Size>, std::ops::Div<usize>, div);
mk_arith!(std::ops::Mul<Size>, std::ops::Mul<usize>, mul);
mk_arith!(std::ops::Rem<Size>, std::ops::Rem<usize>, rem);

impl std::iter::Sum<Size> for Size {
    fn sum<I: Iterator<Item = Size>>(iter: I) -> Self {
        iter.fold(Size::known(0), |a, b| a + b)
    }
}

impl std::iter::Product<Size> for Size {
    fn product<I: Iterator<Item = Size>>(iter: I) -> Self {
        iter.fold(Size::known(1), |a, b| a * b)
    }
}

impl From<Option<usize>> for Size {
    fn from(x: Option<usize>) -> Self {
        match x {
            None => Size::NONE,
            Some(y) => Size::known(y),
        }
    }
}
impl From<Size> for Option<usize> {
    fn from(x: Size) -> Self {
        if x.is_none() {
            None
        } else {
            Some(x.0 as usize)
        }
    }
}

pub fn shape_from_known(x: &[usize]) -> Sv<[Size; 4]> {
    x.iter().map(|a| Size::known(*a)).collect()
}

pub fn shape_eq(a: &[Size], b: &[Size]) -> bool {
    a.len() == b.len() && zip(a, b).all(|(x, y)| Size::eq(x, y))
}

pub fn shape_eq_if_known(x: &[Size], y: &[Size]) -> bool {
    x.len() == y.len() && zip(x, y).all(|(x, y)| x.eq_if_known(*y))
}

pub fn shape_eq_and_known(x: &[Size], y: &[Size]) -> bool {
    shape_is_known(x) && shape_is_known(y) && shape_eq(x, y)
}

pub fn shape_is_known(x: &[Size]) -> bool {
    x.iter().all(|x| x.is_known())
}

pub fn shape_into_known(x: Shape) -> Vec<usize> {
    assert!(shape_is_known(&x), "{}", UNKNOWN_DIM_MESSAGE);
    unsafe { std::mem::transmute::<Vec<Size>, Vec<usize>>(x.into_vec()) }
}
pub fn shape_as_known(x: &[Size]) -> &[usize] {
    assert!(shape_is_known(x), "{}", UNKNOWN_DIM_MESSAGE);
    unsafe { std::mem::transmute::<&[Size], &[usize]>(x) }
}

pub fn shape_try_into_known(x: Shape) -> Option<Vec<usize>> {
    if !shape_is_known(&x) {
        return None;
    }
    Some(unsafe { std::mem::transmute::<Vec<Size>, Vec<usize>>(x.into_vec()) })
}

pub fn shape_try_as_known(x: &[Size]) -> Option<&[usize]> {
    if !shape_is_known(x) {
        return None;
    }
    Some(unsafe { std::mem::transmute::<&[Size], &[usize]>(x) })
}

pub fn shape_as_known_result(x: &[Size]) -> Result<&[usize]> {
    if !shape_is_known(x) {
        bail!(UNKNOWN_DIM_MESSAGE);
    }
    Ok(unsafe { std::mem::transmute::<&[Size], &[usize]>(x) })
}

pub fn shape_join_eq<F>(x: &[Size], y: &[Size], mut err: F) -> Result<Shape>
where
    F: FnMut() -> anyhow::Error,
{
    zip(x, y).map(|(a, b)| a.join_eq(b, &mut err)).collect()
}

pub fn shape_to_py(x: &[Size]) -> PyObject {
    Python::with_gil(|py| PyTuple::new(py, x).into())
}

impl Debug for Size {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.is_known() {
            Debug::fmt(&self.unwrap(), f)
        } else {
            f.write_str("?")
        }
    }
}
impl Display for Size {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.is_known() {
            Display::fmt(&self.unwrap(), f)
        } else {
            f.write_str("?")
        }
    }
}

impl ToPyObject for Size {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.into_py(py)
    }
}

#[crate::pyo3::pyfunction]
#[pyo3(name = "broadcast_shapes", signature = (*shapes))]
pub fn broadcast_shapes_py(shapes: Vec<Shape>) -> Result<PyObject> {
    Ok(shape_to_py(&broadcast_shapes(&shapes)?))
}

/// broadcast, but don't broadcast on 1s
pub fn right_align_shapes(shapes: &[impl Borrow<[Size]>]) -> Result<Shape> {
    broadcast_shapes_impl(shapes, false)
}

pub fn broadcast_shapes(shapes: &[impl Borrow<[Size]>]) -> Result<Shape> {
    broadcast_shapes_impl(shapes, true)
}

pub fn broadcast_shapes_impl(
    shapes: &[impl Borrow<[Size]>],
    special_case_ones: bool,
) -> Result<Shape> {
    if shapes.is_empty() {
        return Ok(sv![]);
    }
    if shapes.len() == 1 {
        return Ok(shapes[0].borrow().into());
    }
    let ranks: Vec<usize> = shapes.iter().map(|x| x.borrow().len()).collect();
    let out_rank = *ranks.iter().max().unwrap();
    let mut existing: Shape = sv![Size::NONE; out_rank];
    let mut seen_here: Vec<bool> = vec![false; out_rank];
    for axis_from_end in 1..out_rank + 1 {
        for (i, shape) in shapes.iter().enumerate() {
            match ranks[i].checked_sub(axis_from_end) {
                None => {}
                Some(j) => {
                    let axis_len = shape.borrow()[j];
                    let cur = existing[out_rank - axis_from_end];
                    let success = cur.eq_if_known(axis_len)
                        || (special_case_ones && cur.unwrap() == 1 && axis_len.unwrap() != 0)
                        || (special_case_ones && axis_len.unwrap() == 1 && cur.unwrap() != 0);
                    if !success {
                        bail!(ShapeError::NotBroadcastable {
                            shapes: shapes.iter().map(|x| x.borrow().into()).collect(),
                        });
                    }
                    let seen_here_ = seen_here[out_rank - axis_from_end];
                    existing[out_rank - axis_from_end] = match (axis_len.t(), cur.t()) {
                        (Some(x), Some(y)) => Size::known(max(x, y)),
                        (Some(x), None) if special_case_ones && seen_here_ && x == 1 => Size::NONE,
                        (None, Some(x)) if special_case_ones && seen_here_ && x == 1 => Size::NONE,
                        (None, _) => cur,
                        _ => axis_len,
                    };
                    seen_here[out_rank - axis_from_end] = true;
                }
            }
        }
    }
    Ok(existing)
}

#[apply(python_error_exception)]
#[base_error_name(Shape)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ShapeError {
    #[error("Shapes aren't broadcastable, {shapes:?} ({e_name})")]
    NotBroadcastable { shapes: Vec<Shape> },
}

#[test]
fn test_broadcast_shapes() {
    let run = |x: &[Sv<[usize; 4]>]| {
        broadcast_shapes(&x.iter().map(|a| shape_from_known(a)).collect::<Vec<_>>())
    };
    let s = |x: Sv<[usize; 4]>| shape_from_known(&x[..]);
    let eq = |x: Shape, y: Shape| shape_eq(&x, &y);
    assert!(eq(run(&[]).unwrap(), sv![]));
    assert!(eq(run(&[sv![], sv![]]).unwrap(), s(sv![])));
    assert!(eq(run(&[sv![], sv![]]).unwrap(), s(sv![])));
    assert!(eq(run(&[sv![1], sv![]]).unwrap(), s(sv![1])));
    assert!(eq(run(&[sv![], sv![1]]).unwrap(), s(sv![1])));
    assert!(eq(run(&[sv![3], sv![]]).unwrap(), s(sv![3])));
    assert!(eq(run(&[sv![], sv![3]]).unwrap(), s(sv![3])));
    assert!(eq(run(&[sv![1], sv![1]]).unwrap(), s(sv![1])));
    assert!(eq(run(&[sv![3], sv![3]]).unwrap(), s(sv![3])));
    assert!(eq(run(&[sv![1], sv![4, 3]]).unwrap(), s(sv![4, 3])));
    assert!(eq(run(&[sv![4, 3], sv![4, 1]]).unwrap(), s(sv![4, 3])));
    assert!(eq(run(&[sv![4, 3], sv![1, 3]]).unwrap(), s(sv![4, 3])));
    assert!(eq(run(&[sv![4, 1], sv![4, 3]]).unwrap(), s(sv![4, 3])));
    assert!(eq(run(&[sv![1, 3], sv![4, 3]]).unwrap(), s(sv![4, 3])));
    assert!(eq(
        run(&[sv![1, 3], sv![4, 3], sv![5, 4, 1]]).unwrap(),
        s(sv![5, 4, 3])
    ));
    assert!(eq(
        run(&[sv![3, 4, 5], sv![3, 4, 5], sv![3, 4, 5]]).unwrap(),
        s(sv![3, 4, 5])
    ));

    assert!(run(&[sv![5], sv![6]]).is_err());
    assert!(run(&[sv![3, 5], sv![5, 1]]).is_err());
    assert!(run(&[sv![5, 0], sv![5, 1]]).is_err());
    assert!(run(&[sv![5, 2], sv![5, 1]]).is_ok());
    assert!(run(&[sv![1, 2, 2], sv![1, 2], sv![3, 2, 2, 2, 172112]]).is_err());

    let run_align = |x: &[Sv<[usize; 4]>]| {
        right_align_shapes(&x.iter().map(|a| shape_from_known(a)).collect::<Vec<_>>())
    };

    assert!(eq(run_align(&[]).unwrap(), sv![]));
    assert!(eq(run_align(&[sv![], sv![]]).unwrap(), s(sv![])));
    assert!(eq(run_align(&[sv![], sv![]]).unwrap(), s(sv![])));
    assert!(eq(run_align(&[sv![1], sv![]]).unwrap(), s(sv![1])));
    assert!(eq(run_align(&[sv![], sv![1]]).unwrap(), s(sv![1])));
    assert!(eq(run_align(&[sv![3], sv![]]).unwrap(), s(sv![3])));
    assert!(eq(run_align(&[sv![], sv![3]]).unwrap(), s(sv![3])));
    assert!(eq(run_align(&[sv![1], sv![1]]).unwrap(), s(sv![1])));
    assert!(eq(run_align(&[sv![3], sv![3]]).unwrap(), s(sv![3])));
    assert!(run_align(&[sv![1], sv![4, 3]]).is_err());
    assert!(run_align(&[sv![4, 3], sv![4, 1]]).is_err());
    assert!(run_align(&[sv![4, 3], sv![1, 3]]).is_err());
    assert!(run_align(&[sv![4, 1], sv![4, 3]]).is_err());
    assert!(run_align(&[sv![1, 3], sv![4, 3]]).is_err());
    assert!(run_align(&[sv![1, 3], sv![4, 3], sv![5, 4, 1]]).is_err());
    assert!(eq(
        run_align(&[sv![3, 4, 5], sv![3, 4, 5], sv![3, 4, 5]]).unwrap(),
        s(sv![3, 4, 5])
    ));

    assert!(run_align(&[sv![5], sv![6]]).is_err());
    assert!(run_align(&[sv![3, 5], sv![5, 1]]).is_err());
    assert!(run_align(&[sv![5, 0], sv![5, 1]]).is_err());
    assert!(run_align(&[sv![5, 2], sv![5, 1]]).is_err());
    assert!(run_align(&[sv![1, 2, 2], sv![1, 2], sv![3, 2, 2, 2, 172112]]).is_err());
}
