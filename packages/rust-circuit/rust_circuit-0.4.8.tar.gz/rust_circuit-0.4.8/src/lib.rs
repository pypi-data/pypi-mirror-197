#![feature(core_intrinsics)]
// Personally, I like or_fun_call as a lint. But currently code fails...
#![allow(clippy::too_many_arguments, clippy::or_fun_call)]
#![feature(map_try_insert)]
use circuit_base::self_funcs::SelfFuncs;
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

use pyo3::{
    types::{PyModule, PyTuple},
    PyResult, PyTypeInfo, Python,
};

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pyo3::pymodule]
pub fn _rust(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    register(py, m)
}

fn register(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    pyo3::anyhow::set_anyhow_to_py_err(Box::new(rr_util::errors_util::anyhow_to_py_err));

    m.add_class::<rr_util::errors_util::ExceptionWithRustContext>()?;
    rr_util::errors_util::register_exceptions(py, m)?;

    rr_util::register(py, m)?;
    circuit_base::register(py, m)?;
    circuit_utils::register(py, m)?;
    expand_node::register(py, m)?;
    circuit_print::register(py, m)?;
    circuit_rewrites::register(py, m)?;
    get_update_node::register(py, m)?;
    nb_operations::register(py, m)?;

    // create dummy object for all the type aliases we use in the stub file
    // TODO: maybe these should somehow be the actual types we use in the stub file
    // (this is kinda annoying)
    m.add("Shape", PyTuple::type_object(py))?;
    for dummy_name in [
        "Axis",
        "IrreducibleNode",
        "Leaf",
        "LeafConstant",
        "Var",
        "MatcherIn",
        "IterativeMatcherIn",
        "TransformIn",
        "SampleSpecIn",
        "TorchAxisIndex",
        "IntOrMatcher",
        "NestEinsumsSpecMultiple",
        "NestEinsumsSpecSub",
        "NestEinsumsSpec",
        "NestAddsSpecMultiple",
        "NestAddsSpecSub",
        "NestAddsSpec",
        "GeneralFunctionSpec",
        "Binder",
        "UpdatedIterativeMatcher",
        "UpdatedIterativeMatcherIn",
        "PrintOptionsBase",
        "CliColor",
        "CircuitColorer",
        "CircuitHtmlColorer",
        "NestedModuleNamer",
        "ModuleConstructCallback",
        "MaybeUpdate",
    ] {
        m.add(dummy_name, py.None())?;
    }

    m.add(
        "__self_funcs",
        SelfFuncs {
            replace_expand_map: expand_node::replace_expand_map,
            replace_expand_bottom_up_dyn: expand_node::replace_expand_bottom_up_dyn,
            repr_circuit_default_no_bijection: |x| {
                let mut po = circuit_print::print::PrintOptions::default();
                po.bijection = false;
                po.repr(x).unwrap()
            },
            repr_shape_always: |x| {
                let mut po = circuit_print::print::PrintOptions::default();
                po.shape_only_when_necessary = false;
                po.repr(x)
            },
            debug_repr: circuit_print::print::debug_repr,
            compiler_default_print: |x| {
                circuit_print::print::PrintOptions::compiler_default()
                    .print(x)
                    .unwrap()
            },
            compiler_default_repr: |x| {
                circuit_print::print::PrintOptions::compiler_default().repr(x)
            },
            repr: |x| circuit_print::print::PrintOptions::default().repr(x),
            PrintOptionsBase_print: circuit_print::print_html::PrintOptionsBase_print,
            PrintHtmlOptions_print: circuit_print::print_html::PrintHtmlOptions_print,
            PrintOptions_repr: circuit_print::print::PrintOptions_repr,
            print_circuit_stats: circuit_print::print::print_circuit_stats,
            parse_circuit: |a, b| circuit_print::parsing::Parser::default().parse_circuit(a, b),
        },
    )?;

    Ok(())
}
