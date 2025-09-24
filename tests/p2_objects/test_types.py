# pylint: disable=missing-function-docstring
import subprocess
import sys

from awesome_math.p2_objects.types_ import (
    first_item_duck,
    get_type,
    get_type_of_type,
    polymorphic_len,
    sum_numbers_duck,
    type_eq_examples_for_list,
)


def test_types_and_isinstance_basics():
    l_obj = [1, 2, 3]
    assert get_type(l_obj) is list
    assert get_type_of_type(l_obj) is type

    eq1, eq2, inst = type_eq_examples_for_list(l_obj)
    assert (eq1, eq2, inst) == (True, True, True)


def test_polymorphism_len_and_first_item_and_sum():
    lens = polymorphic_len(["ab", [1, 2, 3], {"k": 1, "v": 2}])
    assert lens == [2, 3, 2]

    assert first_item_duck("code") == "c"
    assert first_item_duck((10, 11)) == 10
    assert first_item_duck(range(5)) == 0

    assert sum_numbers_duck([1.5, 2.5]) == 4.0
    assert sum_numbers_duck(i * i for i in range(3)) == 5.0


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.types_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "type([1, 2, 3]) -> <class 'list'>" in out
    assert "type(type([1, 2, 3])) -> <class 'type'>" in out
    assert "checks (type==type([]), type==list, isinstance) -> True True True" in out
    assert "polymorphic len -> [2, 3, 2]" in out
    assert "first_item('code') -> c" in out
    assert "first_item(range(5)) -> 0" in out
    assert "sum_numbers_duck([1.5, 2.5]) -> 4.0" in out
    assert "sum_numbers_duck(i*i for i in range(3)) -> 5.0" in out
