# pylint: disable=missing-function-docstring
import types

import pytest

import awesome_math.p16.function_basics as fb


def test_times_numbers_and_strings():
    # числа
    assert fb.times(3, 4) == 12
    # строка * число — повторение
    assert fb.times("Py", 3) == "PyPyPy"
    # список * число — повторение
    assert fb.times([1, 2], 2) == [1, 2, 1, 2]


def test_intersect_strings_and_mixed_types():
    # строки
    assert fb.intersect("HACK", "CHOK") == ["H", "C", "K"]
    # список и кортеж
    assert fb.intersect([1, 2, 3, 2], (1, 4, 2)) == [1, 2, 2]
    # range и множество
    assert fb.intersect(range(5), {2, 4, 6}) == [2, 4]


def test_select_transform_runtime_def_execution():
    upper = fb.select_transform("upper")
    lower = fb.select_transform("lower")
    assert upper("hack") == "HACK"
    assert lower("HACK") == "hack"
    # убеждаемся, что это именно функции
    assert isinstance(upper, types.FunctionType)
    assert isinstance(lower, types.FunctionType)


def test_lambda_cube_is_anonymous_function():
    assert callable(fb.lambda_cube)
    assert fb.lambda_cube(3) == 27


def test_returns_none_default_behavior():
    assert fb.returns_none() is None


def test_first_class_functions_alias_and_attributes():
    # вызов через «псевдоним»
    assert fb.alias_call(fb.times, 2, 5) == 10
    # навешиваем атрибут на функцию
    fb.set_func_attr(fb.times, tag="ok", version=1)
    assert getattr(fb.times, "tag") == "ok"
    assert getattr(fb.times, "version") == 1


def test_polymorphism_errors_when_interface_not_supported():
    # если интерфейс не поддержан — Python сам поднимет исключение
    with pytest.raises(TypeError):
        fb.intersect([1, 2, 3], 42)  # int не итерируем
