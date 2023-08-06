use std::{
    fmt::Debug,
    hash::Hash,
    ops::{BitAnd, BitOr, Not},
    sync::Arc,
};

use anyhow::{Context, Result};
use itertools::Itertools;
use num_bigint::BigUint;
use once_cell::sync::Lazy;
use rr_util::{
    name::Name,
    shape::Shape,
    tensor_util::{TorchDeviceDtype, TorchDeviceDtypeOp},
    util::{HashBytes, NamedAxes},
    IndexSet,
};

use crate::{CircuitNode, CircuitRc};

#[derive(Clone)]
pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub flags: CircuitFlags,
    pub hash: HashBytes,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
    pub free_symbols: Option<Arc<IndexSet<CircuitRc>>>, // always Symbols
    pub name: Option<Name>,
    pub children: Vec<CircuitRc>,
}

impl CachedCircuitInfo {
    // leaves some fields undefined/default for now... TODO move more stuff here
    pub fn incomplete(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
    ) -> Result<CachedCircuitInfo> {
        let ddt = compute_device_dtype(&children, None)?;
        Ok(Self::with_device_dtype(name, shape, children, ddt))
    }
    pub fn with_device_dtype_extra(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
        device_dtype_extra: &[TorchDeviceDtypeOp],
    ) -> Result<Self> {
        let ddt = compute_device_dtype(&children, Some(device_dtype_extra))?;
        Ok(Self::with_device_dtype(name, shape, children, ddt))
    }
    pub fn with_device_dtype(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
        device_dtype: TorchDeviceDtypeOp,
    ) -> Self {
        CachedCircuitInfo {
            shape,
            flags: Default::default(),
            hash: Default::default(),
            device_dtype,
            named_axes: Default::default(),
            free_symbols: compute_free_symbols(&children),
            name,
            children,
        }
    }
}

#[derive(Clone, Copy, Hash, Debug, Eq, PartialEq)]
pub struct CircuitFlags(pub u8);
impl CircuitFlags {
    pub const IS_CONSTANT: CircuitFlags = CircuitFlags(0b0001);
    pub const IS_EXPLICITLY_COMPUTABLE: CircuitFlags = CircuitFlags(0b0010);
    pub const CAN_BE_SAMPLED: CircuitFlags = CircuitFlags(0b0100);
    pub const USE_AUTONAME: CircuitFlags = CircuitFlags(0b1000);

    pub const NONE: CircuitFlags = CircuitFlags(0b0);
    pub fn check(self, other: CircuitFlags) -> bool {
        (self & other).0 != 0
    }

    pub fn all_true() -> Self {
        CircuitFlags::IS_EXPLICITLY_COMPUTABLE
            | CircuitFlags::IS_CONSTANT
            | CircuitFlags::CAN_BE_SAMPLED
            | CircuitFlags::USE_AUTONAME
    }
}

impl Default for CircuitFlags {
    fn default() -> Self {
        Self::all_true()
    }
}

impl BitOr for CircuitFlags {
    type Output = CircuitFlags;
    fn bitor(self, rhs: Self) -> Self::Output {
        Self(self.0 | rhs.0)
    }
}
impl BitAnd for CircuitFlags {
    type Output = CircuitFlags;
    fn bitand(self, rhs: Self) -> Self::Output {
        Self(self.0 & rhs.0)
    }
}
use std::ops::BitOrAssign;
impl BitOrAssign for CircuitFlags {
    fn bitor_assign(&mut self, rhs: Self) {
        self.0 |= rhs.0
    }
}
use std::ops::BitAndAssign;
impl BitAndAssign for CircuitFlags {
    fn bitand_assign(&mut self, rhs: Self) {
        self.0 &= rhs.0
    }
}
impl Not for CircuitFlags {
    type Output = CircuitFlags;
    fn not(self) -> CircuitFlags {
        Self(!self.0)
    }
}

/// don't want to print hash with Debug; print selected fields
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} {:?} {:?}",
            self.name.map_or("", |n| n.str()),
            self.shape,
            self.device_dtype,
        )
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape
            .iter()
            .map(|x| BigUint::from(x.t().unwrap_or(1)))
            .product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        match numel_digits.len() {
            0 => 0,
            1 => numel_digits[0] as usize,
            _ => usize::MAX,
        }
    }

    pub fn naive_mem_use(&self, device_dtype: Option<TorchDeviceDtype>) -> BigUint {
        self.numel()
            * BigUint::from(
                device_dtype
                    .unwrap_or(self.device_dtype.unwrap_or_defaults())
                    .size(),
            )
    }
    // once we're scheduling everything is batch-realizeable so we don't need biguint
    pub fn naive_mem_use_usize(&self, device_dtype: Option<TorchDeviceDtype>) -> usize {
        self.numel_usize().saturating_mul(
            device_dtype
                .unwrap_or(self.device_dtype.unwrap_or_defaults())
                .size(),
        )
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
    pub fn is_constant(&self) -> bool {
        self.flags.check(CircuitFlags::IS_CONSTANT)
    }
    pub fn can_be_sampled(&self) -> bool {
        self.flags.check(CircuitFlags::CAN_BE_SAMPLED)
    }
    pub fn is_explicitly_computable(&self) -> bool {
        self.flags.check(CircuitFlags::IS_EXPLICITLY_COMPUTABLE)
    }
    pub fn use_autoname(&self) -> bool {
        self.flags.check(CircuitFlags::USE_AUTONAME)
    }

    pub fn get_raw_free_symbols(&self) -> &IndexSet<CircuitRc> {
        static NULL_INDEX_SET: Lazy<IndexSet<CircuitRc>> = Lazy::new(IndexSet::default);
        if let Some(z) = &self.free_symbols {
            z
        } else {
            &NULL_INDEX_SET
        }
    }
}

fn compute_free_symbols(children: &[CircuitRc]) -> Option<Arc<IndexSet<CircuitRc>>> {
    // ideally, symbol would just return itself rather than doing this check here
    // but, then the symbol would have a circular reference to itself
    // So we can only include children and then we special case syms in various places. : /
    children
        .iter()
        .filter_map(|x| {
            if x.is_symbol() {
                Some(Arc::new(IndexSet::from_iter([x.clone()])))
            } else {
                x.info().free_symbols.clone()
            }
        })
        .at_most_one()
        .unwrap_or_else(|mut it| {
            let mut a = (*it.next().unwrap()).clone();
            it.for_each(|x| a.extend(x.iter().cloned()));
            Some(Arc::new(a))
        })
}

fn compute_device_dtype(
    children: &[CircuitRc],
    extra: Option<&[TorchDeviceDtypeOp]>,
) -> Result<TorchDeviceDtypeOp> {
    children
        .iter()
        .map(|c| c.info().device_dtype)
        .chain(extra.into_iter().flatten().cloned())
        .try_fold(TorchDeviceDtypeOp::NONE, |acc, new| {
            TorchDeviceDtypeOp::combine(acc, new)
        })
        .with_context(|| {
            format!(
                "Could not combine device_dtype for node with children {:?} and extra {:?}",
                children
                    .iter()
                    .map(|c| c.info().clone())
                    .collect::<Vec<_>>(),
                extra
            )
        })
}
