# pylint: disable=missing-function-docstring
import sys

import pytest

from awesome_math.p8_selections.if_match import (
    and_or_equivalent,
    bool_operands,
    categorize_stmt_match,
    first_truthy,
    guard_demo,
    lines_to_color,
    os_color_match,
    os_year_dict,
    os_year_if,
    pattern_demo,
    short_circuit_or,
    ternary_if_expr,
)

PY310_PLUS = sys.version_info >= (3, 10)


def test_if_and_dict_switch():
    assert os_year_if("Linux") == 1991
    assert os_year_if("AmigaOS") == "Bad choice"
    assert os_year_dict("Windows") == 1985
    assert os_year_dict("Solaris") == "Bad choice"


@pytest.mark.skipif(not PY310_PLUS, reason="match requires Python 3.10+")
def test_match_basic_colors_and_captures():
    assert os_color_match("go") == "green"
    assert os_color_match("halt") == "red"
    assert os_color_match("???") == "yellow"
    cats, which, other = categorize_stmt_match(["if", "while", "try"])
    assert cats == ["logic", "loop", "tbd"]
    assert which == "while"
    assert other == "try"


@pytest.mark.skipif(not PY310_PLUS, reason="match requires Python 3.10+")
def test_match_pattern_demo_literals_sequences_dicts():
    assert pattern_demo(2) == ("or", 2)
    assert pattern_demo([1, 2, 9]) == ("list", 9)
    assert pattern_demo([0, 7, 8]) == ("list", [7, 8])
    assert pattern_demo({"a": 1, "b": 2, "c": 3}) == ("dict", 3)
    typ, what = pattern_demo({"a": 0, "b": 2, "c": 3})
    assert typ == "dict" and what == {"b": 2, "c": 3}
    assert pattern_demo((1, 2, 5)) == ("tuple", 5)
    assert pattern_demo((0, 9, 8)) == ("tuple", [9, 8])
    assert pattern_demo("else") == ("other", "else")


@pytest.mark.skipif(not PY310_PLUS, reason="match requires Python 3.10+")
def test_match_guard_demo():
    assert guard_demo(((1, 2), 3), True) == ("case1", (1, 3))
    # guard False — переходим к следующему case
    t, payload = guard_demo(((1, 2), 3), False)
    assert t == "case2" and payload[0] == (1, 3)


def test_bool_operands_and_short_circuit():
    # or/and возвращают операнды
    assert bool_operands(0, "X") == ("X", 0)
    assert bool_operands("A", "") == ("A", "")
    # short-circuit: f2 не вызовется, если f1 истинен
    f1_called = f2_called = False

    def f1():
        nonlocal f1_called
        f1_called = True
        return "OK"

    def f2():
        nonlocal f2_called
        f2_called = True
        return "NO"

    result, (c1, c2) = short_circuit_or(f1, f2)
    assert result == "OK" and c1 is True and c2 is False and f2_called is False


def test_ternary_and_and_or_equivalent():
    # Эквивалентные случаи (Y истинен)
    assert ternary_if_expr(True, "Y", "Z") == and_or_equivalent(True, "Y", "Z") == "Y"
    assert ternary_if_expr(False, "Y", "Z") == and_or_equivalent(False, "Y", "Z") == "Z"
    # Неэквивалентный случай: Y ложен -> and/or даёт Z даже при X=True
    assert ternary_if_expr(True, "", "Z") == ""
    assert and_or_equivalent(True, "", "Z") == "Z"  # отличие, см. главу


def test_first_truthy_and_batch_match_usage():
    assert first_truthy("", 0, None, "go") == "go"
    assert first_truthy("", 0, None, default="fallback") == "fallback"
    assert lines_to_color(["go", "stop", "???"]) == ["green", "red", "yellow"]
