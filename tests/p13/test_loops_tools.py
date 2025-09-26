# pylint: disable=missing-function-docstring,unnecessary-lambda-assignment
from __future__ import annotations

import itertools

import pytest

import awesome_math.p13.loops_tools as lt


def test_evens_desc_while_continue_basic():
    assert lt.evens_desc_while_continue(10) == [8, 6, 4, 2, 0]
    assert lt.evens_desc_while_continue(1) == [0]
    assert not lt.evens_desc_while_continue(0)


@pytest.mark.parametrize(
    "n, expected_kind",
    [(2, "prime"), (3, "prime"), (4, "factor"), (9, "factor"), (11, "prime")],
)
def test_first_factor_or_prime(n, expected_kind):
    kind, val = lt.first_factor_or_prime(n)
    assert kind == expected_kind
    if expected_kind == "factor":
        assert isinstance(val, int) and val not in (0, 1) and n % val == 0
    else:
        assert val is None


def test_sum_and_prod():
    s, p = lt.sum_and_prod([1, 2, 3, 4])
    assert s == 10
    assert p == 24


def test_rotate_sequence():
    assert lt.rotate_sequence("abcd") == [
        list("abcd"),
        list("bcda"),
        list("cdab"),
        list("dabc"),
    ]
    assert lt.rotate_sequence([1, 2, 3]) == [
        [1, 2, 3],
        [2, 3, 1],
        [3, 1, 2],
    ]


def test_step_slice():
    assert lt.step_slice("abcdefgh", 2) == list("aceg")
    assert lt.step_slice([0, 1, 2, 3, 4, 5], 3) == [0, 3]


def test_pair_sum_zip_truncates_to_shortest():
    assert lt.pair_sum_zip([1, 2, 3], [10, 20, 30, 40]) == [11, 22, 33]
    # работает с любыми итерируемыми
    assert lt.pair_sum_zip(range(3), (100, 200, 300)) == [100, 201, 302]


def test_index_items_enumerate():
    seq = ["a", "b", "c"]
    assert lt.index_items_enumerate(seq) == [(0, "a"), (1, "b"), (2, "c")]
    assert lt.index_items_enumerate(seq, start=5) == [(5, "a"), (6, "b"), (7, "c")]


def test_find_with_for_else_found_and_not_found():
    pred = lambda x: x > 7  # noqa: E731
    assert lt.find_with_for_else([1, 5, 7, 8, 3], pred) == (True, 8)
    assert lt.find_with_for_else([1, 2, 3], pred) == (False, None)


def test_add_one_inplace():
    data = [10, 20, 30]
    out = lt.add_one_inplace(data)
    assert out is data
    assert data == [11, 21, 31]


def test_nested_cartesian():
    xs = [1, 2]
    ys = ["a", "b", "c"]
    expected = [(1, "a"), (1, "b"), (1, "c"), (2, "a"), (2, "b"), (2, "c")]
    assert lt.nested_cartesian(xs, ys) == expected
    # сверка с itertools.product
    assert lt.nested_cartesian(xs, ys) == list(itertools.product(xs, ys))


def test_infinite_noop():
    assert lt.infinite_noop(1) == 1
    assert lt.infinite_noop(5) == 5
