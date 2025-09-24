# tests/p2_objects/test_quiz_ch4.py
# pylint: disable=missing-function-docstring
# pylint: disable=consider-using-f-string

import subprocess
import sys

from awesome_math.p2_objects import quiz_ch4_ as q


def test_core_types_contains_expected_minimum():
    kinds = [k.lower() for k in q.core_types()]
    for must in ("numbers", "strings", "lists", "dicts", "tuples", "sets"):
        assert must in kinds
    # bonus: присутствуют bool/none/type как упомянутые в тексте
    for nice in ("bool", "none", "type"):
        assert nice in kinds


def test_why_core_mentions_literals_and_open():
    txt = q.why_core()
    assert "встроены" in txt and ("литерал" in txt or "синтаксис" in txt)
    assert "open" in txt  # напоминание, что файлы создаются вызовом


def test_immutable_definition_and_kinds():
    definition, kinds = q.immutable_definition()
    assert "нельзя менять" in definition or "нельзя" in definition
    expect = {"numbers", "strings", "tuples"}
    assert set(kinds) == expect


def test_sequence_and_iterable_payload_shape():
    d = q.sequence_and_iterable()
    assert "sequence_def" in d and "iterable_def" in d
    seqs = set(d["sequence_examples"])  # type: ignore[index]
    assert {"strings", "lists", "tuples"} <= seqs
    iters = set(d["iterable_examples"])  # type: ignore[index]
    # файлы и range считаются итерируемыми
    assert {"range", "files"} <= iters


def test_mapping_info_is_dict_and_dict_is_core_mapping():
    d = q.mapping_info()
    assert isinstance(d, dict)
    assert d.get("core_mapping") == "dict"
    assert "порядок" in d.get("notes", "") or "вставк" in d.get("notes", "")


def test_polymorphism_definition_mentions_plus_and_strings():
    s = q.polymorphism_definition()
    assert "+" in s and ("строк" in s or "конкат" in s)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.quiz_ch4_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "Q1 core types ->" in out
    assert "Q2 why core   ->" in out
    assert "Q3 immutable  ->" in out and "numbers" in out and "strings" in out and "tuples" in out
    assert "Q4 sequence   ->" in out and "iterable" in out
    assert "Q5 mapping    ->" in out and "dict" in out
    assert "Q6 polymorph  ->" in out
