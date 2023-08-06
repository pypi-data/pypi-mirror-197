use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*};
use rr_util::{
    compact_data::U8Set,
    name::Name,
    python_error_exception,
    rearrange_spec::RearrangeSpec,
    shape::{Shape, Size},
    tensor_util::TensorIndex,
    util::EinsumAxes,
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use thiserror::Error;

use crate::{
    constant::Symbol,
    generalfunction::GeneralFunctionSpec,
    module::{Module, ModuleArgSpec},
    CircuitRc,
};

#[apply(python_error_exception)]
#[base_error_name(Construct)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ConstructError {
    #[error("{string} ({e_name})")]
    NotSupportedYet { string: String },

    #[error("DiscreteVar doesn't have leading 'samples' dim ({e_name})")]
    DiscreteVarNoSamplesDim {},

    #[error(
        "DiscreteVar no probs_and_group specified and leading dim has unknown size ({e_name})"
    )]
    DiscreteVarSamplesDimUnknownSize {},

    #[error("DiscreteVar samples dim doesn't match probs, {node} vs {probs} ({e_name})")]
    DiscreteVarWrongSamplesDim { node: Size, probs: Size },

    #[error("DiscreteVar probs must be 1d with length matching samples axis 0, got probs of shape {shape:?} ({e_name})")]
    DiscreteVarProbsMustBe1d { shape: Shape },

    #[error("StoredCumulantVar needs first 2 cumulants specified ({e_name})")]
    StoredCumulantVarNeedsMeanVariance {},

    #[error("StoredCumulantVar invalid cumulant number {number} ({e_name})")]
    StoredCumulantVarInvalidCumulantNumber { number: usize },

    #[error("StoredCumulantVar cumulant number {cumulant_number} needs to be base shape, {base_shape:?} times cumulant number, got {cumulant_shape:?} ({e_name})")]
    StoredCumulantVarCumulantWrongShape {
        base_shape: Shape,
        cumulant_shape: Shape,
        cumulant_number: usize,
    },

    #[error("actual_num_children={actual_num_children} != expected_num_children_based_on_axes={expected_num_children_based_on_axes}\neinsum_name={einsum_name:?} ({e_name})")]
    EinsumWrongNumChildren {
        actual_num_children: usize,
        expected_num_children_based_on_axes: usize,
        einsum_name: Option<Name>,
    },

    #[error("len_axes={len_axes} != child_len_shape={child_len_shape}\neinsum_name={einsum_name:?} child_circuit={child_circuit:?} ({e_name})")]
    EinsumLenShapeDifferentFromAxes {
        len_axes: usize,
        child_len_shape: usize,
        einsum_name: Option<Name>,
        child_circuit: CircuitRc,
    },
    #[error("new_size={new_size}!=existing_size={existing_size} for axis={axis}\neinsum_name={einsum_name:?}, size introduced with child_circuit={child_circuit:?} ({e_name})")]
    EinsumAxisSizeDifferent {
        new_size: Size,
        existing_size: Size,
        axis: usize,
        einsum_name: Option<Name>,
        child_circuit: CircuitRc,
    },
    #[error("circuit_name={circuit_name:?} all_input_axes={all_input_axes:?} output_axes={output_axes:?} ({e_name})")]
    EinsumOutputNotSubset {
        circuit_name: Option<Name>,
        all_input_axes: U8Set,
        output_axes: EinsumAxes,
    },

    #[error("Rearrange takes different input shape, shape: {shape:?} spec: {spec:?} ({e_name})")]
    RearrangeWrongInputShape { spec: RearrangeSpec, shape: Shape },

    #[error("Wrong input shapes for GeneralFunction {input_shapes:?} {gf_spec:?} ({e_name})")]
    GeneralFunctionWrongInputShape {
        gf_spec: GeneralFunctionSpec,
        input_shapes: Vec<Shape>,
    },

    #[error("Passed python object isn't instance of GeneralFunctionSpec abstract class, ob={ob} ({e_name})")]
    GeneralFunctionPyNotInstance { ob: PyObject },

    #[error("Concat requires at least one node ({e_name})")]
    ConcatZeroNodes {},

    #[error("Concat nodes have different shapes {shapes:?} ({e_name})")]
    ConcatShapeDifferent { shapes: Vec<Shape> },

    #[error("axis out of bounds: {axis} vs {node_rank} ({e_name})")]
    AxisOutOfBounds { axis: i64, node_rank: usize },

    #[error("Scatter shape wrong, index: {index_shape:?} child: {shape:?} {index:?} ({e_name})")]
    ScatterShapeWrong {
        index: TensorIndex,
        shape: Shape,
        index_shape: Shape,
    },

    #[error("This scatter index not supported yet, {index:?} ({e_name})")]
    ScatterIndexTypeUnimplemented { index: TensorIndex },

    #[error("Unknown GeneralFunction name {spec_name} ({e_name})")]
    UnknownGeneralFunction { spec_name: Name },

    #[error("Module wrong number of children, expected {expected} got {got}\narg_specs={arg_specs:?} nodes={nodes:?} ({e_name})")]
    ModuleWrongNumberChildren {
        expected: usize,
        got: usize,
        arg_specs: Vec<ModuleArgSpec>,
        nodes: Vec<CircuitRc>,
    },

    #[error(
        "Module got unknown keyword argument, {argument}, all_module_inputs={all_module_inputs:?} ({e_name})"
    )]
    ModuleUnknownArgument {
        argument: Name,
        all_module_inputs: Vec<Name>,
    },

    #[error("missing_arguments={missing_arguments:?} ({e_name})")]
    ModuleMissingNames { missing_arguments: Vec<Name> },

    #[error("Module extract: not all leaves present in circuit, {subcirc:?} ({e_name})")]
    ModuleExtractNotPresent { subcirc: CircuitRc },

    #[error("symbols_named_none={symbols_named_none:?} ({e_name})")]
    ModuleSomeArgsNamedNone { symbols_named_none: Vec<Symbol> },

    #[error("dup_names={dup_names:?} ({e_name})")]
    ModuleArgsDupNames { dup_names: HashMap<Name, usize> },

    #[error("spec_circuit={spec_circuit:?} missing_symbols={missing_symbols:?} ({e_name})")]
    ModuleSomeArgsNotPresent {
        spec_circuit: CircuitRc,
        missing_symbols: HashSet<Symbol>,
    },

    #[error("actual_circuit={actual_circuit:?}\n(module children are: spec,sym_0,inp_0,sym_1,inp_1,...,sym_n,inp_n) ({e_name})")]
    ModuleExpectedSymbol { actual_circuit: CircuitRc },

    #[error(
        "orig_module={orig_module:?} got_instead_of_symbol={got_instead_of_symbol:?} ({e_name})"
    )]
    ModuleExpectedSymbolOnMap {
        orig_module: Module,
        got_instead_of_symbol: CircuitRc,
    },

    #[error("Named axis higher than rank ({e_name})")]
    NamedAxisAboveRank {},

    #[error("Failed to construct equivalent explicitly computable circuit ({e_name})")]
    NoEquivalentExplicitlyComputable {},

    #[error("ndim={ndim} ({e_name})")]
    UnflattenButNDimNot1 { ndim: usize },

    #[error("name_prefix='{name_prefix}' module={module:?} ({e_name})")]
    ModulePassedNamePrefixAndUseSelfNameAsPrefix { name_prefix: String, module: Module },

    #[error(
        "Scalar: shape has unknown sizes! shape={shape:?} name={name:?} value={value} ({e_name})"
    )]
    ScalarUnknownSizes {
        shape: Shape,
        name: Option<Name>,
        value: f64,
    },

    #[error("Not currently supported! old_symbol={old_symbol:?} != new_symbol_circ={new_symbol_circ:?}\nmodule={module:?} ({e_name})")]
    ModuleArgSpecSymbolChangedInExpand {
        old_symbol: Symbol,
        new_symbol_circ: CircuitRc,
        module: Module,
    },

    #[error("node_rank={node_rank} < symbol_rank={symbol_rank}, arg_spec={arg_spec:?} node_shape={node_shape:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleRankReduced {
        node_rank: usize,
        symbol_rank: usize,
        arg_spec: ModuleArgSpec,
        node_shape: Shape,
        spec_circuit: CircuitRc,
    },

    #[error("node_rank={node_rank} > symbol_rank={symbol_rank} (which indicates batching) and arg_spec={arg_spec:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleTriedToBatchUnbatchableInput {
        node_rank: usize,
        symbol_rank: usize,
        arg_spec: ModuleArgSpec,
        spec_circuit: CircuitRc,
    },

    #[error("node_shape={node_shape:?} symbol_shape={symbol_shape:?} arg_spec={arg_spec:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleTriedToExpandUnexpandableInput {
        node_shape: Shape,
        symbol_shape: Shape,
        arg_spec: ModuleArgSpec,
        spec_circuit: CircuitRc,
    },
    #[error("new_size={new_size} != old_size={old_size} and old_size not symbolic at dim={dim}\n{}\n({e_name})",
        format!("node_shape={:?}, arg_spec={:?} spec_circuit={:?}", node_shape, arg_spec, spec_circuit))]
    ModuleTriedToExpandOnNonSymbolicSizeAndBanned {
        new_size: Size,
        old_size: Size,
        dim: usize,
        node_shape: Shape,
        arg_spec: ModuleArgSpec,
        spec_circuit: CircuitRc,
    },
}
