from functools import partial
from typing import Dict, Iterable, List, Literal, Optional, Sequence, TypeVar, Union

import torch

import interp.circuit.testing.topdown_circuit as td
import rust_circuit as rc

T = TypeVar("T")


def dedup_with_order(seq: Iterable[T]) -> List[T]:
    seen = set()
    out: List[T] = []
    for x in seq:
        if x in seen:
            continue
        else:
            seen.add(x)
            out.append(x)

    return out


def generate_with_shape(shape) -> torch.Tensor:
    return torch.randn(*shape, dtype=torch.float64)


def make_discrete_var(values_shape, name, batch_size, values_between_zero_one=False, group=None):
    """
    Values are sampled from random normal if values_between_zero_one=False,
    otherwise values are set to be in (0,1)
    """
    sample_shape = (batch_size,) + values_shape
    values = generate_with_shape(sample_shape)
    if values_between_zero_one:
        values = values ** 2
        values /= values.sum()

    out = rc.DiscreteVar(rc.Array(values), probs_and_group=group, name=name)
    return out, values, out.probs_and_group.evaluate()


st_Circuit = partial(td.st_Circuit, rust=True)
