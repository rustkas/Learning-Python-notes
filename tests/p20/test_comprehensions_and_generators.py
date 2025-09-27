# tests/p5_numbers/test_comprehensions_and_generators.py
# pylint: disable=missing-function-docstring
# pylint: disable=unsupported-assignment-operation

from awesome_math.p20.comprehensions_and_generators import (
    consume_all,
    double_gen,
    even_squares,
    first_two,
    gen_squares,
    mymap_func,
    mymap_pad,
    myzip_gen,
    ords_list,
    permute,
    scramble,
)


def test_list_comprehensions_basic():
    assert ords_list("Ab") == [65, 98]
    assert even_squares(10) == [0, 4, 16, 36, 64]


def test_generator_expression_vs_map_equivalence():
    data = [1, -2, 3]
    # Генератор-выражение
    got = list(x for x in (abs(v) for v in data))
    # map(abs, ...)
    exp = list(map(abs, data))
    assert got == exp == [1, 2, 3]


def test_gen_function_basics():
    assert list(gen_squares(5)) == [0, 1, 4, 9, 16]


def test_scramble_rotations_string_and_tuple():
    assert list(scramble("code")) == ["code", "odec", "deco", "ecod"]
    assert list(scramble((1, 2, 3))) == [(1, 2, 3), (2, 3, 1), (3, 1, 2)]


def test_permute_small():
    perms = list(permute("abc"))
    assert sorted(perms) == sorted(["abc", "acb", "bac", "bca", "cab", "cba"])
    # Проверяем, что генератор даёт по одному и совпадает по множеству с материализацией
    assert len(perms) == 6


def test_mymap_func_multiple_iters():
    assert list(mymap_func(pow, [1, 2, 3], [2, 3, 4])) == [1, 8, 81]
    assert list(mymap_func(lambda x, y: x + y, (10, 20), (1, 2))) == [11, 22]


def test_myzip_gen_truncates():
    assert list(myzip_gen("abc", "xyz123")) == [("a", "x"), ("b", "y"), ("c", "z")]


def test_mymap_pad_padding_and_lengths():
    s1, s2 = "abc", "xy"
    assert list(mymap_pad(s1, s2)) == [("a", "x"), ("b", "y"), ("c", None)]
    assert list(mymap_pad(s1, s2, pad=99)) == [("a", "x"), ("b", "y"), ("c", 99)]


def test_generator_is_single_pass():
    g = (x * x for x in range(3))
    first = first_two(g)
    rest = consume_all(g)
    # После двух next() в генераторе остаётся один элемент
    assert first == (0, 1)
    assert rest == [4]


def test_double_gen_pairs():
    assert list(double_gen([1, 2, 3])) == [(1, 1), (2, 2), (3, 3)]
