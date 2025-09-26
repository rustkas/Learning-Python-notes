# pylint: disable=missing-function-docstring
from awesome_math.p6_statements.statements_demo import (
    bracketed_list,
    break_continue_demo,
    interactive_echo,
    interactive_square_float_try,
    interactive_square_int,
    match_case_demo,
    multiline_sum,
    nested_if_demo,
    semicolon_chain,
    single_line_if,
)


def test_interactive_echo_basic():
    inputs = ["python", "312", "stop", "ignored"]
    assert interactive_echo(inputs) == ["PYTHON", "312"]


def test_square_int_with_validation_and_bye():
    inputs = ["5", "xxx", "10", "stop", "99"]
    out = interactive_square_int(inputs)
    assert out[:-1] == [25, "Bad!" * 8, 100]
    assert out[-1] == "Bye"


def test_square_float_try_covers_floats_and_errors():
    inputs = ["50", "40.5", "1.23E-2", "hack", "stop"]
    out = interactive_square_float_try(inputs)
    assert out[0] == 2500.0
    assert out[1] == 1640.25
    assert abs(out[2] - (0.0123**2)) < 1e-12
    assert out[3] == "Bad!" * 8
    assert out[-1] == "Bye"


def test_multiline_and_semicolons_and_singleline_if():
    assert multiline_sum(1, 2, 3, 4) == 10
    assert semicolon_chain() == 3
    assert single_line_if(3, 2) == "gt"
    assert single_line_if(2, 3) == "le"


def test_bracketed_list_and_nested_if_demo():
    data = bracketed_list()
    assert data == [1111, 2222, 3333]
    assert nested_if_demo("19") == "low"
    assert nested_if_demo("20") == str(400)
    assert nested_if_demo("oops").startswith("Bad!")


def test_break_continue_demo():
    # n мало — прерывание по n
    assert break_continue_demo(8) == [1, 3, 5, 7]
    # n велик — прерывание по условию > 10
    assert break_continue_demo(100) == [1, 3, 5, 7, 9, 11]


def test_match_case_demo():
    assert match_case_demo(0) == "zero"
    assert match_case_demo(5) == "positive-int"
    assert match_case_demo(-1.0) == "negative-float"
    assert match_case_demo("hi") == "string:hi"
    assert match_case_demo([1, 2]) == "other"
