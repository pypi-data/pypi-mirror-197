use anyhow::Result;
use circuit_base::{self_funcs::replace_expand_bottom_up_dyn, CircuitRc, DiscreteVar};

pub fn discrete_var_sample_all<F>(circuit: CircuitRc, should_sample: F) -> Result<CircuitRc>
where
    F: Fn(&DiscreteVar) -> bool,
{
    replace_expand_bottom_up_dyn(circuit, &|c: CircuitRc| {
        if c.as_discrete_var()
            .map(|x| should_sample(x))
            .unwrap_or(false)
        {
            Some(c.as_discrete_var().unwrap().values().clone())
        } else {
            None
        }
    })
}
