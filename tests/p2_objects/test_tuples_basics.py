# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.tuples_basics_ import (
    as_dict_key_demo,
    make_tuple_example,
    namedtuple_point_demo,
    nested_mutable_demo,
    rebuild_tuple_replace_first,
    sequence_ops,
    try_assign_first,
    unpack_a_middle_c,
)


def test_sequence_ops_and_immutability_basics():
    t = make_tuple_example()
    first, upto_last, concat_new, repeat_new = sequence_ops(t)
    assert t == (123, "text", 1.23)
    assert first == 123
    assert upto_last == [123, "text"]
    assert concat_new == (123, "text", 1.23, 4, 5, 6)
    assert repeat_new == (123, "text", 1.23, 123, "text", 1.23)
    assert t == (123, "text", 1.23)  # исходный не поменялся


def test_try_assign_first_returns_true_on_typeerror():
    assert try_assign_first((1, 2, 3)) is True


def test_rebuild_tuple_replace_first():
    t2 = rebuild_tuple_replace_first((1, 2, 3), "Z")
    assert t2 == ("Z", 2, 3)


def test_unpack_a_middle_c():
    a, middle, c = unpack_a_middle_c((1, 2, 3, 4))
    assert (a, middle, c) == (1, [2, 3], 4)


def test_as_dict_key_demo():
    d, fetched = as_dict_key_demo()
    assert d[("x", 1)] == "point_x1" and fetched == "point_x1"
    assert ("y", 2) in d


def test_nested_mutable_demo():
    before, after = nested_mutable_demo()
    assert before == (1, [2, 3])
    assert after == (1, [2, 3, 4])


def test_namedtuple_point_demo():
    p, px, py = namedtuple_point_demo()
    # доступ и по полям, и по индексам
    assert (px, py) == (2, 3)
    assert (p[0], p[1]) == (2, 3)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.tuples_basics_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "t = (123, 'text', 1.23)" in out
    assert "t[:-1] = [123, 'text']" in out
    assert "assign_error = True" in out
    assert "replaced_first = ('Z', 1.23" not in out  # просто sanity-check на формат
    assert "dict_by_tuple_key = {('x', 1): 'point_x1', ('y', 2): 'point_y2'}" in out
    assert "dict_by_tuple_key[('x', 1)] = point_x1" in out
    assert "nested before = (1, [2, 3])" in out
    assert "nested after  = (1, [2, 3, 4])" in out
    assert "namedtuple Point = Point(x=2, y=3) 2 3" in out
