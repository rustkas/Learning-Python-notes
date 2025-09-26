# pylint: disable=missing-function-docstring
import sys
from io import StringIO

from awesome_math.p7_assignments.assignments_prints import (
    append_sort_gotcha,
    augmented_list_inplace_shared,
    capture_stderr_of_print,
    concatenation_makes_new_object,
    # новые
    for_star_unpack,
    multi_target_shared_list_demo,
    named_assignment_illegal_targets,
    named_assignment_math_repeat,
    nested_unpacking,
    plus_equal_vs_plus_with_str_sequence,
    print_pack,
    print_with_flush,
    read_until_stop,
    redirect_stdout_demo,
    separate_mutables_demo,
    split_first_rest,
    split_rest_last,
    swap_tuple,
)


def test_swap_tuple_and_nested_unpacking():
    assert swap_tuple(1, 2) == (2, 1)
    assert nested_unpacking("TEXT") == ("T", "E", "XT")


def test_extended_unpacking_first_rest_and_rest_last():
    first, rest = split_first_rest([1, 2, 3, 4])
    assert first == 1 and rest == [2, 3, 4]
    rest2, last = split_rest_last([1, 2, 3, 4])
    assert rest2 == [1, 2, 3] and last == 4


def test_multi_target_shared_and_separate_mutables():
    a, b = multi_target_shared_list_demo()
    assert a is b and a == [42] and b == [42]  # общая ссылка и общее содержимое
    c, d = separate_mutables_demo()
    assert c is not d and not c and d == [42]  # разные объекты


def test_augmented_vs_concatenation_and_sharing():
    l, m = augmented_list_inplace_shared()
    assert l is m and l == [1, 2, 3, 4]  # in-place отражается в обеих ссылках
    l2, m2 = concatenation_makes_new_object()
    assert l2 == [1, 2, 3, 4] and m2 == [1, 2] and l2 is not m2  # новый объект


def test_append_sort_gotcha():
    lst = [3, 1]
    after, sort_result = append_sort_gotcha(lst)
    assert sort_result is None
    assert after == [1, 3, 99]  # список отсортирован на месте и дополнен


def test_named_assignment_in_while_and_wrapper_print():
    f = StringIO("line1\nline2\nSTOP\nline3\n")
    lines = read_until_stop(f)
    assert lines == ["line1", "line2"]

    # проверяем параметры print: sep и end, вывод в StringIO через file=
    buf = StringIO()
    print_pack(1, 2, 3, sep="...", end="!\n", file=buf)
    assert buf.getvalue() == "1...2...3!\n"


def test_redirect_stdout_demo_restores_and_captures():
    before = sys.stdout
    captured = redirect_stdout_demo("hello")
    assert captured == "hello\n"
    assert sys.stdout is before  # stdout восстановлен


def test_named_assignment_math_repeat():
    s, k = named_assignment_math_repeat("Py", 3)
    assert s == "PyPyPy" and k == 3


# ---- новые проверки ---- #


def test_for_star_unpack():
    data = [(1, 2, 3, 4), (5, 6, 7, 8)]
    out = for_star_unpack(data)
    assert out == [(1, [2, 3], 4), (5, [6, 7], 8)]


def test_print_with_flush_calls_flush():
    text, flushed = print_with_flush("ping")
    assert text == "ping\n"
    assert flushed is True


def test_capture_stderr_of_print():
    captured = capture_stderr_of_print("ERR!")
    assert captured == "ERR!\n"


def test_plus_equal_vs_plus_with_str_sequence():
    after, errname = plus_equal_vs_plus_with_str_sequence()
    assert after == ["a", "b", "c"]
    assert errname == "TypeError"


def test_named_assignment_illegal_targets_compiletime_errors():
    ok_index, ok_attr = named_assignment_illegal_targets()
    assert ok_index and ok_attr
