# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.lists_basics_ import (
    bounds_demo,
    comprehensions_demo,
    list_mutations,
    make_list_example,
    make_matrix_3x3,
    make_row_sums_generator,
    row_sums_three,
    sequence_ops,
    set_and_dict_comprehensions,
    sort_and_reverse_demo,
)


def test_sequence_ops_and_immutability_of_original():
    lst = make_list_example()
    first, upto_last, concat_new, repeat_new = sequence_ops(lst)
    assert first == 123
    assert upto_last == [123, "text"]
    assert concat_new == [123, "text", 1.23, 4, 5, 6]
    assert repeat_new == [123, "text", 1.23, 123, "text", 1.23]
    # исходный список не изменился
    assert lst == [123, "text", 1.23]


def test_list_mutations_append_and_pop():
    after_append, popped, after_pop = list_mutations()
    assert after_append == [123, "text", 1.23, "Py"]
    assert popped == 1.23
    assert after_pop == [123, "text", "Py"]


def test_sort_and_reverse_demo():
    after_sort, after_reverse = sort_and_reverse_demo()
    assert after_sort == ["aa", "bb", "cc"]
    assert after_reverse == ["cc", "bb", "aa"]


def test_bounds_demo_reports_errors():
    index_error, assign_error = bounds_demo([123, "text", "Py"])
    assert index_error is True and assign_error is True


def test_matrix_and_indexing():
    m, row2, item = make_matrix_3x3()
    assert m == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert row2 == [4, 5, 6]
    assert item == 6


def test_comprehensions_results():
    m, _, _ = make_matrix_3x3()
    comp = comprehensions_demo(m)
    assert comp["col2"] == [2, 5, 8]
    assert comp["col2_plus1"] == [3, 6, 9]
    assert comp["col2_evens"] == [2, 8]
    assert comp["diag"] == [1, 5, 9]
    assert comp["doubles"] == ["hh", "aa", "cc", "kk"]
    assert comp["squares_cubes"] == [[0, 0], [1, 1], [4, 8], [9, 27]]
    assert comp["positives"] == [[2, 1, 4], [4, 2, 8], [6, 3, 12]]


def test_generators_and_next():
    m, _, _ = make_matrix_3x3()
    g = make_row_sums_generator(m)
    assert next(g) == 6
    assert next(g) == 15
    assert next(g) == 24
    # и эквивалентная обёртка
    assert row_sums_three(m) == [6, 15, 24]


def test_set_and_dict_comprehensions():
    m, _, _ = make_matrix_3x3()
    sums_set, sums_dict = set_and_dict_comprehensions(m)
    assert sums_set == {6, 15, 24}
    assert sums_dict == {0: 6, 1: 15, 2: 24}


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.lists_basics_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "L = [123, 'text', 1.23]" in out
    assert "L[:-1] = [123, 'text']" in out
    assert "after append = [123, 'text', 1.23, 'Py']" in out
    assert "sorted = ['aa', 'bb', 'cc']" in out
    assert "reversed = ['cc', 'bb', 'aa']" in out
    assert "index_error = True assign_error = True" in out
    assert "M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]" in out
    assert "col2 = [2, 5, 8]" in out
    assert "row sums (first 3) = [6, 15, 24]" in out
    assert "sums_set = {24, 6, 15}" in out or "sums_set = {6, 15, 24}" in out
    assert "sums_dict = {0: 6, 1: 15, 2: 24}" in out
