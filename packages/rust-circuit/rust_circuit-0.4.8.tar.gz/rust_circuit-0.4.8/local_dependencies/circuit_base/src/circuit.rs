use std::{
    fmt::{self, Debug},
    hash::Hash,
    ops::{Deref, DerefMut},
    sync::Arc,
};

use anyhow::{anyhow, bail, ensure, Context, Result};
use itertools::Itertools;
use num_bigint::BigUint;
use pyo3::{exceptions, prelude::*, PyTypeInfo};
use rr_util::{
    name::Name,
    py_types::{reduction_to_ints, PyOpAtAxes},
    rearrange_spec::{check_canon_axes_as, RearrangeSpec},
    shape::{Shape, Size},
    sv,
    tensor_util::TensorIndex,
    tu8v,
    util::{arc_ref_clone, arc_unwrap_or_clone, AsOp, HashBytes, NamedAxes},
};
use smallvec::ToSmallVec;

use crate::{
    circuit_info::{CachedCircuitInfo, CircuitFlags},
    self_funcs::SELF_FUNCS,
    CircuitNodeInit, *,
};

pub trait CircuitNodeSelfOnlyHash {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher);
}

#[macro_export]
macro_rules! circuit_node_self_only_hash_default_impl {
    ($type_name:ty) => {
        impl $crate::CircuitNodeSelfOnlyHash for $type_name {
            fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
                use $crate::circuit_node_private::CircuitNodeHashItems;
                self.compute_hash_non_name_non_children(hasher)
            }
        }
    };
}

pub trait CircuitNode: CircuitNodeInit + CircuitNodeSelfOnlyHash + Clone + Debug {
    // ==== implementable section ===
    //
    // NOTE: ALL FNS IN THIS SECTION *MUST* BE COPIED TO THE MACRO AND CircuitRc impl
    // If you add something here with a default impl, write a new impl for macro!
    // (up until default only section)
    //
    // we could enforce this sort of stuff with some proc macros, but seems like overkill atm.

    fn info(&self) -> &CachedCircuitInfo;
    /// child -> child dim -> parent dim it's the same as
    /// same as = index on that dim commutes w/ self
    /// must be None if not or if unsure
    /// if any parent dim is Some, then it must be sound to push down index into only the children w/ that dim
    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>>;

    /// free children must come first in children
    fn num_free_children(&self) -> usize {
        0
    }

    /// assumes children.len() == self.children().len()
    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self>
    where
        Self: Sized;

    fn node_type_uuid(&self) -> [u8; 16];

    fn self_flops(&self) -> BigUint {
        BigUint::from(0usize)
    }

    fn c(self) -> Circuit;
    fn rc(self) -> CircuitRc {
        CircuitRc(Arc::new(self.c()))
    }

    /// for nodes with fixed uuid, should be same as node_type_uuid
    fn static_node_type_uuid() -> [u8; 16]
    where
        Self: Sized,
    {
        *uuid::Uuid::nil().as_bytes()
    }

    fn get_autoname(&self) -> Result<Option<Name>>;

    // ==== default only section ===
    // FUNCTIONS BELOW HERE *shouldn't* be overridden by implementors!
    // (if you do implement, this won't be picked up on by union types & CircuitRc
    #[inline]
    fn compute_flags_default(&self) -> CircuitFlags {
        let mut result: CircuitFlags = CircuitFlags::all_true();
        for child in self.children_sl() {
            result &= child.info().flags;
        }
        result
    }

    fn hash_base16(&self) -> String {
        base16::encode_lower(&self.info().hash)
    }

    fn initial_init_info(self) -> Result<Self>
    where
        Self: Sized,
    {
        self.initial_init_info_impl()
    }
    fn rename(self, new_name: Option<Name>) -> Self
    where
        Self: Sized,
    {
        self.rename_impl(new_name)
    }
    fn update_info<F>(self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo),
    {
        self.update_info_impl(f)
    }

    // implementation helper
    fn already_set_named_axes(&self) -> Option<NamedAxes> {
        (!self.info().named_axes.is_empty()).then(|| self.info().named_axes.clone())
    }

    fn crc(&self) -> CircuitRc {
        self.clone().rc()
    }

    // TODO: add more map utils for non_free as needed

    fn children(&self) -> std::iter::Cloned<std::slice::Iter<'_, CircuitRc>> {
        self.info().children.iter().cloned()
    }

    fn non_free_children(
        &self,
    ) -> std::iter::Skip<std::iter::Cloned<std::slice::Iter<'_, CircuitRc>>> {
        self.children().skip(self.num_free_children())
    }

    fn children_sl(&self) -> &[CircuitRc] {
        &self.info().children
    }

    fn non_free_children_sl(&self) -> &[CircuitRc] {
        &self.info().children[self.num_free_children()..]
    }

    fn num_children(&self) -> usize {
        self.info().children.len()
    }

    fn replace_children(&self, new_children: Vec<CircuitRc>) -> Result<Self> {
        anyhow::ensure!(
            new_children.len() == self.num_children(),
            "replace_children: wrong number of children"
        );
        // TODO disabled because reconstructing might need to trigger autoname
        // if &new_children == self.children_sl() {
        //     Ok(self.clone())
        // } else {
        self._replace_children(new_children.clone())
            .with_context(|| {
                format!("while replacing children of\n{self:?}\nnew_children={new_children:#?}")
            })
        // }
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let out: Vec<CircuitRc> = self
            .children()
            .enumerate()
            .map(|(i, x)| f(i, x))
            .collect::<Result<Vec<_>>>()?;
        self.replace_children(out)
    }

    fn map_non_free_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let mut f = f;
        let n = self.num_free_children();

        self.map_children_enumerate(|ix, c| if ix < n { Ok(c) } else { f(ix - n, c) })
    }

    fn map_children<F>(&self, f: F) -> Result<Self>
    where
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        let out = self.children().map(f).collect::<Result<Vec<_>>>()?;
        self.replace_children(out)
    }
    fn map_non_free_children<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        self.map_non_free_children_enumerate(|_i, x| f(x))
    }

    fn map_children_unwrap<F>(&self, f: F) -> Self
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        let out = self.children().map(f).collect();
        self.replace_children(out).unwrap()
    }
    fn map_non_free_children_unwrap<F>(&self, f: F) -> Self
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        let mut f = f;
        let n = self.num_free_children();

        self.map_children_unwrap_enumerate(|ix, c| if ix < n { c } else { f(c) })
    }

    fn map_children_unwrap_enumerate<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> CircuitRc,
    {
        let out = self.children().enumerate().map(|(i, x)| f(i, x)).collect();
        self.replace_children(out).unwrap()
    }

    /// if any return Some, return child mapped, otherwise None
    fn map_children_op<F>(&self, mut f: F) -> Option<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Option<CircuitRc>,
    {
        let mut any_modified = false;
        let out: Vec<CircuitRc> = self
            .children_sl()
            .iter()
            .map(|x| {
                if let Some(new) = f(x.clone()) {
                    any_modified = true;
                    new
                } else {
                    x.clone()
                }
            })
            .collect();
        if any_modified {
            Some(self.replace_children(out).unwrap())
        } else {
            None
        }
    }
    fn with_autoname_disabled(&self, autoname_disabled: bool) -> Self
    where
        Self: Sized,
    {
        self.clone()
            .update_info(|info| {
                if !autoname_disabled {
                    info.flags |= CircuitFlags::USE_AUTONAME;
                } else {
                    info.flags &= !CircuitFlags::USE_AUTONAME;
                }
            })
            .unwrap()
    }
    fn repr(&self) -> Result<String> {
        (SELF_FUNCS.repr)(self.crc())
    }

    fn print(&self) -> Result<()> {
        rr_util::python_println!("{}", self.repr()?);
        Ok(())
    }

    fn repru(&self) -> String {
        self.repr().unwrap()
    }

    fn printu(&self) {
        self.print().unwrap()
    }

    fn debug_repr(&self) -> Result<String> {
        (SELF_FUNCS.debug_repr)(self.crc())
    }

    fn debug_repru(&self) -> String {
        self.debug_repr().unwrap()
    }

    fn get_hash(&self) -> HashBytes {
        self.info().hash
    }
    fn rank(&self) -> usize {
        self.info().rank()
    }
    fn ndim(&self) -> usize {
        self.info().rank()
    }
    fn shape(&self) -> &Shape {
        &self.info().shape
    }
    fn numel(&self) -> usize {
        self.info().numel_usize()
    }

    fn sum(&self, axes: &[i64], name: Option<Name>) -> Result<Einsum> {
        let axes = check_canon_axes_as(self.rank(), axes)?;
        Ok(Einsum::new(
            vec![(self.crc(), (0u8..self.rank() as u8).collect())],
            (0u8..self.rank() as u8)
                .filter(|i| !axes.contains(i))
                .collect(),
            name,
        ))
    }

    fn mean(&self, axes: &[i64], name: Option<Name>, scalar_name: Option<Name>) -> Result<Einsum> {
        let total_size: Option<usize> = check_canon_axes_as(self.rank(), axes)?
            .into_iter()
            .map(|i| self.info().shape[*i as usize].t())
            .product();
        if total_size.is_none() {
            bail!(
                "mean: can't take mean over axis/axes {axes:?} with unknown size(s), shape={:?}",
                self.shape()
            );
        }
        let total_size = total_size.unwrap();
        let sum = self.sum(axes, None)?;
        Ok(Einsum::new(
            sum.args_cloned()
                .into_iter()
                .chain(std::iter::once((
                    Scalar::nrc(
                        1. / (total_size as f64),
                        sv![],
                        scalar_name
                            .or_else(|| self.info().name.map(|s| format!("mean_div_{}", s).into())),
                    ),
                    tu8v![],
                )))
                .collect(),
            sum.out_axes,
            name,
        ))
    }

    fn reduce(&self, op_name: Name, axes: &[i64], name: Option<Name>) -> Result<Circuit> {
        match op_name.str() {
            "mean" => return self.mean(axes, name, None).map(CircuitNode::c),
            "sum" => return self.sum(axes, name).map(CircuitNode::c),
            _ => (),
        }

        let axes = check_canon_axes_as(self.rank(), axes)?;

        Ok(GeneralFunction::new_by_name(
            vec![Rearrange::nrc(
                self.crc(),
                RearrangeSpec::combine_axes_at_end(self.rank().try_into()?, axes).unwrap(),
                None,
            )],
            op_name,
            name,
        )
        .unwrap()
        .c())
    }
    fn min_(&self, axes: &[i64], name: Option<Name>) -> Result<Circuit> {
        self.reduce("min".into(), axes, name)
    }
    fn max_(&self, axes: &[i64], name: Option<Name>) -> Result<Circuit> {
        self.reduce("max".into(), axes, name)
    }
    fn add(&self, other: CircuitRc, name: Option<Name>) -> Result<Add> {
        Add::try_new(vec![self.crc(), other], name)
    }
    fn sub(&self, other: CircuitRc, name: Option<Name>) -> Result<Add> {
        let other_neg_name = other.info().name.map(|s| format!("neg {}", s).into());
        self.add(
            Einsum::scalar_mul(other, -1.0, other_neg_name, Some("neg_1".into())).rc(),
            name,
        )
    }
    fn mul(&self, other: CircuitRc, name: Option<Name>) -> Result<Einsum> {
        Einsum::elementwise_broadcasted(vec![self.crc(), other], name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<Name>,
        scalar_name: Option<Name>,
    ) -> Result<Einsum> {
        self.mul(Scalar::nrc(scalar, sv![], scalar_name), name)
    }
    fn index(&self, index: TensorIndex, name: Option<Name>) -> Result<Index> {
        Index::try_new(self.crc(), index, name)
    }
    fn expand_at_axes(
        &self,
        axes: Vec<usize>,
        counts: Vec<usize>,
        name: Option<Name>,
    ) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::expand_at_axes(self.rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: Vec<usize>, name: Option<Name>) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unsqueeze(self.rank(), axes)?,
            name,
        ))
    }
    fn squeeze(&self, axes: PyOpAtAxes, name: Option<Name>) -> Result<Rearrange> {
        let axes = check_canon_axes_as(self.rank(), &reduction_to_ints(Some(axes), self.rank()))?;
        if axes.iter().any(|i| !self.info().shape[*i as usize].is(1)) {
            bail!(anyhow!(
                "trying to squeeze non-1 axes, shape {:?} axes {:?}",
                &self.info().shape,
                &axes
            ))
        }
        let num_ints = self.rank() - axes.len();
        let mut input_ints = sv![];
        let mut counter = 0;
        for i in 0..self.rank() as u8 {
            if axes.iter().contains(&i) {
                input_ints.push(tu8v![])
            } else {
                input_ints.push(tu8v![counter]);
                counter += 1;
            }
        }
        Rearrange::try_new(
            self.crc(),
            RearrangeSpec {
                input_ints,
                output_ints: (0..num_ints).map(|i| tu8v![i as u8]).collect(),
                int_sizes: sv![Size::NONE;num_ints],
            },
            name,
        )
    }
    fn flatten(&self, name: Option<Name>) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::flatten_usize(self.ndim())?,
            name,
        ))
    }
    fn unflatten(&self, shape: Shape, name: Option<Name>) -> Result<Rearrange> {
        Rearrange::unflatten(self.crc(), shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<Name>) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn unflatten_axis_usize(
        &self,
        axis: usize,
        shape: Shape,
        name: Option<Name>,
    ) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis_usize(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<Name>) -> Result<Rearrange> {
        Rearrange::try_new(self.crc(), spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<Name>) -> Result<Rearrange> {
        Rearrange::from_string(self.crc(), string, name)
    }
    fn repeat_to(&self, new_shape: Shape, name: Option<Name>) -> Result<CircuitRc> {
        ensure!(new_shape.len() >= self.ndim());
        let n = new_shape.len() - self.ndim();
        ensure!(self.shape()[..] == new_shape[n..]);
        Ok(self
            .rearrange(
                RearrangeSpec::prepend_batch_shape(new_shape[..n].to_smallvec(), self.ndim())?,
                name,
            )?
            .crc())
    }
    fn add_suffix(self, suffix: Option<&str>) -> Self
    where
        Self: Sized,
    {
        match suffix {
            Some(suffix) => {
                let name = self.info().name.map(|x| format!("{}_{}", x, suffix).into());
                self.rename_impl(name)
            }
            None => self,
        }
    }
    fn maybe_rename(self, name: Option<Option<Name>>) -> Self {
        if let Some(n) = name {
            self.rename(n)
        } else {
            self
        }
    }
}

pub trait CircuitNodeAutoName: CircuitNode {
    /// There are three kinds of automatically generated names:
    /// - infix, like Add and Einsum. Parenthesis are added around children which would have had wrong priority
    /// - functions, like GeneralFunction and Cumulant, which use the standard function notation f(x1, ... xn)
    /// - postfix, like Rearrange and index, which behave like the unary operator "!". Parenthesis are added if needed
    /// utils to add the parenthesis can be found in circuit_utils.rs
    fn auto_name(&self) -> Option<Name>;

    const PRIORITY: OperatorPriority = OperatorPriority::NotOperator {};
    const CHILD_NAME_MAX_LEN: usize = 100; // TODO: fix me!
    /// we shorten children names on multi child nodes
    fn shorten_child_name(name: &str) -> String {
        if name.len() > Self::CHILD_NAME_MAX_LEN {
            name[..Self::CHILD_NAME_MAX_LEN].to_owned() + "..."
        } else {
            name.to_owned()
        }
    }
}

pub trait CircuitNodeUnion {
    type TypeTag;
    fn variant_string(&self) -> String;
    fn type_tag(&self) -> Self::TypeTag;
}

// not really needed to be so pedantic with ::std::...
#[macro_export]
macro_rules! circuit_node_eq_ord_debug {
    ($type_name:ty) => {
        rr_util::impl_eq_by_big_hash!($type_name);

        impl ::std::cmp::Ord for $type_name {
            fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
                use $crate::prelude::*;
                // name and then
                (self.info().name, self.info().hash).cmp(&(other.info().name, other.info().hash))
            }
        }

        impl ::std::cmp::PartialOrd for $type_name {
            fn partial_cmp(&self, other: &Self) -> ::std::option::Option<::std::cmp::Ordering> {
                Some(::std::cmp::Ord::cmp(self, other))
            }
        }

        impl std::fmt::Debug for $type_name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                f.write_str(&self.debug_repru())
            }
        }

        impl std::fmt::Display for $type_name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                f.write_str(&$crate::self_funcs::repr_circuit_default_no_bijection(
                    self.crc(),
                ))
            }
        }
    };
}

// this is what peak rust development looks like
#[doc(hidden)]
#[macro_export]
macro_rules! define_circuit_union_impl {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        #[derive(::std::clone::Clone,pyo3::FromPyObject)]
        pub enum $name {
            $(
                $x($x),
            )*
        }

        paste::paste! {
            #[macro_export]
            macro_rules! [<$name:snake _map>] {
                ($match_expr:expr; $wrap_name:ident => $e:expr) => (
                    [<$name:snake _map_construct>]!($match_expr; ($wrap_name, __constructor_name) => $e)
                )
            }

            #[macro_export]
            macro_rules! [<$name:snake _map_construct>] {
                ($match_expr:expr; ($wrap_name:ident, $constructor_name:ident) => $e:expr) => (
                    match $match_expr {
                    $(
                        $name::$x($wrap_name) => {
                            let $constructor_name = $name::$x;
                            $e
                        },
                    )*
                    }
                )
            }

            #[macro_export]
            macro_rules! [<on_ $name:snake _names>] {
                ($m:ident) => (
                    $m!( $( $x,)*);
                )
            }
        }

        impl rr_util::eq_by_big_hash::EqByBigHash for $name {
            #[inline]
            fn hash(&self) -> rr_util::util::HashBytes {
                self.info().hash
            }
        }

        paste::paste! {
            #[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, PartialOrd, Ord)]
            pub enum [<$name Type>] {
                $(
                    $x,
                )*
            }


            impl<'source> pyo3::FromPyObject<'source> for [<$name Type>] {
                fn extract(inp: &'source pyo3::PyAny) -> pyo3::PyResult<Self> {
                    use pyo3::{ types::PyType};

                    let pairings: Vec<(Py<PyType>, [<$name Type>])> =
                        Python::with_gil(|py| vec![
                        $(
                            ($x::type_object(py).into(), [<$name Type>]::$x),
                        )*
                        ]);

                    for (t, out) in pairings {
                        if t.is(inp) {
                            return Ok(out);
                        }
                    }

                    Err(PyErr::new::<exceptions::PyTypeError, _>(format!(
                        "Expected one of the {} types",
                        stringify!($name)
                    )))
                }
            }

            impl pyo3::IntoPy<pyo3::PyObject> for [<$name Type>] {
                fn into_py(self, py: pyo3::Python<'_>) -> pyo3::PyObject {
                    match self {
                        $(
                            Self::$x => $x::type_object(py).into(),
                        )*
                    }
                }
            }

            impl std::fmt::Display for [<$name Type>] {
                fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                    let out = match self {
                        $(
                        Self::$x => stringify!($x),
                        )*
                    };
                    f.write_str(out)
                }
            }

            impl std::str::FromStr for [<$name Type>] {
                type Err = ();
                fn from_str(s: &str) -> Result<Self, Self::Err> {
                    match s {
                        $(
                        stringify!($x) => Ok(Self::$x),
                        )*
                        _ => Err(())
                    }
                }
            }

        }


        circuit_node_eq_ord_debug!($name);

        paste::paste! {
            $(
                impl $name {
                    pub fn [<into_ $x:snake>](self) -> Option<$crate::$x> {
                        self.into_op()
                    }
                    pub fn [<as_ $x:snake>](&self) -> Option<&$crate::$x> {
                        self.as_op()
                    }
                    pub fn [<as_mut_ $x:snake>](&mut self) -> Option<&mut $crate::$x> {
                        self.as_mut_op()
                    }

                    pub fn [<into_ $x:snake _unwrap>](self) -> $crate::$x {
                        self.into_unwrap()
                    }
                    pub fn [<as_ $x:snake _unwrap>](&self) -> &$crate::$x {
                        self.as_unwrap()
                    }
                    pub fn [<as_mut_ $x:snake _unwrap>](&mut self) -> &mut $crate::$x {
                        self.as_mut_unwrap()
                    }

                    pub fn [<is_ $x:snake>](&self) -> bool {
                        self.[<as_ $x:snake>]().is_some()
                    }
                }
                impl AsOp<$crate::$x> for $name {
                    fn into_op(self) -> Option<$crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_op(&self) -> Option<&$crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_mut_op(&mut self) -> Option<&mut $crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                }
            )*
        }



        paste::paste! {
        impl $crate::CircuitNodeInit for $name {
            fn init_info_impl(self, is_initial: bool) -> Result<Self> {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => Ok(construct(node.init_info_impl(is_initial)?)))
            }

            fn rename_impl(self, new_name: Option<Name>) -> Self {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => construct(node.rename(new_name)))
            }

            fn update_info_impl<F>(self, f: F) -> Result<Self>
            where
                F: FnOnce(&mut $crate::circuit_info::CachedCircuitInfo),
            {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => Ok(construct(node.update_info(f)?)))
            }
        }

        impl $crate::CircuitNodeSelfOnlyHash for $name {
            fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
                [<$name:snake _map>]!(self; node => node.compute_self_only_hash(hasher))
            }
        }

        impl $crate::CircuitNode for $name {
            fn info(&self) -> &circuit_info::CachedCircuitInfo {
                [<$name:snake _map>]!(self; node => node.info())
            }

            fn num_free_children(&self) -> usize {
                [<$name:snake _map>]!(self; node => node.num_free_children())
            }

            fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
                [<$name:snake _map_construct>]!(self; (node, construct) => Ok(construct(node._replace_children(children)?)))
            }

            fn node_type_uuid(&self) -> [u8; 16] {
                [<$name:snake _map>]!(self; node => node.node_type_uuid())
            }

            fn self_flops(&self) -> BigUint {
                [<$name:snake _map>]!(self; node => node.self_flops())
            }

            fn c(self) -> Circuit { ite_is_circuit!($name, self, [<$name:snake _map>]!(self; node => node.c())) }
            fn get_autoname(&self) -> Result<Option<Name>> { [<$name:snake _map>]!(self; node => node.get_autoname()) }
            fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> { [<$name:snake _map>]!(self; node => node.child_axis_map()) }
        }
        }

        paste::paste! {
            impl $crate::CircuitNodeUnion for $name {
                type TypeTag = [<$name Type>];

                fn variant_string(&self) -> String {
                    self.type_tag().to_string()
                }

                fn type_tag(&self) -> Self::TypeTag {
                    match self {
                        $(
                            Self::$x(_) => Self::TypeTag::$x,
                        )*
                    }
                }
            }

            impl pyo3::IntoPy<pyo3::PyObject> for $name {
                fn into_py(self, py: pyo3::Python<'_>) -> pyo3::PyObject {
                    [<$name:snake _map>]!(self; node => pyo3::IntoPy::into_py(node, py))
                }
            }
        }

        $(
            impl From<$x> for $name {
                fn from(item: $x) -> Self {
                    Self::$x(item)
                }
            }
        )*
    }
}
macro_rules! ite_is_circuit {
    (Circuit, $t:expr, $e:expr) => {
        $t
    };
    ($n:ident, $t:expr, $e:expr) => {
        $e
    };
}
macro_rules! define_circuit {
    [$($x:ident),+ $(,)?] => {
        define_circuit_union_impl!(Circuit {$($x,)*});



        // you have to wrap pymethods in the paste for this to work due to how
        // pymethods proc macro works
        paste::paste! {
            #[pymethods]
            impl PyCircuitBase {
            $(
                pub fn [<maybe_ $x:snake>](&self) -> Option<$crate::$x> {
                    arc_ref_clone(&self).into_op()
                }

                pub fn [<cast_ $x:snake>](&self) -> PyResult<$x> {
                    arc_ref_clone(&self).into_op().ok_or_else(|| {
                        // could use fresh error type if we wanted
                        PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                            "expected {} but got {}",
                            stringify!($x),
                            self.type_tag()
                        ))
                    })
                }

                pub fn [<is_ $x:snake>](&self) -> bool {
                    self.0.[<is_ $x:snake>]()
                }
            )*
            }
        }

    }
}

define_circuit!(
    Einsum,
    Array,
    Symbol,
    Scalar,
    Add,
    Rearrange,
    Index,
    GeneralFunction,
    Concat,
    Scatter,
    Conv,
    Module,
    Tag,
    DiscreteVar,
    StoredCumulantVar,
    Cumulant,
);

#[pyfunction]
pub fn print_circuit_type_check(x: CircuitType) -> CircuitType {
    dbg!(x);
    x
}

/// Define adhoc unions of different circuit types
#[macro_export]
macro_rules! define_circuit_union {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        $crate::define_circuit_union_impl!($name {$($x,)*});

        impl ::std::convert::From<$crate::Circuit> for ::std::option::Option<$name> {
            fn from(item: $crate::Circuit) -> ::std::option::Option<$name> {
                match item {
                    $(
                        $crate::Circuit::$x(node) => Some(node.into()),
                    )*
                    _=>None
                }
            }
        }
        impl $name{
            pub fn matches(circuit:&$crate::Circuit)->bool{
                let op: ::std::option::Option<$name>=circuit.clone().into();
                op.is_some()
            }
        }
        paste::paste! {
            impl ::std::convert::From<$name> for $crate::Circuit {
                fn from(item: $name) -> Self {
                    [<$name:snake _map>]!(item; node => node.into())
                }
            }
        }
    }
}

macro_rules! define_circuit_union_special {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        define_circuit_union!($name {$($x,)*});
        paste::paste! {
            impl Circuit {
                pub fn [<is_ $name:snake>](&self) -> bool {
                    match self {
                        $(
                            $crate::Circuit::$x(_) => true,
                        )*
                        _ => false
                    }
                }
                pub fn [<into_ $name:snake>](self) -> Option<$name> {
                    self.into()
                }
            }
        }
    }
}

// These nodes are uneffected by rewrites, and satisfy
// AlgebraicRewrite(Replace(X, IrreducibleNode->Y)) == Replace(AlgebraicRewrite(IrreducibleNode), IrreducibleNode->Y)
// except for hashmap iteration order or other unfortunate nondeterminism
define_circuit_union_special!(IrreducibleNode { Array, Symbol });

define_circuit_union_special!(Leaf {
    Array,
    Symbol,
    Scalar,
});

define_circuit_union_special!(LeafConstant { Array, Scalar });

define_circuit_union_special!(Var {
    StoredCumulantVar,
    DiscreteVar,
});

// work around for fact that we can't implement foreign trait on constrained type
#[macro_export]
macro_rules! circuit_node_extra_impl {
    ($type_name:ident, self_hash_default) => {
        $crate::circuit_node_extra_impl!($type_name);
        $crate::circuit_node_self_only_hash_default_impl!($type_name);
    };
    ($type_name:ident) => {
        $crate::circuit_node_eq_ord_debug!($type_name);

        impl $crate::CircuitNodePrivate for $type_name {
            fn info_mut(&mut self) -> &mut $crate::CachedCircuitInfo {
                &mut self.info
            }
        }
        impl rr_util::eq_by_big_hash::EqByBigHash for $type_name {
            #[inline]
            fn hash(&self) -> rr_util::util::HashBytes {
                self.info().hash
            }
        }
        impl $type_name {
            fn into_init(self) -> PyClassInitializer<Self> {
                // kinda awkward clone... (but probably basically free)
                (self.clone(), $crate::PyCircuitBase(self.rc())).into()
            }
        }

        impl IntoPy<PyObject> for $type_name {
            fn into_py(self, py: Python<'_>) -> PyObject {
                // this is slightly gross. I wonder if possible to do better?
                // when does this unwrap fail?
                {
                    Py::new(py, self.into_init()).unwrap().into_py(py)
                }
            }
        }
    };
}

#[macro_export]
macro_rules! circuit_node_auto_impl {
    ($the_uuid:literal) => {
        $crate::circuit_node_auto_impl!($the_uuid, none);

        fn get_autoname(&self) -> Result<Option<Name>> {
            Ok(self.auto_name())
        }
    };
    ($the_uuid:literal, none) => {
        #[inline]
        fn info(&self) -> &$crate::circuit_info::CachedCircuitInfo {
            &self.info
        }
        fn node_type_uuid(&self) -> [u8; 16] {
            Self::static_node_type_uuid()
        }
        fn static_node_type_uuid() -> [u8; 16]
        where
            Self: Sized,
        {
            *uuid::uuid!($the_uuid).as_bytes()
        }
        fn c(self) -> $crate::Circuit {
            self.into()
        }
    };

    ($the_uuid:literal, no_autoname) => {
        $crate::circuit_node_auto_impl!($the_uuid, none);

        fn get_autoname(&self) -> anyhow::Result<Option<Name>> {
            anyhow::bail!("this node type doesn't support autoname");
        }
    };
}

pub type CircResult = Result<CircuitRc>;

#[derive(Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct CircuitRc(pub Arc<Circuit>);

impl CircuitNodeSelfOnlyHash for CircuitRc {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
        self.0.compute_self_only_hash(hasher)
    }
}
impl CircuitNode for CircuitRc {
    fn info(&self) -> &CachedCircuitInfo {
        self.0.info()
    }

    fn num_free_children(&self) -> usize {
        self.0.num_free_children()
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.0.child_axis_map()
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        self.0._replace_children(children).map(|x| x.rc())
    }

    fn node_type_uuid(&self) -> [u8; 16] {
        self.0.node_type_uuid()
    }

    fn self_flops(&self) -> BigUint {
        self.0.self_flops()
    }

    fn c(self) -> Circuit {
        arc_unwrap_or_clone(self.0)
    }
    fn rc(self) -> CircuitRc {
        self
    }
    fn crc(&self) -> CircuitRc {
        self.clone()
    }

    // fn static_node_type_uuid() -> [u8; 16] { self.0.static_node_type_uuid() }

    fn get_autoname(&self) -> Result<Option<Name>> {
        self.0.get_autoname()
    }
}

impl fmt::Debug for CircuitRc {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Debug::fmt(&***self, f)
    }
}
impl fmt::Display for CircuitRc {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&***self, f)
    }
}

impl IntoPy<PyObject> for CircuitRc {
    fn into_py(self, py: Python<'_>) -> PyObject {
        {
            (*self.0).clone().into_py(py)
        }
    }
}

impl IntoPy<PyObject> for &CircuitRc {
    fn into_py(self, py: Python<'_>) -> PyObject {
        {
            (*self.0).clone().into_py(py)
        }
    }
}

impl<'source> FromPyObject<'source> for CircuitRc {
    fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
        {
            if !circuit_obj.is_instance_of::<PyCircuitBase>()? {
                return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                    "object of {} cannot be converted to 'Circuit'",
                    circuit_obj.get_type()
                )));
            }
            let circ: Circuit = circuit_obj.extract()?;
            Ok(circ.rc())
        }
    }
}

impl<T: CircuitNode + Into<Circuit>> From<T> for CircuitRc {
    fn from(x: T) -> Self {
        x.rc()
    }
}

impl From<Arc<Circuit>> for CircuitRc {
    fn from(x: Arc<Circuit>) -> Self {
        CircuitRc(x)
    }
}

impl Deref for CircuitRc {
    type Target = Arc<Circuit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for CircuitRc {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl CircuitNodeInit for CircuitRc {
    fn init_info_impl(self, is_initial: bool) -> Result<Self> {
        Ok(self.c().init_info_impl(is_initial)?.rc())
    }

    fn rename_impl(self, new_name: Option<Name>) -> Self {
        self.c().rename(new_name).rc()
    }

    fn update_info_impl<F>(self, f: F) -> Result<Self>
    where
        F: FnOnce(&mut CachedCircuitInfo),
    {
        Ok(self.c().update_info_impl(f)?.rc())
    }
}
