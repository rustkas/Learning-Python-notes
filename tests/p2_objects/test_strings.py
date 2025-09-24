# pylint: disable=missing-function-docstring
# pylint: disable=unsupported-assignment-operation
import subprocess
import sys

import pytest

from awesome_math.p2_objects.strings_ import (
    char_at,
    concat,
    copy_string,
    everything_but_last,
    first_char,
    last_char,
    neg_index_equivalence,
    repeat,
    seq_len,
    slice_between,
    slice_from,
    slice_to,
)


def test_basic_index_and_len():
    s = "Code"
    assert seq_len(s) == 4
    assert first_char(s) == "C"
    assert char_at(s, 1) == "o"
    assert last_char(s) == "e"
    assert char_at(s, -2) == "d"


def test_negative_index_equivalence():
    s = "Code"
    a, b = neg_index_equivalence(s, -1)
    assert a == b == "e"
    a, b = neg_index_equivalence(s, -2)
    assert a == b == "d"


def test_slices_variants():
    s = "Code"
    assert slice_between(s, 1, 3) == "od"
    assert slice_from(s, 1) == "ode"
    assert slice_between(s, 0, 3) == "Cod"
    assert slice_to(s, 3) == "Cod"
    assert everything_but_last(s) == "Cod"
    assert copy_string(s) == "Code"


def test_concat_and_repeat():
    s = "Code"
    assert concat(s, "xyz") == "Codexyz"
    assert s == "Code"  # неизменяемость
    assert repeat(s, 2) == "CodeCode"
    assert repeat("", 8) == ""
    with pytest.raises(ValueError):
        repeat(s, -1)


def test_index_errors_and_slice_clipping():
    s = "Code"
    with pytest.raises(IndexError):
        char_at(s, 999)  # индексация падает
    # а срез не падает — просто пустая строка
    assert slice_between(s, 999, 1000) == ""


def test_immutable_assignment_disallowed():
    s = "Code"
    with pytest.raises(TypeError):
        # type: ignore[index]
        s[0] = "X"  # строки неизменяемы


def test_run_as_module():
    """Проверяем, что демонстрация запускается и печатает ожидаемые строки."""
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "s = Code" in out
    assert "len(s) = 4" in out
    assert "s[1:3] = od" in out
    assert "s + 'xyz' = Codexyz" in out
