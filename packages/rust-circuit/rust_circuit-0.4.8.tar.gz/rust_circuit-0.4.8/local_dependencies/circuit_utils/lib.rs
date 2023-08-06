mod set_of_circuits;

use std::{collections::BTreeSet, iter::zip};

use circuit_base::{
    circuit_utils::{
        apply_fn_cache, deep_map_op_context_preorder_stoppable, deep_map_op_pre_new_children,
        deep_map_preorder_unwrap, deep_map_unwrap, visit_circuit_non_free, visit_circuit_unwrap,
        visit_circuits_stoppable,
    },
    toposort_circuit, Array, Circuit, CircuitNode, CircuitRc, Index,
};
use itertools::izip;
use num_bigint::BigUint;
use pyo3::{prelude::*, types::PyModule, wrap_pyfunction, PyResult};
use rr_util::{
    tensor_util::{TensorAxisIndex, TensorIndex, TorchDeviceDtype, TorchDtype},
    util::HashBytes,
    IndexSet,
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
pub use set_of_circuits::SetOfCircuitIdentities;

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cast_circuit, m)?)?;
    m.add_function(wrap_pyfunction!(replace_all_randn_seeded, m)?)?;
    m.add_function(wrap_pyfunction!(replace_nodes_py, m)?)?;

    m.add_class::<SetOfCircuitIdentities>()?;

    Ok(())
}

#[pyfunction]
#[pyo3(name = "replace_nodes")]
pub fn replace_nodes_py(circuit: CircuitRc, map: HashMap<CircuitRc, CircuitRc>) -> CircuitRc {
    deep_map_preorder_unwrap(circuit, |x: CircuitRc| -> CircuitRc {
        map.get(&x).cloned().unwrap_or(x)
    })
}

#[pyfunction]
pub fn cast_circuit(
    circ: CircuitRc,
    device_dtype: &rr_util::tensor_util::TorchDeviceDtypeOp,
) -> CircuitRc {
    deep_map_op_pre_new_children(
        circ.clone(),
        |circ, children: &Vec<CircuitRc>| match &**circ {
            Circuit::Array(node) => {
                if (*device_dtype)
                    .combine(node.value.device_dtype().into())
                    .is_err()
                {
                    Some(Array::nrc(
                        device_dtype.cast_tensor(node.value.clone()),
                        node.info().name,
                    ))
                } else {
                    None
                }
            }
            Circuit::Index(node) => {
                if node
                    .index
                    .0
                    .iter()
                    .any(|x| matches!(x, TensorAxisIndex::Tensor(_)))
                {
                    Some(Index::nrc(
                        children[0].clone(),
                        TensorIndex(
                            node.index
                                .0
                                .iter()
                                .map(|idx| match idx {
                                    TensorAxisIndex::Tensor(tensor) => TensorAxisIndex::Tensor(
                                        TorchDeviceDtype {
                                            device: device_dtype
                                                .device
                                                .unwrap_or(tensor.device_dtype().device),
                                            dtype: TorchDtype::int64,
                                        }
                                        .cast_tensor((**tensor).clone())
                                        .try_into()
                                        .unwrap(),
                                    ),
                                    _ => idx.clone(),
                                })
                                .collect(),
                        ),
                        node.info().name,
                    ))
                } else {
                    None
                }
            }
            _ => None,
        },
    )
    .unwrap_or(circ)
}

pub fn hash_to_node_non_free(
    circuit: CircuitRc,
    recur_into_free: bool,
) -> HashMap<HashBytes, CircuitRc> {
    let mut result: HashMap<HashBytes, CircuitRc> = HashMap::default();
    visit_circuit_non_free(
        circuit,
        &mut |x: CircuitRc| {
            result.insert(x.info().hash, x.clone());
            Ok(())
        },
        recur_into_free,
    )
    .unwrap();
    result
}

pub fn hash_to_node(circuit: CircuitRc) -> HashMap<HashBytes, CircuitRc> {
    hash_to_node_non_free(circuit, true)
}

#[pyfunction]
pub fn sum_of_node_sizes(circuit: CircuitRc) -> BigUint {
    let mut result: BigUint = BigUint::from(0usize);
    visit_circuit_unwrap(circuit, &mut |x: CircuitRc| {
        if !matches!(&**x, Circuit::Array(_)) {
            result += x.info().numel();
        }
    });
    result
}

pub fn sum_of_node_sizes_cached(
    circuit: CircuitRc,
    cache: &mut HashMap<HashBytes, BigUint>,
) -> BigUint {
    apply_fn_cache(
        &circuit,
        |x| sum_of_node_sizes(x.clone()),
        cache,
        |x| x.info().hash,
    )
}

#[pyfunction]
pub fn get_leaves(circuit: CircuitRc) -> Vec<CircuitRc> {
    let mut result: Vec<CircuitRc> = vec![];
    visit_circuit_unwrap(circuit, &mut |c: CircuitRc| {
        if c.num_children() == 0 {
            result.push(c);
        }
    });
    result
}

struct Parents {
    map: HashMap<CircuitRc, Vec<CircuitRc>>,
}

impl Parents {
    fn new() -> Self {
        Self {
            map: HashMap::default(),
        }
    }
    fn add(&mut self, c: CircuitRc) {
        if self.map.contains_key(&c) {
            return;
        }
        for ch in c.children() {
            self.add(ch.clone());
            self.map.entry(ch).or_insert(vec![]).push(c.clone());
        }
    }
    fn remove(&mut self, c: CircuitRc) {
        assert!(!self.map.contains_key(&c));
        for ch in c.children() {
            let v = self.map.get_mut(&ch).unwrap();
            v.swap_remove(v.iter().position(|a| *a == c).unwrap());
            if v.is_empty() {
                self.map.remove(&ch);
                self.remove(ch);
            }
        }
    }
    fn replace(&mut self, x: &CircuitRc, y: &CircuitRc) {
        if x == y {
            return;
        }
        let p = self.map.remove(x).unwrap_or(vec![]);
        self.map.entry(y.clone()).or_insert(vec![]).extend(p);
        self.add(y.clone());
        self.remove(x.clone());
    }
    fn get(&mut self, x: &CircuitRc) -> &Vec<CircuitRc> {
        static EMPTY_VEC: Vec<CircuitRc> = vec![];
        self.map.get(x).unwrap_or(&EMPTY_VEC)
    }
}

// only supports f replacing circuits already seen (e.g. arg/parents of arg), otherwise order might be wrong
// replacements are also visited, but nodes that are dead after replacements aren't
// a circuit will be visited multiple times if its parents change after it's first visited
pub fn visit_circuit_topoorder_replace<F>(circuit: CircuitRc, mut f: F) -> CircuitRc
where
    F: FnMut(CircuitRc) -> Option<Vec<(CircuitRc, CircuitRc)>>,
{
    struct Refcounts {
        map: HashMap<CircuitRc, usize>,
        dead: HashSet<CircuitRc>,
    }

    impl Refcounts {
        fn new() -> Self {
            Self {
                map: HashMap::default(),
                dead: HashSet::default(),
            }
        }
        fn inc(&mut self, c: CircuitRc) {
            *self.map.entry(c.clone()).or_insert(0) += 1;
            if self.map[&c] != 1 {
                return;
            }
            self.dead.remove(&c);
            for ch in c.children() {
                self.inc(ch.clone())
            }
        }
        fn dec(&mut self, c: CircuitRc) {
            assert!(self.map[&c] > 0);
            *self.map.get_mut(&c).unwrap() -= 1;
            if self.map[&c] == 0 {
                self.map.remove(&c);
                for ch in c.children() {
                    self.dec(ch)
                }
                self.dead.insert(c);
            }
        }
    }

    fn toposort(queue: &mut IndexSet<CircuitRc>, circs: &Vec<CircuitRc>) {
        let mut num_refs: HashMap<CircuitRc, usize> = HashMap::default();

        visit_circuits_stoppable(circs, |c| {
            if queue.contains(&c) {
                return true;
            }
            for ch in c.children() {
                if !queue.contains(&ch) {
                    *num_refs.entry(ch).or_insert(0) += 1;
                }
            }
            false
        });
        let mut ready: BTreeSet<CircuitRc> = circs
            .iter()
            .filter(|x| !queue.contains(*x))
            .cloned()
            .collect();
        let mut result: Vec<CircuitRc> = vec![];
        while let Some(here) = ready.pop_first() {
            for child in here.children() {
                if let Some(&r) = num_refs.get(&child) {
                    num_refs.insert(child.clone(), r - 1);
                    if r == 1 {
                        ready.insert(child);
                    }
                }
            }
            result.push(here)
        }
        queue.extend(result.into_iter().rev())
    }

    let mut queue: IndexSet<CircuitRc> = IndexSet::default();
    let mut refcounts = Refcounts::new();
    toposort(&mut queue, &vec![circuit.clone()]);
    refcounts.inc(circuit.clone());

    let mut replacements: HashMap<CircuitRc, CircuitRc> = HashMap::default();
    while let Some(a) = queue.pop() {
        if refcounts.dead.contains(&a) {
            continue;
        }
        if let Some(repl) = f(a.clone()) {
            // valid bc only replace nodes that we've already hit in toposort order and
            // nodes are either new = can't be referenced by nodes already in queue, or existing = already in queue
            toposort(&mut queue, &repl.iter().map(|(_, b)| b).cloned().collect());
            for (x, y) in repl {
                replacements.insert(x.clone(), y.clone());
                refcounts.inc(y);
                refcounts.dec(x);
            }
        }
    }
    // refcounts.dead.iter().for_each(|d| {
    //     replacements.remove(d);
    // });
    // assert!(replacements.is_empty());
    // assert!(all_children(out.clone())
    //     .iter()
    //     .all(|c| !refcounts.dead.contains(c)));
    deep_map_op_context_preorder_stoppable(
        circuit.clone(),
        &|c, rs: &mut HashMap<CircuitRc, CircuitRc>| (rs.remove(&c), false),
        &mut replacements,
        &mut HashMap::default(),
    )
    .unwrap_or(circuit)
}

pub fn deep_replace_parents_fix<F>(circuit: CircuitRc, mut f: F) -> CircuitRc
where
    // (circ, parents) -> new_parents. new_parents = replacements for parents
    F: FnMut(CircuitRc, &Vec<CircuitRc>) -> Option<Vec<CircuitRc>>,
{
    let mut parents = Parents::new();
    parents.add(circuit.clone());
    visit_circuit_topoorder_replace(circuit, |x| {
        let p = parents.get(&x);
        if let Some(p_new) = f(x, p) {
            let v: Vec<_> = izip!(p.clone(), p_new).collect();
            for (a, b) in &v[..] {
                parents.replace(a, b)
            }
            Some(v)
        } else {
            None
        }
    })
}

pub fn deep_map_pass_up<F, T>(circuit: CircuitRc, mut f: F) -> (CircuitRc, T)
where
    T: Clone,
    F: FnMut(CircuitRc, Vec<T>) -> (CircuitRc, T),
{
    let topo = toposort_circuit(circuit.clone());
    let mut pass_ups: HashMap<CircuitRc, T> = HashMap::default();
    for c in topo {
        let passed_up = c.children().map(|c| pass_ups[&c].clone()).collect();
        let (new, pass_here) = f(c.clone(), passed_up);
        pass_ups.insert(c.clone(), pass_here.clone());
        if c == circuit {
            return (new, pass_here);
        }
    }
    panic!();
}

pub fn deep_map_pass_down<F, F2, T>(circuit: CircuitRc, pass_down: F, make_circuit: F2) -> CircuitRc
where
    F: Fn(CircuitRc, &Vec<T>) -> Vec<T>,
    F2: Fn(CircuitRc, &Vec<T>) -> CircuitRc,
{
    let mut toposorted = toposort_circuit(circuit.clone());
    toposorted.reverse();
    let mut passed_down: HashMap<CircuitRc, Vec<T>> = HashMap::default();
    for c in toposorted {
        let pass = pass_down(c.clone(), passed_down.get(&c).unwrap_or(&vec![]));
        for (child, pass) in zip(c.children(), pass) {
            passed_down
                .entry(child.clone())
                .or_insert(vec![])
                .push(pass);
        }
    }
    deep_map_unwrap(circuit, |c| {
        make_circuit(c.clone(), passed_down.get(&c).unwrap_or(&vec![]))
    })
}

#[pyfunction]
pub fn replace_all_randn_seeded(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |node| match &**node {
        Circuit::Array(ac) => Array::randn_full(
            ac.info().shape.clone(),
            ac.info().name,
            ac.info().device_dtype,
            // We use the tensor hash instead of the circuit hash
            Some(ac.value.hash_usize().unwrap()),
        )
        .unwrap()
        .rc(),
        Circuit::Index(index) => Index::nrc(
            index.node(),
            TensorIndex(
                zip(&index.index.0, index.node().info().shape.clone())
                    .map(|(i, l)| {
                        if let TensorAxisIndex::Tensor(t) = i {
                            return TensorAxisIndex::new_tensor_randint_seeded(
                                t.shape()[0].t().unwrap_or_else(|| t.max_usize().unwrap()),
                                l.unwrap(), // FIXME take max of t if unknown
                                index.info().device_dtype,
                                t.hash_usize().unwrap(),
                            );
                        }
                        i.clone()
                    })
                    .collect(),
            ),
            index.info().name,
        ),
        _ => node.clone(),
    })
}

/// Replaces child nodes recursively with a mapping
/// In pre-order so that high level nodes are replaced first
/// This function isn't panic safe even if you replace nodes with identically shaped nodes.
pub fn replace_nodes(circuit: CircuitRc, map: &HashMap<HashBytes, CircuitRc>) -> CircuitRc {
    deep_map_op_context_preorder_stoppable(
        circuit.clone(),
        &|x: CircuitRc, _| {
            let rc = x;
            let result = map.get(&rc.info().hash).cloned();
            let stop = result.is_some();
            (result, stop)
        },
        &mut (),
        &mut Default::default(),
    )
    .unwrap_or(circuit)
}

#[pyfunction]
pub fn prefix_all_names(circuit: CircuitRc, prefix: String) -> CircuitRc {
    deep_map_unwrap(circuit, |x| {
        if let Some(name) = x.info().name {
            return x
                .clone()
                .rename(Some((prefix.clone() + name.into()).into()));
        }
        x
    })
}

pub fn is_definitely_view_on_child(circuit: CircuitRc) -> bool {
    if circuit.num_children() != 1 {
        return false;
    }
    match &**circuit {
        Circuit::Rearrange(rr) => {
            rr.spec.input_ints.iter().all(|x| x.len() < 2)
                && rr.spec.output_ints.iter().all(|x| x.len() < 2)
            // this is too conservative
        }
        Circuit::Index(idx) => !idx
            .index
            .0
            .iter()
            .any(|x| matches!(x, TensorAxisIndex::Tensor(_))),
        Circuit::Tag(_) => true,
        _ => false,
    }
}

pub fn biggest_non_leaf(circuit: CircuitRc) -> Option<(CircuitRc, BigUint)> {
    let mut r: Option<(CircuitRc, BigUint)> = None;
    let big_uint_0: BigUint = 0u8.into();
    visit_circuit_unwrap(circuit, |x| {
        if !x.is_leaf() {
            let m = x.info().naive_mem_use(None);
            if &m > r.as_ref().map_or_else(|| &big_uint_0, |x| &x.1) {
                r = Some((x, m));
            }
        }
    });
    r
}
