use rr_util::name::Name;

use crate::{
    Add, Circuit, CircuitNode, CircuitNodeAutoName, CircuitRc, Concat, Conv, Cumulant, DiscreteVar,
    Einsum, GeneralFunction, Index, Module, Rearrange, Scatter, StoredCumulantVar, Tag,
};

/// For naming only
#[derive(Debug)]
pub enum OperatorPriority {
    Infix { priority: u8 },
    InfixAmbiguous {},
    PostFix {},
    Function {},
    NotOperator {},
}

pub fn get_priority(circuit: CircuitRc) -> OperatorPriority {
    match &**circuit {
        Circuit::Einsum(_) => Einsum::PRIORITY,
        Circuit::Add(_) => Add::PRIORITY,
        Circuit::Concat(_) => Concat::PRIORITY,
        Circuit::Rearrange(_) => Rearrange::PRIORITY,
        Circuit::Index(_) => Index::PRIORITY,
        Circuit::Scatter(_) => Scatter::PRIORITY,
        Circuit::Tag(_) => Tag::PRIORITY,
        Circuit::DiscreteVar(_) => DiscreteVar::PRIORITY,
        Circuit::GeneralFunction(_) => GeneralFunction::PRIORITY,
        Circuit::Module(_) => Module::PRIORITY,
        Circuit::Cumulant(_) => Cumulant::PRIORITY,
        Circuit::StoredCumulantVar(_) => StoredCumulantVar::PRIORITY,
        Circuit::Conv(_) => Conv::PRIORITY,
        _ => OperatorPriority::NotOperator {},
    }
}

#[test]
fn f() {
    println!("{:?}", Einsum::PRIORITY)
}

pub fn do_add_parenthesis_to_name(parent_priority: &OperatorPriority, child: CircuitRc) -> bool {
    match (parent_priority, get_priority(child)) {
        (OperatorPriority::NotOperator {}, _) => false, // Should not happen
        (OperatorPriority::Function {}, _) => false,
        (_, OperatorPriority::NotOperator {}) | (_, OperatorPriority::Function {}) => false,
        (OperatorPriority::PostFix {}, OperatorPriority::PostFix {}) => false,
        (OperatorPriority::PostFix {}, _) => true,
        (_, OperatorPriority::PostFix {}) => false,
        (OperatorPriority::InfixAmbiguous {}, _) => true,
        (OperatorPriority::Infix { .. }, OperatorPriority::InfixAmbiguous {}) => true,
        (
            OperatorPriority::Infix { priority: p_parent },
            OperatorPriority::Infix { priority: p_child },
        ) => *p_parent > p_child,
    }
}

/// Return the name surrounded with parenthesis if appropriate, and None if name is None
pub fn child_name_with_maybe_paren(
    parent_priority: &OperatorPriority,
    child: CircuitRc,
) -> Option<Name> {
    child.info().name.map(|name| {
        if do_add_parenthesis_to_name(parent_priority, child) {
            format!("({name})").into()
        } else {
            name
        }
    })
}

/// Return the names surrounded with parenthesis if appropriate, and None if any of the name is None
pub fn children_names_with_maybe_paren(
    parent_priority: &OperatorPriority,
    children: Vec<CircuitRc>,
) -> Option<Vec<Name>> {
    if children.iter().any(|x| x.info().name.is_none()) {
        None
    } else {
        Some(
            children
                .into_iter()
                .map(|x| child_name_with_maybe_paren(parent_priority, x).unwrap())
                .collect::<Vec<Name>>(),
        )
    }
}
