# pylint: disable=missing-function-docstring,
import subprocess
import sys

import pytest

from awesome_math.p2_objects.strings_more_ import (
    align_variants,
    count_sub,
    index_or_raise,
    join_with_sep,
    normalize_casefold,
    partition_once,
    remove_punctuation,
    rpartition_once,
    safe_find,
    split_lines,
    starts_and_ends,
    strip_variants,
)


def test_starts_ends_and_find_index_count():
    s = "abc,def"
    starts, ends = starts_and_ends(s, "ab", "ef")
    assert starts is True and ends is True
    assert safe_find(s, ",") == 3
    assert count_sub(s, "e") == 1
    with pytest.raises(ValueError):
        index_or_raise(s, "ZZZ")  # строгий поиск — должен упасть


def test_strip_variants_default_and_custom_chars():
    assert strip_variants("  hello  ") == ("hello", "hello  ", "  hello")
    assert strip_variants("**hello**", "*") == ("hello", "hello**", "**hello")


def test_casefold_vs_lower_example():
    # важный пример: ß -> ss
    assert normalize_casefold("straße") == "strasse"


def test_partition_and_rpartition():
    assert partition_once("a,b,c", ",") == ("a", ",", "b,c")
    assert rpartition_once("a,b,c", ",") == ("a,b", ",", "c")
    # если разделителя нет — стандартное поведение:
    assert partition_once("abc", ",") == ("abc", "", "")
    assert rpartition_once("abc", ",") == ("", "", "abc")


def test_splitlines_keepends_and_join():
    s = "x\ny\r\nz"
    assert split_lines(s, keepends=False) == ["x", "y", "z"]
    assert split_lines(s, keepends=True) == ["x\n", "y\r\n", "z"]
    assert join_with_sep(["a", "b", "c"], "-") == "a-b-c"


def test_remove_punctuation_and_align():
    assert remove_punctuation("Hello, world! (v2)") == "Hello world v2"
    left, right, center = align_variants("hi", 5, ".")
    assert left == "hi..."
    assert right == "...hi"
    assert center in ("..hi.", ".hi..")  # центрирование ок, один символ может «гулять»


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_more_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "starts/ends: (True, True)" in out
    assert "find(',') = 6" in out
    assert "count('n') = 2" in out
    assert "partition(',')  = ('a', ',', 'b,c')" in out
    assert "rpartition(',') = ('a,b', ',', 'c')" in out
    assert "remove punctuation = Hello world v2" in out
    assert "align '.' width=5 = ('hi...', '...hi', " in out
