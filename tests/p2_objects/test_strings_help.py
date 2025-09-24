# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.strings_help_ import (
    dunder_add_equivalence,
    help_snippet_for_replace,
    list_string_attrs,
    method_doc,
    type_name,
)


def test_dir_contains_core_names():
    s = "Code"
    attrs = list_string_attrs(s)
    for name in ("upper", "replace", "split", "__add__"):
        assert name in attrs


def test_dunder_add_equivalence_matches_plus():
    s = "Code"
    a, b = dunder_add_equivalence(s, "head!")
    assert a == b == "Codehead!"


def test_method_doc_has_keywords():
    doc = method_doc(str, "replace").lower()
    # робастные проверки: не зависят от точной формулировки
    assert "replace" in doc
    assert "old" in doc and "new" in doc


def test_type_name_is_str():
    assert type_name("x") == "str"


def test_help_snippet_for_replace_contains_replace_word():
    snippet = help_snippet_for_replace().lower()
    assert "replace" in snippet
    # часто встречается "built-in function" или "method"
    assert ("function" in snippet) or ("method" in snippet)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_help_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "s = Code" in out
    assert "'upper' in dir?  True" in out
    assert "'__add__' in dir?  True" in out
    assert "s + 'head!' = Codehead!" in out
    assert "replace doc has 'old' and 'new'?  True" in out
    assert "type_name(s) = str" in out
