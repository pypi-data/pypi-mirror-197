use anyhow::Result;
use circuit_base::{prelude::*, CircuitType, Index};
use circuit_rewrites::algebraic_rewrite::{index_elim_identity, push_down_index_raw};
use get_update_node::{new_traversal, IterativeMatcherRc, Matcher, MatcherData};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{cached_lambda, util::HashBytes};

#[pyfunction]
pub fn default_index_traversal() -> IterativeMatcherRc {
    new_traversal(
        None,
        None,
        Matcher::types(vec![CircuitType::Index, CircuitType::Array]).rc(),
    )
    .rc()
}

#[pyfunction]
#[pyo3(signature=(
    index,
    traversal = default_index_traversal(),
    into_module_spec = MatcherData::Always(false).into(),
    suffix = None,
    allow_partial_pushdown = false,
    elim_identity = true,
))]
pub fn push_down_index(
    index: Index,
    traversal: IterativeMatcherRc,
    into_module_spec: IterativeMatcherRc,
    suffix: Option<String>,
    allow_partial_pushdown: bool,
    elim_identity: bool,
) -> Result<CircuitRc> {
    #[apply(cached_lambda)]
    #[key((index.info().hash, traversal.clone(), into_module_spec.clone()), (HashBytes, IterativeMatcherRc, IterativeMatcherRc))]
    #[use_try]
    fn push_down_rec(
        index: Index,
        traversal: IterativeMatcherRc,
        into_module_spec: IterativeMatcherRc,
    ) -> Result<CircuitRc> {
        if elim_identity {
            if let Some(removed_node) = index_elim_identity(&index) {
                return Ok(removed_node);
            }
        }
        let (_, finished, traversal_per_child) = traversal.match_iterate_continue(index.node())?;
        let (into_module_spec_here, _, into_module_spec_per_child) =
            into_module_spec.match_iterate_continue(index.node())?;

        if finished {
            return Ok(index.rc());
        }

        push_down_index_raw(
            &index,
            allow_partial_pushdown,
            &mut |i, new_index| {
                push_down_rec(
                    new_index,
                    traversal_per_child[i].clone(),
                    into_module_spec_per_child[i].clone(),
                )
            },
            suffix.clone(),
            into_module_spec_here,
        )
    }

    push_down_rec(index, traversal, into_module_spec)
}
