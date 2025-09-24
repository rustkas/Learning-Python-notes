# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.strings_methods_ import (
    advanced_formats,
    find_substring,
    format_three_ways,
    replace_substring,
    rstrip_line,
    split_csv,
    strip_then_split,
    upper_and_isalpha,
)


def test_find_and_replace_do_not_mutate_original():
    s = "Code"
    assert find_substring(s, "od") == 1
    replaced = replace_substring(s, "od", "abl")
    assert replaced == "Cable"
    assert s == "Code"  # неизменяемость: исходная строка не изменилась


def test_split_and_chain_with_rstrip():
    line = "aaa,bbb,ccccc,dd\n"
    assert rstrip_line(line) == "aaa,bbb,ccccc,dd"
    assert split_csv("aaa,bbb,ccccc,dd") == ["aaa", "bbb", "ccccc", "dd"]
    assert strip_then_split(line) == ["aaa", "bbb", "ccccc", "dd"]


def test_case_and_isalpha():
    s = "code"
    up, is_alpha = upper_and_isalpha(s)
    assert up == "CODE"
    assert is_alpha is True


def test_format_three_ways():
    f1, f2, f3 = format_three_ways("Python", 3, 3)
    assert f1 == "Using Python version 3.12"
    assert f2 == "Using Python version 3.12"
    assert f3 == "Using Python version 3.12"


def test_advanced_formats_examples():
    a, b, c = advanced_formats()
    assert a == "3.14 | -0062"
    assert b == "296,999.26 | app"
    assert c == "296,999.26 | app"


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_methods_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "s = Code" in out
    assert "s.find('od') = 1" in out
    assert "s.replace('od','abl') = Cable" in out
    assert "line.rstrip().split(',') = ['aaa', 'bbb', 'ccccc', 'dd']" in out
    assert "format %  = Using Python version 3.12" in out
    assert "advanced2 = 296,999.26 | app" in out
