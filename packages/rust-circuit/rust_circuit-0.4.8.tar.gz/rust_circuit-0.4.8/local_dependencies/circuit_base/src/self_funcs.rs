#![allow(non_snake_case)]
use anyhow::Result;
use once_cell::sync::Lazy;
use pyo3::{pyclass, PyObject, Python};
use rr_util::{lru_cache::TensorCacheRrfs, py_types::SELF_MODULE};

use crate::{Circuit, CircuitRc};

#[pyclass]
#[derive(Clone)]
// break deps to allow splitting up into smaller crates (to improve check/compile time)
pub struct SelfFuncs {
    pub replace_expand_map: fn(CircuitRc, Vec<(CircuitRc, CircuitRc)>) -> Result<CircuitRc>,
    pub replace_expand_bottom_up_dyn:
        fn(CircuitRc, &dyn Fn(CircuitRc) -> Option<CircuitRc>) -> Result<CircuitRc>,
    pub repr_circuit_default_no_bijection: fn(CircuitRc) -> String,
    pub debug_repr: fn(CircuitRc) -> Result<String>,
    pub compiler_default_print: fn(CircuitRc) -> (),
    pub compiler_default_repr: fn(CircuitRc) -> Result<String>,
    pub repr: fn(CircuitRc) -> Result<String>,
    pub repr_shape_always: fn(CircuitRc) -> Result<String>,
    pub print_circuit_stats: fn(&Circuit) -> (),
    pub PrintOptionsBase_print: fn(Option<PyObject>, &[CircuitRc]) -> Result<()>,
    pub PrintHtmlOptions_print: fn(Option<PyObject>, &[CircuitRc]) -> Result<()>,
    pub PrintOptions_repr: fn(Option<PyObject>, CircuitRc) -> Result<String>,
    pub parse_circuit: fn(&str, &mut Option<TensorCacheRrfs>) -> Result<CircuitRc>,
}

pub static SELF_FUNCS: Lazy<SelfFuncs> = Lazy::new(|| {
    Python::with_gil(|py| {
        SELF_MODULE
            .getattr(py, "__self_funcs")
            .unwrap()
            .extract(py)
            .unwrap()
    })
});

pub fn replace_expand_map(
    circuit: CircuitRc,
    map: Vec<(CircuitRc, CircuitRc)>,
) -> Result<CircuitRc> {
    (SELF_FUNCS.replace_expand_map)(circuit, map)
}

pub fn replace_expand_bottom_up_dyn(
    circuit: CircuitRc,
    replacer: &dyn Fn(CircuitRc) -> Option<CircuitRc>,
) -> Result<CircuitRc> {
    (SELF_FUNCS.replace_expand_bottom_up_dyn)(circuit, replacer)
}

pub fn repr_circuit_default_no_bijection(circuit: CircuitRc) -> String {
    (SELF_FUNCS.repr_circuit_default_no_bijection)(circuit)
}

pub fn print_circuit_stats(circuit: &CircuitRc) {
    (SELF_FUNCS.print_circuit_stats)(circuit)
}

pub fn compiler_default_print(circuit: &CircuitRc) {
    (SELF_FUNCS.compiler_default_print)(circuit.clone())
}

pub fn compiler_default_repr(circuit: &CircuitRc) -> Result<String> {
    (SELF_FUNCS.compiler_default_repr)(circuit.clone())
}

pub fn repr_shape_always(circuit: CircuitRc) -> Result<String> {
    (SELF_FUNCS.repr_shape_always)(circuit)
}

pub fn parse_circuit(x: &str, cache: &mut Option<TensorCacheRrfs>) -> Result<CircuitRc> {
    (SELF_FUNCS.parse_circuit)(x, cache)
}
