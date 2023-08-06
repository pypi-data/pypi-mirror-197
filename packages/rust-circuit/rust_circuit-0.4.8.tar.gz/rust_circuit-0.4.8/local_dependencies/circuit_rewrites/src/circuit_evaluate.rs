use std::iter::zip;

use anyhow::{bail, Result};
use circuit_base::{generalfunction::SpecTrait, Circuit, CircuitNode, CircuitRc, Module};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, pyfunction, IntoPy, PyObject, Python};
use rr_util::{
    py_types::{
        einops_repeat, einsum_py, make_diagonal_py, scalar_to_tensor, scalar_to_tensor_py,
        ExtraPySelfOps, Tensor, PY_UTILS,
    },
    pycall, python_error_exception, sv,
    tensor_util::{upcast_tensor_device_dtypes, TorchDeviceDtypeOp},
    util::EinsumAxes,
};
use thiserror::Error;

#[pyfunction]
pub fn check_evaluable(circuit: CircuitRc) -> Result<()> {
    if !circuit.info().is_explicitly_computable() {
        bail!(TensorEvalError::NotExplicitlyComputable { circuit })
    }
    if !circuit.info().is_constant() {
        bail!(TensorEvalError::NotConstant { circuit })
    }
    Ok(())
}

pub fn eval_tensors(x: &CircuitRc, tensors: &[Tensor]) -> Result<Tensor> {
    Python::with_gil(|py| match &***x {
        Circuit::Einsum(e) => {
            let tensors = upcast_tensor_device_dtypes(tensors);
            if e.in_axes.is_empty() {
                return scalar_to_tensor_py(py, 1., sv![], Default::default());
            }
            let out_axes_deduped: EinsumAxes = e.out_axes.unique();
            let result_non_diag: Tensor = einsum_py(
                py,
                zip(tensors.iter().cloned(), e.in_axes.iter().cloned()).collect(),
                out_axes_deduped.clone(),
            )?;

            if out_axes_deduped.len() != e.out_axes.len() {
                Ok(make_diagonal_py(
                    py,
                    &result_non_diag,
                    out_axes_deduped,
                    e.out_axes.clone(),
                )?)
            } else {
                Ok(result_non_diag)
            }
        }
        Circuit::Array(a) => Ok(a.value.clone()),
        Circuit::Symbol(_) => {
            Err(TensorEvalError::NotExplicitlyComputableInternal { circuit: x.clone() }.into())
        }

        Circuit::Scalar(s) => scalar_to_tensor(s.value, s.info().shape.clone(), Default::default()),
        Circuit::Add(_) => {
            if tensors.is_empty() {
                return scalar_to_tensor(0.0, sv![], Default::default());
            }
            let tensors = upcast_tensor_device_dtypes(tensors);
            let mut out = tensors[0].clone();
            Python::with_gil(|py| {
                for tensor in tensors[1..].iter() {
                    out = tensor.clone().py_add(py, out.clone()).unwrap();
                }
            });
            Ok(out)
        }
        Circuit::Rearrange(r) => {
            // avoid using self.spec.apply so we get shape errors correctly
            let (string, letter_sizes) = r
                .conform_to_input_shape_spec()
                .to_einops_string_and_letter_sizes();
            einops_repeat(&tensors[0], string, letter_sizes)
        }
        Circuit::Index(i) => {
            let tensors = upcast_tensor_device_dtypes(tensors);
            assert_eq!(tensors.len(), 1);
            Python::with_gil(|py| {
                PY_UTILS
                    .index_apply_dimwise
                    .call(py, (tensors[0].clone(), i.index.clone()), None)
                    .map_err(|err| err.into())
                    .map(|x| x.extract(py).unwrap())
            })
        }
        Circuit::GeneralFunction(g) => g.spec.function(tensors),
        Circuit::Concat(c) => {
            let tensors = upcast_tensor_device_dtypes(tensors);
            PY_UTILS
                .torch
                .getattr(py, "cat")
                .unwrap()
                .call(py, (tensors.to_vec(), c.axis), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        }
        Circuit::Scatter(s) => {
            let tensors = upcast_tensor_device_dtypes(tensors);
            PY_UTILS
                .scatter
                .call(
                    py,
                    (s.index.clone(), s.shape().clone(), tensors[0].clone()),
                    None,
                )
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        }
        Circuit::Conv(c) => {
            let tensors = upcast_tensor_device_dtypes(tensors);
            pycall!(
                PY_UTILS.conv,
                (
                    c.dims(),
                    tensors[0].clone(),
                    tensors[1].clone(),
                    c.stride.clone(),
                    c.padding.clone(),
                ),
                anyhow
            )
        }
        Circuit::Module(m) => {
            bail!(TensorEvalError::ModulesCantBeDirectlyEvalutedInternal { module: m.clone() })
        }
        Circuit::Tag(_t) => {
            assert_eq!(tensors.len(), 1);
            Ok(tensors[0].clone())
        }
        Circuit::DiscreteVar(_d) => {
            Err(TensorEvalError::NotExplicitlyComputableInternal { circuit: x.clone() }.into())
        }
        Circuit::StoredCumulantVar(_v) => {
            Err(TensorEvalError::NotExplicitlyComputableInternal { circuit: x.clone() }.into())
        }
        Circuit::Cumulant(c) => {
            if !c.children().all(|x| x.info().is_constant()) {
                bail!(TensorEvalError::NotExplicitlyComputableInternal { circuit: c.crc() })
            }
            let tensors = upcast_tensor_device_dtypes(tensors);
            let out = match (c.children_sl(), &tensors[..]) {
                ([], []) => scalar_to_tensor(1., sv![], Default::default())?,
                ([_], [t]) => t.clone(),
                _ => scalar_to_tensor(
                    0.,
                    c.info().shape.clone(),
                    c.info().device_dtype.unwrap_or_defaults(),
                )?,
            };
            Ok(out)
        }
    })
}

const INTERNAL_EVAL_ERROR_MESSAGE: &str = "this is likely an internal error (earlier errors should have triggered or an invalid circuit was constructed)";

#[apply(python_error_exception)]
#[base_error_name(TensorEval)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum TensorEvalError {
    #[error(
        "reached not explicitly computable. {}\ncircuit={circuit:?}) ({e_name})",
        INTERNAL_EVAL_ERROR_MESSAGE
    )]
    NotExplicitlyComputableInternal { circuit: CircuitRc },
    #[error("not explicitly computable: {circuit:?}) ({e_name})")]
    NotExplicitlyComputable { circuit: CircuitRc },
    #[error("not constant: {circuit:?}) ({e_name})")]
    NotConstant { circuit: CircuitRc },
    #[error(
        "You can't directly evaluate  module. {}\nmodule={module:?}) ({e_name})",
        INTERNAL_EVAL_ERROR_MESSAGE
    )]
    ModulesCantBeDirectlyEvalutedInternal { module: Module },
    #[error("incompatible dtype circ:{circ:?} passed:{passed:?} ({e_name})")]
    DeviceDtypeError {
        circ: TorchDeviceDtypeOp,
        passed: TorchDeviceDtypeOp,
    },
}
