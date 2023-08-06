use pyo3::{types::PyModule, PyResult, Python};
use rr_util::errors_util::print_exception_stubs;
pub fn main() -> PyResult<()> {
    pyo3::prepare_freethreaded_python();
    println!("# to generate below exception stubs, `cargo run --bin print_exception_stubs`");
    Python::with_gil(|py| -> PyResult<()> {
        let m = PyModule::new(py, "_dummy").unwrap();
        rust_circuit::_rust(py, m)?; // hack to ensure we're linked with everything
        println!("{}", print_exception_stubs(py)?);
        Ok(())
    })
}
