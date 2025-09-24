# pylint: disable=missing-function-docstring
import subprocess
import sys

from awesome_math.p2_objects.dicts_basics_ import (
    build_by_assignment,
    fetch_and_change,
    from_keywords,
    from_zip,
    insertion_order_demo,
    iteration_materials,
    loop_formats_examples,
    make_person_literal,
    missing_key_strategies,
    nested_record_demo,
    update_and_union_demo,
)


def test_make_and_change():
    person = make_person_literal()
    assert person == {"name": "Pat", "job": "dev", "age": 40}
    name, changed = fetch_and_change()
    assert name == "Pat"
    assert changed == {"name": "Pat", "job": "mgr", "age": 40}


def test_building_variants():
    assert build_by_assignment() == {"name": "Pat", "job": "dev", "age": 40}
    assert from_keywords() == {"name": "Pat", "job": "dev", "age": 40}
    assert from_zip() == {"name": "Pat", "job": "dev", "age": 40}


def test_insertion_order():
    assert insertion_order_demo() == ["x", "y", "z"]


def test_nested_record_and_append():
    rec0, name_dict, last, jobs0, last_job, rec1 = nested_record_demo()
    assert name_dict == {"first": "Pat", "last": "Smith"}
    assert last == "Smith"
    assert jobs0[:2] == ["dev", "mgr"]
    assert last_job == "mgr"
    assert rec1["jobs"] == ["dev", "mgr", "janitor"]
    assert rec0["jobs"] == ["dev", "mgr", "janitor"]  # возвращено уже после append


def test_missing_key_strategies_and_growth():
    miss = missing_key_strategies()
    assert miss["dict"] == {"a": 1, "b": 2, "c": 3, "d": 4}
    assert miss["exists_e"] is False
    assert miss["safe_get_e"] == "missing"
    assert miss["ternary_e"] == 0


def test_update_and_union():
    base, updated, union_new = update_and_union_demo()
    assert base == {"a": 1, "b": 2}
    assert updated == {"a": 1, "b": 200, "c": 3}
    assert union_new == {"a": 1, "b": 200, "c": 3}


def test_iteration_helpers_and_loops():
    d, keys_list, values_list, items_list = iteration_materials()
    assert d == {"a": 1, "b": 2, "c": 3}
    assert keys_list == ["a", "b", "c"]
    assert values_list == [1, 2, 3]
    assert items_list == [("a", 1), ("b", 2), ("c", 3)]
    a, b = loop_formats_examples(d)
    assert a == ["a => 1", "b => 2", "c => 3"]
    assert b == ["a => 1", "b => 2", "c => 3"]


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.dicts_basics_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "person = {'name': 'Pat', 'job': 'dev', 'age': 40}" in out
    assert "name = Pat" in out
    assert "after change job = {'name': 'Pat', 'job': 'mgr', 'age': 40}" in out
    assert "from keywords = {'name': 'Pat', 'job': 'dev', 'age': 40}" in out
    assert "from zip = {'name': 'Pat', 'job': 'dev', 'age': 40}" in out
    assert "insertion order = ['x', 'y', 'z']" in out
    assert (
        "rec after append = {'name': {'first': 'Pat', 'last': 'Smith'}, 'jobs': ['dev', 'mgr', 'janitor'], 'age': 40.5}"
        in out
    )
    assert "exists_e = False" in out
    assert "safe_get_e = missing" in out
    assert "ternary_e = 0" in out
    assert "updated = {'a': 1, 'b': 200, 'c': 3}" in out
    assert "union_new = {'a': 1, 'b': 200, 'c': 3}" in out
    assert "keys = ['a', 'b', 'c']" in out
    assert "items = [('a', 1), ('b', 2), ('c', 3)]" in out
    assert "loop implicit keys = ['a => 1', 'b => 2', 'c => 3']" in out
    assert "loop items = ['a => 1', 'b => 2', 'c => 3']" in out
