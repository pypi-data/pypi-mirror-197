use std::{cmp::Ordering, iter::zip};

use anyhow::{anyhow, bail, Context, Result};
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::{prelude::*, types::PyTuple};
use rr_util::{
    atr,
    compact_data::U8Set,
    name::Name,
    opt_einsum::EinsumSpec,
    py_types::{PyEinsumAxes, PY_UTILS},
    pycall,
    rearrange_spec::{RInnerInts, RearrangeSpec},
    shape::{broadcast_shapes, shape_eq_and_known, shape_eq_if_known, shape_is_known, Size},
    sv,
    tensor_util::{
        check_canon_axes, IndexError, IndexTensor, Slice, TensorAxisIndex, TensorIndex,
        TensorIndexSync, TorchDeviceDtypeOp,
    },
    tu8v,
    util::{cumsum, dict_to_list, hashmap_collect_except_duplicates, AxisInt, EinsumAxes},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use uuid::uuid;

use crate::{
    auto_name::{child_name_with_maybe_paren, children_names_with_maybe_paren, OperatorPriority},
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{
        CircuitNodeComputeInfoImpl, CircuitNodeHashItems, CircuitNodeHashWithChildren,
    },
    new_rc_unwrap,
    prelude::*,
    CachedCircuitInfo, CircuitNodeSelfOnlyHash, ConstructError, PyCircuitBase, Scalar, Shape,
};

/// our Einsum supports diag output
/// this means `a->aa` is valid and produces a tensor with the input on the diagonal
/// also `aa->aa` only copies the diagonal, and ignores the rest
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Einsum {
    pub in_axes: Vec<EinsumAxes>,
    pub out_axes: EinsumAxes,
    info: CachedCircuitInfo,
}

circuit_node_extra_impl!(Einsum);

impl CircuitNodeComputeInfoImpl for Einsum {}
impl CircuitNodeHashWithChildren for Einsum {
    fn compute_hash_non_name(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.out_axes);
        for (c, axes) in self.args() {
            // no need to delimit because we have hash each loop
            hasher.update(&c.info().hash);
            hasher.update(axes);
        }
    }
}
impl CircuitNodeSelfOnlyHash for Einsum {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.out_axes);
        for axes in &self.in_axes {
            hasher.update(uuid!("3749ab7f-4f4c-4fdb-a268-af9c084e70ef").as_bytes());
            hasher.update(axes);
        }
    }
}

impl CircuitNode for Einsum {
    circuit_node_auto_impl!("ed15422c-7c02-40c2-a3c2-e9224514d063");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let out_inv: HashMap<AxisInt, usize> = hashmap_collect_except_duplicates(
            self.out_axes.iter().enumerate().map(|(i, x)| (*x, i)),
        );
        self.in_axes
            .iter()
            .map(|ints| {
                ints.iter()
                    .map(|i| {
                        if ints.iter().filter(|z| *z == i).count() > 1 {
                            return None;
                        }
                        out_inv.get(i).cloned()
                    })
                    .collect()
            })
            .collect()
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(
            children
                .iter()
                .zip(&self.in_axes)
                .map(|(c, axes)| (c.clone(), axes.clone()))
                .collect(),
            self.out_axes.clone(),
            self.info().name,
        )
    }

    fn self_flops(&self) -> BigUint {
        self.get_spec().flops()
    }
}

pub type EinsumArgs = Vec<(CircuitRc, EinsumAxes)>;
impl Einsum {
    fn shape_map_(
        children: &Vec<CircuitRc>,
        in_axes: &Vec<EinsumAxes>,
        name: Option<Name>,
    ) -> Result<HashMap<AxisInt, Size>> {
        let mut out = HashMap::default();
        for (circ, axes) in zip(children, in_axes) {
            if circ.rank() != axes.len() {
                bail!(ConstructError::EinsumLenShapeDifferentFromAxes {
                    len_axes: axes.len(),
                    child_len_shape: circ.rank(),
                    einsum_name: name,
                    child_circuit: circ.clone(),
                });
            }
            for (&circuit_size, axis) in circ.info().shape.iter().zip(axes) {
                let existing_size = out.entry(*axis).or_insert(circuit_size);
                *existing_size = existing_size.join_eq(&circuit_size, || {
                    anyhow!(ConstructError::EinsumAxisSizeDifferent {
                        new_size: circuit_size,
                        existing_size: *existing_size,
                        axis: *axis as usize,
                        einsum_name: name,
                        child_circuit: circ.clone(),
                    })
                })?;
            }
        }

        Ok(out)
    }

    pub fn shape_map(&self) -> Result<HashMap<AxisInt, Size>> {
        Self::shape_map_(&self.info.children, &self.in_axes, self.info().name)
    }

    #[apply(new_rc_unwrap)]
    pub fn try_new(args: EinsumArgs, out_axes: EinsumAxes, name: Option<Name>) -> Result<Self> {
        let (children, in_axes) = args.into_iter().unzip();
        let map = Self::shape_map_(&children, &in_axes, name)?;

        let shape = out_axes
            .iter()
            .map(|a| map.get(a).cloned())
            .collect::<Option<Shape>>()
            .ok_or_else(|| {
                anyhow::Error::from(ConstructError::EinsumOutputNotSubset {
                    circuit_name: name,
                    all_input_axes: map.into_keys().collect(),
                    output_axes: out_axes.clone(),
                })
            })?;

        // TODO: reduce axes nums!
        let out = Self {
            out_axes,
            info: CachedCircuitInfo::incomplete(name, shape, children)?,
            in_axes,
        };

        out.initial_init_info()
    }

    pub fn try_from_spec(
        spec: &EinsumSpec,
        circuits: &[CircuitRc],
        name: Option<Name>,
    ) -> Result<Self> {
        // TODO: maybe check int sizes!
        assert_eq!(spec.input_ints.len(), circuits.len());
        let to_idx =
            |vals: &[usize]| -> EinsumAxes { vals.iter().map(|&x| x as AxisInt).collect() };
        Self::try_new(
            circuits
                .iter()
                .zip(&spec.input_ints)
                .map(|(c, vals)| (c.clone(), to_idx(vals)))
                .collect(),
            to_idx(&spec.output_ints),
            name,
        )
    }

    pub fn axes_in_input(&self) -> HashSet<AxisInt> {
        // could be 256 bit bitmask
        self.in_axes.iter().flatten().copied().collect()
    }

    pub fn args(&self) -> impl Iterator<Item = (CircuitRc, &EinsumAxes)> {
        self.children().zip(self.in_axes.iter())
    }

    pub fn args_cloned(&self) -> Vec<(CircuitRc, EinsumAxes)> {
        self.args().map(|(a, b)| (a, b.clone())).collect()
    }
}

impl CircuitNodeAutoName for Einsum {
    const PRIORITY: OperatorPriority = OperatorPriority::Infix { priority: 1 };

    fn auto_name(&self) -> Option<Name> {
        children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(|names| {
            names
                .iter()
                .map(|name| Self::shorten_child_name(name))
                .collect::<Vec<String>>()
                .join(" * ")
                .into()
        })
    }
}

pub struct PyEinsumArgs(EinsumArgs);
impl<'source> FromPyObject<'source> for PyEinsumArgs {
    fn extract(args_obj: &'source PyAny) -> PyResult<Self> {
        let args: Vec<(CircuitRc, EinsumAxes)> = args_obj.extract()?;

        Ok(PyEinsumArgs(args.into_iter().collect()))
    }
}
impl IntoPy<PyObject> for PyEinsumArgs {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0
            .into_iter()
            .map(|(c, axes)| (c, PyEinsumAxes(axes)))
            .collect::<Vec<_>>()
            .into_py(py)
    }
}
#[pymethods]
impl Einsum {
    #[new]
    #[pyo3(signature=(*args, out_axes, name = None))]
    fn new_py(
        args: Vec<(CircuitRc, EinsumAxes)>,
        out_axes: EinsumAxes,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(args, out_axes, name)?;

        Ok(out.into_init())
    }

    #[getter(args)]
    fn args_py(&self) -> PyEinsumArgs {
        PyEinsumArgs(self.args_cloned())
    }

    #[getter]
    fn out_axes(&self) -> PyEinsumAxes {
        PyEinsumAxes(self.out_axes.clone())
    }

    fn all_input_axes(&self) -> Vec<PyEinsumAxes> {
        self.in_axes.iter().cloned().map(PyEinsumAxes).collect()
    }

    #[staticmethod]
    pub fn from_nodes_ints(
        nodes: Vec<CircuitRc>,
        input_ints: Vec<EinsumAxes>,
        output_ints: EinsumAxes,
        name: Option<Name>,
    ) -> Result<Self> {
        if nodes.len() != input_ints.len() {
            bail!(ConstructError::EinsumWrongNumChildren {
                actual_num_children: nodes.len(),
                expected_num_children_based_on_axes: input_ints.len(),
                einsum_name: name
            })
        }
        Self::try_new(zip(nodes, input_ints).collect(), output_ints, name)
    }

    #[staticmethod]
    #[pyo3(signature=(string, *nodes, name = None))]
    pub fn from_einsum_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<Name>,
    ) -> Result<Self> {
        let (mut input_ints, output_ints) = EinsumSpec::string_to_ints(string.to_owned())?;
        if input_ints.len() == 1 && input_ints[0].is_empty() && nodes.is_empty() {
            input_ints.clear()
        }
        Self::from_nodes_ints(nodes, input_ints, output_ints, name)
    }

    #[staticmethod]
    #[pyo3(signature=(string, *nodes, name = None))]
    pub fn from_fancy_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<Name>,
    ) -> Result<Self> {
        let (mut input_ints, output_ints) = EinsumSpec::fancy_string_to_ints(string.to_owned())?;
        if input_ints.len() == 1 && input_ints[0].is_empty() && nodes.is_empty() {
            input_ints.clear()
        }
        Self::from_nodes_ints(nodes, input_ints, output_ints, name)
    }

    #[staticmethod]
    #[pyo3(signature=(spec, *nodes, name = None))]
    pub fn from_spec_py(
        spec: EinsumSpec,
        nodes: Vec<CircuitRc>,
        name: Option<Name>,
    ) -> Result<Self> {
        Self::try_from_spec(&spec, &nodes, name)
    }

    #[staticmethod]
    pub fn new_diag(node: CircuitRc, ints: EinsumAxes, name: Option<Name>) -> Self {
        Einsum::try_new(vec![(node, ints.unique())], ints, name).unwrap()
    }

    #[staticmethod]
    pub fn new_trace(node: CircuitRc, ints: EinsumAxes, name: Option<Name>) -> Self {
        let deduped = ints.unique();
        Einsum::try_new(vec![(node, ints)], deduped, name).unwrap()
    }

    #[staticmethod]
    pub fn scalar_mul(
        node: CircuitRc,
        scalar: f64,
        name: Option<Name>,
        scalar_name: Option<Name>,
    ) -> Self {
        let axes: EinsumAxes = (0..node.rank()).map(|x| x as u8).collect();
        Einsum::try_new(
            vec![
                (node, axes.clone()),
                (Scalar::new(scalar, sv![], scalar_name).rc(), tu8v![]),
            ],
            axes,
            name,
        )
        .unwrap()
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, name = None))]
    pub fn elementwise_broadcasted(nodes: Vec<CircuitRc>, name: Option<Name>) -> Result<Einsum> {
        let out_shape = broadcast_shapes(&nodes.iter().map(|x| &x.shape()[..]).collect::<Vec<_>>())
            .context("failed to broadcast for einsum mul")?;
        let mut prev_one_shape = out_shape.len().saturating_sub(1) as u8;
        Einsum::try_new(
            nodes
                .iter()
                .map(|node| {
                    let rank_difference = out_shape.len() - node.rank();
                    (
                        node.clone(),
                        node.info()
                            .shape
                            .iter()
                            .enumerate()
                            .map(|(i, l)| {
                                if !l.eq_if_known(out_shape[i + rank_difference]) {
                                    prev_one_shape += 1;
                                    prev_one_shape
                                } else {
                                    (i + rank_difference) as u8
                                }
                            })
                            .collect(),
                    )
                })
                .collect(),
            (0u8..out_shape.len() as u8).collect(),
            name,
        )
    }

    #[staticmethod]
    pub fn empty(name: Option<Name>) -> Self {
        Einsum::try_new(vec![], tu8v![], name).unwrap()
    }

    #[staticmethod]
    pub fn identity(node: CircuitRc, name: Option<Name>) -> Self {
        let axes: EinsumAxes = (0..node.rank()).map(|x| x as u8).collect();
        Einsum::try_new(vec![(node, axes.clone())], axes, name).unwrap()
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, name = None, out_axes_permutation = None))]
    pub fn new_outer_product(
        nodes: Vec<CircuitRc>,
        name: Option<Name>,
        out_axes_permutation: Option<Vec<usize>>,
    ) -> Self {
        let sections: Vec<_> = nodes.iter().map(|n| n.rank()).collect();
        let starts = cumsum(&sections);
        let mut out_axes: EinsumAxes = nodes
            .iter()
            .enumerate()
            .flat_map(|(i, _n)| (starts[i] as u8..(starts[i] + sections[i]) as u8))
            .collect();
        if let Some(permutation) = out_axes_permutation {
            let new_out_axes = permutation.iter().map(|i| out_axes[*i]).collect();
            out_axes = new_out_axes;
        }
        Einsum::try_new(
            nodes
                .iter()
                .enumerate()
                .map(|(i, n)| {
                    (
                        n.clone(),
                        (starts[i] as u8..(starts[i] + sections[i]) as u8).collect(),
                    )
                })
                .collect(),
            out_axes,
            name,
        )
        .unwrap()
    }

    pub fn evolve(&self, args: Option<EinsumArgs>, out_axes: Option<EinsumAxes>) -> Einsum {
        Einsum::try_new(
            args.unwrap_or_else(|| self.args_cloned()),
            out_axes.unwrap_or_else(|| self.out_axes.clone()),
            self.info().name,
        )
        .unwrap()
    }

    pub fn reduced_axes(&self) -> U8Set {
        self.in_axes
            .iter()
            .flatten()
            .filter(|i| !self.out_axes.contains(i))
            .copied()
            .collect()
    }

    pub fn next_axis(&self) -> u8 {
        self.in_axes
            .iter()
            .flatten()
            .max()
            .map(|x| x + 1)
            .unwrap_or(0)
    }

    pub fn get_spec(&self) -> EinsumSpec {
        let to_usize = |vals: &[u8]| -> Vec<usize> { vals.iter().map(|&x| x as usize).collect() };
        EinsumSpec {
            input_ints: self.in_axes.iter().map(|x| to_usize(x)).collect(),
            output_ints: to_usize(&self.out_axes),
            int_sizes: dict_to_list(
                &self
                    .shape_map()
                    .unwrap()
                    .iter()
                    .map(|(key, val)| (*key as usize, *val))
                    .collect(),
                None,
                Size::known(0),
            ),
        }
    }

    pub fn normalize_ints(&self) -> Einsum {
        let spec = self.get_spec();
        let spec_normalized = spec.normalize();
        Einsum::try_from_spec(&spec_normalized, &self.info.children, self.info().name).unwrap()
    }
}

/// Add supports broadcasting
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Add {
    info: CachedCircuitInfo,
}

impl Add {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, name: Option<Name>) -> Result<Self> {
        let shape = broadcast_shapes(
            &nodes
                .iter()
                .map(|x| &x.info().shape[..])
                .collect::<Vec<_>>(),
        )
        .with_context(|| format!("Sum isn't broadcastable name={:?}", name))?;
        // TODO: reduce axes nums!
        let out = Self {
            info: CachedCircuitInfo::incomplete(name, shape, nodes)?,
        };
        out.initial_init_info()
    }

    pub fn try_from_counts(nodes: &HashMap<CircuitRc, usize>, name: Option<Name>) -> Result<Self> {
        Self::try_new(
            nodes
                .iter()
                .flat_map(|(circ, &count)| vec![circ.clone(); count])
                .collect(),
            name,
        )
    }
}

#[pymethods]
impl Add {
    #[new]
    #[pyo3(signature=(*nodes, name = None))]
    fn new_py(nodes: Vec<CircuitRc>, name: Option<Name>) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(nodes, name)?;

        Ok(out.into_init())
    }

    pub fn has_broadcast(&self) -> bool {
        !self.children().all(|node| node.shape() == self.shape())
    }

    pub fn nodes_and_rank_differences(&self) -> Vec<(CircuitRc, usize)> {
        self.children()
            .map(|node| (node.clone(), self.rank() - node.info().rank()))
            .collect()
    }

    pub fn to_counts(&self) -> HashMap<CircuitRc, usize> {
        let mut counts = HashMap::default();
        counts.reserve(20);
        for item in self.children() {
            *counts.entry(item).or_insert(0) += 1;
        }

        counts
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes_and_weights, use_1_weights = false, name = None))]
    pub fn from_weighted_nodes(
        nodes_and_weights: Vec<(CircuitRc, f64)>,
        use_1_weights: bool,
        name: Option<Name>,
    ) -> Result<Self> {
        let children = nodes_and_weights
            .iter()
            .map(|(node, weight)| {
                if use_1_weights || *weight != 1. {
                    Einsum::scalar_mul(node.to_owned(), *weight, None, None).rc()
                } else {
                    node.to_owned()
                }
            })
            .collect();
        Self::try_new(children, name)
    }

    #[staticmethod]
    pub fn minus(positive: CircuitRc, negative: CircuitRc, name: Option<Name>) -> Result<Self> {
        positive.sub(negative, name)
    }
}

circuit_node_extra_impl!(Add, self_hash_default);

impl CircuitNodeComputeInfoImpl for Add {}

impl CircuitNodeHashItems for Add {}

impl CircuitNode for Add {
    circuit_node_auto_impl!("88fb29e5-c81e-47fe-ae4c-678b22994670");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.nodes_and_rank_differences()
            .iter()
            .map(|(node, rank_difference)| {
                node.info()
                    .shape
                    .iter()
                    .enumerate()
                    .map(|(i, _x)| {
                        if self.info().shape[i + rank_difference].eq_and_known(node.info().shape[i])
                        {
                            Some(i + rank_difference)
                        } else {
                            None
                        }
                    })
                    .collect()
            })
            .collect()
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(children, self.info().name)
    }

    fn self_flops(&self) -> BigUint {
        self.info.numel() * self.num_children()
    }
}

impl CircuitNodeAutoName for Add {
    const PRIORITY: OperatorPriority = OperatorPriority::Infix { priority: 0 };

    fn auto_name(&self) -> Option<Name> {
        children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(|names| {
            names
                .iter()
                .map(|name| Self::shorten_child_name(name))
                .collect::<Vec<String>>()
                .join(" + ")
                .into()
        })
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Rearrange {
    #[pyo3(get)]
    pub spec: Box<RearrangeSpec>,
    info: CachedCircuitInfo,
}

impl Rearrange {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, spec: RearrangeSpec, name: Option<Name>) -> Result<Self> {
        // Check that RearrangeSpec is valid for input
        let shape = spec
            .conform_to_input_shape(&node.info().shape)
            .with_context(|| {
                format!(
                    "{}\nname={:?}, child={:?}",
                    "rearrange spec conform_to_input_shape failed in construct rearrange",
                    name,
                    node
                )
            })?
            .shapes()?
            .1;

        // spec must be valid because we enforce that on construction!
        // TODO: reduce axes nums!
        let out = Self {
            spec: Box::new(spec),
            info: CachedCircuitInfo::incomplete(name, shape, vec![node])?,
        };

        out.initial_init_info()
    }

    pub fn evolve(&self, node: Option<CircuitRc>, spec: Option<RearrangeSpec>) -> Rearrange {
        Rearrange::try_new(
            node.unwrap_or_else(|| self.node()),
            spec.unwrap_or_else(|| (*self.spec).clone()),
            self.info().name,
        )
        .unwrap()
    }

    pub fn nrc_elim_identity(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<Name>,
    ) -> CircuitRc {
        if spec.is_identity() {
            node
        } else {
            Rearrange::nrc(node, spec, name)
        }
    }

    pub fn unflatten(node: CircuitRc, shape: Shape, name: Option<Name>) -> Result<Self> {
        if node.ndim() != 1 {
            bail!(ConstructError::UnflattenButNDimNot1 { ndim: node.ndim() })
        }
        Ok(Rearrange::new(node, RearrangeSpec::unflatten(shape)?, name))
    }
}

circuit_node_extra_impl!(Rearrange, self_hash_default);

impl CircuitNodeComputeInfoImpl for Rearrange {}

impl CircuitNodeHashItems for Rearrange {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.spec.compute_hash());
    }
}

impl CircuitNode for Rearrange {
    circuit_node_auto_impl!("13204d30-2f12-4edd-8765-34bc8b458ef2");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![self
            .spec
            .input_ints
            .iter()
            .map(|ints| {
                if ints.len() != 1 {
                    return None;
                }
                self.spec.output_ints.iter().position(|z| z == ints)
            })
            .collect()]
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(children[0].clone(), (*self.spec).clone(), self.info().name)
    }
}

impl CircuitNodeAutoName for Rearrange {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self) -> Option<Name> {
        child_name_with_maybe_paren(&Self::PRIORITY, self.node())
            .map(|n| (n.string() + " rearrange").into())
    }
}

#[pymethods]
impl Rearrange {
    #[new]
    fn new_py(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Rearrange::try_new(node, spec, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    pub fn from_string(node: CircuitRc, string: &str, name: Option<Name>) -> Result<Self> {
        Rearrange::try_new(
            node,
            string
                .parse()
                .context("failed to construct spec for Rearrange::new_string")?,
            name,
        )
    }

    #[staticmethod]
    fn reshape(node: CircuitRc, shape: Shape) -> Result<Self> {
        let rank: u8 = node.rank().try_into().unwrap();
        let flat_rs = RearrangeSpec::flatten(rank);
        let unflat_rs = RearrangeSpec::unflatten(shape)?;

        Rearrange::try_new(
            Rearrange::try_new(node, flat_rs, None)?.rc(),
            unflat_rs,
            None,
        )
    }

    #[getter]
    pub fn node(&self) -> CircuitRc {
        self.info.children[0].clone()
    }

    pub fn conform_to_input_shape_spec(&self) -> RearrangeSpec {
        self.spec
            .conform_to_input_shape(self.node().shape())
            .unwrap()
    }

    pub fn conform_to_input_shape(&self) -> Self {
        Rearrange::try_new(self.node(), self.conform_to_input_shape_spec(), None).unwrap()
    }
}

/// Index indexes a node dimwise.
/// each axis can be Int, Slice, or 1-d tensor
/// and each 1-d tensor is iterated independently, unlike torch or numpy
/// tensor indices which are iterated together.

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Index {
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
}

impl Index {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, index: TensorIndex, name: Option<Name>) -> Result<Self> {
        let mut index = index;
        let node_rank = node.rank();
        match index.0.len().cmp(&node_rank) {
            Ordering::Greater => {
                bail!(IndexError::IndexRankTooHigh {
                    index_rank: index.0.len(),
                    node_rank,
                });
            }
            Ordering::Less => index.0.extend(vec![
                TensorAxisIndex::Slice(Slice {
                    start: None,
                    stop: None
                });
                node_rank - index.0.len()
            ]),
            _ => {}
        }

        let index = TensorIndex(
            index
                .0
                .into_iter()
                .map(|x| match x {
                    TensorAxisIndex::Tensor(tensor) => Ok(TensorAxisIndex::Tensor(
                        tensor.hashed()?.try_into().unwrap(),
                    )),
                    _ => Ok(x),
                })
                .collect::<Result<_>>()?,
        );

        index.validate(&node.info().shape)?;

        let out = Self {
            info: CachedCircuitInfo::with_device_dtype_extra(
                name,
                index.apply_to_shape(&node.info().shape),
                vec![node],
                &index
                    .0
                    .iter()
                    .filter_map(|x| match x {
                        TensorAxisIndex::Tensor(tensor) if !tensor.shape().is_empty() => {
                            let mut out: TorchDeviceDtypeOp = tensor.device_dtype().into();
                            out.dtype = None;
                            Some(out)
                        }
                        _ => None,
                    })
                    .collect::<Vec<_>>(),
            )?,
            index,
        };

        out.initial_init_info()
    }
}

circuit_node_extra_impl!(Index, self_hash_default);

impl CircuitNodeComputeInfoImpl for Index {}

impl CircuitNodeHashItems for Index {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.index.compute_hash());
    }
}

impl CircuitNode for Index {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        vec![zip(&self.node().info().shape, &self.index.0)
            .map(|(l, idx)| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(cur as usize)
                } else {
                    None
                }
            })
            .collect()]
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(children[0].clone(), self.index.clone(), self.info().name)
    }
}

impl CircuitNodeAutoName for Index {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self) -> Option<Name> {
        child_name_with_maybe_paren(&Self::PRIORITY, self.node())
            .map(|n| (n.string() + " idx").into())
    }
}

#[pymethods]
impl Index {
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<Index>> {
        let out = Index::try_new(node, index, name)?;

        Ok(out.into_init())
    }

    #[getter]
    pub fn node(&self) -> CircuitRc {
        self.info.children[0].clone()
    }

    // TODO: add support for synchronized index construction like python
    pub fn slice_edges_to_none(&self) -> Self {
        Index::try_new(
            self.node(),
            self.index.edges_to_none(&self.node().info().shape),
            self.info().name,
        )
        .unwrap()
    }
    #[staticmethod]
    pub fn new_synchronized_to_start(
        node: CircuitRc,
        index: TensorIndexSync, // tensor index
        name: Option<Name>,
    ) -> Result<Self> {
        let index: TensorIndex = index.0;
        // let broadcast_shape = broadc
        let (tensor_part_is, nontensor_part_is) = (
            (0..index.0.len() as u8)
                .filter(|i| matches!(&index.0[*i as usize], &TensorAxisIndex::Tensor(_)))
                .collect::<RInnerInts>(),
            (0..index.0.len() as u8)
                .filter(|i| !matches!(&index.0[*i as usize], &TensorAxisIndex::Tensor(_)))
                .collect::<RInnerInts>(),
        );
        if tensor_part_is.is_empty() {
            bail!(anyhow!(
                "index synchronized_to_start needs to have at least one tensor axis"
            ))
        }
        let rearranged_tensors_idxs_first = Rearrange::try_new(
            node.clone(),
            RearrangeSpec {
                input_ints: (0..index.0.len() as u8).map(|x| tu8v![x]).collect(),
                output_ints: std::iter::once(tensor_part_is.clone())
                    .chain(nontensor_part_is.iter().map(|x| tu8v![*x]))
                    .collect(),
                int_sizes: sv![Size::NONE;index.0.len()],
            },
            name.as_ref().map(|x| format!("{}_pre_idx_flat", x).into()),
        )?
        .rc();
        let tensors_index = TensorIndex(
            tensor_part_is
                .iter()
                .map(|x| index.0[*x as usize].clone())
                .collect(),
        );
        let broadcasted_tensor: IndexTensor = pycall!(
            atr!(
                pycall!(
                    PY_UTILS.just_join_indices_sync,
                    (
                        tensors_index.clone(),
                        Python::with_gil(|py| PyObject::from(PyTuple::new(
                            py,
                            tensor_part_is
                                .iter()
                                .map(|x| node.info().shape[*x as usize])
                                .collect::<Vec<_>>()
                        ))),
                        match &tensors_index.0[0] {
                            TensorAxisIndex::Tensor(t) => {
                                t.device_dtype().device
                            }
                            _ => panic!(),
                        }
                    ),
                    raw
                ),
                flatten,
                raw
            ),
            ()
        );
        let indexed = Index::try_new(
            rearranged_tensors_idxs_first,
            TensorIndex(vec![TensorAxisIndex::Tensor(broadcasted_tensor)]),
            name.as_ref().map(|x| format!("{}_t_idx", x).into()),
        )?
        .rc();
        let broadcasted_shape = broadcast_shapes(
            &tensors_index
                .0
                .iter()
                .map(|x| match x {
                    TensorAxisIndex::Tensor(t) => &t.shape()[..],
                    _ => panic!(),
                })
                .collect::<Vec<_>>(),
        )?;
        let rearranged_back = Rearrange::try_new(
            indexed,
            RearrangeSpec {
                input_ints: std::iter::once((0..broadcasted_shape.len() as u8).collect())
                    .chain(
                        (broadcasted_shape.len() as u8
                            ..broadcasted_shape.len() as u8 + nontensor_part_is.len() as u8)
                            .map(|x| tu8v![x]),
                    )
                    .collect(),
                output_ints: (0..broadcasted_shape.len() as u8 + nontensor_part_is.len() as u8)
                    .map(|x| tu8v![x])
                    .collect(),
                int_sizes: broadcasted_shape
                    .iter()
                    .copied()
                    .chain(nontensor_part_is.iter().map(|_| Size::NONE))
                    .collect(),
            },
            name.as_ref().map(|x| format!("{}_post_t_shape", x).into()),
        )?
        .rc();
        let nontensor_index: Vec<TensorAxisIndex> = nontensor_part_is
            .iter()
            .map(|i| index.0[*i as usize].clone())
            .collect();
        Index::try_new(
            rearranged_back,
            TensorIndex(
                vec![TensorAxisIndex::IDENT; broadcasted_shape.len()]
                    .into_iter()
                    .chain(nontensor_index)
                    .collect(),
            ),
            name,
        )
    }

    pub fn child_axis_map_including_slices(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        let result = vec![self
            .index
            .0
            .iter()
            .map(|idx| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if matches!(idx, TensorAxisIndex::Slice(_)) {
                    Some(cur as usize)
                } else {
                    None
                }
            })
            .collect()];
        result
    }

    /// this is the same as "is view (not copy) on child"
    pub fn has_tensor_axes(&self) -> bool {
        self.index
            .0
            .iter()
            .any(|x| matches!(x, TensorAxisIndex::Tensor(_)))
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Concat {
    #[pyo3(get)]
    pub axis: usize,
    info: CachedCircuitInfo,
}

impl Concat {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, axis: usize, name: Option<Name>) -> Result<Self> {
        if nodes.is_empty() {
            return Err(ConstructError::ConcatZeroNodes {}.into());
        }
        let mut shape = nodes[0].info().shape.clone();

        for node in &nodes[1..] {
            if node.ndim() != nodes[0].ndim() {
                return Err(ConstructError::ConcatShapeDifferent {
                    shapes: nodes.iter().map(|x| x.info().shape.clone()).collect(),
                }
                .into());
            }
            for (i, s) in node.info().shape.iter().enumerate() {
                if i != axis {
                    shape[i] = shape[i].join_eq(s, || {
                        anyhow!(ConstructError::ConcatShapeDifferent {
                            shapes: nodes.iter().map(|x| x.info().shape.clone()).collect()
                        })
                    })?;
                }
            }
        }

        shape[axis] = nodes.iter().map(|n| n.info().shape[axis]).sum();

        let out = Self {
            axis,
            info: CachedCircuitInfo::incomplete(name, shape, nodes)?,
        };
        out.initial_init_info()
    }

    fn convert_axis(nodes: &[CircuitRc], axis: i64, is_stack: bool) -> Result<usize> {
        if nodes.is_empty() {
            bail!(ConstructError::ConcatZeroNodes {})
        }
        let extra = if is_stack { 1 } else { 0 };
        Ok(check_canon_axes(nodes[0].rank() + extra, &[axis])?[0])
    }

    pub fn new_signed_axis(nodes: Vec<CircuitRc>, axis: i64, name: Option<Name>) -> Result<Concat> {
        let axis = Self::convert_axis(&nodes, axis, false)?;
        let out = Self::try_new(nodes, axis, name)?;
        Ok(out)
    }
}

circuit_node_extra_impl!(Concat, self_hash_default);

impl CircuitNodeComputeInfoImpl for Concat {}

impl CircuitNodeHashItems for Concat {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.axis.to_le_bytes());
    }
}

impl CircuitNode for Concat {
    circuit_node_auto_impl!("f2684583-c215-4f67-825e-6e4e51091ca7");

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(children, self.axis, self.info().name)
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![
            (0..self.rank())
                .map(|i| match i == self.axis {
                    true => None,
                    false => Some(i),
                })
                .collect();
            self.num_children()
        ]
    }
}

impl CircuitNodeAutoName for Concat {
    const PRIORITY: OperatorPriority = OperatorPriority::InfixAmbiguous {};

    fn auto_name(&self) -> Option<Name> {
        children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(|names| {
            names
                .iter()
                .map(|name| Self::shorten_child_name(name))
                .collect::<Vec<String>>()
                .join(" ++ ")
                .into()
        })
    }
}

#[pymethods]
impl Concat {
    #[new]
    #[pyo3(signature=(*nodes, axis, name = None))]
    fn new_py(
        nodes: Vec<CircuitRc>,
        axis: i64,
        name: Option<Name>,
    ) -> Result<PyClassInitializer<Concat>> {
        Self::new_signed_axis(nodes, axis, name).map(|x| x.into_init())
    }

    pub fn get_sizes_at_axis(&self) -> Vec<Size> {
        self.children().map(|x| x.info().shape[self.axis]).collect()
    }

    #[staticmethod]
    #[pyo3(signature=(*nodes, axis, name = None))]
    pub fn stack(nodes: Vec<CircuitRc>, axis: i64, name: Option<Name>) -> Result<Self> {
        let axis = Self::convert_axis(&nodes, axis, true)?;
        let to_cat = nodes
            .into_iter()
            .map(|c| {
                c.unsqueeze(
                    vec![axis],
                    c.info()
                        .name
                        .map(|s| format!("{}_unsqueeze_stack", s).into()),
                )
                .map(|x| x.rc())
            })
            .collect::<Result<_>>()
            .context("failed to unsqueeze for stack (axis invalid?)")?;
        Self::try_new(to_cat, axis, name).context("failed to concat for stack after unsqueeze")
    }
}

/// Scatter is equivalent to:
/// result = torch.zeros(shape)
/// result[index] = node.evaluate()
/// but index is considered dimwise
///
/// right now rewrites only work with slices, maybe will support others later
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Scatter {
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
}

impl Scatter {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<Name>,
    ) -> Result<Self> {
        let index = index.canonicalize(&shape);
        let index_shape = index.apply_to_shape(&shape);
        if index.all_uslices().is_none() || !shape_is_known(&shape) {
            return Err(ConstructError::ScatterIndexTypeUnimplemented { index }.into());
        }
        if !shape_eq_if_known(&index_shape, node.shape()) {
            return Err(ConstructError::ScatterShapeWrong {
                shape,
                index,
                index_shape,
            }
            .into());
        }

        let out = Self {
            index,
            info: CachedCircuitInfo::incomplete(name, shape, vec![node])?,
        };
        // todo check not too many axes / oob
        out.initial_init_info()
    }
}

circuit_node_extra_impl!(Scatter, self_hash_default);

impl CircuitNodeComputeInfoImpl for Scatter {}

impl CircuitNodeHashItems for Scatter {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.index.compute_hash());
        for i in &self.info().shape {
            hasher.update(&i.to_le_bytes());
        }
    }
}

impl CircuitNode for Scatter {
    circuit_node_auto_impl!("50cce6d3-457c-4f52-9a23-1903bdc76533");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        vec![zip(&self.info().shape, &self.index.0)
            .enumerate()
            .map(|(i, (l, idx))| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(i)
                } else {
                    None
                }
            })
            .collect()]
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(
            children[0].clone(),
            self.index.clone(),
            self.info().shape.clone(),
            self.info().name,
        )
    }
}

impl CircuitNodeAutoName for Scatter {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self) -> Option<Name> {
        child_name_with_maybe_paren(&Self::PRIORITY, self.node())
            .map(|n| (n.string() + " scatter").into())
    }
}

#[pymethods]
impl Scatter {
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<Scatter>> {
        let out = Scatter::try_new(node, index, shape, name)?;

        Ok(out.into_init())
    }

    #[getter]
    pub fn node(&self) -> CircuitRc {
        self.info.children[0].clone()
    }

    pub fn is_identity(&self) -> bool {
        shape_eq_and_known(self.shape(), self.node().shape()) && self.index.all_uslices().is_some()
    }
}

#[pyfunction]
pub fn flat_concat(circuits: Vec<CircuitRc>) -> Result<Concat> {
    let flatteneds = circuits
        .iter()
        .map(|x| -> Result<_> {
            Ok(Rearrange::try_new(
                x.clone(),
                RearrangeSpec::flatten_usize(x.rank())?,
                Some("flatten".into()),
            )
            .unwrap()
            .rc())
        })
        .collect::<Result<_>>()?;
    Ok(Concat::try_new(flatteneds, 0, Some("flat_concat".into())).unwrap())
}

#[pyfunction]
pub fn flat_concat_back(circuits: Vec<CircuitRc>) -> Result<(Concat, Vec<CircuitRc>)> {
    let flat = flat_concat(circuits.clone())?;
    let sections = flat.get_sizes_at_axis();
    if !sections.iter().all(|x| x.is_known()) {
        bail!("flat_concat_back: some concattands of unknown size {sections:?}")
    }
    let sections: Vec<usize> = sections.iter().map(|x| x.unwrap()).collect();
    let starts = cumsum(&sections);
    let out = (
        flat.clone(),
        zip(circuits, zip(starts, sections))
            .map(|(c, (start, sec))| {
                Ok(Rearrange::nrc(
                    Index::nrc(
                        flat.crc(),
                        TensorIndex(vec![TensorAxisIndex::new_plain_slice(start, start + sec)]),
                        None,
                    ),
                    RearrangeSpec::unflatten(c.info().shape.clone())?,
                    None,
                ))
            })
            .collect::<Result<_>>()?,
    );
    Ok(out)
}

/// input is shape (batch_dims..batch_dims, conv_dims..conv_dims, in_channels)
/// filter is shape (batch_dims_broadcastable_with_input..b,out_channels, conv_dims..conv_dims, in_channels)
/// some features this API can represent aren't actually supported yet bc pytorch
/// doesn't expose all options
/// Batch dims on filter aren't supported yet
/// different padding before and after not supported yet
#[pyclass(unsendable, extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Conv {
    #[pyo3(get)]
    pub stride: Vec<usize>,
    #[pyo3(get)]
    pub padding: Vec<(usize, usize)>,
    info: CachedCircuitInfo,
}

impl Conv {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: Vec<(usize, usize)>,
        name: Option<Name>,
    ) -> Result<Self> {
        let shape =
            rr_util::conv_shape::conv_shape(input.shape(), filter.shape(), &stride, &padding)?;

        let out = Self {
            stride,
            padding,
            info: CachedCircuitInfo::incomplete(name, shape, vec![input, filter])?,
        };
        // todo check not too many axes / oob
        out.initial_init_info()
    }
}

circuit_node_extra_impl!(Conv, self_hash_default);

impl CircuitNodeComputeInfoImpl for Conv {}
impl CircuitNodeHashItems for Conv {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        // this is ok because all looped over items are fixed len and we follow this with uuid (from children hash)
        for (i, (j, k)) in zip(&self.stride, &self.padding) {
            hasher.update(&i.to_le_bytes());
            hasher.update(&j.to_le_bytes());
            hasher.update(&k.to_le_bytes());
        }
    }
}

impl CircuitNode for Conv {
    circuit_node_auto_impl!("a329465f-a18f-4313-a2a6-51d8ebad7dd6");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        // todo: this doesn't state all available axis linkings
        vec![
            (0..self.input_batch_shape().len())
                .map(Some)
                .chain(vec![
                    None;
                    self.input().rank() - self.input_batch_shape().len()
                ])
                .collect(),
            vec![None; self.filter().rank()],
        ]
    }

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Self::try_new(
            children[0].clone(),
            children[1].clone(),
            self.stride.clone(),
            self.padding.clone(),
            self.info().name,
        )
    }
}

impl CircuitNodeAutoName for Conv {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self) -> Option<Name> {
        let input_name = self.input().info().name?;
        let filter_name = self.filter().info().name?;
        Some(format!("Conv({input_name}, {filter_name})").into())
    }
}

#[derive(FromPyObject)]
pub enum ConvPaddingShorthand {
    Single(usize),
    Symmetric(Vec<usize>),
    Full(Vec<(usize, usize)>),
}

impl ConvPaddingShorthand {
    pub fn expand(self, l: usize) -> Vec<(usize, usize)> {
        match self {
            ConvPaddingShorthand::Single(single) => vec![(single, single); l],
            ConvPaddingShorthand::Symmetric(sym) => sym.into_iter().map(|s| (s, s)).collect(),
            ConvPaddingShorthand::Full(full) => full,
        }
    }
}

#[pymethods]
impl Conv {
    #[new]
    #[pyo3(signature=(input, filter, stride, padding = ConvPaddingShorthand::Single(0), name = None))]
    fn new_py(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: ConvPaddingShorthand,
        name: Option<Name>,
    ) -> PyResult<PyClassInitializer<Conv>> {
        let padding = padding.expand(stride.len());
        let out = Conv::try_new(input, filter, stride, padding, name)?;

        Ok(out.into_init())
    }
    pub fn dims(&self) -> usize {
        self.stride.len()
    }
    pub fn input_batch_shape(&self) -> Shape {
        self.input().info().shape[..self.rank() - 1 - self.dims()]
            .iter()
            .cloned()
            .collect()
    }
    #[getter]
    pub fn input(&self) -> CircuitRc {
        self.info.children[0].clone()
    }
    #[getter]
    pub fn filter(&self) -> CircuitRc {
        self.info.children[1].clone()
    }
}
