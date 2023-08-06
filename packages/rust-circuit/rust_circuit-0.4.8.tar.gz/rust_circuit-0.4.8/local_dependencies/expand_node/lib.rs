use std::{
    collections::BTreeMap,
    iter::{self, zip},
    ops::Deref,
    sync::Arc,
};

use anyhow::{bail, Context, Result};
use circuit_base::{
    prelude::*, Add, Concat, Cumulant, Einsum, GeneralFunction, Index, Module, ModuleArgSpec,
    ModuleSpec, Rearrange, Scatter, Symbol, Tag,
};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*, types::PyModule, wrap_pyfunction, PyResult};
use rr_util::{
    cached_method,
    caching::FastUnboundedCache,
    eq_by_big_hash::EqByBigHash,
    impl_eq_by_big_hash, pycall, python_error_exception,
    rearrange_spec::RearrangeSpec,
    shape::{right_align_shapes, shape_eq, Shape, Size},
    sv,
    tensor_util::{TensorAxisIndex, TensorIndex},
    tu8v,
    util::{arc_unwrap_or_clone, EinsumAxes, HashBytes},
};
use rustc_hash::FxHashMap as HashMap;
use smallvec::ToSmallVec;
use thiserror::Error;

pub fn register(_py: pyo3::Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(expand_node_py, m)?)?;
    m.add_function(wrap_pyfunction!(replace_expand_bottom_up_dict_py, m)?)?;
    m.add_function(wrap_pyfunction!(replace_expand_bottom_up_py, m)?)?;

    Ok(())
}

#[pyfunction]
#[pyo3(name = "expand_node")]
pub fn expand_node_py(circuit: CircuitRc, inputs: Vec<CircuitRc>) -> Result<CircuitRc> {
    expand_node(circuit, &inputs, &mut |_, _, _| {
        bail!("fancy module expanding not supported via python expand node")
    })
}

#[derive(Clone, Debug)]
pub struct ReplaceMapRc {
    replace_map: Arc<BTreeMap<CircuitRc, CircuitRc>>,
    hash: HashBytes,
}

impl Default for ReplaceMapRc {
    fn default() -> Self {
        Self::new(Default::default())
    }
}

impl Deref for ReplaceMapRc {
    type Target = BTreeMap<CircuitRc, CircuitRc>;

    fn deref(&self) -> &Self::Target {
        &self.replace_map
    }
}

impl ReplaceMapRc {
    pub fn new(replace_map: BTreeMap<CircuitRc, CircuitRc>) -> Self {
        let mut hasher = blake3::Hasher::new();
        for (k, v) in replace_map.iter() {
            hasher.update(&k.hash());
            hasher.update(&v.hash());
        }
        Self {
            replace_map: Arc::new(replace_map),
            hash: hasher.finalize().into(),
        }
    }

    pub fn into_map(self) -> <Self as Deref>::Target {
        arc_unwrap_or_clone(self.replace_map)
    }

    pub fn extend_into(&self, new: Vec<(CircuitRc, CircuitRc)>) -> Self {
        let mut m = (*self.replace_map).clone();
        m.extend(new);
        Self::new(m)
    }

    /// handle the module case
    pub fn per_child(&self, circuit: &CircuitRc) -> Vec<Self> {
        if let Some(m) = circuit.as_module() {
            if m.spec
                .arg_specs
                .iter()
                .any(|arg_spec| self.contains_key(&arg_spec.symbol.crc()))
            {
                let mut removed_map = (*self.replace_map).clone();
                for arg_spec in &m.spec.arg_specs {
                    removed_map.remove(&arg_spec.symbol.crc());
                }

                return iter::once(Self::new(removed_map))
                    .chain(iter::repeat(self).take(m.num_args()).cloned())
                    .collect();
            }
        }
        vec![self.clone(); circuit.num_children()]
    }
}

impl EqByBigHash for ReplaceMapRc {
    fn hash(&self) -> HashBytes {
        self.hash
    }
}
impl_eq_by_big_hash!(ReplaceMapRc);

pub fn expand_node(
    circuit: CircuitRc,
    inputs: &Vec<CircuitRc>,
    rerun_with_extra_replacements: &mut dyn FnMut(
        CircuitRc,
        Vec<(CircuitRc, CircuitRc)>,
        usize,
    ) -> Result<CircuitRc>,
) -> Result<CircuitRc> {
    expand_node_raw(circuit.clone(), inputs, rerun_with_extra_replacements)
        .with_context(|| format!("expand failed for\n{circuit:?}\nwith new_children={inputs:#?}"))
}

fn expand_node_raw(
    circuit: CircuitRc,
    inputs: &Vec<CircuitRc>,
    rerun_with_extra_replacements: &mut dyn FnMut(
        CircuitRc,
        Vec<(CircuitRc, CircuitRc)>,
        usize,
    ) -> Result<CircuitRc>,
) -> Result<CircuitRc> {
    if inputs.len() != circuit.num_children() {
        bail!(ExpandError::WrongNumChildren {
            expected: circuit.num_children(),
            got: inputs.len(),
        });
    }
    if inputs == circuit.children_sl() {
        return Ok(circuit); // in all identical case we can return same circuit for efficiency
    }
    if inputs
        .iter()
        .zip(circuit.children())
        .all(|(new, old)| shape_eq(new.shape(), old.shape()))
    {
        // all shapes equivalent, so no need to expand or do anything fancy
        // Just special casing for efficiency
        // We can't use unwrap because we still want to propagate errors from
        // stuff like dtype mismatches or constraint violations.
        return circuit.replace_children(inputs.clone());
    }

    let batch_ranks: Vec<usize> = zip(circuit.children(), inputs)
        .filter_map(|(old, new)| new.rank().checked_sub(old.info().rank()))
        .collect();
    if batch_ranks.len() != inputs.len() {
        bail!(ExpandError::BatchingRankTooLow {
            default: circuit.children().map(|x| x.rank()).collect(),
            got: inputs.iter().map(|x| x.rank()).collect(),
        });
    }

    let batch_shapes: Vec<&[Size]> = zip(&batch_ranks, inputs)
        .map(|(br, new)| &new.info().shape[0..*br])
        .collect();

    // TODO: maybe we should allow for inconsistent symbolic batch shapes?
    // (probably not...)
    let broadcasted_batch_shape =
        right_align_shapes(&batch_shapes).context("batch shapes didn't match (expand)")?;
    let batch_rank = broadcasted_batch_shape.len();

    let get_expanded_inputs = |batchable: &[bool]| -> Result<Vec<CircuitRc>, usize> {
        let br = batch_rank;
        assert_eq!(batchable.len(), batch_ranks.len());
        assert_eq!(inputs.len(), batch_ranks.len());
        inputs
            .iter()
            .zip(&batch_ranks)
            .zip(batchable)
            .enumerate()
            .map(|(i, ((x, &r), batchable_x))| {
                assert!(br >= r);
                if !batchable_x && r > 0 {
                    return Err(i);
                }
                if br == r || !batchable_x {
                    return Ok(x.clone());
                }
                Ok(Rearrange::nrc(
                    x.clone(),
                    RearrangeSpec::prepend_batch_shape(
                        broadcasted_batch_shape[..br - r].into(),
                        x.ndim(),
                    )
                    .unwrap(),
                    x.info().name.map(|x| format!("{} rep_for_batch", x).into()),
                ))
            })
            .collect()
    };

    let out: CircuitRc = match &**circuit {
        Circuit::Array(_) | Circuit::Symbol(_) | Circuit::Scalar(_) => circuit.clone(),
        // handling of rearrange is basically a hack to deal with rewrites (and maybe other places?) not preserving wildcards
        // the correct thing would be to preserve wildcards and only allow expand changing dims where there's wildcards in rearrange
        Circuit::Rearrange(node) => {
            let input_shape_non_batch = inputs[0].info().shape[batch_ranks[0]..].to_smallvec();

            // TODO: test me better!
            Rearrange::try_new(
                inputs[0].clone(),
                node.spec
                    .expand_to(&input_shape_non_batch)?
                    .add_batch_dims(batch_ranks[0]),
                circuit.info().name,
            )?
            .rc()
        }
        // I think we just don't do any symbolic shape munging in Index/Scatter?
        Circuit::Index(node) => {
            let inner = node.node();
            // for now non-batch non-identity dims can't change
            // slice(0, end) is treated as identity to match child_axis_map
            for i in 0..inner.rank() {
                if !inner.shape()[i].eq_if_known(inputs[0].shape()[i + batch_ranks[0]])
                    && !node.index.0[i].is_identity(inner.shape()[i])
                {
                    bail!(ExpandError::FixedIndex {
                        index: circuit.clone(),
                        old_shape: inner.shape().clone(),
                        new_shape: inputs[0].shape().clone(),
                    });
                }
            }
            Index::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(
                            node.index
                                .expand_to_shape(
                                    inner.shape(),
                                    &inputs[0].shape()[batch_ranks[0]..],
                                )
                                .0
                                .into_iter(),
                        )
                        .collect(),
                ),
                node.info().name,
            )
        }
        Circuit::Scatter(node) => {
            let inner = node.node();
            // for now non-batch non-identity dims can't change
            // slice(0, end) is treated as identity to match child_axis_map
            for i in 0..inner.rank() {
                if !inner.shape()[i].eq_if_known(inputs[0].shape()[i + batch_ranks[0]])
                    && !node.index.0[i].is_identity(inner.shape()[i])
                {
                    bail!(ExpandError::FixedIndex {
                        index: circuit.clone(),
                        old_shape: inner.shape().clone(),
                        new_shape: inputs[0].shape().clone(),
                    });
                }
            }
            Scatter::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(
                            node.index
                                .expand_to_shape(
                                    inner.shape(),
                                    &inputs[0].shape()[batch_ranks[0]..],
                                )
                                .0
                                .into_iter(),
                        )
                        .collect(),
                ),
                inputs[0].info().shape[0..batch_ranks[0]]
                    .iter()
                    .cloned()
                    .chain(node.info().shape.iter().cloned())
                    .collect(),
                node.info().name,
            )
        }
        Circuit::Concat(node) => {
            // TODO: error on concat axis having symbolic size? (or maybe concat axis is fine???
            let br = batch_rank;

            let inputs = get_expanded_inputs(&vec![true; inputs.len()]).unwrap();

            let new_axis = node.axis + br;
            if !zip(node.children(), &inputs).all(|(old, new)| {
                old.info().shape[node.axis].eq_if_known(new.info().shape[new_axis])
            }) {
                bail!(ExpandError::ConcatAxis {
                    axis: node.axis,
                    old_shape: sv![],
                    new_shape: sv![],
                });
            }

            Concat::try_new(inputs, new_axis, node.info().name)?.rc()
        }
        Circuit::Add(node) => {
            let inputs: Vec<_> = inputs
                .iter()
                .zip(&batch_ranks)
                .map(|(inp, &b_rank)| {
                    let unbatched_rank = inp.rank() - b_rank;
                    let rank_diff = node.rank() - unbatched_rank;
                    if rank_diff > 0 && b_rank > 0 {
                        inp.unsqueeze(
                            (b_rank..rank_diff + b_rank).collect(),
                            inp.info().name.map(|x| format!("{} unsq_b_add", x).into()),
                        )
                        .unwrap()
                        .rc()
                    } else {
                        inp.clone()
                    }
                })
                .collect();

            Add::try_new(inputs, node.info().name)?.rc()
        }
        Circuit::GeneralFunction(node) => {
            // TODO: symbolic? (annoying to handle, would require changes to spec)
            // We could optimize out these input expansions in various cases.
            // TODO: we could run into strange issues with general functions and expand.
            // Maybe resolve with an assert...
            // TODO: maybe alow for batching over individual inputs like:
            // (This is a bit annoying in various ways and probably shouldn't be supported).
            // - [b_0, b_1, b_2, (stuff)]
            // - [b_2, (other stuff)]
            GeneralFunction::try_new(
                get_expanded_inputs(&node.input_batchability).map_err(|input_i| {
                    ExpandError::GeneralFunctionTriedToBatchNonBatchableInput {
                        input_i,
                        batched_inputs: inputs.clone(),
                        general_function: node.clone(),
                    }
                })?,
                node.spec.clone(),
                node.info().name,
            )?
            .rc()
        }
        Circuit::Einsum(node) => {
            let br = batch_rank;
            let next_axis = node.next_axis();
            assert!(next_axis as usize + br <= u8::MAX as usize);
            let end_axis = next_axis + br as u8;
            let out_axes = (next_axis..end_axis)
                .chain(node.out_axes.iter().cloned())
                .collect();
            let new_args: Vec<_> = node
                .in_axes
                .iter()
                .zip(inputs)
                .zip(batch_ranks)
                .map(|((ints, inp), r)| {
                    assert!(br >= r);
                    (
                        inp.clone(),
                        (next_axis + (br - r) as u8..end_axis)
                            .chain(ints.iter().cloned())
                            .collect::<EinsumAxes>(),
                    )
                })
                .collect();

            let mut shape_map_many = HashMap::default();
            for (circ, axes) in &new_args {
                for (&circuit_shape, axis) in circ.info().shape.iter().zip(axes) {
                    shape_map_many
                        .entry(*axis)
                        .or_insert(Vec::new())
                        .push(circuit_shape);
                }
            }

            Einsum::try_new(new_args, out_axes, node.info().name)?.rc()
        }
        Circuit::Tag(node) => Tag::nrc(inputs[0].clone(), node.uuid, node.info().name),
        Circuit::Cumulant(node) => {
            // For now, only supports expansion in easy cases
            if zip(inputs, node.children())
                .skip(1)
                .any(|(new_c, old_c)| new_c.rank() != old_c.rank())
            {
                bail!(ExpandError::CumulantRankChanged { circuit })
            }
            Cumulant::nrc(inputs.clone(), node.info().name)
        }
        Circuit::Module(node) => {
            assert_eq!(inputs.len(), node.num_children());
            let mut children = inputs.clone();
            let new_nodes = children.split_off(1);
            let spec_circuit = children.pop().unwrap();

            if node.num_args() == 0 {
                // handle empty case so we can assume non-empty below
                return Ok(Module::nrc(
                    vec![],
                    ModuleSpec {
                        circuit: spec_circuit,
                        arg_specs: vec![],
                    },
                    node.info().name,
                ));
            }

            // Approach:
            // suppose that orig node shapes are:
            // [     b_1, b_2, | x_0, x_1]
            // [          b_2, | y_0]
            // [b_0, b_1, b_2, | z_0, z_1]
            // Where x/y/z is the part which matches up with the input symbol
            // (with a | to indicate the division) and the `b_i` are batched
            // over by the module itself. (I aligned batch shapes in the
            // diagram for clarity, the number of batch dims is different for
            // each input)
            //
            // Suppose this yields an overall module shape of
            // [b_0, b_1, b_2, | w_0, w_1, w_2, w_3]
            // Where w_0, ..., w_3 are from the spec circuit itself and b_0, b_1, b_2
            // are the batching done by the module.
            //
            //
            // Now suppose we get new shapes:
            // [               n_3,      b_1, b_2, x_0, x_1]
            // [          n_2, n_3,           b_2, y_0]
            // [n_0, n_1, n_2, n_3, b_0, b_1, b_2, z_0, z_1]
            // (n is for 'new')
            // (we first need to make sure that b0, ..., b_2 match up by resolving symbolic sizes)
            //
            // Then we'll first move new dims into the symbol part as needed to
            // make batching 'contiguous' (via a rearrange)
            // [               b_1, b_2, | n_3, x_0, x_1]
            // [                    b_2, | n_2, n_3, y_0]
            // [n_0, n_1, b_0, b_1, b_2, | n_2, n_3, z_0, z_1]
            //
            // Note this requires changing the symbol shapes - we'll have to prepend the extra new dims.
            //
            // Now the module will originally have the following shape because we shifted dims around:
            // [n_0, n_1, b_0, b_1, b_2, | n_2, n_3, w_0, w_1, w_2, w_3]
            //
            // So we'll 'unshift' these dims to yield:
            // [n_0, n_1, n_2, n_3, b_0, b_1, b_2,  w_0, w_1, w_2, w_3]

            let current_node_batch_ranks: Vec<_> = node
                .args()
                .zip(&node.spec.arg_specs)
                .map(|(node, arg_spec)| node.ndim().checked_sub(arg_spec.symbol.ndim()).unwrap())
                .collect();
            let current_batch_rank = *current_node_batch_ranks.iter().max().unwrap();

            let spec_circuit_batch_rank = batch_ranks[0]; // spec circuit is 0th child
            let new_node_batch_over_ranks: Vec<_> = batch_ranks[1..].to_vec(); // and then nodes are rest

            // how many dims do we have to move to make batching 'contiguous'
            let rank_to_push_into_spec_circuit = current_node_batch_ranks
                .iter()
                .zip(&new_node_batch_over_ranks)
                .map(|(this_current_batch_rank, this_new_batch_rank)| {
                    if *this_current_batch_rank == current_batch_rank {
                        0
                    } else {
                        *this_new_batch_rank
                    }
                })
                .chain(iter::once(spec_circuit_batch_rank))
                .max()
                .unwrap();

            let (spec_circuit, arg_specs, new_nodes) = if rank_to_push_into_spec_circuit > 0 {
                let to_unzip = node
                    .spec
                    .arg_specs
                    .iter()
                    .zip(new_node_batch_over_ranks)
                    .zip(new_nodes)
                    .zip(current_node_batch_ranks)
                    .map(
                        |(((arg_spec, this_new_batch_rank), node), this_current_batch_rank)| {
                            let this_sym_extra_rank =
                                rank_to_push_into_spec_circuit.min(this_new_batch_rank);
                            // move some of new batch rank dims to make batching contiguous
                            let new_sym = Symbol::new(
                                node.shape()[this_new_batch_rank - this_sym_extra_rank
                                    ..this_new_batch_rank]
                                    .iter()
                                    .chain(arg_spec.symbol.shape())
                                    .cloned()
                                    .collect(),
                                arg_spec.symbol.uuid,
                                arg_spec.symbol.info().name,
                            );
                            let node = if this_current_batch_rank > 0 && this_sym_extra_rank > 0 {
                                let old_sym_rank = arg_spec.symbol.rank();
                                let node_rank = node.rank();
                                let up_to_old_sym_rank = node_rank - old_sym_rank;
                                let shift_name = node
                                    .info()
                                    .name
                                    .map(|x| format!("{} shift_batch", x).into());
                                let spec = RearrangeSpec::new_permute(
                                    (0..this_new_batch_rank - this_sym_extra_rank)
                                        .chain(this_new_batch_rank..up_to_old_sym_rank)
                                        .chain(
                                            this_new_batch_rank - this_sym_extra_rank
                                                ..this_new_batch_rank,
                                        )
                                        .chain(up_to_old_sym_rank..node_rank)
                                        .collect(),
                                )
                                .unwrap();
                                assert!(!spec.is_identity()); // if statement should be checking for identity
                                Rearrange::nrc(node, spec, shift_name)
                            } else {
                                node
                            };

                            (
                                (arg_spec.symbol.crc(), new_sym.crc()),
                                ModuleArgSpec {
                                    symbol: new_sym,
                                    ..arg_spec.clone()
                                },
                                node,
                            )
                        },
                    );
                let (replacements, new_arg_specs, new_nodes): (Vec<_>, _, _) =
                    itertools::multiunzip(to_unzip);
                let replacements: Vec<(_, _)> = replacements // this is just for efficiency
                    .into_iter()
                    .filter_map(|(a, b)| (a != b).then_some((a, b)))
                    .collect();

                let new_spec_circuit = rerun_with_extra_replacements(
                    node.spec.circuit.clone(),
                    replacements,
                    0,
                )
                .with_context(|| {
                    "failed to rerun batching for spec circuit with expanded symbols! (TODO: info)"
                        .to_string()
                })?;

                assert!(
                    new_spec_circuit.ndim()
                        <= rank_to_push_into_spec_circuit + node.spec.circuit.ndim(),
                    "this assumption should hold due to guarantees that batching makes!"
                );

                (new_spec_circuit, new_arg_specs, new_nodes)
            } else {
                (spec_circuit, node.spec.arg_specs.clone(), new_nodes)
            };

            let spec = ModuleSpec {
                circuit: spec_circuit,
                arg_specs,
            };

            let out = Module::try_new(new_nodes, spec, node.info().name)?.rc();

            // unshift dims
            let final_out = if current_batch_rank > 0 && rank_to_push_into_spec_circuit > 0 {
                let orig_spec_ndim = node.spec.circuit.ndim();
                assert!(
                    out.ndim() <= current_batch_rank + batch_rank + orig_spec_ndim,
                    "this assumption should hold due to guarantees that batching makes!"
                );
                let missing_from_push_into_spec_circuit =
                    current_batch_rank + batch_rank + orig_spec_ndim - out.ndim();
                assert!(batch_rank >= rank_to_push_into_spec_circuit);
                let batch_rank_done_via_mod = batch_rank - rank_to_push_into_spec_circuit;
                let total_new_old_batch_via_mod = batch_rank_done_via_mod + current_batch_rank;

                // starting to get a bit complicated : )
                let new_batch_dims_via_mod = 0..batch_rank_done_via_mod;
                let end_all_batching = total_new_old_batch_via_mod + rank_to_push_into_spec_circuit
                    - missing_from_push_into_spec_circuit;
                let new_batch_dims_via_push_into_spec_circuit =
                    total_new_old_batch_via_mod..end_all_batching;
                let old_batch_dims = batch_rank_done_via_mod..total_new_old_batch_via_mod;
                let remaining_spec_circuit_dims =
                    end_all_batching..end_all_batching + orig_spec_ndim;
                assert_eq!(end_all_batching + orig_spec_ndim, out.ndim());

                let spec = RearrangeSpec::new(
                    (0..out.ndim() as u8).map(|i| tu8v![i]).collect(),
                    new_batch_dims_via_mod
                        .chain(out.ndim()..out.ndim() + missing_from_push_into_spec_circuit)
                        .chain(new_batch_dims_via_push_into_spec_circuit)
                        .chain(old_batch_dims)
                        .chain(remaining_spec_circuit_dims)
                        .map(|i| tu8v![i as u8])
                        .collect(),
                    iter::repeat(Size::NONE)
                        .take(out.ndim())
                        .chain(
                            broadcasted_batch_shape[batch_rank_done_via_mod
                                ..missing_from_push_into_spec_circuit + batch_rank_done_via_mod]
                                .iter()
                                .cloned(),
                        )
                        .collect(),
                )
                .unwrap();
                assert!(!spec.is_identity()); // if statement should be checking for identity

                let shift_name = out.info().name.map(|x| format!("{} shift_batch", x).into());
                let out_name = out.info().name;
                Rearrange::nrc(out.rename(shift_name), spec, out_name)
            } else {
                out
            };

            final_out
        }
        _ => {
            if &inputs[..] == circuit.children_sl() {
                circuit.clone()
            } else {
                bail!(ExpandError::NodeUnhandledVariant {
                    variant: circuit.variant_string(),
                })
            }
        }
    };
    assert_eq!(&out.shape()[..batch_rank], &broadcasted_batch_shape[..]);
    // assert_eq!(&out.shape()[batch_rank..], &circuit.shape()[..]); // only true ignoring sym shapes
    assert!(
        out.ndim() == circuit.ndim() + batch_rank,
        "batching assumption violated!"
    );
    Ok(out)
}

#[apply(python_error_exception)]
#[base_error_name(Expand)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ExpandError {
    #[error("expand wrong number of children, expected {expected} got {got} ({e_name})")]
    WrongNumChildren { expected: usize, got: usize },

    #[error("Batching Rank Too Low ({e_name})")]
    BatchingRankTooLow {
        default: Vec<usize>,
        got: Vec<usize>,
    },

    #[error("Trying to expand fixed index, index {index:?} old shape{old_shape:?} new shape {new_shape:?} ({e_name})")]
    FixedIndex {
        index: CircuitRc,
        old_shape: Shape,
        new_shape: Shape,
    },

    #[error(
        "Trying to expand concat axis, index {axis} old shape{old_shape:?} new shape {new_shape:?} ({e_name})"
    )]
    ConcatAxis {
        axis: usize,
        old_shape: Shape,
        new_shape: Shape,
    },

    // error could be improved...
    #[error("input_i={input_i} is not batchable, but tried to batch\nbatched_inputs={batched_inputs:?} general_function={general_function:?}\n ({e_name})")]
    GeneralFunctionTriedToBatchNonBatchableInput {
        input_i: usize,
        batched_inputs: Vec<CircuitRc>,
        general_function: GeneralFunction,
    },

    #[error("trying to expand node, unknown variant {variant} ({e_name})")]
    NodeUnhandledVariant { variant: String },

    #[error(
        "Can only change the rank of the first circuit of the cumulant {circuit:?} ({e_name})"
    )]
    CumulantRankChanged { circuit: CircuitRc },
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up_dict")]
pub fn replace_expand_bottom_up_dict_py(
    circuit: CircuitRc,
    dict: HashMap<CircuitRc, CircuitRc>,
) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| dict.get(&x).cloned())
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up")]
pub fn replace_expand_bottom_up_py(circuit: CircuitRc, f: PyObject) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| pycall!(f, (x.clone(),)))
}

pub trait ReplaceForExpand {
    fn replace(&mut self, circuit: CircuitRc) -> Option<CircuitRc>;
    fn done(&mut self, _circuit: CircuitRc) -> bool {
        false
    }
}

pub struct ReplaceForExpandFn<F: FnMut(CircuitRc) -> Option<CircuitRc>>(pub F);

impl<F: FnMut(CircuitRc) -> Option<CircuitRc>> ReplaceForExpand for ReplaceForExpandFn<F> {
    fn replace(&mut self, circuit: CircuitRc) -> Option<CircuitRc> {
        self.0(circuit)
    }
}

#[derive(Debug, Clone)]
pub struct ReplaceExpander<F: ReplaceForExpand> {
    replacer: F,
    // TODO: this holds onto array tensors forever!
    // We could try to use 'weak' for the cache, but this is a bit sad... (drops a bunch of stuff instantly)
    // Fix me!
    cache: FastUnboundedCache<(HashBytes, HashBytes), CircuitRc>,
}

impl<F: FnMut(CircuitRc) -> Option<CircuitRc>> ReplaceExpander<ReplaceForExpandFn<F>> {
    fn new_fn(replacer: F) -> Self {
        Self::new(ReplaceForExpandFn(replacer))
    }
}

#[derive(Debug, Clone, Copy)]
pub struct ReplaceForExpandNoop;

impl ReplaceForExpand for ReplaceForExpandNoop {
    fn replace(&mut self, _circuit: CircuitRc) -> Option<CircuitRc> {
        None
    }
    fn done(&mut self, _circuit: CircuitRc) -> bool {
        true
    }
}

pub type MapReplaceExpander = ReplaceExpander<ReplaceForExpandNoop>;
impl MapReplaceExpander {
    pub fn new_noop() -> Self {
        Self {
            replacer: ReplaceForExpandNoop,
            cache: FastUnboundedCache::default(),
        }
    }
}

impl<F: ReplaceForExpand> ReplaceExpander<F> {
    pub fn new(replacer: F) -> Self {
        Self {
            replacer,
            cache: FastUnboundedCache::default(),
        }
    }

    pub fn replace_expand(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self.replace_expand_with_map(circuit, &Default::default())
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, extra_replacements.hash()))]
    #[use_try]
    #[cache_expr(cache)]
    pub fn replace_expand_with_map(
        &mut self,
        circuit: CircuitRc,
        extra_replacements: &ReplaceMapRc,
    ) -> Result<CircuitRc> {
        if extra_replacements.is_empty() && self_.replacer.done(circuit.clone()) {
            return Ok(circuit);
        }
        if let Some(replaced) = self_.replacer.replace(circuit.clone()) {
            return Ok(replaced);
        }
        if let Some(replaced) = extra_replacements.get(&circuit) {
            return Ok(replaced.clone());
        }

        let per_child_extra = extra_replacements.per_child(&circuit);

        // TODO: optimize this as needed
        let new_children = circuit
            .children()
            .zip(per_child_extra.clone())
            .map(|(c, rep)| self_.replace_expand_with_map(c, &rep))
            .collect::<Result<_>>()?;

        expand_node(circuit, &new_children, &mut |c, rep, child_idx| {
            self_.replace_expand_with_map(c, &per_child_extra[child_idx].extend_into(rep))
        })
    }
}

pub fn replace_expand_bottom_up<F>(circuit: CircuitRc, replacer: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    ReplaceExpander::new_fn(replacer).replace_expand(circuit)
}

pub fn replace_expand_bottom_up_dyn(
    circuit: CircuitRc,
    replacer: &dyn Fn(CircuitRc) -> Option<CircuitRc>,
) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, replacer)
}

pub fn replace_expand_map(
    circuit: CircuitRc,
    map: Vec<(CircuitRc, CircuitRc)>,
) -> Result<CircuitRc> {
    ReplaceExpander::new_noop()
        .replace_expand_with_map(circuit, &ReplaceMapRc::new(map.into_iter().collect()))
}

#[test]
fn check_map_override() {
    let m: BTreeMap<_, _> = [(1, 2), (3, 4), (5, 7), (3, 9)].into_iter().collect();
    assert_eq!(m[&3], 9);
    let m: BTreeMap<_, _> = [(1, 2), (3, 4), (5, 7), (1, 9)].into_iter().collect();
    assert_eq!(m[&1], 9);
    let m: BTreeMap<_, _> = [(1, 2), (3, 4), (5, 7), (1, 9)].into_iter().collect();
    assert_eq!(m[&5], 7);
    let m: BTreeMap<_, _> = [(1, 2), (3, 4), (5, 7), (1, 9), (5, 4), (5, 8), (3, 7)]
        .into_iter()
        .collect();
    assert_eq!(m[&1], 9);
    assert_eq!(m[&5], 8);
    assert_eq!(m[&3], 7);
}
