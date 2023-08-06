use std::{
    fmt,
    fmt::{Debug, Write},
    hash::{Hash, Hasher},
    iter,
    sync::Mutex,
};

use anyhow::{bail, Context, Error, Result};
use circuit_base::{
    cached_circuit_properties::max_non_leaf_size,
    circuit_utils::{count_nodes, total_flops},
    generalfunction::SpecTrait,
    opaque_iterative_matcher::{
        get_opaque_type_matcher, OpaqueIterativeMatcher, OpaqueIterativeMatcherVal,
    },
    prelude::*,
    CircuitType,
};
use itertools::Itertools;
use num_bigint::BigUint;
use pyo3::{once_cell::GILLazy, prelude::*};
use rr_util::{
    clicolor, fn_struct,
    name::Name,
    print::{color, last_child_arrows, oom_fmt, CliColor},
    py_types::MaybeNotSet,
    python_println,
    tensor_db::write_tensor_to_dir_tree,
    util::{HashBytes, ALPHABET},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use crate::parsing::{get_reference_circuits, ParseCircuitError};

#[allow(non_snake_case)]
pub fn PrintOptions_repr(x: Option<PyObject>, y: CircuitRc) -> Result<String> {
    Python::with_gil(|py| {
        x.map_or_else(|| Ok(Default::default()), |x| x.extract::<PrintOptions>(py))?
            .repr(y)
    })
}

// see also rr_util::print
const DOWN_ELBOW: &str = "┌";
const HORIZ_BAR: &str = "─";
const UP_ELBOW: &str = "└";

fn_struct!(pub CircuitToColorCode:Fn(circuit:CircuitRc)->CliColor);
fn_struct!(pub CircuitCommenter:Fn(circuit:CircuitRc)->String);

#[pyclass]
#[derive(Clone)]
pub struct PrintOptions {
    #[pyo3(get, set)]
    pub bijection: bool,
    #[pyo3(get)]
    pub reference_circuits: HashMap<CircuitRc, Name>, /* TODO: make a checking setter for me as needed */
    #[pyo3(get, set)]
    pub shape_only_when_necessary: bool,
    pub traversal: Option<OpaqueIterativeMatcherVal>,
    #[pyo3(get, set)]
    pub leaves_on_top: bool,
    #[pyo3(get, set)]
    pub arrows: bool,
    #[pyo3(get, set)]
    pub force_use_serial_numbers: bool,
    #[pyo3(get, set)]
    pub number_leaves: bool,
    #[pyo3(get, set)]
    pub colorer: Option<CircuitToColorCode>,
    #[pyo3(get, set)]
    pub comment_arg_names: bool,
    #[pyo3(get, set)]
    pub commenters: Vec<CircuitCommenter>,
    #[pyo3(get, set)]
    pub sync_tensors: bool,
    #[pyo3(get, set)]
    pub seen_children_same_line: bool,
    #[pyo3(get, set)]
    pub only_child_below: bool,
    #[pyo3(get, set)]
    pub tensor_index_literal: bool,
    #[pyo3(get, set)]
    pub show_all_named_axes: bool,
    #[pyo3(get, set)]
    pub tensor_save_dir: Option<String>,
}

impl Default for PrintOptions {
    fn default() -> Self {
        Self {
            bijection: true,
            reference_circuits: Default::default(),
            shape_only_when_necessary: true,
            traversal: None,
            leaves_on_top: false,
            arrows: false,
            force_use_serial_numbers: false,
            number_leaves: false,
            colorer: None,
            comment_arg_names: false,
            commenters: vec![],
            sync_tensors: false,
            seen_children_same_line: false,
            only_child_below: false,
            tensor_index_literal: false,
            show_all_named_axes: false,
            tensor_save_dir: None,
        }
        .validate_ret()
        .unwrap()
    }
}

impl PrintOptions {
    pub fn repr(&self, circuit: CircuitRc) -> Result<String> {
        self.repr_circuits(vec![circuit])
    }
    pub fn print(&self, circuit: CircuitRc) -> Result<()> {
        self.print_circuits(vec![circuit])
    }
    pub fn repr_depth(circuit: CircuitRc, end_depth: usize) -> String {
        Self::repr_circuits_depth(vec![circuit], end_depth)
    }
    pub fn print_depth(circuit: CircuitRc, end_depth: usize) {
        Self::print_circuits_depth(vec![circuit], end_depth)
    }
    pub fn validate_ret(self) -> Result<Self> {
        self.validate()?;
        Ok(self)
    }

    /// returns whether or not we finished here
    pub fn repr_full_line(
        &self,
        circ: &Circuit,
        result: &mut String,
        seen_hashes: &mut HashMap<HashBytes, (String, String)>,
        runnning_serial_number: &mut usize,
        disallow_name_ident: Option<&HashMap<Name, bool>>,
    ) -> Result<bool> {
        if let Some(ident) = self.reference_circuits.get(&circ.clone().rc()) {
            result.push_str(&self.string_escape(ident));
            return Ok(true);
        }

        let mut repeat_info = None; // only matters for 'print_as_tree';
        if let Some((rep_str, line_prefix)) = seen_hashes.get(&circ.info().hash) {
            if !self.is_print_as_tree() {
                result.push_str(rep_str);
                return Ok(true);
            } else {
                repeat_info = Some((rep_str.clone(), line_prefix.clone()));
            }
        }

        // allow_name_ident is_some iff !self.force_use_serial_numbers
        let disallow_name = disallow_name_ident
            .zip(circ.info().name)
            .map(|(map, name)| map[&name])
            .unwrap_or(true);

        let (repeat_string, line_prefix) = match (
            repeat_info,
            disallow_name,
            circ.info().name.map(|z| z.str()),
        ) {
            (Some(x), _, _) => x,
            (None, true, Some(name)) => {
                let escaped = self.string_escape(name);
                let this_serial_number = runnning_serial_number.to_string();
                *runnning_serial_number += 1;
                let out = this_serial_number + " " + &escaped;
                (out.clone(), out)
            }
            (None, false, Some(name)) => {
                let escaped = self.string_escape(name);
                (escaped.clone(), escaped)
            }
            (None, true, None) => {
                let this_serial_number = runnning_serial_number.to_string();
                *runnning_serial_number += 1;
                (
                    this_serial_number.clone() + " " + &circ.variant_string(),
                    this_serial_number,
                )
            }

            (None, false, None) => unreachable!(),
        };

        result.push_str(&line_prefix);

        seen_hashes.insert(circ.info().hash, (repeat_string, line_prefix));

        result.push_str(
            &self
                .repr_line_info(circ.clone().rc())
                .with_context(|| format!("repr line info failed for circuit={:?}", circ))?,
        );

        Ok(false)
    }

    pub fn has_child_info(&self, circ: &Circuit) -> bool {
        circ.is_module() && circ.num_children() > 0
    }

    pub fn get_child_info(
        &self,
        circ: &Circuit,
        seen_hashes: &mut HashMap<HashBytes, (String, String)>,
        runnning_serial_number: &mut usize,
        disallow_name_ident: Option<&HashMap<Name, bool>>,
        child_idx: usize,
    ) -> Option<String> {
        if let Some(m) = circ.as_module() {
            if child_idx == 0 {
                return None;
            }

            let arg_spec = &m.spec.arg_specs[child_idx - 1];
            let mut result = String::new();
            self.repr_full_line(
                &arg_spec.symbol.clone().c(),
                &mut result,
                seen_hashes,
                runnning_serial_number,
                disallow_name_ident,
            )
            .unwrap();

            if !(arg_spec.batchable && arg_spec.expandable && arg_spec.ban_non_symbolic_size_expand)
            {
                result.push_str(&format!(
                    " {}{}{}",
                    TerseBool(arg_spec.batchable),
                    TerseBool(arg_spec.expandable),
                    TerseBool(arg_spec.ban_non_symbolic_size_expand)
                ));
            }

            Some(result)
        } else {
            None
        }
    }
}

const DEFAULT_END_DEPTH: usize = 2;

#[derive(Debug, Clone)]
pub struct TerseBool(pub bool);

impl fmt::Display for TerseBool {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(if self.0 { "t" } else { "f" })
    }
}
impl std::str::FromStr for TerseBool {
    type Err = Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let out = match s {
            "t" => true,
            "f" => false,
            _ => bail!(ParseCircuitError::InvalidTerseBool { got: s.to_owned() }),
        };
        Ok(TerseBool(out))
    }
}
impl TryFrom<char> for TerseBool {
    type Error = Error;
    fn try_from(value: char) -> Result<Self, Self::Error> {
        let out = match value {
            't' => true,
            'f' => false,
            _ => bail!(ParseCircuitError::InvalidTerseBool {
                got: value.to_string()
            }),
        };
        Ok(TerseBool(out))
    }
}

pub fn op_traversal_per(
    op_traversal: Option<OpaqueIterativeMatcherVal>,
    circ: CircuitRc,
) -> Result<Option<Vec<Option<OpaqueIterativeMatcherVal>>>> {
    let num_children = circ.num_children();
    let new_traversal_per = if let Some(traversal) = op_traversal {
        let updated = traversal
            .opaque_match_iterate(circ.crc())?
            .updated
            .unwrap_or_else(|| Some(traversal).into());
        if updated.all_finished() {
            return Ok(None);
        }
        updated
            .per_child_with_term(num_children)
            .into_iter()
            .map(Some)
            .collect()
    } else {
        vec![None; num_children]
    };
    Ok(Some(new_traversal_per))
}

#[pymethods]
impl PrintOptions {
    // new function for rust and python (in rust for validation)
    #[new]
    #[pyo3(signature=(
        bijection = PrintOptions::default().bijection,
        reference_circuits = PrintOptions::default().reference_circuits,
        reference_circuits_by_name = vec![],
        shape_only_when_necessary = PrintOptions::default().shape_only_when_necessary,
        traversal = None,
        leaves_on_top = PrintOptions::default().leaves_on_top,
        arrows = PrintOptions::default().arrows,
        force_use_serial_numbers = PrintOptions::default().force_use_serial_numbers,
        number_leaves = PrintOptions::default().number_leaves,
        colorer = None,
        comment_arg_names = PrintOptions::default().comment_arg_names,
        commenters = PrintOptions::default().commenters,
        sync_tensors = PrintOptions::default().sync_tensors,
        seen_children_same_line = PrintOptions::default().seen_children_same_line,
        only_child_below = PrintOptions::default().only_child_below,
        tensor_index_literal = PrintOptions::default().tensor_index_literal,
        show_all_named_axes = PrintOptions::default().show_all_named_axes,
        tensor_save_dir = None
    ))]
    pub fn new(
        bijection: bool,
        reference_circuits: HashMap<CircuitRc, Name>,
        reference_circuits_by_name: Vec<CircuitRc>,
        shape_only_when_necessary: bool,
        traversal: Option<OpaqueIterativeMatcherVal>,
        leaves_on_top: bool,
        arrows: bool,
        force_use_serial_numbers: bool,
        number_leaves: bool,
        colorer: Option<CircuitToColorCode>,
        comment_arg_names: bool,
        commenters: Vec<CircuitCommenter>,
        sync_tensors: bool,
        seen_children_same_line: bool,
        only_child_below: bool,
        tensor_index_literal: bool,
        show_all_named_axes: bool,
        tensor_save_dir: Option<String>,
    ) -> Result<Self> {
        let result = Self {
            bijection,
            reference_circuits: get_reference_circuits(
                reference_circuits
                    .into_iter()
                    .map(|(a, b)| (b, a))
                    .collect(),
                reference_circuits_by_name,
            )?
            .into_iter()
            .map(|(a, b)| (b, a))
            .collect(),
            shape_only_when_necessary,
            traversal,
            leaves_on_top,
            arrows,
            force_use_serial_numbers,
            number_leaves,
            colorer,
            comment_arg_names,
            commenters,
            sync_tensors,
            seen_children_same_line,
            only_child_below,
            tensor_index_literal,
            show_all_named_axes,
            tensor_save_dir,
        };
        result.validate()?;
        Ok(result)
    }

    #[pyo3(signature=(
        bijection = Default::default(),
        reference_circuits = Default::default(),
        shape_only_when_necessary = Default::default(),
        traversal = Default::default(),
        leaves_on_top = Default::default(),
        arrows = Default::default(),
        force_use_serial_numbers = Default::default(),
        number_leaves = Default::default(),
        colorer = Default::default(),
        comment_arg_names = Default::default(),
        commenters = Default::default(),
        sync_tensors = Default::default(),
        seen_children_same_line = Default::default(),
        only_child_below = Default::default(),
        tensor_index_literal = Default::default(),
        show_all_named_axes = Default::default(),
        tensor_save_dir = Default::default()
    ))]
    pub fn evolve(
        &self,
        bijection: MaybeNotSet<bool>,
        reference_circuits: MaybeNotSet<HashMap<CircuitRc, Name>>,
        shape_only_when_necessary: MaybeNotSet<bool>,
        traversal: MaybeNotSet<Option<OpaqueIterativeMatcherVal>>,
        leaves_on_top: MaybeNotSet<bool>,
        arrows: MaybeNotSet<bool>,
        force_use_serial_numbers: MaybeNotSet<bool>,
        number_leaves: MaybeNotSet<bool>,
        colorer: MaybeNotSet<Option<CircuitToColorCode>>,
        comment_arg_names: MaybeNotSet<bool>,
        commenters: MaybeNotSet<Vec<CircuitCommenter>>,
        sync_tensors: MaybeNotSet<bool>,
        seen_children_same_line: MaybeNotSet<bool>,
        only_child_below: MaybeNotSet<bool>,
        tensor_index_literal: MaybeNotSet<bool>,
        show_all_named_axes: MaybeNotSet<bool>,
        tensor_save_dir: MaybeNotSet<Option<String>>,
    ) -> Result<Self> {
        let cloned = self.clone();
        Self::new(
            bijection.0.unwrap_or(cloned.bijection),
            reference_circuits.0.unwrap_or(cloned.reference_circuits),
            vec![],
            shape_only_when_necessary
                .0
                .unwrap_or(cloned.shape_only_when_necessary),
            traversal.0.unwrap_or(cloned.traversal),
            leaves_on_top.0.unwrap_or(cloned.leaves_on_top),
            arrows.0.unwrap_or(cloned.arrows),
            force_use_serial_numbers
                .0
                .unwrap_or(cloned.force_use_serial_numbers),
            number_leaves.0.unwrap_or(cloned.number_leaves),
            colorer.0.unwrap_or(cloned.colorer),
            comment_arg_names.0.unwrap_or(cloned.comment_arg_names),
            commenters.0.unwrap_or(cloned.commenters),
            sync_tensors.0.unwrap_or(cloned.sync_tensors),
            seen_children_same_line
                .0
                .unwrap_or(cloned.seen_children_same_line),
            only_child_below.0.unwrap_or(cloned.only_child_below),
            tensor_index_literal
                .0
                .unwrap_or(cloned.tensor_index_literal),
            show_all_named_axes.0.unwrap_or(cloned.show_all_named_axes),
            tensor_save_dir.0.unwrap_or(cloned.tensor_save_dir),
        )
    }

    #[getter(traversal)]
    pub fn py_get_traversal(&self) -> PyObject {
        OpaqueIterativeMatcherVal::op_to_object(&self.traversal)
    }

    #[setter(traversal)]
    pub fn py_set_traversal(&mut self, traversal: Option<OpaqueIterativeMatcherVal>) {
        self.traversal = traversal
    }

    #[staticmethod]
    pub fn compiler_default() -> PrintOptions {
        Self {
            force_use_serial_numbers: true,
            ..Default::default()
        }
        .validate_ret()
        .unwrap()
    }

    #[staticmethod]
    #[pyo3(signature=(end_depth = DEFAULT_END_DEPTH))]
    pub fn debug_default(end_depth: Option<usize>) -> PrintOptions {
        Self {
            bijection: false,
            shape_only_when_necessary: false,
            traversal: end_depth.map(OpaqueIterativeMatcherVal::for_end_depth),
            ..Default::default()
        }
        .validate_ret()
        .unwrap()
    }

    #[staticmethod]
    pub fn type_nest_default(
        circuit_type: CircuitType,
        traversal: Option<OpaqueIterativeMatcherVal>,
    ) -> PrintOptions {
        Self {
            bijection: false,
            number_leaves: true,
            traversal: Some(get_opaque_type_matcher(circuit_type, traversal)),
            ..Default::default()
        }
        .validate_ret()
        .unwrap()
    }

    #[staticmethod]
    pub fn einsum_nest_default(traversal: Option<OpaqueIterativeMatcherVal>) -> PrintOptions {
        Self::type_nest_default(CircuitType::Einsum, traversal)
    }

    #[staticmethod]
    pub fn add_nest_default(traversal: Option<OpaqueIterativeMatcherVal>) -> PrintOptions {
        Self::type_nest_default(CircuitType::Add, traversal)
    }

    #[getter]
    pub fn is_print_as_tree(&self) -> bool {
        // other configuration might require printing as tree
        self.number_leaves
    }

    pub fn validate(&self) -> Result<()> {
        if self.bijection && self.leaves_on_top {
            bail!("bijection print cant have leaves on top")
        }
        if self.bijection && self.traversal.is_some() {
            bail!("bijection print cant terminate early, so traversal must be None")
        }
        if self.bijection && self.seen_children_same_line {
            bail!("bijection doesn't support seen children same line, but technically could")
        }
        if self.bijection && self.tensor_index_literal {
            bail!("bijection doesn't support index tensor literal")
        }
        if self.seen_children_same_line && (self.comment_arg_names || !self.commenters.is_empty()) {
            bail!("children same line + commenting (arg names, commenter) not supported")
        }
        if self.bijection && self.is_print_as_tree() {
            bail!("bijection print can't print as tree (caused by number_leaves)")
        }
        Ok(())
    }

    #[pyo3(name = "print", signature=(*circuits))]
    pub fn print_circuits(&self, circuits: Vec<CircuitRc>) -> Result<()> {
        python_println!("{}", self.repr_circuits(circuits)?);
        Ok(())
    }

    pub fn string_escape(&self, name: &str) -> String {
        if self.bijection {
            format!("'{}'", name.replace('\\', r"\\").replace('\'', r"\'"))
        } else {
            name.to_owned()
        }
    }

    pub fn repr_line_info(&self, circ: CircuitRc) -> Result<String> {
        let mut result = "".to_owned();

        if self.bijection && !circ.info().use_autoname() {
            result.push_str(" AD");
        }

        if !self.shape_only_when_necessary
            || matches!(
                &**circ,
                Circuit::Scalar(_)
                    | Circuit::Scatter(_)
                    | Circuit::Symbol(_)
                    | Circuit::Array(_)
                    | Circuit::Index(_)
            )
            || self.show_all_named_axes && !circ.info().named_axes.is_empty()
        {
            result.push_str(&format!(
                " [{}]",
                (0..circ.rank())
                    .map(|x| match circ.info().named_axes.get(&(x as u8)) {
                        None => circ.shape()[x].to_string(),
                        Some(s) => format!("{}:{}", s, circ.shape()[x]),
                    })
                    .collect::<Vec<_>>()
                    .join(",")
            ))
        }
        result.push(' ');
        let variant_string = circ.variant_string();
        let vs: &str = &variant_string;
        result.push_str(vs);
        result.push(' ');
        result.push_str(&self.repr_extra_info(circ)?);

        for _ in 0..2 {
            result = result
                .strip_suffix(' ')
                .map(|x| x.to_owned())
                .unwrap_or(result); // remove trailing spaces
        }
        Ok(result)
    }
    pub fn repr_extra_info(&self, circ: CircuitRc) -> Result<String> {
        Ok(match &**circ {
            Circuit::Scalar(scalar) => {
                format!("{}", scalar.value)
            }
            Circuit::Rearrange(rearrange) => rearrange.spec.to_maybe_fancy_einops_string(
                rearrange.node().info().named_axes.clone(),
                rearrange.info().named_axes.clone(),
            ),
            Circuit::Einsum(einsum) => einsum.get_spec().to_maybe_fancy_string(
                einsum.info().named_axes.clone(),
                einsum
                    .children()
                    .map(|c| c.info().named_axes.clone())
                    .collect(),
            ),
            Circuit::Index(index) => {
                if self.bijection || self.tensor_index_literal {
                    index.index.repr_bijection(self.tensor_index_literal)?
                } else {
                    format!("{}", index.index)
                }
            }
            Circuit::Scatter(scatter) => {
                if self.bijection {
                    scatter.index.repr_bijection(self.tensor_index_literal)?
                } else {
                    format!("{}", scatter.index)
                }
            }
            Circuit::Concat(concat) => concat.axis.to_string(),
            Circuit::GeneralFunction(gf) => {
                if self.bijection {
                    gf.spec
                        .serialize()
                        .context("failed to get general function spec serialize in print, maybe you want circ.print(rust_circuit.PrintOptions(bijection=False)) ?")?
                } else {
                    gf.spec.name().to_owned()
                }
            }
            Circuit::Symbol(sy) => {
                if sy.uuid.is_nil() {
                    "".to_owned()
                } else {
                    format!("{}", &sy.uuid)
                }
            }
            Circuit::Array(ac) => {
                if self.sync_tensors {
                    ac.save_rrfs(true)?;
                }
                if self.bijection {
                    if let Some(save_dir) = &self.tensor_save_dir {
                        write_tensor_to_dir_tree(save_dir, ac.value.clone(), false)?;
                    } else {
                        ac.save_rrfs(false)?;
                    }
                    ac.tensor_hash_base16()[..24].to_owned()
                } else {
                    "".to_owned()
                }
            }
            Circuit::Tag(at) => at.uuid.to_string(),
            Circuit::StoredCumulantVar(scv) => {
                format!(
                    "{}|{}",
                    scv.cumulant_ixs
                        .iter()
                        .map(|k| k.to_string())
                        .collect::<Vec<_>>()
                        .join(", "),
                    scv.uuid,
                )
            }
            _ => "".to_owned(),
        })
    }
    #[pyo3(name = "repr", signature=(*circuits))]
    pub fn repr_circuits(&self, circuits: Vec<CircuitRc>) -> Result<String> {
        let mut seen_hashes = HashMap::default();

        let disallow_name_ident = if !self.force_use_serial_numbers {
            let mut multiple_with_name: HashMap<Name, bool> = HashMap::default();
            let mut seen = HashSet::default();

            fn recurse(
                circ: CircuitRc,
                seen: &mut HashSet<HashBytes>,
                multiple_with_name: &mut HashMap<Name, bool>,
            ) {
                if !seen.insert(circ.info().hash) {
                    return;
                }
                if let Some(name) = circ.info().name {
                    use std::collections::hash_map::Entry::*;
                    match multiple_with_name.entry(name) {
                        Occupied(mut entry) => {
                            entry.insert(true);
                        }
                        Vacant(entry) => {
                            entry.insert(false);
                        }
                    }
                }

                for child in circ.children() {
                    recurse(child, seen, multiple_with_name)
                }
                if let Some(m) = circ.as_module() {
                    for spec in &m.spec.arg_specs {
                        recurse(spec.symbol.crc(), seen, multiple_with_name)
                    }
                }
            }
            for c in &circuits {
                recurse(c.clone(), &mut seen, &mut multiple_with_name)
            }
            Some(multiple_with_name)
        } else {
            None
        };

        // ideally this would separate method, but to avoid breaking blame we keep like this
        fn recurse(
            circ: &Circuit,
            depth: usize,
            is_only_child: bool,
            result: &mut String,
            seen_hashes: &mut HashMap<HashBytes, (String, String)>,
            runnning_serial_number: &mut usize,
            runnning_leaf_number: &mut usize,
            selfy: &PrintOptions,
            is_last_child: &Vec<bool>,
            traversal: Option<OpaqueIterativeMatcherVal>,
            disallow_name_ident: Option<&HashMap<Name, bool>>,
            parent_info: Option<(&Circuit, usize)>,
            mut node_comments: Vec<String>,
        ) -> Result<()> {
            result.push_str(&last_child_arrows(
                is_last_child,
                !(is_only_child && selfy.only_child_below),
                selfy.arrows,
            ));
            let mut used_color = false;
            if let Some(colorer) = &selfy.colorer {
                let color = colorer
                    .call(circ.clone().rc())
                    .context("colorer errored in print")?;
                if color.is_some() {
                    used_color = true;
                    result.push_str(&color.start_str());
                }
            }

            let term_on_repeat_or_reference = selfy.repr_full_line(
                circ,
                result,
                seen_hashes,
                runnning_serial_number,
                disallow_name_ident,
            )?;

            if used_color {
                result.push_str("\u{001b}[0m");
            }

            let info_from_parent = parent_info.and_then(|(parent, child_idx)| {
                selfy.get_child_info(
                    parent,
                    seen_hashes,
                    runnning_serial_number,
                    disallow_name_ident,
                    child_idx,
                )
            });
            if let Some(info) = info_from_parent {
                result.push_str(&format!(" ! {}", info));
            }

            let num_children = circ.num_children();

            let new_traversal_per_op = if !term_on_repeat_or_reference {
                let new_traversal_per_op = op_traversal_per(traversal, circ.crc())
                    .context("traversal failed in printer")?;
                if new_traversal_per_op.is_none() && circ.num_children() != 0 {
                    // all finished case
                    // traversal can't be used with bijection, so we can add ... without having to parse later
                    result.push_str(" ...");
                }
                new_traversal_per_op
            } else {
                None
            };

            let leaf_terming_here = circ.num_children() == 0 || new_traversal_per_op.is_none();

            if selfy.number_leaves && leaf_terming_here {
                node_comments.push(color(
                    &format!("{}", *runnning_leaf_number),
                    clicolor!(Magenta),
                ));
                *runnning_leaf_number += 1;
            }

            write_comment(result, node_comments, &selfy.commenters, circ.crc())?;
            result.push('\n');

            if term_on_repeat_or_reference || new_traversal_per_op.is_none() {
                return Ok(());
            }
            let new_traversal_per = new_traversal_per_op.unwrap();

            if selfy.seen_children_same_line && !selfy.has_child_info(circ) {
                let child_prints_seen = circ
                    .children()
                    .filter_map(|c| seen_hashes.get(&c.info().hash).as_ref().map(|x| &x.0))
                    .join(HORIZ_BAR);
                let unseen: Vec<_> = circ
                    .children()
                    .zip(new_traversal_per)
                    .filter(|(c, _t)| !seen_hashes.contains_key(&c.info().hash))
                    .enumerate()
                    .collect();
                if !child_prints_seen.is_empty() {
                    let mut spacing = last_child_arrows(
                        &is_last_child
                            .iter()
                            .copied()
                            .chain(iter::once(unseen.is_empty()))
                            .collect(),
                        true,
                        selfy.arrows,
                    );
                    spacing.pop();
                    spacing.push_str(if selfy.arrows { HORIZ_BAR } else { UP_ELBOW });
                    writeln!(result, "{}{}", spacing, child_prints_seen).unwrap();
                }
                for (i, (child, new_traversal)) in &unseen {
                    let new_last_child = is_last_child
                        .iter()
                        .copied()
                        .chain(iter::once(*i == unseen.len() - 1))
                        .collect();
                    recurse(
                        child,
                        depth + 1,
                        circ.num_children() == 1,
                        result,
                        seen_hashes,
                        runnning_serial_number,
                        runnning_leaf_number,
                        selfy,
                        &new_last_child,
                        new_traversal.clone(),
                        disallow_name_ident,
                        None,
                        vec![],
                    )?;
                }
                return Ok(());
            }
            if selfy.only_child_below && circ.num_children() == 1 {
                writeln!(
                    result,
                    "{}▼",
                    last_child_arrows(is_last_child, false, selfy.arrows)
                )
                .unwrap();
                recurse(
                    &circ.children().next().unwrap(),
                    depth,
                    circ.num_children() == 1,
                    result,
                    seen_hashes,
                    runnning_serial_number,
                    runnning_leaf_number,
                    selfy,
                    is_last_child,
                    new_traversal_per[0].clone(),
                    disallow_name_ident,
                    Some((circ, 0)),
                    vec![],
                )?;
                return Ok(());
            }
            for (i, (child, new_traversal)) in circ.children().zip(new_traversal_per).enumerate() {
                let new_last_child = is_last_child
                    .iter()
                    .copied()
                    .chain(iter::once(i == num_children - 1))
                    .collect();
                let child_specific_commenters = if selfy.comment_arg_names {
                    get_child_comments(circ, i)
                } else {
                    vec![]
                };
                recurse(
                    &child,
                    depth + 1,
                    circ.num_children() == 1,
                    result,
                    seen_hashes,
                    runnning_serial_number,
                    runnning_leaf_number,
                    selfy,
                    &new_last_child,
                    new_traversal,
                    disallow_name_ident,
                    Some((circ, i)),
                    child_specific_commenters,
                )?;
            }
            Ok(())
        }
        let mut result = String::new();
        let mut runnning_serial_number = 0;
        let mut runnning_leaf_number = 0;
        for circuit in circuits {
            recurse(
                &circuit,
                0,
                circuit.num_children() == 1,
                &mut result,
                &mut seen_hashes,
                &mut runnning_serial_number,
                &mut runnning_leaf_number,
                self,
                &vec![],
                self.traversal.clone(),
                disallow_name_ident.as_ref(),
                None,
                vec![],
            )?;
        }

        if self.leaves_on_top {
            result = result
                .trim()
                .lines()
                .rev()
                .map(|x| x.replace(UP_ELBOW, DOWN_ELBOW))
                .collect::<Vec<_>>()
                .join("\n");
        }
        if result.ends_with('\n') {
            result.pop();
        }
        Ok(result)
    }

    #[staticmethod]
    #[pyo3(name = "repr_depth", signature=(*circuits, end_depth = 3))]
    pub fn repr_circuits_depth(circuits: Vec<CircuitRc>, end_depth: usize) -> String {
        PrintOptions {
            bijection: false,
            traversal: Some(OpaqueIterativeMatcherVal::for_end_depth(end_depth)),
            ..Default::default()
        }
        .validate_ret()
        .expect("these options are valid")
        .repr_circuits(circuits)
        .expect("depth matcher can't fail + bijection is off")
    }
    #[staticmethod]
    #[pyo3(name = "print_depth", signature=(*circuits, end_depth = 3))]
    pub fn print_circuits_depth(circuits: Vec<CircuitRc>, end_depth: usize) {
        python_println!("{}", PrintOptions::repr_circuits_depth(circuits, end_depth))
    }

    #[staticmethod]
    pub fn size_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|c| Ok(circuit_to_size_color_code(c))))
    }

    #[staticmethod]
    pub fn type_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|circuit: CircuitRc| {
            let mut hasher = rustc_hash::FxHasher::default();
            circuit.variant_string().hash(&mut hasher);
            Ok(CliColor::new(hasher.finish() as usize))
        }))
    }

    #[staticmethod]
    pub fn hash_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|circuit: CircuitRc| {
            Ok(CliColor::new(circuit.info().hash_usize()))
        }))
    }
    #[staticmethod]
    pub fn fixed_color(color: CliColor) -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(move |_circuit: CircuitRc| Ok(color)))
    }

    #[staticmethod]
    pub fn computability_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|c| Ok(circuit_to_computability_color_code(c))))
    }

    #[staticmethod]
    pub fn circuit_set_colorer(map: HashMap<CliColor, HashSet<CircuitRc>>) -> CircuitToColorCode {
        let map: HashMap<HashBytes, CliColor> = map
            .into_iter()
            .flat_map(|(color, c)| c.into_iter().map(move |c| (c.info().hash, color)))
            .collect();

        CircuitToColorCode::new_dyn(Box::new(move |c| {
            Ok(map.get(&c.info().hash).cloned().into())
        }))
    }

    #[staticmethod]
    #[pyo3(signature=(threshold = 400_000_000))]
    pub fn size_threshold_commenter(threshold: usize) -> CircuitCommenter {
        CircuitCommenter::new_dyn(Box::new(move |circ| {
            let sz = circ.info().numel();
            if sz > BigUint::from(threshold) && !circ.is_array() {
                Ok(color(&oom_fmt(sz), clicolor!(Red)))
            } else {
                Ok("".to_string())
            }
        }))
    }

    #[staticmethod]
    #[pyo3(signature=(*, only_arrays = false))]
    pub fn dtype_commenter(only_arrays: bool) -> CircuitCommenter {
        CircuitCommenter::new_dyn(Box::new(move |circ| {
            if let Some(dtype) = &circ.info().device_dtype.dtype && (!only_arrays || circ.is_array()) {
                Ok(dtype.into())
            } else {
                Ok("".to_string())
            }
        }))
    }
}

fn init_print_options() -> PrintOptions {
    let end_depth_str =
        std::env::var("RR_DEBUG_END_DEPTH").unwrap_or_else(|_| DEFAULT_END_DEPTH.to_string());
    let end_depth = if end_depth_str.to_lowercase() == "none" {
        None
    } else {
        Some(end_depth_str.parse().unwrap_or_else(|_| {
            eprintln!(
                "failed to parse RR_DEBUG_END_DEPTH={}, expected 'None' or positive integer (default: {})",
                end_depth_str, DEFAULT_END_DEPTH,
            );
            DEFAULT_END_DEPTH
        }))
    };
    PrintOptions::debug_default(end_depth)
}

pub fn circuit_to_size_color_code(circuit: CircuitRc) -> CliColor {
    let size = circuit.info().numel_usize();
    if size == usize::MAX {
        clicolor!(Magenta)
    } else if size > 10_000_000_000 {
        clicolor!(Red)
    } else if size > 300_000_000 {
        clicolor!(Yellow)
    } else if size > 300_000 {
        clicolor!(Green)
    } else {
        CliColor::NONE
    }
}

pub fn circuit_to_computability_color_code(circuit: CircuitRc) -> CliColor {
    if !circuit.info().can_be_sampled() {
        clicolor!(Green)
    } else if !circuit.info().is_explicitly_computable() {
        clicolor!(Yellow)
    } else {
        CliColor::NONE
    }
}

static DEBUG_PRINT_OPTIONS: GILLazy<Mutex<PrintOptions>> =
    GILLazy::new(|| Mutex::new(init_print_options()));

#[pyfunction]
pub fn set_debug_print_options(options: PrintOptions) {
    *DEBUG_PRINT_OPTIONS.lock().unwrap() = options;
}

pub fn debug_repr(circ: CircuitRc) -> Result<String> {
    Ok(format!(
        "<{}>", /* we wrap in <> to make it clear what's a single circuit, similar to python <function __main__.<lambda>(x)> */
        DEBUG_PRINT_OPTIONS.lock().unwrap().repr(circ)?
    ))
}

pub fn print_circuit_stats(circuit: &Circuit) {
    let mut result = String::new();
    result.push_str(
        &circuit
            .info()
            .name
            .map(|x| x.string() + " ")
            .unwrap_or(" ".to_owned()),
    );
    result.push_str(&circuit.variant_string());
    result.push_str(&format!(
        " nodes {} max_size {} flops {}",
        count_nodes(circuit.crc()),
        oom_fmt(max_non_leaf_size(circuit.clone().rc())),
        oom_fmt(total_flops(circuit.crc()))
    ));
    println!("{}", result);
}

pub fn get_child_comments(parent: &Circuit, child_pos: usize) -> Vec<String> {
    vec![match parent {
        Circuit::Einsum(ein) => ein.in_axes[child_pos]
            .iter()
            .map(|int| ALPHABET[*int as usize].clone())
            .join(""),
        Circuit::DiscreteVar(_dv) => match child_pos {
            0 => "Values".to_owned(),
            1 => "Probs and Group".to_owned(),
            _ => {
                panic!()
            }
        },
        Circuit::Conv(_conv) => match child_pos {
            0 => "Input".to_owned(),
            1 => "Filter".to_owned(),
            _ => {
                panic!()
            }
        },
        Circuit::StoredCumulantVar(scv) => {
            format!("K{}", scv.cumulant_ixs[child_pos])
        }
        Circuit::Module(_) => {
            if child_pos == 0 {
                "Spec".to_owned()
            } else {
                "".to_owned()
            }
        }
        _ => "".to_owned(),
    }]
}

pub fn write_comment(
    result: &mut String,
    node_comments: Vec<String>,
    commenters: &Vec<CircuitCommenter>,
    circuit: CircuitRc,
) -> Result<()> {
    for comment in node_comments.into_iter().chain(
        commenters
            .iter()
            .map(|commenter| {
                commenter
                    .call(circuit.clone())
                    .context("commenter errored in print")
            })
            .collect::<Result<Vec<String>>>()?,
    ) {
        if !comment.is_empty() {
            write!(result, " # {}", comment).unwrap();
        }
    }
    Ok(())
}
