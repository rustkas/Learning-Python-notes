# pylint: disable=missing-function-docstring
from __future__ import annotations

import io
import sys

import pytest

from awesome_math.p18.arguments_basics import (
    call_with_unpack,
    collect_keyword,
    collect_positional,
    greater,
    intersect,
    kw_defaults,
    kwonly,
    less,
    min_varargs,
    minmax,
    mix_collect,
    multiple_results,
    mutate_first_item,
    posonly,
    print3,
    rebind_local,
    sum4,
    union,
)


def test_pass_by_assignment_and_mutation():
    x = 1
    y = [1, 2]
    _ = rebind_local(x)
    assert x == 1  # локальное переназначение не влияет
    mutate_first_item(x, y)
    assert y == ["mod", 2]  # мутация на месте видна


def test_multiple_results_unpack():
    x, lst = multiple_results(0, [0])  # was: l
    assert x == 2 and lst == [3, 4]


def test_keywords_and_defaults():
    assert kw_defaults(1) == (1, 2, 3)
    assert kw_defaults(1, c=5) == (1, 2, 5)
    assert kw_defaults(a=7, b=8, c=9) == (7, 8, 9)


def test_collectors_and_unpacking():
    assert collect_positional(1, 2, 3) == (1, 2, 3)
    assert collect_keyword(a=1, b=2) == {"a": 1, "b": 2}
    a, pargs, kargs = mix_collect(1, 2, 3, x=4)
    assert a == 1 and pargs == (2, 3) and kargs == {"x": 4}

    assert sum4(1, 2, 3, 4) == 10
    assert call_with_unpack((1, 2), {"c": 3, "d": 4}) == 10
    # микс звёздочек
    assert sum4(*(1, 2), **{"c": 3, "d": 4}) == 10


def test_keyword_only_and_positional_only():
    assert kwonly(1) == (1, " ", "\n")
    assert kwonly(1, sep=".", end="!") == (1, ".", "!")
    with pytest.raises(TypeError):
        # sep нельзя позиционно
        kwonly(1, ".")  # type: ignore[misc]  # pylint: disable=too-many-function-args

    assert posonly(1, 2, 3) == (1, 2, 3)
    assert posonly(1, 2, c=3) == (1, 2, 3)
    with pytest.raises(TypeError):
        posonly(a=1, b=2, c=3)  # type: ignore[call-arg]  # pylint: disable=positional-only-arguments-expected


def test_min_and_minmax():
    assert min_varargs(3, 4.0, 1, 2) == 1
    assert min_varargs("bb", "aa") == "aa"
    with pytest.raises(ValueError):
        min_varargs()

    nums = (4, 2, 1, 5, 6, 3)
    assert minmax(less, *nums) == 1
    assert minmax(greater, *nums) == 6


def test_intersect_union():
    s1, s2, s3 = "HACKK", "CODE", "CASH"
    assert intersect(s1, s2) == ["C"]
    assert intersect([1, 2, 3, 4], (1, 4)) == [1, 4]
    assert intersect(s1, s2, s3) == ["C"]

    u = union(s1, s2, s3)
    assert u == ["H", "A", "C", "K", "O", "D", "E", "S"]


def test_print3_emulation_captures_output(monkeypatch: pytest.MonkeyPatch):
    buf = io.StringIO()
    print3(1, 2, 3, sep=":", end="!", file=buf)
    assert buf.getvalue() == "1:2:3!"

    # по умолчанию пишет в stdout
    buf2 = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf2)
    print3("x", "y")
    assert buf2.getvalue() == "x y\n"

    # неизвестный ключ — TypeError (keyword-only)
    with pytest.raises(TypeError):
        print3(1, 2, bad="x")  # type: ignore[call-arg]  # pylint: disable=unexpected-keyword-arg
