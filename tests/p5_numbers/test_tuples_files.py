# pylint: disable=missing-function-docstring
from pathlib import Path

from awesome_math.p5_numbers.tuples_files import (
    compare_dicts_by_items,
    cyclic_structure_repr,
    json_roundtrip,
    make_namedtuple_record,
    none_preallocate,
    pickle_roundtrip,
    read_binary,
    read_text_lines,
    repetition_gotcha_demo,
    replace_first_in_tuple,
    shallow_vs_deep_copy,
    truthiness,
    tuple_basics,
    write_binary,
    write_text_lines,
)


def test_tuple_basics_and_replace():
    out = tuple_basics([1, 2, 3])
    assert out["t"] == (1, 2, 3)
    assert out["len"] == 3
    assert out["slice"] == (2,)
    assert out["replaced_first"] == (999, 2, 3)
    assert out["repeated"] == (1, 2, 3, 1, 2, 3)
    assert out["concatenated"] == (1, 2, 3, 0, 1)
    assert out["unpacked_literal"] == (1, 2, 3, -1, 0, 1, 2)

    assert replace_first_in_tuple((), 7) == (7,)
    assert replace_first_in_tuple((4, 5, 6), 1) == (1, 5, 6)


def test_namedtuple_record():
    out = make_namedtuple_record("Pat", 40.5, ["dev", "mgr"])
    rec = out["rec"]
    assert rec.name == "Pat"
    assert out["by_pos"] == ("Pat", ["dev", "mgr"])
    assert out["by_attr"] == ("Pat", ["dev", "mgr"])
    # _asdict даёт "словари-подобный" вид
    assert out["as_dict"]["age"] == 40.5


def test_shallow_vs_deep_copy():
    out = shallow_vs_deep_copy()
    assert out["original"]["a"][0] == 999
    assert out["shallow"]["a"][0] == 999  # разделяет вложенный список
    assert out["deep"]["a"][0] == 1  # глубокая копия независима
    assert out["shallow"]["b"]["x"] == 42
    assert out["deep"]["b"]["x"] == 10


def test_truthiness_and_none_preallocate():
    vals = ["", "x", [], [1], 0, 3, None, {}]
    assert truthiness(vals) == [False, True, False, True, False, True, False, False]

    pre = none_preallocate(3)
    assert pre == [None, None, "OK"]


def test_compare_dicts_by_items():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}
    d3 = {"a": 1, "b": 3}
    out12 = compare_dicts_by_items(d1, d2)
    assert out12["eq"] is True
    out13 = compare_dicts_by_items(d1, d3)
    assert out13["lt_by_items"] is True or out13["gt_by_items"] is True  # одна из сторон больше


def test_repetition_gotcha_and_cyclic_repr():
    out = repetition_gotcha_demo()
    assert out["y_shared"] == [[4, 0, 6], [4, 0, 6], [4, 0, 6]]
    assert out["y_isolated"][0][1] == 99
    assert out["y_isolated"][1] == [4, 5, 6]
    # циклическая структура печатается с [...]
    assert "[...]" in cyclic_structure_repr()


def test_text_file_roundtrip(tmp_path: Path):
    path = tmp_path / "notes.txt"
    write_text_lines(path, ["hello", "world"])
    lines = read_text_lines(path)
    assert lines == ["hello", "world"]


def test_binary_file_roundtrip(tmp_path: Path):
    path = tmp_path / "blob.bin"
    data = b"\x00\x01Python\x02\x03"
    write_binary(path, data)
    read_back = read_binary(path)
    assert read_back == data
    # срезы bytes ведут себя как строки
    assert read_back[2:8] == b"Python"


def test_pickle_roundtrip(tmp_path: Path):
    obj = {"a": 1, "b": [2, 3]}
    out = pickle_roundtrip(obj, tmp_path / "data.pkl")
    assert out == obj
    assert out is not obj  # новый объект


def test_json_roundtrip(tmp_path: Path):
    obj = {"name": {"first": "Pat", "last": "Smith"}, "job": ["dev", "mgr"], "age": 40.5}
    out = json_roundtrip(obj, tmp_path / "data.json")
    assert out == obj
