# pylint: disable=missing-function-docstring
import subprocess
import sys
from typing import get_type_hints

from awesome_math.p2_objects import type_hinting_ as th


def test_runtime_not_enforced_and_vars_annotations():
    # аннотировано как int, но работает и для строк — рантайм не проверяет типы
    assert th.add(1, 2) == 3
    assert th.add("1", "2") == "12"

    # переменная с хинтом int, но значение строка
    ua = th.user_annotations()
    user_keys = sorted(ua["raw"].keys())
    print(f"User.__annotations__ keys -> {user_keys}")
    print("User annotations resolved ->", ua["resolved"])
    assert isinstance(th.variable_v, str) and th.variable_v == "anything"

    # greet аннотирован str, но число проходит
    assert th.greet(123) == "Hi 123"


def test_class_and_function_annotations_introspection():
    ua = th.user_annotations()
    assert set(ua["raw"].keys()) == {"name", "age"}
    # resolved обычно те же значения типов
    assert ua["resolved"]["name"] is str
    assert ua["resolved"]["age"] is int

    fa = th.func_annotations()
    assert fa["raw"]["a"] is int and fa["raw"]["b"] is int and fa["raw"]["return"] is int
    resolved = get_type_hints(th.add)
    assert resolved["a"] is int and resolved["b"] is int and resolved["return"] is int


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.type_hinting_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "add(1, 2) -> 3" in out
    assert "add('1','2') -> 12" in out
    assert "greet(123) -> Hi 123" in out
    assert "variable_v annotation -> <class 'int'>, value -> anything" in out
    assert "User.__annotations__ keys -> ['age', 'name']" in out
    assert (
        "add annotations raw -> {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}"
        in out
    )
