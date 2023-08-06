use std::{collections::BTreeSet, hash::Hash, iter::zip};

use anyhow::{bail, Result};
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::prelude::*;
use rr_util::{
    cached_lambda,
    py_types::{Tensor, SELF_MODULE},
    pycallable,
    tensor_util::{TorchDeviceDtype, TorchDeviceDtypeOp},
    util::HashBytes,
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use crate::{Circuit, CircuitNode, CircuitRc};

pub fn evaluate(circ: CircuitRc) -> Result<Tensor> {
    Python::with_gil(|py| {
        Ok(SELF_MODULE
            .call_method1(py, "scheduled_evaluate_naive", (circ,))?
            .extract(py)?)
    })
}

pub fn check_combine_evaluate_device_dtype(
    circ: CircuitRc,
    device_dtype: TorchDeviceDtypeOp,
) -> Result<TorchDeviceDtype> {
    if device_dtype
        .dtype
        .map(|x| !x.is_floating_point())
        .unwrap_or(false)
    {
        bail!("evaluate dtype is used for scalars and other base cases and must be floating point");
    }
    let out = TorchDeviceDtypeOp {
        device: device_dtype.device.or(circ.info().device_dtype.device),
        dtype: device_dtype
            .dtype
            .or(circ.info().device_dtype.only_keep_floating().dtype),
    }
    .unwrap_or_defaults();
    Ok(out)
}

#[pyfunction]
pub fn total_flops(circuit: CircuitRc) -> BigUint {
    let mut result = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        result += x.self_flops();
    });
    result
}

#[pyfunction]
pub fn total_arrayconstant_size(circuit: CircuitRc) -> BigUint {
    let mut result: BigUint = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        if let Circuit::Array(x) = &**x {
            result += x.info().numel();
        }
    });
    result
}

#[pyfunction]
pub fn count_nodes(circuit: CircuitRc) -> usize {
    let mut result: usize = 0;
    visit_circuit_unwrap(circuit, &mut |_x: CircuitRc| {
        result += 1;
    });
    result
}

#[apply(pycallable)]
#[pyo3(name = "deep_map")]
pub fn deep_map<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let inner_mapped = circ.map_children(&mut recurse)?.rc();
        f(inner_mapped)
    }
    recurse(circuit)
}

#[apply(pycallable)]
#[pyo3(name = "deep_map_preorder")]
pub fn deep_map_preorder<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        f(circ)?.map_children(&mut recurse).map(|z| z.rc())
    }
    recurse(circuit)
}

pub fn visit_circuit_with_parents<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>),
{
    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();

    for (_i, sub) in toposort_circuit(circuit).into_iter().rev().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]));
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
}

pub fn visit_circuit_with_parents_fallible<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>) -> Result<()>,
{
    let mut toposorted = toposort_circuit(circuit);
    toposorted.reverse(); // its children first by default

    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();
    for (_i, sub) in toposorted.into_iter().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]))?;
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
    Ok(())
}

/// does not visit children of circuits where f fails. It does visit all children even if one fails
/// even though this is more work than stopping on the first child that fails
/// because it's semantically cleaner to not have to think about which children are first
pub fn visit_circuit_non_free<F>(circuit: CircuitRc, f: F, recur_into_free: bool) -> Result<()>
where
    F: FnMut(CircuitRc) -> Result<()>,
{
    let mut f = f;
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(
        circ: &CircuitRc,
        seen: &mut HashSet<HashBytes>,
        f: &mut F,
        recur_into_free: bool,
    ) -> Result<()>
    where
        F: FnMut(CircuitRc) -> Result<()>,
    {
        if seen.insert(circ.info().hash) {
            f(circ.clone())?;

            let children = if recur_into_free {
                circ.children_sl()
            } else {
                circ.non_free_children_sl()
            };
            children
                .iter()
                .map(|child| recurse(child, seen, f, recur_into_free))
                .collect::<Vec<_>>() // intermediate collect causes all recurses to happen even if one errors
                .into_iter()
                .collect::<Result<Vec<_>, _>>()?;
        }
        Ok(())
    }
    recurse(&circuit, &mut seen, &mut f, recur_into_free)
}

#[apply(pycallable)]
#[pyo3(name = "visit_circuit")]
pub fn visit_circuit<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut((circuit, CircuitRc)) -> Result<()>,
{
    visit_circuit_non_free(circuit, f, true)
}

pub fn visit_circuits_stoppable<F>(circuits: &[CircuitRc], f: F)
where
    F: FnMut(CircuitRc) -> bool,
{
    let mut f = f;
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(circ: CircuitRc, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(CircuitRc) -> bool,
    {
        if seen.insert(circ.info().hash) {
            if f(circ.clone()) {
                return;
            }

            circ.children().for_each(|c| recurse(c, seen, f))
        }
    }
    for circuit in circuits {
        recurse(circuit.clone(), &mut seen, &mut f)
    }
}

#[pyfunction]
pub fn all_children(circuit: CircuitRc) -> HashSet<CircuitRc> {
    let mut seen: HashSet<CircuitRc> = HashSet::default();
    fn recurse(circ: CircuitRc, seen: &mut HashSet<CircuitRc>) {
        if seen.insert(circ.clone()) {
            for child in circ.children() {
                recurse(child, seen)
            }
        }
    }
    recurse(circuit, &mut seen);
    seen
}

pub fn visit_circuit_postorder<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc),
{
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(circ: CircuitRc, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(CircuitRc),
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            for child in circ.children() {
                recurse(child, seen, f)
            }
            f(circ);
        }
    }
    recurse(circuit, &mut seen, &mut f);
}

pub fn deep_map_op<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let inner_mapped = circ.map_children_op(&mut recurse).map(|z| z.rc());
        inner_mapped
            .map(|x| f(x.clone()).unwrap_or(x))
            .or_else(|| f(circ))
    }
    recurse(circuit)
}

pub fn deep_map_pre_new_children<F>(circuit: CircuitRc, f: F) -> CircuitRc
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> CircuitRc {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children = old_children.into_iter().map(recurse).collect();
        f(circ, &new_children)
    }
    recurse(circuit)
}

pub fn deep_map_op_pre_new_children<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children_sl().to_vec();
        let new_children: Vec<Option<CircuitRc>> =
            old_children.iter().cloned().map(recurse).collect();
        if new_children.iter().all(|x| x.is_none()) {
            f(circ, &old_children)
        } else {
            let new_real_children = zip(old_children, new_children)
                .map(|(old, new)| new.unwrap_or(old))
                .collect();
            Some(
                f(circ.clone(), &new_real_children)
                    .unwrap_or_else(|| circ.replace_children(new_real_children).unwrap().rc()),
            )
        }
    }
    recurse(circuit)
}

pub fn deep_map_fallible_pre_new_children<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children_sl().to_vec(); // need to define this for borrow reasons
        let new_children: Result<Vec<CircuitRc>> = old_children.into_iter().map(recurse).collect();
        new_children.and_then(|a| f(circ, &a))
    }
    recurse(circuit)
}

pub fn apply_fn_cache<I, K, O, F, FK>(i: &I, f: F, c: &mut HashMap<K, O>, fk: FK) -> O
where
    F: Fn(&I) -> O,
    FK: Fn(&I) -> K,
    O: Clone,
    K: Eq + Hash,
{
    let k = fk(i);
    match c.get(&k) {
        Some(r) => r.clone(),
        None => {
            let r = f(i);
            c.insert(k, r.clone());
            r
        }
    }
}

pub fn deep_map_op_context<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> Option<CircuitRc>,
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let inner_mapped = circuit.map_children_op(|x| deep_map_op_context(x, f, context, self_cache));
    let result = match inner_mapped {
        Some(z) => f(z.crc(), context).or(Some(z.rc())),
        None => f(circuit.clone(), context),
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn deep_map_op_context_preorder_stoppable<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> (Option<CircuitRc>, bool),
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let (circuit_applied, stop) = f(circuit.clone(), context);
    if stop {
        return circuit_applied;
    }
    let result = if let Some(applied) = circuit_applied {
        Some(
            applied
                .map_children_op(|x| {
                    deep_map_op_context_preorder_stoppable(x, f, context, self_cache)
                })
                .map(|x| x.rc())
                .unwrap_or(applied),
        )
    } else {
        circuit
            .map_children_op(|x| deep_map_op_context_preorder_stoppable(x, f, context, self_cache))
            .map(|x| x.rc())
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn deep_map_pass_down_branching<F, F2, T>(
    circuit: CircuitRc,
    pass_down_f: F,
    make_circuit_f: F2,
    initial_pass_down: T,
) -> CircuitRc
where
    T: Hash + Eq + Clone,
    F: Fn(CircuitRc, &T) -> Vec<T>,
    F2: Fn(CircuitRc, &T, &Vec<CircuitRc>) -> CircuitRc,
{
    let mut pass_down_cache: HashMap<(CircuitRc, T), Vec<T>> = HashMap::default();
    let mut construct_cache: HashMap<(CircuitRc, T), CircuitRc> = HashMap::default();

    fn recurse<F, F2, T>(
        circuit: CircuitRc,
        passed: T,
        pdf: &F,
        mcf: &F2,
        pdc: &mut HashMap<(CircuitRc, T), Vec<T>>,
        cc: &mut HashMap<(CircuitRc, T), CircuitRc>,
    ) -> CircuitRc
    where
        T: Hash + Eq + Clone,
        F: Fn(CircuitRc, &T) -> Vec<T>,
        F2: Fn(CircuitRc, &T, &Vec<CircuitRc>) -> CircuitRc,
    {
        let pass_key = (circuit.clone(), passed.clone());
        if let Some(result) = cc.get(&pass_key) {
            return result.clone();
        }
        let passing = pdc.get(&pass_key).cloned().unwrap_or_else(|| {
            let result = pdf(circuit.clone(), &passed);
            pdc.insert(pass_key.clone(), result.clone());
            result
        });
        let new_children: Vec<CircuitRc> = zip(circuit.children(), passing)
            .map(|(child, pass)| recurse(child, pass, pdf, mcf, pdc, cc))
            .collect();

        let result = mcf(circuit, &passed, &new_children);
        cc.insert(pass_key, result.clone());
        result
    }
    recurse(
        circuit,
        initial_pass_down,
        &pass_down_f,
        &make_circuit_f,
        &mut pass_down_cache,
        &mut construct_cache,
    )
}

#[pyfunction]
/// children first
pub fn toposort_circuit(circuit: CircuitRc) -> Vec<CircuitRc> {
    let mut num_refs: HashMap<CircuitRc, usize> = HashMap::default();
    visit_circuit_unwrap(circuit.clone(), |c| {
        for child in c.children() {
            *num_refs.entry(child).or_insert(0) += 1;
        }
    });
    let mut ready: BTreeSet<CircuitRc> = BTreeSet::from([circuit]);
    let mut result: Vec<CircuitRc> = vec![];
    while let Some(here) = ready.pop_first() {
        for child in here.children() {
            num_refs.insert(child.clone(), num_refs[&child] - 1);
            if num_refs[&child] == 0 {
                ready.insert(child);
            }
        }
        result.push(here.clone())
    }
    result.reverse();
    result
}
