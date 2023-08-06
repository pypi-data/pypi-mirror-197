use std::{
    cmp::Ordering,
    iter::{once, zip},
};

use anyhow::Result;
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{name::Name, rearrange_spec::RearrangeSpec, shape::Size, sv, tu8v, util::cumsum};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    auto_name::OperatorPriority,
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    new_rc, Add, CachedCircuitInfo, CircuitFlags, CircuitNode, CircuitNodeAutoName, CircuitRc,
    ConstructError, Einsum, PyCircuitBase, Rearrange, Scalar,
};

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Cumulant {
    info: CachedCircuitInfo,
}

pub fn circuit_order_cmp_name_first(a: &CircuitRc, b: &CircuitRc) -> Ordering {
    a.info().name.cmp(&b.info().name).then(a.cmp(b))
}

impl Cumulant {
    #[apply(new_rc)]
    pub fn new(nodes: Vec<CircuitRc>, name: Option<Name>) -> (Self) {
        let out = Self {
            info: CachedCircuitInfo::incomplete(
                name,
                nodes.iter().flat_map(|c| c.info().shape.clone()).collect(),
                nodes,
            )
            .unwrap(),
        };
        out.initial_init_info().unwrap()
    }

    pub fn new_canon(nodes: Vec<CircuitRc>, name: Option<Name>) -> Self {
        let mut sorting_perm: Vec<usize> = (0..nodes.len()).collect();
        sorting_perm.sort_by(|a, b| circuit_order_cmp_name_first(&nodes[*a], &nodes[*b]));

        let nodes_sorted = sorting_perm.iter().map(|i| nodes[*i].clone()).collect();
        Cumulant::new(
            nodes_sorted,
            name.map(|i| ("canon ".to_owned() + &i).into()),
        )
    }
}

circuit_node_extra_impl!(Cumulant, self_hash_default);

impl CircuitNodeComputeInfoImpl for Cumulant {
    // default impl of compute can_be_sampled + is_explicitly_computable is fine

    fn compute_flags(&self) -> CircuitFlags {
        self.compute_flags_default() | CircuitFlags::IS_CONSTANT
    }
}

impl CircuitNodeHashItems for Cumulant {}

impl CircuitNode for Cumulant {
    circuit_node_auto_impl!("0954a2b9-e138-480d-b967-305cfc6c5a2b");

    fn _replace_children(&self, children: Vec<CircuitRc>) -> Result<Self> {
        Ok(Self::new(children, self.info().name))
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut place = 0;
        self.children()
            .map(|child| {
                let rank = child.rank();
                place += rank;
                (place - rank..place).map(|i| Some(i)).collect()
            })
            .collect()
    }
}

impl CircuitNodeAutoName for Cumulant {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self) -> Option<Name> {
        if self.children().any(|x| x.info().name.is_none()) {
            None
        } else {
            Some(
                format!(
                    "K{}({})",
                    self.num_children(),
                    self.children()
                        .map(|x| Self::shorten_child_name(x.info().name.unwrap().str()))
                        .collect::<Vec<String>>()
                        .join(", ")
                )
                .into(),
            )
        }
    }
}

#[pymethods]
impl Cumulant {
    #[new]
    #[pyo3(signature=(*nodes, name = None))]
    fn new_py(nodes: Vec<CircuitRc>, name: Option<Name>) -> PyResult<PyClassInitializer<Cumulant>> {
        let out = Cumulant::new(nodes, name);

        Ok(out.into_init())
    }

    /// Make a cumulant where the nodes are in canonical order, then rearrange to the specified order
    #[staticmethod]
    #[pyo3(signature=(*nodes, name = None))]
    pub fn new_canon_rearrange(nodes: Vec<CircuitRc>, name: Option<Name>) -> Result<Rearrange> {
        let mut sorting_perm: Vec<usize> = (0..nodes.len()).collect();
        sorting_perm.sort_by(|a, b| circuit_order_cmp_name_first(&nodes[*a], &nodes[*b]));

        let nodes_sorted = sorting_perm.iter().map(|i| nodes[*i].clone()).collect();
        let cum = Cumulant::new(
            nodes_sorted,
            name.map(|i| ("canon ".to_owned() + &i).into()),
        );
        let sections = nodes.iter().map(|child| child.rank()).collect::<Vec<_>>();
        let perm_blocks = permutation_from_block_permutation(sorting_perm, sections);
        Rearrange::try_new(
            cum.crc(),
            RearrangeSpec::new(
                perm_blocks
                    .into_iter()
                    .map(|i| Ok(tu8v![i.try_into()?]))
                    .collect::<Result<_>>()?,
                (0..cum.rank())
                    .map(|i| Ok(tu8v![i.try_into()?]))
                    .collect::<Result<_>>()?,
                sv![Size::NONE;cum.rank()],
            )
            .unwrap(),
            name,
        )
    }

    #[getter]
    pub fn cumulant_number(&self) -> usize {
        self.num_children()
    }

    pub fn equivalent_explicitly_computable_circuit(&self) -> Result<CircuitRc> {
        if self.info().is_explicitly_computable() {
            return match self.children_sl() {
                [] => Ok(Scalar::nrc(0.0, sv![], None)),
                [x] => Ok(x.clone()),
                _ => Ok(Scalar::nrc(0.0, self.info().shape.clone(), None)),
            };
        }
        Err(ConstructError::NoEquivalentExplicitlyComputable {}.into())
    }

    /// formula from https://en.wikipedia.org/wiki/Cumulant#Joint_cumulants
    pub fn basic_expectation(&self) -> CircuitRc {
        let partition_circuits = partitions(self.num_children())
            .map(|partition| {
                let multiplier = Scalar::nrc(CUMULANT_MULTIPLIERS[partition.len()], sv![], None);
                let expectations = partition.iter().map(|x| {
                    product_expectation(x.iter().map(|i| self.children_sl()[*i].clone()).collect())
                        .rc()
                });
                let node_permutation: Vec<usize> = partition.iter().flatten().cloned().collect();
                let idx_permutation = permutation_from_block_permutation(
                    node_permutation.clone(),
                    node_permutation
                        .iter()
                        .map(|i| self.children_sl()[*i].rank())
                        .collect(),
                );
                Einsum::new_outer_product(
                    expectations.chain(once(multiplier)).collect(),
                    None,
                    Some(idx_permutation),
                )
                .rc()
            })
            .collect();
        Add::nrc(partition_circuits, None)
    }

    // /// source: https://arxiv.org/pdf/1701.05420.pdf
    // pub fn factored_cumulant_expectation_and_aux(&self)->(CircuitRc,Cumulant,Vec<CircuitRc>){
    //     if self.nodes.len()<=1{
    //         return (self.clone(),self.clone(),vec![])
    //     }
    //     centered_mom = Cumulant::new()
    // }
    // pub fn factored_cumulant_expectation(&self)->CircuitRc{
    //     self.factored_cumulant_expectation_and_aux().0
    // }

    // def factored_cumulant_expectation_rewrite_full(
    //     cumulant: Cumulant, apply_to_nested: Callable[[Cumulant], Circuit] = lambda x: x
    // ) -> Tuple[Circuit, Cumulant, List[Circuit]]:
    //     """source: https://arxiv.org/pdf/1701.05420.pdf"""
    //     if len(cumulant.circuits) <= 1:
    //         return cumulant, cumulant, []

    //     centered_mom = Cumulant(
    //         (centered_product(*cumulant.circuits, apply_to_centering=apply_to_nested),),
    //         name=f"{cumulant.name}_centered_moment",
    //     )
    //     sub: List[Circuit] = []

    //     for p in partition(list(enumerate(cumulant.circuits))):
    //         if any(len(b) < 2 for b in p) or len(p) == 1:
    //             continue

    //         cumulants = [Cumulant.from_spec(CircuitMultiset.from_values(x[1] for x in b)).rename_to_canonical() for b in p]

    //         permutation = dim_permutation_for_circuits(p, [m.circuits for m in cumulants], len(cumulant.circuits))

    //         new_out = Einsum.outer_product(*cumulants, out_axes_permute=permutation)
    //         assert new_out.shape == tuple(itertools.chain.from_iterable(c.shape for c in cumulant.circuits))
    //         sub.append(new_out)

    //     return (
    //         Add.from_weighted_nodes([(centered_mom, 1.0), *[(v, -1.0) for v in sub]], name=f"{cumulant.name}_decompose"),
    //         centered_mom,
    //         sub,
    //     )

    // def factored_cumulant_expectation_rewrite(
    //     cumulant: Cumulant, apply_to_nested: Callable[[Cumulant], Circuit] = lambda x: x
    // ) -> Circuit:
    //     return factored_cumulant_expectation_rewrite_full(cumulant, apply_to_nested=apply_to_nested)[0]
}

pub fn product_expectation(nodes: Vec<CircuitRc>) -> Cumulant {
    let product = Einsum::new_outer_product(nodes, None, None).rc();
    Cumulant::new(vec![product], None)
}
/// this uses lots of boxed iterators. this may be faster, but is annoying and confusing.
pub fn partitions(n: usize) -> Box<dyn Iterator<Item = Vec<Vec<usize>>>> {
    match n {
        0 => Box::new(once(vec![])),
        1 => Box::new(once(vec![vec![0]])),
        _ => {
            let first = n - 1;
            let smallers = partitions(n - 1);
            Box::new(smallers.flat_map(move |smaller| {
                let smaller_copy = smaller.clone(); // for borrow checker reasons
                Box::new(
                    smaller
                        .clone()
                        .into_iter()
                        .enumerate()
                        .map(move |(i, subset)| {
                            smaller_copy
                                .clone()
                                .into_iter()
                                .take(i)
                                .chain(once(subset.iter().cloned().chain(once(first)).collect()))
                                .chain(smaller_copy.clone().into_iter().skip(i + 1))
                                .collect()
                        })
                        .chain(once(smaller.into_iter().chain([vec![first]]).collect())),
                )
            }))
        }
    }
}

pub fn permutation_from_block_permutation(
    permutation: Vec<usize>,
    block_sizes: Vec<usize>,
) -> Vec<usize> {
    let starts = cumsum(&block_sizes);
    permutation
        .iter()
        .flat_map(|i| (starts[*i]..starts[*i] + block_sizes[*i]))
        .collect()
}

pub fn dim_permutation_for_circuits(
    indexed_orig_partitions: Vec<Vec<(usize, CircuitRc)>>,
    partitions_orderings: Vec<&[CircuitRc]>,
    count: usize,
) -> Vec<usize> {
    let mut permutation_segments: Vec<Option<Vec<usize>>> = vec![None; count];
    let mut running_offset = 0;

    for (b, m) in zip(indexed_orig_partitions, partitions_orderings) {
        let mut b_to_idxs: HashMap<CircuitRc, Vec<usize>> = HashMap::default();

        for (i, y) in b {
            (*b_to_idxs.entry(y).or_insert(vec![])).push(i);
        }

        for x in m {
            let next_idx = b_to_idxs.get_mut(x).unwrap().pop().unwrap();
            permutation_segments[next_idx] =
                Some((running_offset..(running_offset + x.rank())).collect());
            running_offset += x.rank();
        }
    }

    let mut r = vec![];
    for segment in permutation_segments {
        r.extend(segment.unwrap())
    }
    r
}

#[test]
fn test_permutation_to_block() {
    dbg!(permutation_from_block_permutation(
        vec![1, 0, 2],
        vec![1, 2, 3]
    ));
}

#[test]
fn test_partition() {
    let r: Vec<_> = partitions(3).collect();
    dbg!(&r);
}

/// CUMULANT_MULTIPLIERS[i] = i!*(-1)^i
#[rustfmt::skip]
static CUMULANT_MULTIPLIERS:[f64;64] = [1.0, -1.0, 2.0, -6.0, 24.0, -120.0, 720.0, -5040.0, 40320.0, -362880.0, 3628800.0, -39916800.0, 479001600.0, -6227020800.0, 87178291200.0, -1307674368000.0, 20922789888000.0, -355687428096000.0, 6402373705728000.0, -1.21645100408832e+17, 2.43290200817664e+18, -5.109_094_217_170_944e19, 1.124_000_727_777_607_7e21, -2.585_201_673_888_498e22, 6.204_484_017_332_394e23, -1.551_121_004_333_098_6e25, 4.032_914_611_266_056_5e26, -1.088_886_945_041_835_2e28, 3.048_883_446_117_138_7e29, -8.841_761_993_739_702e30, 2.652_528_598_121_910_7e32, -8.222_838_654_177_922e33, 2.631_308_369_336_935e35, -8.683_317_618_811_886e36, 2.952_327_990_396_041_6e38, -1.033_314_796_638_614_5e40, 3.719_933_267_899_012_5e41, -1.376_375_309_122_634_6e43, 5.230_226_174_666_011e44, -2.039_788_208_119_744_4e46, 8.159_152_832_478_977e47, -3.345_252_661_316_381e49, 1.40500611775288e+51, -6.041_526_306_337_383e52, 2.658_271_574_788_449e54, -1.196_222_208_654_801_9e56, 5.502_622_159_812_089e57, -2.586_232_415_111_681_8e59, 1.241_391_559_253_607_3e61, -6.082_818_640_342_675e62, 3.041_409_320_171_337_6e64, -1.551_118_753_287_382_2e66, 8.065_817_517_094_388e67, -4.274_883_284_060_025_5e69, 2.308_436_973_392_414e71, -1.269_640_335_365_827_6e73, 7.109_985_878_048_635e74, -4.052_691_950_487_721_4e76, 2.350_561_331_282_878_5e78, -1.386_831_185_456_898_4e80, 8.32098711274139e+81, -5.075_802_138_772_248e83, 3.146_997_326_038_794e85, -1.98260831540444e+87];
