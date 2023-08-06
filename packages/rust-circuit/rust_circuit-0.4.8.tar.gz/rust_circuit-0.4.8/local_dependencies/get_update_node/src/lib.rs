#![feature(let_chains)]
//! Basic TODO: add more rust helpers + builders as needed!

pub mod iterative_matcher;
pub mod library;
pub mod matcher;
pub mod matcher_debug;
pub mod operations;
pub mod sampler;
pub mod transform;

pub use iterative_matcher::{
    new_traversal, restrict, restrict_sl, IterateMatchResults, IterativeMatcher,
    IterativeMatcherData, IterativeMatcherRc,
};
pub use matcher::{Matcher, MatcherData, MatcherFromPy, MatcherFromPyBase, MatcherRc};
pub use operations::{
    AnyFound, BoundAnyFound, BoundGetter, BoundUpdater, Expander, Getter, Updater,
};
use pyo3::{types::PyModule, wrap_pyfunction, PyResult};
pub use transform::{Transform, TransformData, TransformRc};

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<crate::Matcher>()?;
    m.add_class::<crate::matcher::RegexWrap>()?;
    m.add_class::<crate::IterativeMatcher>()?;
    m.add_function(wrap_pyfunction!(crate::restrict, m)?)?;
    m.add_function(wrap_pyfunction!(crate::restrict_sl, m)?)?;
    m.add_function(wrap_pyfunction!(crate::new_traversal, m)?)?;
    m.add_class::<crate::IterateMatchResults>()?;
    m.add_class::<crate::Transform>()?;
    m.add_class::<crate::Updater>()?;
    m.add_class::<crate::BoundUpdater>()?;
    m.add_class::<crate::Getter>()?;
    m.add_class::<crate::BoundGetter>()?;
    m.add_class::<crate::AnyFound>()?;
    m.add_class::<crate::BoundAnyFound>()?;
    m.add_class::<crate::Expander>()?;

    m.add_function(wrap_pyfunction!(crate::sampler::default_var_matcher, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::library::replace_outside_traversal_symbols_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(crate::library::apply_in_traversal_py, m)?)?;
    m.add_class::<crate::sampler::RandomSampleSpec>()?;
    m.add_class::<crate::sampler::RunDiscreteVarAllSpec>()?;
    m.add_class::<crate::sampler::Sampler>()?;
    m.add_function(wrap_pyfunction!(crate::sampler::default_hash_seeder, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::matcher_debug::append_matchers_to_names,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::matcher_debug::print_matcher_debug,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::matcher_debug::repr_matcher_debug,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::sampler::factored_cumulant_expectation_rewrite,
        m
    )?)?;

    Ok(())
}
