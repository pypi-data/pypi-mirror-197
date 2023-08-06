from typing import cast

import hypothesis
import torch
from torch.testing import assert_close

import rust_circuit as rc
from interp.circuit.testing.topdown_circuit import CircuitProbs as CP
from interp.circuit.testing.utils import mark_not_interesting_if
from rust_circuit import *

from .test_rust_rewrite import get_c_st

po = rc.PrintOptions(tensor_index_literal=True, bijection=False)


@hypothesis.settings(deadline=None)
@hypothesis.given(get_c_st(max_growth_steps=20))
@mark_not_interesting_if(SchedulingOOMError)
def test_schedule(circ):
    raw_test_schedule(circ)


def raw_test_schedule(circ):
    circ = rc.cast_circuit(circ, TorchDeviceDtypeOp(device="cpu", dtype="float64"))
    # circ = rc.substitute_all_modules(circ)
    schedule = optimize_to_schedule(circ)
    # hypothesis.note("circ: " + circ.repr(po))
    # hypothesis.note("optimized: " + rc.optimize_circuit(circ).repr(po))

    # hypothesis.note(repr(schedule))

    hypothesis.assume(
        all(not ix.cast_index().has_tensor_axes() for ix in circ.get(rc.Index))
    )  # might go away due to Index.canonicalize, so can't replace them

    circ_out = circ.evaluate()
    assert_close(circ_out, schedule.evaluate().type(circ_out.dtype))

    circ_replaced = circ.update(rc.Array, lambda x: Array(cast(Array, x).value + 9.1))
    # hypothesis.note("replaced: " + circ_replaced.repr(po))
    # hypothesis.note("replaced optimized: " + rc.optimize_circuit(circ_replaced).repr(po))
    # hypothesis.note(repr({x.hash.hex(): x for x in rc.all_children(circ) if x.is_array()}))
    # hypothesis.note(repr({x.hash.hex(): x for x in schedule.constants.values()}))
    circ_replaced_in_rust = schedule.replace_tensors(
        {x.hash: x.cast_array().value + 9.1 for x in rc.all_children(circ) if x.is_array()},
        allow_missing=True,  # sometimes Arrays go away, e.g. due to 0*x = 0
    )
    # hypothesis.note(repr(schedule))
    # hypothesis.note(repr([(x, y, y.hash.hex()) for x, y in schedule.constants.items()]))
    x = circ_replaced.evaluate()
    y = circ_replaced_in_rust.evaluate().type(x.dtype)
    # hypothesis.note(repr(x))
    # hypothesis.note(repr(y))
    assert_close(x, y)


@hypothesis.given(get_c_st(probs_per_depth=[CP.kw(all=0, branches=1, Module=0)]).filter(lambda c: c.num_children > 0))
def test_opt_eval_many(circ):
    circ = rc.cast_circuit(circ, TorchDeviceDtypeOp(dtype="float64"))
    circs = circ.children
    many_evaled = optimize_and_evaluate_many(circs)
    for circ, evaled in zip(circs, many_evaled):
        assert_close(circ.evaluate(), evaled)
