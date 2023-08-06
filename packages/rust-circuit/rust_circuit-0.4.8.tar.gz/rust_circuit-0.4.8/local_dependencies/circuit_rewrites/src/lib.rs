#![feature(let_chains)]
#![feature(map_try_insert)]
#![feature(portable_simd)]
#![feature(is_some_and)]
pub mod algebraic_rewrite;
pub mod batching;
pub mod canonicalize;
pub mod circuit_evaluate;
pub mod circuit_manipulation;
pub mod circuit_optimizer;
pub mod compiler_heuristics;
pub mod compiler_strip;
pub mod concat_rewrite;
pub mod debugging;
pub mod deep_rewrite;
pub mod diag_rewrite;
pub mod generalfunction_rewrite;
pub mod module_rewrite;
pub mod nb_rewrites;
pub mod sampling;
pub mod scatter_rewrite;
pub mod schedule_send;
pub mod scheduled_execution;
pub mod scheduling_alg;
pub mod server;

use pyo3::{types::PyModule, wrap_pyfunction, PyResult};

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    use crate::{
        algebraic_rewrite::{
            add_collapse_scalar_inputs, add_deduplicate, add_elim_zeros, add_flatten_once,
            add_fuse_scalar_multiples, add_make_broadcasts_explicit, add_pull_removable_axes,
            concat_elim_identity, concat_merge_uniform, concat_pull_removable_axes,
            concat_repeat_to_rearrange, distribute_all, distribute_once, einsum_concat_to_add,
            einsum_elim_identity, einsum_elim_zero, einsum_flatten_once, einsum_merge_scalars,
            einsum_nest_path, einsum_of_permute_merge, einsum_pull_removable_axes, extract_add,
            generalfunction_pull_removable_axes, index_elim_identity, index_fuse,
            index_merge_scalar, index_split_axes, make_broadcast_py, permute_of_einsum_merge,
            push_down_index_once, rearrange_elim_identity, rearrange_fuse, rearrange_merge_scalar,
            remove_add_few_input,
        },
        canonicalize::{canonicalize_node_py, deep_canonicalize_py},
        circuit_manipulation::{filter_nodes_py, path_get, update_nodes_py, update_path_py},
        circuit_optimizer::{optimize_and_evaluate, optimize_and_evaluate_many},
        compiler_heuristics::deep_maybe_distribute_py,
        concat_rewrite::{
            concat_drop_size_zero, concat_fuse, index_concat_drop_unreached, pull_concat_once,
            pull_concat_once_raw, split_to_concat,
        },
        deep_rewrite::{
            deep_heuristic_nest_adds, deep_pull_concat, deep_pull_concat_messy,
            deep_pull_concat_new, deep_push_down_index_raw,
        },
        diag_rewrite::{add_pull_diags, einsum_push_down_trace},
        scatter_rewrite::{
            add_pull_scatter, einsum_pull_scatter, index_einsum_to_scatter, scatter_elim_identity,
            scatter_pull_removable_axes, scatter_to_concat,
        },
        scheduled_execution::{
            py_circuit_to_schedule, py_circuit_to_schedule_many, scheduled_evaluate,
            scheduled_evaluate_naive,
        },
    };

    m.add_class::<crate::circuit_optimizer::OptimizationSettings>()?;
    m.add_class::<crate::circuit_optimizer::OptimizationContext>()?;

    m.add_class::<crate::scheduled_execution::Schedule>()?;
    m.add_class::<crate::scheduled_execution::ScheduleStats>()?;
    m.add_class::<crate::schedule_send::ScheduleToSend>()?;

    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::fuse_concat_modules,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::circuit_evaluate::check_evaluable,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(add_collapse_scalar_inputs, m)?)?;
    m.add_function(wrap_pyfunction!(add_deduplicate, m)?)?;
    m.add_function(wrap_pyfunction!(remove_add_few_input, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_flatten_once, m)?)?;
    m.add_function(wrap_pyfunction!(add_flatten_once, m)?)?;

    m.add_function(wrap_pyfunction!(einsum_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(index_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_merge_uniform, m)?)?;
    m.add_function(wrap_pyfunction!(generalfunction_pull_removable_axes, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::generalfunction_rewrite::generalfunction_merge_inverses,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::generalfunction_rewrite::generalfunction_special_case_simplification,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::generalfunction_rewrite::generalfunction_evaluate_simple,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::generalfunction_rewrite::generalfunction_gen_index_const_to_index,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(concat_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_make_broadcasts_explicit, m)?)?;
    m.add_function(wrap_pyfunction!(make_broadcast_py, m)?)?;
    m.add_function(wrap_pyfunction!(distribute_once, m)?)?;
    m.add_function(wrap_pyfunction!(distribute_all, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_of_permute_merge, m)?)?;
    m.add_function(wrap_pyfunction!(permute_of_einsum_merge, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_elim_zero, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_merge_scalars, m)?)?;
    m.add_function(wrap_pyfunction!(push_down_index_once, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::concat_rewrite::concat_elim_split,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(index_split_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_elim_zeros, m)?)?;

    m.add_function(wrap_pyfunction!(deep_canonicalize_py, m)?)?;
    m.add_function(wrap_pyfunction!(canonicalize_node_py, m)?)?;
    m.add_function(wrap_pyfunction!(crate::canonicalize::deep_normalize, m)?)?;
    m.add_function(wrap_pyfunction!(crate::canonicalize::normalize_node_py, m)?)?;

    m.add_function(wrap_pyfunction!(crate::batching::batch_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(crate::batching::batch_einsum_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::compiler_strip::strip_names_and_tags_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(deep_maybe_distribute_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::compiler_heuristics::maybe_distribute_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(einsum_nest_path, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::algebraic_rewrite::einsum_nest_optimize_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::deep_rewrite::deep_optimize_einsums_py,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(index_einsum_to_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_pull_removable_axes, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::circuit_optimizer::optimize_circuit_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(scatter_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(scheduled_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(scheduled_evaluate_naive, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate_many, m)?)?;
    m.add_function(wrap_pyfunction!(py_circuit_to_schedule, m)?)?;
    m.add_function(wrap_pyfunction!(py_circuit_to_schedule_many, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::circuit_optimizer::optimize_to_schedule,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::circuit_optimizer::optimize_to_schedule_many,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(deep_heuristic_nest_adds, m)?)?;
    m.add_function(wrap_pyfunction!(pull_concat_once_raw, m)?)?;
    m.add_function(wrap_pyfunction!(pull_concat_once, m)?)?;
    m.add_function(wrap_pyfunction!(concat_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(index_concat_drop_unreached, m)?)?;
    m.add_function(wrap_pyfunction!(concat_drop_size_zero, m)?)?;
    m.add_function(wrap_pyfunction!(split_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(deep_push_down_index_raw, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat_messy, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat_new, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat, m)?)?;

    m.add_function(wrap_pyfunction!(add_pull_diags, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_push_down_trace, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_concat_to_add, m)?)?;
    m.add_function(wrap_pyfunction!(concat_repeat_to_rearrange, m)?)?;
    m.add_function(wrap_pyfunction!(extract_add, m)?)?;
    m.add_function(wrap_pyfunction!(add_fuse_scalar_multiples, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::scatter_rewrite::concat_to_scatter,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::debugging::opt_eval_each_subcircuit_until_fail,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::algebraic_rewrite::add_outer_product_broadcasts_on_top,
        m
    )?)?;

    m.add_class::<crate::deep_rewrite::SimpFnSubset>()?;
    m.add_function(wrap_pyfunction!(
        crate::deep_rewrite::compiler_simp_step_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::deep_rewrite::compiler_simp_py, m)?)?;
    m.add_function(wrap_pyfunction!(crate::deep_rewrite::simp, m)?)?;

    m.add_function(wrap_pyfunction!(filter_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(update_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(path_get, m)?)?;
    m.add_function(wrap_pyfunction!(update_path_py, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::algebraic_rewrite::einsum_permute_to_rearrange,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::nb_rewrites::add_elim_removable_axes_weak,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::nb_rewrites::einsum_elim_removable_axes_weak,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(crate::server::circuit_server_serve, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::elim_empty_module,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::elim_no_input_module,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::module_remove_unused_inputs,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::py_deep_module_remove_unused_inputs,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::module_rewrite::extract_rewrite_raw,
        m
    )?)?;

    Ok(())
}
