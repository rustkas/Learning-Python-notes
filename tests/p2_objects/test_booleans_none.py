# pylint: disable=missing-function-docstring
import subprocess
import sys

from awesome_math.p2_objects.booleans_none_ import (
    bool_value,
    booleans_as_ints,
    compare_demo,
    default_if_none,
    is_none,
    list_of_nones,
)


def test_compare_demo_and_truthiness():
    gt, lt = compare_demo(1, 2)
    assert gt is False and lt is True

    assert bool_value("hack") is True
    assert bool_value("") is False
    assert bool_value(0) is False
    assert bool_value([0]) is True  # непустой контейнер — True


def test_list_of_nones_and_identity():
    lst = list_of_nones(100)
    assert len(lst) == 100
    assert all(item is None for item in lst)


def test_booleans_as_ints():
    t_eq1, f_eq0, is_int = booleans_as_ints()
    assert t_eq1 is True
    assert f_eq0 is True
    assert is_int is True


def test_default_if_none_and_is_none():
    assert default_if_none(None, 42) == 42
    assert default_if_none(0, 42) == 0
    assert default_if_none("", "x") == ""
    assert is_none(None) is True
    assert is_none(0) is False
    assert is_none(False) is False


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.booleans_none_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "1 > 2 -> False" in out
    assert "1 < 2 -> True" in out
    assert "bool('hack') -> True" in out
    assert "None demo: None" in out
    assert "list_of_none size: 100" in out
    assert "True == 1, False == 0, isinstance(True,int) -> True True True" in out
    assert "default_if_none(None, 'X') -> X" in out
    assert "default_if_none(0, 'X') -> 0" in out
    assert "is_none(0) -> False" in out
    assert "is_none(None) -> True" in out
