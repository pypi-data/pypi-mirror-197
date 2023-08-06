#![feature(let_chains)]
#![feature(iterator_try_reduce)]
pub mod cumulant_rewrites;
pub mod diff;
pub mod distribute_and_factor;
pub mod generalfunction;
pub mod index_rewrites;
pub mod modules;
pub mod nest;

use pyo3::{types::PyModule, wrap_pyfunction, PyResult};

pub fn register(py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<crate::generalfunction::GeneralFunctionSpecTester>()?;

    m.add_function(wrap_pyfunction!(crate::diff::diff_circuits, m)?)?;
    m.add_function(wrap_pyfunction!(crate::diff::compute_self_hash, m)?)?;

    m.add_function(wrap_pyfunction!(crate::modules::extract_rewrite, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::index_rewrites::default_index_traversal,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::index_rewrites::push_down_index, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::distribute_and_factor::traverse_until_depth,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::distribute_and_factor::distribute,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::modules::module_new_bind, m)?)?;
    m.add_class::<crate::modules::BindItem>()?;
    m.add_class::<crate::modules::ModulePusher>()?;
    m.add_function(wrap_pyfunction!(
        crate::modules::default_nested_module_namer,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::modules::default_update_bindings_nested_namer,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::modules::update_bindings_nested, m)?)?;
    m.add_function(wrap_pyfunction!(crate::modules::extract_symbols, m)?)?;
    m.add_function(wrap_pyfunction!(crate::modules::extract_symbols_get, m)?)?;
    m.add_function(wrap_pyfunction!(crate::modules::pull_out_of_modules, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::modules::pull_out_of_modules_get,
        m
    )?)?;

    crate::nest::register(py, m)?;

    m.add_function(wrap_pyfunction!(
        crate::cumulant_rewrites::rewrite_cum_to_circuit_of_cum,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::cumulant_rewrites::kappa_term_py,
        m
    )?)?;

    Ok(())
}
