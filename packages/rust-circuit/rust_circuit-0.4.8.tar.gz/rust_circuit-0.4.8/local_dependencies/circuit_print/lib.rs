#![feature(let_chains)]
#![feature(if_let_guard)]
pub mod parsing;
pub mod print;
pub mod print_html;

use pyo3::{types::PyModule, wrap_pyfunction, PyResult};

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<print::PrintOptions>()?;
    m.add_class::<print_html::PrintHtmlOptions>()?;
    m.add_function(wrap_pyfunction!(print::set_debug_print_options, m)?)?;
    m.add_class::<parsing::Parser>()?;

    Ok(())
}
