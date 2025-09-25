# pylint: disable=missing-function-docstring

from awesome_math.p5_numbers.dynamic_typing import (
    eq_vs_is,
    func_args_binding,
    rebind_vs_mutate_demo,
    shallow_vs_deep_copy,
    type_hint_is_optional,
    weakref_demo,
)


def test_rebind_vs_mutate_demo():
    l1, l2, l3 = rebind_vs_mutate_demo()
    # l1 и l2 — это один и тот же объект (shared), мутация отразилась в обоих
    assert l1 is l2
    assert l1 == [99, 2, 3]
    assert l2 == [99, 2, 3]
    # l3 — независимая копия
    assert l3 == [99, 2, 3, 4] or l3 == [1, 2, 3, 4]
    # Формально l3 не обязан быть is l1/l2 и обычно им не является
    assert l3 is not l1 and l3 is not l2


def test_func_args_binding():
    outer_list = [0]
    outer_x = 100
    lst_after, inner_x = func_args_binding(outer_list, outer_x)

    # Мутация списка видна снаружи
    assert outer_list == [0, 42]
    assert lst_after is outer_list

    # Перепривязка скалярного параметра внутри функции не меняет внешний объект
    assert outer_x == 100
    assert inner_x == "rebound"


def test_eq_vs_is_basic():
    # Для независимых списков: равны по значению, но не тождественны
    a = [1, 2, 3]
    b = [1, 2, 3]
    eq, ident = eq_vs_is(a, b)
    assert eq is True
    assert ident is False

    # Для одной и той же ссылки — оба True
    c = a
    eq2, ident2 = eq_vs_is(a, c)
    assert eq2 is True
    assert ident2 is True


def test_shallow_vs_deep_copy():
    data = {"x": [1, 2], "y": {"z": 3}}
    shallow, deep = shallow_vs_deep_copy(data)

    # Топ-уровень разные объекты
    assert shallow is not data
    assert deep is not data

    # При неглубокой копии вложенные объекты — те же
    assert shallow["x"] is data["x"]
    assert shallow["y"] is data["y"]

    # При глубокой копии вложенные объекты — новые
    assert deep["x"] is not data["x"]
    assert deep["y"] is not data["y"]

    # Изменение вложенного списка затронет shallow, но не deep
    data["x"].append(99)
    assert shallow["x"] == [1, 2, 99]
    assert deep["x"] == [1, 2]


def test_weakref_demo():
    w, steps = weakref_demo()
    # Слабая ссылка должна обнулиться (объект собран GC)
    assert w() is None
    # Обычно достаточно 0–1 шагов; но допустим небольшой разброс
    assert steps in (1, 2, 3)


def test_type_hint_is_optional():
    # Аннотации не ограничивают тип: можно передать любой
    s1 = type_hint_is_optional(123)
    s2 = type_hint_is_optional("abc")
    s3 = type_hint_is_optional([1, 2, 3])

    assert "value=123" in s1 and "type=int" in s1
    assert "value='abc'" in s2 and "type=str" in s2
    assert "value=[1, 2, 3]" in s3 and "type=list" in s3
