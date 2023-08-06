use anyhow::{bail, Result};
use circuit_base::{prelude::*, Einsum};
use circuit_rewrites::algebraic_rewrite::{distribute_once_raw, DistributeError};
use get_update_node::{new_traversal, IterativeMatcherRc, MatcherData};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{cached_lambda, util::HashBytes};

#[pyfunction]
pub fn traverse_until_depth(depth: Option<u32>) -> IterativeMatcherRc {
    new_traversal(
        None,
        depth.map(|i| i + 1),
        MatcherData::Always(false).into(),
    )
    .rc()
}

// TODO: improve me: fixed operand index isn't very flexible in deep case (though I'm not sure that deep distribute rewrite is that important...)
#[pyfunction]
#[pyo3(signature=(
    einsum,
    operand_idx,
    traversal = traverse_until_depth(Some(1)),
    prefix = None,
    suffix = None,
    allow_partial_distribute = true,
    do_broadcasts = true
))]
pub fn distribute(
    einsum: Einsum,
    operand_idx: usize,
    traversal: Option<IterativeMatcherRc>,
    prefix: Option<String>,
    suffix: Option<String>,
    allow_partial_distribute: bool, // noop if can't distribute
    do_broadcasts: bool,
) -> Result<CircuitRc> {
    #[apply(cached_lambda)]
    #[key((einsum.info().hash, traversal.clone()), (HashBytes, IterativeMatcherRc))]
    #[use_try]
    fn distribute_rec(einsum: Einsum, traversal: IterativeMatcherRc) -> Result<CircuitRc> {
        if operand_idx >= einsum.num_children() {
            if allow_partial_distribute {
                return Ok(einsum.rc());
            } else {
                bail!(DistributeError::OperandIdxTooLarge {
                    einsum,
                    operand_idx,
                })
            };
        }

        let (_, finished, traversal_per_child) =
            traversal.match_iterate_continue(einsum.children_sl()[operand_idx].clone())?;

        if finished {
            return Ok(einsum.rc());
        }

        let distributed = distribute_once_raw(
            &einsum,
            operand_idx,
            do_broadcasts,
            prefix.as_deref(),
            suffix.as_deref(),
            |i, new_einsum| distribute_rec(new_einsum, traversal_per_child[i].clone()),
        );
        if distributed.is_err() && allow_partial_distribute {
            return Ok(einsum.rc());
        }
        Ok(distributed?.rc())
    }

    let result = distribute_rec(
        einsum.clone(),
        traversal.unwrap_or(traverse_until_depth(Some(1))),
    );
    if let Ok(result_some)=&result && result_some.info().hash==einsum.info().hash{
        bail!(DistributeError::Noop { einsum, operand_idx })
    }
    result
}
