use std::{
    collections::hash_map::Entry,
    fmt::{self, Display},
    iter::zip,
};

use anyhow::{anyhow, bail, Context, Result};
use circuit_base::{
    cached_circuit_properties::max_non_leaf_size,
    circuit_utils::toposort_circuit,
    generalfunction::GeneralFunctionOutputSpec,
    module::{
        any_children_with_symbolic_sizes, any_modules, conform_all_modules, substitute_all_modules,
    },
    prelude::*,
    visit_circuit_non_free, Array, GeneralFunction, GeneralFunctionSpec, IrreducibleNode, Leaf,
    ModuleSpec, Scalar, Symbol,
};
use circuit_utils::{biggest_non_leaf, hash_to_node_non_free, is_definitely_view_on_child};
use itertools::Itertools;
use macro_rules_attribute::apply;
use miniserde::json;
use num_bigint::BigUint;
use pyo3::{exceptions::PyValueError, prelude::*, types::PyBytes};
use rr_util::{
    lru_cache::TensorCacheRrfs,
    print::oom_fmt,
    py_types::{
        is_python_running, scalar_to_tensor, tensor_scale, ExtraPySelfOps, Tensor, PY_UTILS,
    },
    pycall, python_error_exception,
    shape::Shape,
    sv,
    tensor_util::{TorchDevice, TorchDeviceDtype},
    timed, unwrap,
    util::{arc_ref_clone, hash_to_hex, with_context_failable, HashBytes},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use thiserror::Error;

use crate::{
    circuit_evaluate::eval_tensors,
    circuit_optimizer::{OptimizationContext, OptimizationSettings},
    module_rewrite::deep_module_remove_unused_inputs,
    schedule_send::ScheduleToSend,
    scheduling_alg::{Dag, DagSimpSettings},
};

#[derive(Clone, Debug)]
pub enum Instruction {
    Drop(usize),
    Compute(usize, CircuitRc),
}

impl IntoPy<PyObject> for Instruction {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Instruction::Drop(hb) => hb.into_py(py),
            Instruction::Compute(key, circ) => (key, circ).into_py(py),
        }
    }
}

/// allow for having tensors directly so we can bypass hashing (which isn't
/// important for scheduling)
#[derive(Clone, Debug, FromPyObject)]
pub enum ScheduleConstant {
    Circ(IrreducibleNode),
    Tensor(Tensor),
}

impl IntoPy<PyObject> for ScheduleConstant {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            ScheduleConstant::Circ(circ) => circ.into_py(py),
            ScheduleConstant::Tensor(tensor) => tensor.into_py(py),
        }
    }
}

impl ScheduleConstant {
    pub fn as_symbol(&self) -> Option<&Symbol> {
        if let Self::Circ(circ) = self {
            circ.as_symbol()
        } else {
            None
        }
    }
    pub fn as_array(&self) -> Option<&Array> {
        if let Self::Circ(circ) = self {
            circ.as_array()
        } else {
            None
        }
    }
    pub fn as_tensor(&self) -> Option<&Tensor> {
        if let Self::Tensor(t) = self {
            Some(t)
        } else {
            None
        }
    }
    pub fn convert_as_tensor(&self) -> Option<&Tensor> {
        match self {
            Self::Circ(circ) => circ.as_array().map(|x| &x.value),
            Self::Tensor(tensor) => Some(tensor),
        }
    }
    pub fn shape(&self) -> &Shape {
        match self {
            Self::Circ(circ) => &circ.info().shape,
            Self::Tensor(tensor) => tensor.shape(),
        }
    }
    pub fn device_dtype(&self) -> TorchDeviceDtype {
        match self {
            ScheduleConstant::Circ(c) => c.info().device_dtype.unwrap_or_defaults(),
            ScheduleConstant::Tensor(t) => t.device_dtype,
        }
    }
}

/// Schedule is an optimized sequence of operations to perform to compute a circuit
/// it keeps arrayconstants seperately, and replacing arrayconstants in a schedule should produce the same
/// output + ~performance as optimizing the circuit with different arrayconstants from the beginning
/// Schedule stores intermediate nodes as circuits with Symbol children, where the name of the symbol
/// contains the "id" of that node
#[pyclass]
#[derive(Clone, Debug)]
pub struct Schedule {
    #[pyo3(get)]
    pub instructions: Vec<Instruction>,
    #[pyo3(get)]
    pub constants: HashMap<usize, ScheduleConstant>,
    // keep scalar constants seperate so adjust numerical scale can work without losing precision
    // before when these were in tensors, they had to be right dtype and therefore overflowed when
    // adjustment needed
    #[pyo3(get)]
    pub scalars: HashMap<usize, Scalar>,
    pub output_circuits: Option<Vec<(usize, CircuitRc)>>,
    pub old_constant_hashes: HashMap<HashBytes, usize>,
}

#[pymethods]
impl Schedule {
    pub fn validate(&self, validate_output: bool) -> Result<()> {
        // NOTE: values can't be computed or dropped multiple times atm.
        let mut prior_compute_numbers = HashSet::default();
        let mut prior_drop_numbers = HashSet::default();

        for num in self.scalars.keys() {
            if self.constants.contains_key(num) {
                bail!("num={num} used for both constants and scalars!");
            }
        }
        for instruction in &self.instructions {
            match instruction {
                Instruction::Drop(drop) => {
                    if !prior_compute_numbers.contains(drop) {
                        bail!("drop={drop} not previously computed");
                    }
                    if !prior_drop_numbers.insert(drop) {
                        bail!("drop={drop} was already dropped!");
                    }
                }
                Instruction::Compute(key, circuit) => {
                    if !prior_compute_numbers.insert(key) {
                        bail!("key={key} was already computed!");
                    }
                    if circuit.is_leaf() {
                        bail!("leaf circuit is being computed circuit={circuit:?}");
                    }
                }
            }
        }

        if validate_output {
            let output_ids: HashSet<usize> = self
                .output_circuits
                .as_ref()
                .ok_or(anyhow!("no output!"))?
                .iter()
                .map(|x| x.0)
                .collect();
            for computed in prior_compute_numbers {
                if !prior_drop_numbers.contains(computed) && !output_ids.contains(computed) {
                    bail!("computed={computed} is never dropped (or returned)");
                }
            }
        }

        Ok(())
    }

    #[pyo3(signature=(map, allow_missing = false))]
    pub fn replace_tensors(
        &self,
        map: HashMap<HashBytes, Tensor>,
        allow_missing: bool,
    ) -> Result<Self> {
        let mut result = self.clone();
        for (k, v) in map {
            if !result.old_constant_hashes.contains_key(&k) {
                if allow_missing {
                    continue;
                }
                return Err(PyErr::new::<pyo3::exceptions::PyKeyError, _>(format!(
                    "key circuit {k_hex} wasn't present in original",
                    k_hex = hash_to_hex(&k)
                ))
                .into());
            }
            // should be present because we checked above
            let entry = unwrap!(
                result.constants.entry(result.old_constant_hashes[&k]),
                Entry::Occupied
            );
            if entry.get().shape() != v.shape() {
                bail!(
                    "key {k_hex}: original shape {orig_shape:?} doesn't match replacement shape {new_shape:?}",
                    k_hex=hash_to_hex(&k),
                    orig_shape = entry.get().shape(),
                    new_shape = v.shape(),
                );
            }

            *entry.into_mut() = ScheduleConstant::Tensor(v);
        }
        Ok(result)
    }

    #[pyo3(name = "map_tensors")]
    pub fn map_tensors_py(&self, f: PyObject) -> PyResult<Self> {
        let mut result = self.clone();

        result.old_constant_hashes.iter().for_each(|(key, id)| {
            let maybe_tensor: Option<Tensor> =
                Python::with_gil(|py| pycall!(f, (PyBytes::new(py, key),)));
            if let Some(t) = maybe_tensor {
                result.constants.insert(*id, ScheduleConstant::Tensor(t));
            }
        });
        Ok(result)
    }
    #[pyo3(signature=(settings = Default::default()))]
    pub fn evaluate_many(&self, settings: OptimizationSettings) -> Result<Vec<Tensor>> {
        let timed = settings.verbose >= 1;
        let eval = || -> Result<_> {
            let v = if settings.adjust_numerical_scale {
                evaluate_schedule_adjust_numerical_scale(self, settings)
            } else {
                evaluate_schedule(self)
            }?;
            Ok(self
                .output_circuits
                .as_ref()
                .unwrap()
                .iter()
                .map(|(id, _)| v[id].clone())
                .collect())
        };
        Ok(timed!(eval()?, 10, timed))
    }

    // TODO: I think we can still panic on other non-explicitly computable stuff? (e.g., cumulants etc)
    pub fn check_no_syms(&self) -> Result<()> {
        let mut iter = self
            .constants
            .iter()
            .filter_map(|x| x.1.as_symbol())
            .peekable();
        if iter.peek().is_some() {
            bail!(SchedulingError::EvaluateCalledWithSyms {
                syms: iter.cloned().collect()
            })
        }
        Ok(())
    }
    pub fn check_no_raw_tensor_constants(&self) -> Result<()> {
        let mut iter = self
            .constants
            .iter()
            .filter_map(|x| x.1.as_tensor())
            .peekable();
        if iter.peek().is_some() {
            bail!("has raw tensor constant")
        }
        Ok(())
    }

    #[pyo3(signature=(settings = Default::default()))]
    pub fn evaluate(&self, settings: OptimizationSettings) -> Result<Tensor> {
        let many = self.evaluate_many(settings)?;
        if many.len() != 1 {
            bail!("Schedule.evaluate but schedule returned more than one tensor (did you mean to use evaluate_many?)")
        }
        Ok(many[0].clone())
    }

    pub fn get_stats(&self) -> ScheduleStats {
        let mut mem: BigUint = BigUint::from(0usize);
        let mut max_mem: BigUint = BigUint::from(0usize);
        let mut biggest: HashMap<usize, CircuitRc> = HashMap::default();
        let mut current: HashMap<usize, CircuitRc> = HashMap::default();
        for instruction in self.instructions.clone() {
            match instruction {
                Instruction::Drop(drop) => {
                    let dropped = current.remove(&drop).unwrap();
                    mem -= dropped.info().naive_mem_use(None);
                }
                Instruction::Compute(key, circuit) => {
                    current.insert(key, circuit.clone());
                    mem += circuit.info().naive_mem_use(None);
                    if mem > max_mem {
                        max_mem = mem.clone();
                        biggest = current.clone();
                    }
                }
            }
        }
        ScheduleStats {
            max_mem,
            constant_mem: self
                .constants
                .values()
                .map(|t| {
                    t.shape().iter().map(|x| x.unwrap()).product::<usize>()
                        * t.device_dtype().size()
                })
                .sum(),
            max_circuit_set: biggest.values().cloned().collect(),
        }
    }

    pub fn next_key(&self) -> usize {
        *self
            .constants
            .keys()
            .chain(self.scalars.keys())
            .chain(self.instructions.iter().filter_map(|ins| match ins {
                Instruction::Compute(k, _c) => Some(k),
                _ => None,
            }))
            .max()
            .unwrap_or(&0)
            + 1
    }

    pub fn serialize(&self) -> Result<String> {
        let tosend: ScheduleToSend = self.try_into()?;
        Ok(json::to_string(&tosend))
    }

    #[staticmethod]
    #[pyo3(name = "deserialize")]
    pub fn deserialize_py(string: String, tensor_cache: Option<TensorCacheRrfs>) -> Result<Self> {
        let mut tensor_cache = tensor_cache;
        Schedule::deserialize(string, &mut tensor_cache)
    }

    pub fn tosend(&self) -> Result<ScheduleToSend> {
        self.try_into()
    }

    pub fn evaluate_remote(&self, remote_url: String) -> Result<Tensor> {
        self.tosend()?.evaluate_remote(remote_url, TorchDevice::Cpu)
    }
    pub fn evaluate_remote_many(&self, remote_url: String) -> Result<Vec<Tensor>> {
        self.tosend()?
            .evaluate_remote_many(remote_url, TorchDevice::Cpu)
    }
    fn __repr__(&self) -> String {
        format!("{}", &self)
    }
}
impl Schedule {
    pub fn deserialize(string: String, tensor_cache: &mut Option<TensorCacheRrfs>) -> Result<Self> {
        let sent: ScheduleToSend =
            json::from_str(&string).context("schedule deserialization failed due to json error")?;
        sent.load(tensor_cache)
    }
}

impl Display for Schedule {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Schedule: instructions\n{}\nTensors: {} Arrays: {} Symbols: {} Scalars: {}",
            self.instructions
                .iter()
                .filter_map(|i| {
                    if let Instruction::Compute(k, c) = i {
                        return Some(
                            k.to_string()
                                + " "
                                + &c.variant_string()
                                + " "
                                + &format!("{:?}", c.info().device_dtype.dtype)
                                + " "
                                + &c.children()
                                    .map(|x| get_child_key(x).to_string())
                                    .collect::<Vec<String>>()
                                    .join(" "),
                        );
                    }
                    None
                })
                .collect::<Vec<String>>()
                .join("\n"),
            self.constants
                .iter()
                .filter_map(|(k, c)| c.as_tensor().map(|_| k.to_string()))
                .collect::<Vec<String>>()
                .join(" "),
            self.constants
                .iter()
                .filter_map(|(k, c)| c.as_array().map(|_| k.to_string()))
                .collect::<Vec<String>>()
                .join(" "),
            self.constants
                .iter()
                .filter_map(|(k, c)| c.as_symbol().map(|_| k.to_string()))
                .collect::<Vec<String>>()
                .join(" "),
            self.scalars
                .keys()
                .map(|k| k.to_string())
                .collect::<Vec<String>>()
                .join(" "),
        )
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct ScheduleStats {
    #[pyo3(get)]
    max_mem: BigUint,
    #[pyo3(get)]
    constant_mem: BigUint, // this has already been allocated so it can't be over 2^64
    #[pyo3(get)]
    max_circuit_set: HashSet<CircuitRc>,
}

static SCHEDULING_ERROR_NOTE: &'static str = "(see circuit_to_schedule docstring for tips)";

#[apply(python_error_exception)]
#[base_error_name(SchedulingOOM)]
#[base_exception(PyValueError)]
#[derive(Error, Clone, Debug)]
pub enum SchedulingOOMError {
    #[error("Schedule doesn't fit into max_memory={max_mem}, {stats} ({e_name}) {SCHEDULING_ERROR_NOTE}", max_mem=oom_fmt(*max_memory))]
    OverMemoryLimit {
        max_memory: usize,
        stats: ScheduleStats,
    },
    #[error("Single {} element doesn't fit max_single_tensor_memory={} max_memory={} {circuit:?} ({e_name})", oom_fmt(mem_usage.clone()), oom_fmt(*max_single_tensor_memory), oom_fmt(*max_memory))]
    Single {
        max_single_tensor_memory: usize,
        max_memory: usize,
        mem_usage: BigUint,
        circuit: CircuitRc,
    },
    #[error("Threading failed! bug! ({e_name})")]
    ThreadsLost {},
    #[error("BUG: Schedule exhaustive timed out, at size {size} iters {iters}. maybe your circuit is gigantic (exabytes mem usage)? ({e_name}) {SCHEDULING_ERROR_NOTE}")]
    ExhaustiveTimeout { iters: usize, size: usize },
}

#[apply(python_error_exception)]
#[base_error_name(Scheduling)]
#[base_exception(PyValueError)]
#[derive(Error, Debug)]
pub enum SchedulingError {
    #[error("circuit={circuit:?} ({e_name})")]
    NotExplicitlyComputable { circuit: CircuitRc },

    #[error("syms={syms:?} ({e_name})")]
    EvaluateCalledWithSyms { syms: Vec<Symbol> },
}

impl Display for ScheduleStats {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let shapes_and_percents = self
            .max_circuit_set
            .iter()
            .map(|x| (x.info().shape.clone(), x.info().naive_mem_use_usize(None)))
            .counts()
            .into_iter()
            .sorted_by_key(|((_, mem), count)| std::cmp::Reverse(count * mem))
            .map(|(x, c)| {
                format!(
                    "{c} {:?} {}%",
                    x.0,
                    // biguint doesn't have cast f64? that would be less lossy than truncate
                    ((x.1 * c) as f64 / self.max_mem.to_u64_digits()[0] as f64 * 100.0) as i64
                )
            })
            .collect::<Vec<String>>()
            .join(", ");
        let result = format!(
            "ScheduleStats: max: {} const: {} shapes: {}",
            oom_fmt(self.max_mem.clone()),
            oom_fmt(self.constant_mem.clone()),
            shapes_and_percents
        );
        write!(f, "{}", result)
    }
}

fn get_child_key(circuit: CircuitRc) -> usize {
    circuit
        .as_symbol()
        .unwrap()
        .info()
        .name
        .unwrap()
        .parse::<usize>()
        .unwrap()
}

fn child_from_key(key: usize, child: CircuitRc) -> Symbol {
    Symbol::new_device_dtype_random_uuid(
        child.info().shape.clone(),
        Some(key.to_string().into()),
        child.info().device_dtype,
    )
}

pub fn get_children_keys(circuit: CircuitRc) -> Vec<usize> {
    circuit.children().map(get_child_key).collect()
}

/// see https://pyo3.rs/main/doc/pyo3/marker/struct.python#method.new_pool
pub unsafe fn with_gil_pool<F, R>(f: F) -> R
where
    F: for<'py> FnOnce(Python<'py>) -> R,
{
    Python::with_gil(|py| {
        let pool = unsafe { py.new_pool() };
        let py = pool.python();
        f(py)
    })
}

pub fn evaluate_schedule(schedule: &Schedule) -> Result<HashMap<usize, Tensor>> {
    schedule.check_no_syms()?;
    let mut live: HashMap<usize, Tensor> = schedule
        .constants
        .iter()
        .map(|x| x.1.convert_as_tensor().map(|z| (*x.0, z.clone())))
        .collect::<Option<HashMap<_, _>>>()
        .unwrap();
    live.extend(
        schedule
            .scalars
            .iter()
            .map(|x| (*x.0, eval_tensors(&x.1.crc(), &[]).unwrap())),
    );
    for s in &schedule.instructions {
        let run = |_py: Python| match s {
            Instruction::Compute(key, circ) => {
                let child_keys: Vec<usize> = circ.children().map(get_child_key).collect();
                child_keys.iter().for_each(|child_key| {
                    if !live.contains_key(child_key) {
                        panic!("FAIL");
                    }
                });
                let tensors: Vec<Tensor> = child_keys
                    .iter()
                    .map(|child_key| live[child_key].clone())
                    .collect();
                let result_err = eval_tensors(circ, &tensors);
                if result_err.is_err() {
                    println!("errored evaluate");
                    circ.print().unwrap()
                }
                let result = result_err.unwrap();
                assert!(
                    result.shape() == circ.shape(),
                    "circ={:?}, result_shape={:?}",
                    circ,
                    result.shape()
                );
                live.insert(*key, result);
            }
            Instruction::Drop(key) => {
                live.remove(key);
            }
        };
        unsafe { with_gil_pool(run) }
    }
    Ok(live)
}

/// evaluate a circuit while measuring the numerical scale of tensor contents
/// and computing "10^10 * x" or such instead of x to avoid numerical overflow
pub fn evaluate_schedule_adjust_numerical_scale(
    schedule: &Schedule,
    settings: OptimizationSettings,
) -> Result<HashMap<usize, Tensor>> {
    schedule.check_no_syms()?;

    // we store (tensor, scale) where scale is a number the tensor's been multiplied by
    // so (tensor(1e10),1.0) evaluates to same as (tensor(1),1e-10)
    let mul = |tup: &(Tensor, f64), m: f64| -> (Tensor, f64) {
        Python::with_gil(|py| (tup.0.clone().py_mul(py, m).unwrap(), tup.1 * m))
    };
    let set_scale = |tup: &(Tensor, f64), new_scale: f64| -> (Tensor, f64) {
        Python::with_gil(|py| {
            (
                tup.0.clone().py_mul(py, new_scale / tup.1).unwrap(),
                new_scale,
            )
        })
    };
    let clamp = |tup: &(Tensor, f64)| -> (Tensor, f64) {
        let scale = tensor_scale(&tup.0).unwrap();
        if (scale > settings.numerical_scale_max || scale < settings.numerical_scale_min)
            && scale != 0.0
        {
            mul(tup, 1.0 / scale)
        } else {
            tup.clone()
        }
    };
    let uniformize = |tups: &Vec<(Tensor, f64)>| -> Vec<(Tensor, f64)> {
        if tups.is_empty() || tups.iter().all(|x| x.1 == tups[0].1) {
            tups.clone()
        } else {
            let new_scale: f64 = tups
                .iter()
                .map(|x| x.1)
                .reduce(|a, b| if a > b { a } else { b })
                .unwrap();
            tups.iter().map(|x| set_scale(x, new_scale)).collect()
        }
    };

    let mut live: HashMap<usize, (Tensor, f64)> = schedule
        .constants
        .iter()
        .map(|(key, x)| (*key, clamp(&(x.convert_as_tensor().unwrap().clone(), 1.0))))
        .collect();
    live.extend(schedule.scalars.iter().map(|(h, s)| {
        (*h, {
            let value_scale = s.value.abs();
            if value_scale > settings.numerical_scale_max
                || value_scale < settings.numerical_scale_min && value_scale != 0.0
            {
                (
                    scalar_to_tensor(s.value.signum(), s.info().shape.clone(), Default::default())
                        .unwrap(),
                    1.0 / value_scale,
                )
            } else {
                (
                    scalar_to_tensor(s.value, s.info().shape.clone(), Default::default()).unwrap(),
                    1.0,
                )
            }
        })
    }));
    for s in &schedule.instructions {
        let run = |_py: Python| match s {
            Instruction::Compute(key, circ) => {
                circ.children().for_each(|x: CircuitRc| {
                    if !live.contains_key(&get_child_key(x)) {
                        panic!("FAIL");
                    }
                });
                let tensors_and_scales: Vec<(Tensor, f64)> = circ
                    .children()
                    .map(|x| live[&get_child_key(x)].clone())
                    .collect();
                let tensors: Vec<Tensor> = tensors_and_scales.iter().map(|x| x.0.clone()).collect();
                let result = match &***circ {
                    Circuit::Einsum(_) => {
                        let new_scale = tensors_and_scales.iter().map(|x| x.1).product();
                        clamp(&(eval_tensors(circ, &tensors).unwrap(), new_scale))
                    }
                    Circuit::Add(_) | Circuit::Concat(_) => {
                        let new_ts = uniformize(&tensors_and_scales);
                        (
                            eval_tensors(
                                circ,
                                &new_ts.iter().map(|x| x.0.clone()).collect::<Vec<_>>(),
                            )
                            .unwrap(),
                            new_ts[0].1,
                        )
                    }
                    Circuit::GeneralFunction(_) => {
                        let new_ts: Vec<(Tensor, f64)> = tensors_and_scales
                            .iter()
                            .map(|x| set_scale(x, 1.0))
                            .collect();
                        clamp(&(
                            eval_tensors(
                                circ,
                                &new_ts.iter().map(|x| x.0.clone()).collect::<Vec<_>>(),
                            )
                            .unwrap(),
                            1.0,
                        ))
                    }
                    Circuit::Index(_) | Circuit::Rearrange(_) | Circuit::Scatter(_) => (
                        eval_tensors(
                            circ,
                            &tensors_and_scales
                                .iter()
                                .map(|x| x.0.clone())
                                .collect::<Vec<_>>(),
                        )
                        .unwrap(),
                        tensors_and_scales[0].1,
                    ),
                    Circuit::Scalar(_) | Circuit::Array(_) | Circuit::Symbol(_) => {
                        panic!("constant found as schedule instruction, not supposed to happen")
                    }
                    Circuit::Tag(_) => tensors_and_scales[0].clone(),
                    _ => {
                        unimplemented!()
                    }
                };
                assert!(result.0.shape()[..] == circ.info().shape[..]);
                live.insert(*key, result);
            }
            Instruction::Drop(hash) => {
                live.remove(hash);
            }
        };
        unsafe { with_gil_pool(run) }
    }
    let out = live
        .iter()
        .map(|(k, v)| (*k, set_scale(v, 1.0).0))
        .collect();
    Ok(out)
}

/// this supports dropping and recomputing. if you have an Evaluate(CircuitRc) of something you already evaluated
/// it's assumed you dropped this and are recomputing it
pub fn order_to_schedule(
    order: &Vec<CircuitRc>,
    constants: &Vec<IrreducibleNode>,
    scalars: &Vec<Scalar>,
    to_keep: &[HashBytes],
) -> (Schedule, Vec<usize>) {
    let to_keep_set: HashSet<HashBytes> = to_keep.iter().cloned().collect();
    let mut circ_to_id: HashMap<HashBytes, usize> = Default::default();
    let constants: HashMap<usize, _> = constants
        .iter()
        .map(|x| {
            circ_to_id.insert(x.info().hash, circ_to_id.len());
            (circ_to_id.len() - 1, x.clone())
        })
        .collect();
    let mut result: Schedule = Schedule {
        instructions: vec![],
        scalars: scalars
            .iter()
            .map(|x| {
                circ_to_id.insert(x.info().hash, circ_to_id.len());
                (circ_to_id.len() - 1, x.clone())
            })
            .collect(),
        output_circuits: None,
        old_constant_hashes: constants
            .iter()
            .map(|(id, node)| (node.info().hash, *id))
            .collect(),
        constants: constants
            .into_iter()
            .map(|(h, n)| (h, ScheduleConstant::Circ(n)))
            .collect(),
    };
    let mut seen_dependencies: HashSet<usize> = HashSet::default();
    for ex in order.iter().rev() {
        for child in ex.non_free_children() {
            let next_id = circ_to_id.len();
            let dep = *circ_to_id.entry(child.info().hash).or_insert(next_id);
            if !Leaf::matches(&child)
                && seen_dependencies.insert(dep)
                && !to_keep_set.contains(&child.info().hash)
            {
                result.instructions.push(Instruction::Drop(dep));
            }
        }
        let next_id = circ_to_id.len();
        let our_id = *circ_to_id.entry(ex.info().hash).or_insert(next_id);
        let node_here_symbol_children = (**ex.map_non_free_children_unwrap(|child| {
            child_from_key(circ_to_id[&child.info().hash], child).rc()
        }))
        .clone()
        .rc();
        result
            .instructions
            .push(Instruction::Compute(our_id, node_here_symbol_children));
        // seen_dependencies.remove(&ex.info().hash);
    }
    result.instructions.reverse();
    (result, to_keep.iter().map(|x| circ_to_id[x]).collect())
}

pub fn circuit_to_dag(circuit: CircuitRc) -> Dag {
    let mut result: Dag = Default::default();
    let mut to_merge_with_child: Vec<u32> = vec![];
    // append the circuit to the dag if it's not already there, and return its index
    let number_node = |c: CircuitRc, result: &mut Dag, to_merge_with_child: &mut Vec<u32>| -> u32 {
        if let Some(idx) = result.hash_to_node.get(&c.info().hash) {
            return *idx as u32;
        }
        result.node_costs.push(c.info().naive_mem_use_usize(None));
        result.node_hashes.push(c.info().hash);
        result
            .hash_to_node
            .insert(c.info().hash, result.node_hashes.len() - 1);
        result.children.push(sv![]);
        result.parents.push(sv![]);
        let output = (result.node_hashes.len() - 1) as u32;

        if is_definitely_view_on_child(c) {
            to_merge_with_child.push(output)
        }
        output
    };
    // non free so we avoid recuring into module spec.circuit
    visit_circuit_non_free(
        circuit,
        |c: CircuitRc| {
            // Arrays are never added to the dag to begin with because they're always 0 cost

            if !c.is_leaf() {
                let my_number: u32 = number_node(c.clone(), &mut result, &mut to_merge_with_child);

                let children_to_consider: Vec<CircuitRc> = c
                    .non_free_children()
                    .filter(|child| !Leaf::matches(child))
                    .collect();
                result.children[my_number as usize] = children_to_consider
                    .iter()
                    .map(|child| number_node(child.clone(), &mut result, &mut to_merge_with_child))
                    .unique()
                    .collect();
                for child in children_to_consider {
                    let new_num = number_node(child.clone(), &mut result, &mut to_merge_with_child);
                    if !result.parents[new_num as usize]
                        .iter()
                        .contains(&(my_number as u32))
                    {
                        result.parents[new_num as usize].push(my_number as u32);
                    }
                }
            }

            Ok(())
        },
        false,
    )
    .unwrap();
    result.node_to_orig = (0..result.node_costs.len() as u32)
        .map(|x| (x, sv![x]))
        .collect();
    for tmp in to_merge_with_child {
        assert!(result.children[tmp as usize].len() < 2);
        if result.children[tmp as usize].len() == 1 {
            result.merge_larger(result.children[tmp as usize][0], tmp, false)
        }
    }
    result
}

pub fn circuit_to_schedule(
    circuit: CircuitRc,
    context: &mut OptimizationContext,
) -> Result<Schedule> {
    // we could avoid this if we wanted, but a bit annoying
    // (requires handle rearrange due to unused arg + empty instruction case!)
    let circuit = deep_module_remove_unused_inputs(
        circuit,
        &mut context.cache.module_removed_unused,
        true,
        true,
        true,
    );
    let circuit = conform_all_modules(circuit);
    if is_python_running() && any_children_with_symbolic_sizes(circuit.clone()) {
        Python::with_gil(|py| {
            pyo3::PyErr::warn(
                py,
                PY_UTILS.optimizing_symbolic_size_warning.as_ref(py),
                concat!("you're scheduling with symbolic sizes. This is not recommended!",),
                1,
            )
        })?;
    }
    if is_python_running() && any_modules(circuit.clone()) {
        Python::with_gil(|py| {
            pyo3::PyErr::warn(
                py,
                PY_UTILS.optimizing_modules_warning.as_ref(py),
                "you're scheduling a circuit with modules. this is currently buggy, you might want to substitute_all_modules first",
                1,
            )
        })?;
    }

    if let Some((circ, mem)) = biggest_non_leaf(circuit.clone()) && mem > BigUint::from(context.settings.max_single_tensor_memory.min(context.settings.max_memory))
    {
        bail!(SchedulingOOMError::Single {
            max_single_tensor_memory: context.settings.max_single_tensor_memory,
            max_memory: context.settings.max_memory,
            mem_usage: max_non_leaf_size(circuit.clone()),
            circuit: circ
        });
    }
    let mut dag = circuit_to_dag(circuit.clone());
    let order_result = {
        let mut dag_simp_settings: DagSimpSettings = Default::default();
        dag_simp_settings.verbose = context.settings.verbose;
        dag_simp_settings.parallelism = context.settings.optimization_parallelism;
        dag_simp_settings.exhaustive_give_up_ns = context.settings.scheduling_timeout * 1_000_000;
        dag_simp_settings.mem_limit = context.settings.max_memory;
        if context.settings.scheduling_simplify {
            timed!(
                dag.simplify(&dag_simp_settings)?,
                10,
                context.settings.verbose >= 2
            );
        }
        timed!(
            dag.compute_schedule(&dag_simp_settings),
            10,
            context.settings.verbose >= 2
        )
    };
    let order = with_context_failable(order_result, || {
        Ok(format!("getting schedule failed for circuit:\n{circuit:?}",))
    })?;

    let to_node = hash_to_node_non_free(circuit.clone(), false);
    let mut circuit_order: Vec<CircuitRc> = order
        .iter()
        .map(|x| to_node[&dag.node_hashes[*x as usize]].clone())
        .collect();

    let circuits = if let Circuit::GeneralFunction(g) = &**circuit
                   && let GeneralFunctionSpec::Output(_) = g.spec {
        circuit_order.pop();
        g.children_sl().to_vec()
    } else {
        vec![circuit.clone()]
    };
    let (mut out, kept_keys) = order_to_schedule(
        &circuit_order,
        &to_node
            .iter()
            .filter_map(|x| Option::<IrreducibleNode>::from(arc_ref_clone(x.1)))
            .collect(),
        &to_node
            .iter()
            .filter_map(|x| x.1.as_scalar().cloned())
            .collect(),
        &circuits.iter().map(|x| x.info().hash).collect::<Vec<_>>(),
    );
    out.output_circuits = Some(zip(kept_keys, circuits.clone()).collect());
    let out = replace_module_schedules(&out, context)?;
    out.validate(true)?;
    let stats = out.get_stats();
    // scheduling simplify & exhaustive currently overestimates mem usage by a lot (todo debug?), so we currently don't error during scheduling & just recheck & error here. also this is nice since it tells user schedule memory usage & takes modules into account!
    if stats.max_mem > context.settings.max_memory.into() {
        bail!(SchedulingOOMError::OverMemoryLimit {
            max_memory: context.settings.max_memory,
            stats: stats
        })
    }
    Ok(out)
}

pub fn circuit_to_schedule_naive_toposort(circuit: CircuitRc) -> Result<Schedule> {
    let circuit = substitute_all_modules(circuit);
    let toposorted = toposort_circuit(circuit.clone());
    let mut order = Vec::new();
    let mut scalars = Vec::new();
    let mut constants = Vec::new();

    for c in toposorted {
        if let Some(sc) = c.as_scalar() {
            scalars.push(sc.clone())
        } else if let Some(constant) = Option::<IrreducibleNode>::from(c.clone().c()) {
            constants.push(constant)
        } else {
            order.push(c)
        }
    }

    let circuits = if let Circuit::GeneralFunction(g) = &**circuit
                   && let GeneralFunctionSpec::Output(_) = g.spec {
        order.pop();
        g.children_sl().to_vec()
    } else {
        vec![circuit]
    };
    let (mut result, kept_keys) = order_to_schedule(
        &order,
        &constants,
        &scalars,
        &circuits.iter().map(|x| x.info().hash).collect::<Vec<_>>(),
    );
    result.output_circuits = Some(zip(kept_keys, circuits).collect());
    result.validate(true).expect("should be valid");
    Ok(result)
}

pub fn schedule_out_many(circuits: Vec<CircuitRc>) -> CircuitRc {
    GeneralFunction::try_new(
        circuits,
        GeneralFunctionSpec::Output(GeneralFunctionOutputSpec()),
        None,
    )
    .unwrap()
    .crc()
}

#[pyfunction]
pub fn scheduled_evaluate(circuit: CircuitRc, settings: OptimizationSettings) -> Result<Tensor> {
    let schedule = if settings.scheduling_naive {
        circuit_to_schedule_naive_toposort(circuit)
    } else {
        circuit_to_schedule(
            circuit.clone(),
            &mut OptimizationContext::new_settings(settings.clone()),
        )
    }?;
    schedule.evaluate(settings)
}

#[pyfunction]
pub fn scheduled_evaluate_naive(circuit: CircuitRc) -> Result<Tensor> {
    let schedule = circuit_to_schedule_naive_toposort(circuit)?;
    schedule.evaluate(Default::default())
}

#[pyfunction]
#[pyo3(name = "circuit_to_schedule")]
pub fn py_circuit_to_schedule(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    circuit_to_schedule(circuit, &mut OptimizationContext::new_settings(settings))
}

#[pyfunction]
#[pyo3(name = "circuit_to_schedule_many")]
pub fn py_circuit_to_schedule_many(
    circuits: Vec<CircuitRc>,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    py_circuit_to_schedule(schedule_out_many(circuits), settings)
}

fn schedule_module_spec(spec: &ModuleSpec, context: &mut OptimizationContext) -> Result<Schedule> {
    context
        .cache
        .module_specs_scheduled_same_settings
        .get(spec)
        .cloned()
        .map_or_else(
            || {
                let result = circuit_to_schedule(spec.circuit.clone(), context)?;
                context
                    .cache
                    .module_specs_scheduled_same_settings
                    .insert(spec.clone(), result.clone());
                Ok(result)
            },
            |x| Ok(x),
        )
}

/// note: this doesn't allow for any tensors in constants
fn replace_module_schedules(
    schedule: &Schedule,
    context: &mut OptimizationContext,
) -> Result<Schedule> {
    let mut result = schedule.clone();
    let mut scalar_to_id: HashMap<Scalar, usize> = schedule
        .scalars
        .iter()
        .map(|(a, b)| (b.clone(), *a))
        .collect();
    let mut irreducible_to_id: HashMap<IrreducibleNode, usize> = schedule
        .constants
        .iter()
        .map(|(a, b)| (unwrap!(b, ScheduleConstant::Circ).clone(), *a))
        .collect();
    result.instructions = vec![];
    let mut next_key = schedule.next_key();
    for ins in &schedule.instructions {
        match ins {
            Instruction::Drop(_d) => result.instructions.push(ins.clone()),
            Instruction::Compute(outermost_k, v) => match &***v {
                Circuit::Module(mn) => {
                    mn.spec
                        .check_all_inputs_used()
                        .expect("unused args removed at start of circuit_to_schedule!");

                    let original_children: Vec<usize> =
                        mn.args().cloned().map(get_child_key).collect();

                    let inner_schedule = schedule_module_spec(&mn.spec, context)
                        .with_context(|| format!("while scheduling Module spec {mn:?}"))?;
                    let mut inner_to_outer_key = HashMap::default();
                    for (inner_k, sc) in &inner_schedule.scalars {
                        let outer = scalar_to_id.get(sc).cloned().unwrap_or_else(|| {
                            let this_key = next_key;
                            scalar_to_id.insert(sc.clone(), this_key);
                            result.scalars.insert(this_key, sc.clone());
                            next_key += 1;
                            this_key
                        });
                        inner_to_outer_key.try_insert(*inner_k, outer).unwrap();
                    }
                    for (inner_k, irreducible) in &inner_schedule.constants {
                        let irreducible = unwrap!(irreducible, ScheduleConstant::Circ);
                        let outer =
                            irreducible_to_id
                                .get(irreducible)
                                .cloned()
                                .unwrap_or_else(|| {
                                    if let Some(pos) =
                                        mn.spec.arg_specs.iter().position(|argspec| {
                                            argspec.symbol.info().hash == irreducible.info().hash
                                        })
                                    {
                                        original_children[pos]
                                    } else {
                                        let this_key = next_key;
                                        irreducible_to_id.insert(irreducible.clone(), this_key);
                                        result.constants.insert(
                                            this_key,
                                            ScheduleConstant::Circ(irreducible.clone()),
                                        );
                                        assert!(result
                                            .old_constant_hashes
                                            .insert(irreducible.info().hash, this_key)
                                            .is_none());
                                        next_key += 1;
                                        this_key
                                    }
                                });
                        inner_to_outer_key.try_insert(*inner_k, outer).unwrap();
                    }

                    assert!(
                        !inner_schedule.instructions.is_empty(),
                        "empty_modules removed at start of circuit to schedule"
                    );

                    inner_to_outer_key
                        .try_insert(
                            inner_schedule
                                .output_circuits
                                .unwrap()
                                .iter()
                                .exactly_one()
                                .unwrap()
                                .0,
                            *outermost_k,
                        )
                        .unwrap();

                    for inner_ins in &inner_schedule.instructions {
                        match inner_ins {
                            Instruction::Drop(drop) => {
                                result
                                    .instructions
                                    .push(Instruction::Drop(inner_to_outer_key[drop]));
                            }
                            Instruction::Compute(inner_k, c) => {
                                assert!(!c.is_module());
                                let new_c = c
                                    .map_children_unwrap(|child| {
                                        let child_inner_k = get_child_key(child.clone());
                                        let child_outer_k =
                                            inner_to_outer_key.get(&child_inner_k).unwrap();
                                        child_from_key(*child_outer_k, child).rc()
                                    })
                                    .rc();
                                let key =
                                    inner_to_outer_key.get(inner_k).cloned().unwrap_or_else(|| {
                                        let this_key = next_key;
                                        inner_to_outer_key.insert(*inner_k, this_key);
                                        next_key += 1;
                                        this_key
                                    });
                                result.instructions.push(Instruction::Compute(key, new_c));
                                inner_to_outer_key.insert(*inner_k, key);
                            }
                        }
                    }
                }
                // Note: if other node types have free we'd have to handle that here!
                _ => {
                    result.instructions.push(ins.clone());
                }
            },
        }
    }
    result.validate(result.output_circuits.is_some())?;

    Ok(result)
}
