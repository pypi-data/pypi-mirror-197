import pytest

import rust_circuit as rc


# TODO: more tests
def test_symbolic_expand_simple():
    P = rc.Parser()

    scl, v, new = P.parse_circuits(
        """
    1 [7] Scalar 1.3
    0 Einsum i,i->i
      1
      2 [7] Scalar 1.5
    'new' [?] Symbol
    """
    )

    assert rc.expand_node(v, [scl, new]).shape == (7,)


def test_symbolic_rearrange_expand():
    P = rc.Parser()
    scl, sym, rearrange = P.parse_circuits(
        """
    0 [6] Scalar 1.3
    'sym' [?] Symbol rand
    1 Rearrange (a:2 b:3) -> b a
      0
    """
    )

    # should use set symbolic
    expanded = rc.Expander((scl, lambda _: sym))(rearrange)
    assert expanded.shape == (3, 2)

    scl0, scl1, scl2, sym, rearrange = P.parse_circuits(
        """
    'scl0' [?] Symbol
    'scl1' [24] Scalar 1.3
    'scl2' [17] Scalar 1.3
    'sym' [?] Symbol rand
    2 Add
      3 Rearrange (a b:3) -> b a
        'scl0'
      4 Rearrange (b:3 a:8) -> a b 1
        'scl1'
      8 Einsum i->
        7 Add
          5 Rearrange a:17 -> a
            'scl2'
          6 Rearrange a -> a
            'scl2'
    """
    )

    expanded = rc.Expander(({scl0, scl1, scl2}, lambda _: sym))(rearrange)
    s0, *_ = rc.symbolic_sizes()
    assert expanded.shape == (8, 3, s0)


def test_multiple_symbolic_product():
    s = """
    'a' [?] Symbol 07a8025a-d8ba-4c57-946d-cd7cc7e78a66
    'b' Rearrange a b c -> (a b c)
      'c' [?, ?, ?] Symbol 0b108f80-b37f-4e2c-821f-45cbedcbde75
    'd' Rearrange a c -> (a c)
      'e' [?, ?] Symbol 3f8aaf28-58f8-44fc-8dbc-497844a5a837
    """
    a, b, d = rc.Parser().parse_circuits(s)
    assert a.repr() == "'a' [?] Symbol 07a8025a-d8ba-4c57-946d-cd7cc7e78a66"
    assert (
        rc.PrintOptions(shape_only_when_necessary=False).repr(b)
        == "'b' [?] Rearrange a b c -> (a b c)\n  'c' [?,?,?] Symbol 0b108f80-b37f-4e2c-821f-45cbedcbde75"
    )
    assert (
        rc.PrintOptions(shape_only_when_necessary=False).repr(d)
        == "'d' [?] Rearrange a b -> (a b)\n  'e' [?,?] Symbol 3f8aaf28-58f8-44fc-8dbc-497844a5a837"
    )
