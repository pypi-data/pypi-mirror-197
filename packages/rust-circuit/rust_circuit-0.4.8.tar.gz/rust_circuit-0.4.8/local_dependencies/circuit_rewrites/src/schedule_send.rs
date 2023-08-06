// temporary schedule sending setup
use anyhow::{Context, Result};
use circuit_base::{
    self_funcs::{parse_circuit, repr_shape_always},
    CircuitNode, IrreducibleNode, Scalar,
};
use miniserde::{json, Deserialize, Serialize};
use pyo3::{prelude::*, types::PyByteArray};
use rr_util::{
    lru_cache::TensorCacheRrfs,
    py_types::{Tensor, PY_UTILS},
    pycall,
    shape::{shape_into_known, Shape},
    sv,
    tensor_util::{TorchDevice, TorchDeviceDtype, TorchDtype},
    unwrap,
};
use rustc_hash::FxHashMap as HashMap;

use crate::scheduled_execution::{get_children_keys, Instruction, Schedule, ScheduleConstant};

#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct InstructionToSend {
    variant: String,
    key: usize,
    info: String,
    children: Vec<usize>,
}

#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScheduleToSend {
    pub instructions: Vec<InstructionToSend>,
    pub constants: ::std::collections::HashMap<usize, String>,
    pub scalars: ::std::collections::HashMap<usize, String>,
    pub output_circuits: Vec<(usize, Vec<usize>)>,
    pub old_constant_hashes: Vec<(Vec<u8>, usize)>,
}

#[pymethods]
impl ScheduleToSend {
    pub fn evaluate_remote_many(
        &self,
        remote_url: String,
        device: TorchDevice,
    ) -> Result<Vec<Tensor>> {
        let self_string = json::to_string(&self);
        let response = ureq::post(&remote_url)
            .send_string(&self_string)
            .context("during evaluate_remote http request")?;
        let mut body: Vec<u8> = vec![];
        response.into_reader().read_to_end(&mut body).unwrap();
        let mut offset = 0usize;
        self.output_circuits
            .iter()
            .map(|circ| {
                let len = usize::from_le_bytes(body[offset..offset + 8].try_into().unwrap());
                let dtype = unsafe { std::mem::transmute::<u8, TorchDtype>(body[offset + 8]) };
                offset += 9;
                let body_pybytes: PyObject =
                    Python::with_gil(|py| PyByteArray::new(py, &body[offset..offset + len]).into());
                offset += len;
                let out_shape = circ.1.clone();
                let count: usize = out_shape.iter().product();
                pycall!(
                    PY_UTILS.tensor_from_bytes,
                    (
                        TorchDeviceDtype { dtype, device },
                        out_shape,
                        body_pybytes,
                        count,
                    ),
                    anyhow
                )
            })
            .collect()
    }
    pub fn evaluate_remote(&self, remote_url: String, device: TorchDevice) -> Result<Tensor> {
        let r = self.evaluate_remote_many(remote_url, device)?;
        anyhow::ensure!(
            r.len() == 1,
            "evaluate_remote: got multiple tensors (maybe you want evaluate_remote_many?)"
        );
        Ok(r[0].clone())
    }
}

impl ScheduleToSend {
    pub fn load(self, cache: &mut Option<TensorCacheRrfs>) -> Result<Schedule> {
        let mut result = Schedule {
            instructions: vec![],
            constants: Default::default(),
            scalars: Default::default(),
            output_circuits: Some(
                self.output_circuits
                    .iter()
                    .map(|x| (x.0, Scalar::nrc(0.0, sv![], None)))
                    .collect(),
            ),
            old_constant_hashes: self
                .old_constant_hashes
                .iter()
                .map(|(b, i)| (b.to_vec().try_into().unwrap(), *i))
                .collect(),
        };

        let mut shapes: HashMap<usize, Shape> = <HashMap<usize, Shape> as Default>::default();
        result.constants = self
            .constants
            .iter()
            .map(|(k, v)| {
                let parsed = parse_circuit(v, cache)?;
                shapes.insert(*k, parsed.info().shape.clone());
                let irreducible: Option<IrreducibleNode> = (**parsed).clone().into();
                Ok((*k, ScheduleConstant::Circ(irreducible.unwrap())))
            })
            .collect::<Result<_>>()?;
        result.scalars = self
            .scalars
            .iter()
            .map(|(k, v)| {
                Ok((*k, {
                    let resulty = parse_circuit(v, cache)?.as_scalar().unwrap().clone();
                    shapes.insert(*k, resulty.info().shape.clone());
                    resulty
                }))
            })
            .collect::<Result<_>>()?;
        result.instructions = self
            .instructions
            .iter()
            .map(|ins| {
                let v: &str = &ins.variant;
                match v {
                    "Drop" => Ok(Instruction::Drop(ins.key)),
                    "Compute" => Ok(Instruction::Compute(ins.key, {
                        let result = parse_circuit(&ins.info, cache)?;
                        shapes.insert(ins.key, result.info().shape.clone());
                        result
                    })),
                    _ => {
                        panic!()
                    }
                }
            })
            .collect::<Result<Vec<Instruction>>>()?;
        Ok(result)
    }
}

impl TryFrom<&Schedule> for ScheduleToSend {
    type Error = anyhow::Error;

    fn try_from(x: &Schedule) -> Result<Self, Self::Error> {
        x.check_no_syms().context(concat!(
            "schedules with symbols can't be sent\n",
            "(TODO: we should maybe avoid this check so that you can ",
            "always serialize schedules, but ScheduleToSend doesn't eror check well...)"
        ))?;
        x.check_no_raw_tensor_constants()
            .context("schedules with already replaced raw tensors can't be sent")?;

        fn map_to_str<'a, N: CircuitNode + Clone + 'a>(
            map: impl IntoIterator<Item = (&'a usize, &'a N)>,
        ) -> Result<std::collections::HashMap<usize, String>> {
            map.into_iter()
                .map(|(k, v)| Ok((*k, repr_shape_always(v.crc())?)))
                .collect::<Result<_>>()
        }

        let out = Self {
            instructions: x
                .instructions
                .iter()
                .map(|i| {
                    let out = match i {
                        Instruction::Compute(key, circ) => InstructionToSend {
                            key: *key,
                            variant: "Compute".to_owned(),
                            info: repr_shape_always(circ.clone())?,
                            children: get_children_keys(circ.clone()),
                        },
                        Instruction::Drop(key) => InstructionToSend {
                            key: *key,
                            variant: "Drop".to_owned(),
                            info: "".to_owned(),
                            children: vec![],
                        },
                    };
                    Ok(out)
                })
                .collect::<Result<_>>()?,
            constants: map_to_str(
                x.constants
                    .iter()
                    .map(|(h, x)| (h, unwrap!(x, ScheduleConstant::Circ))), /* we checked no raw tensors above */
            )?,
            scalars: map_to_str(&x.scalars)?,
            output_circuits: x
                .output_circuits
                .as_ref()
                .unwrap()
                .iter()
                .map(|c| (c.0, shape_into_known(c.1.info().shape.clone())))
                .collect(),
            old_constant_hashes: x
                .old_constant_hashes
                .iter()
                .map(|(b, i)| (b.to_vec(), *i))
                .collect(),
        };
        Ok(out)
    }
}
