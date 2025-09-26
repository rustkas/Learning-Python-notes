# pylint: disable=missing-function-docstring
import itertools

import awesome_math.p14.iter_comp_tools as it


def test_squares_equivalence():
    data = [1, 2, 3, 4]
    assert it.squares_with_for(data) == it.squares_with_list_comp(data) == [1, 4, 9, 16]


def test_rstrip_and_nonblank_count():
    lines = [" a \n", "\n", "b\t", "  \t  "]
    assert it.rstrip_lines(lines) == [" a", "", "b", ""]
    assert it.count_nonblank(lines) == 2


def test_cartesian_concat():
    assert it.cartesian_concat("ab", "12") == ["a1", "a2", "b1", "b2"]


def test_zip_enumerate_demo():
    out = it.zip_enumerate_demo(["a", "b", "c"], [10, 20, 30])
    assert out == ["0:a+10", "1:b+20", "2:c+30"]


def test_map_filter_equivalents():
    s = "py3"
    assert it.map_ord(s) == it.map_ord_comp(s) == [112, 121, 51]
    seq = ["42", "x7", "007", "abc"]
    assert it.filter_digit(seq) == it.filter_digit_comp(seq) == ["42", "007"]


def test_manual_collect_matches_for_behavior():
    data = ["a", "b", "c"]
    assert it.manual_collect(data) == list(data)
    # и на однопроходном генераторе
    gen = (x * 2 for x in "ab")
    assert it.manual_collect(gen) == ["aa", "bb"]


def test_iterability_inspection():
    # список — многопроходный
    info_list = it.inspect_iterable([1, 2, 3])
    assert info_list.is_self_iterator is False
    assert info_list.independent_iters is True

    # range — тоже многопроходный
    info_range = it.inspect_iterable(range(3))
    assert info_range.is_self_iterator is False
    assert info_range.independent_iters is True

    # zip — однопроходный
    info_zip = it.inspect_iterable(zip("ab", "12"))
    assert info_zip.is_self_iterator is True
    assert info_zip.independent_iters is None


def test_single_vs_multi_pass_examples():
    sp = it.SinglePassRange(3)
    assert list(sp) == [0, 1, 2]
    # повторный «проход» продолжает прошлый (ничего не осталось)
    assert not list(sp)

    mp = it.MultiPassListWrapper([10, 20, 30])
    # каждый проход независим
    assert list(mp) == [10, 20, 30]
    assert list(mp) == [10, 20, 30]

    # демонстрация различий через два итератора поверх одного объекта
    sp2 = it.SinglePassRange(2)
    i1 = iter(sp2)
    i2 = iter(sp2)
    assert next(i1) == 0
    # i2 не независим: продолжает i1
    assert next(i2) == 1

    mp2 = it.MultiPassListWrapper([1, 2])
    j1, j2 = iter(mp2), iter(mp2)
    assert next(j1) == 1
    # j2 независим и тоже начинает с 1
    assert next(j2) == 1


def test_genexpr_and_dict_comp():
    lines = ["Testing file IO\n", "Learning Python, 6E\n", "Python 3.12\n"]
    # генераторное выражение + сбор в список
    assert it.genexpr_upper(lines) == [
        "TESTING FILE IO\n",
        "LEARNING PYTHON, 6E\n",
        "PYTHON 3.12\n",
    ]
    # dict comprehension с фильтром
    d = it.dict_comp_index(["A\n", "Learning\n", "Python\n", "zzz\n"])
    assert d == {0: "Learning\n", 1: "Python\n"}


def test_protocol_works_with_star_unpacked_inputs():
    # имитируем поведение join/extend/sum-like через itertools.chain
    parts = ["X", *itertools.chain(["a"], ["b"], ["c"]), "Z"]
    assert parts == ["X", "a", "b", "c", "Z"]
