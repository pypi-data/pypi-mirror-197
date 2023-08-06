#![feature(let_chains)]
#![feature(fs_try_exists)]
#![feature(string_leak)]
#![feature(if_let_guard)]
#![feature(iter_intersperse)]
/// reexport
pub use pyo3;
pub use uuid;

#[macro_use]
pub mod caching;
pub mod eq_by_big_hash;
pub mod repr;
#[macro_use]
pub mod errors_util;
pub mod char_tokenizer;
pub mod compact_data;
pub mod conv_shape;
pub mod lazy;
pub mod lru_cache;
pub mod name;
pub mod opt_einsum;
pub mod print;
pub mod py_types;
pub mod python_callables;
pub mod python_wrapped;
pub mod rearrange_spec;
pub mod rrfs;
pub mod set_cover;
pub mod shape;
pub mod tensor_db;
pub mod tensor_util;
pub mod union_find;
pub mod util;

pub type IndexSet<T> =
    indexmap::set::IndexSet<T, core::hash::BuildHasherDefault<rustc_hash::FxHasher>>;

#[macro_export]
macro_rules! sv {
    [$($tt:tt)*] => {
        smallvec::smallvec!($($tt)*)
    };
}

use pyo3::{exceptions::PyValueError, types::PyModule, wrap_pyfunction, PyResult};

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    // we assume throughout the codebase that usize is 8 bytes, and otherwise error here
    if !core::mem::size_of::<usize>() == 8 {
        return PyResult::Err(PyValueError::new_err("Only supports x64"));
    }
    if !cfg!(target_endian = "little") {
        return PyResult::Err(PyValueError::new_err("tried to build non little endian, crate::compact_data::TinyVecU8 relies on little endian"));
    }

    m.add_class::<crate::char_tokenizer::CharTokenizer>()?;

    m.add_class::<crate::rearrange_spec::RearrangeSpec>()?;

    m.add_class::<crate::shape::PySize>()?;

    m.add_function(wrap_pyfunction!(crate::shape::broadcast_shapes_py, m)?)?;
    m.add_class::<crate::tensor_util::TorchDeviceDtype>()?;
    m.add_class::<crate::tensor_util::TorchDeviceDtypeOp>()?;

    m.add_class::<crate::lru_cache::TensorCacheRrfs>()?;

    m.add_function(wrap_pyfunction!(crate::shape::symbolic_sizes, m)?)?;

    m.add_function(wrap_pyfunction!(crate::print::oom_fmt_py, m)?)?;

    m.add_function(wrap_pyfunction!(
        crate::tensor_util::upcast_tensor_device_dtypes_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::tensor_util::upcast_tensor_devices_py,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(crate::rrfs::save_tensor_rrfs, m)?)?;
    m.add_function(wrap_pyfunction!(crate::rrfs::tensor_from_hash, m)?)?;
    m.add_function(wrap_pyfunction!(crate::rrfs::tensor_from_hash, m)?)?;
    m.add(
        "OptimizingSymbolicSizeWarning",
        crate::py_types::PY_UTILS
            .optimizing_symbolic_size_warning
            .clone(),
    )?;

    m.add_function(wrap_pyfunction!(crate::py_types::hash_tensor, m)?)?;
    m.add_class::<crate::py_types::NotSet>()?;
    m.add("NOT_SET", crate::py_types::NotSet)?;

    m.add_function(wrap_pyfunction!(crate::tensor_db::save_tensor, m)?)?;
    m.add_function(wrap_pyfunction!(crate::tensor_db::get_tensor_prefix, m)?)?;
    m.add_function(wrap_pyfunction!(
        crate::tensor_db::sync_all_unsynced_tensors,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::tensor_db::sync_specific_tensors,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        crate::tensor_db::migrate_tensors_from_old_dir,
        m
    )?)?;

    Ok(())
}
