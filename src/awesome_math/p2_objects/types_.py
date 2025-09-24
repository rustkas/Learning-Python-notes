# pylint: disable=unidiomatic-typecheck
from __future__ import annotations

from typing import Any, Iterable, List, Tuple

__all__ = [
    "get_type",
    "get_type_of_type",
    "type_eq_examples_for_list",
    "polymorphic_len",
    "first_item_duck",
    "sum_numbers_duck",
    "main",
]


def get_type(obj: Any) -> type:
    """Вернуть класс (тип) объекта: type(obj)."""
    return type(obj)


def get_type_of_type(obj: Any) -> type:
    """Вернуть тип типа: type(type(obj)) — обычно это <class 'type'>."""
    return type(type(obj))


def type_eq_examples_for_list(obj: Any) -> Tuple[bool, bool, bool]:
    """
    Три способа проверки «списочности»:
    1) type(obj) is type([])   2) type(obj) is list   3) isinstance(obj, list)
    """
    same_as_real_object = type(obj) is type([])  # OK для Ruff: сравнение типов через `is`
    same_as_type_name = type(obj) is list  # OK для Ruff
    is_instance = isinstance(obj, list)  # предпочтительный способ
    return (same_as_real_object, same_as_type_name, is_instance)


def polymorphic_len(objs: Iterable[Any]) -> List[int]:
    """
    Полиморфизм: len() работает для множества контейнеров без проверок типов.
    Возвращаем список длин.
    """
    return [len(o) for o in objs]  # EAFP: предположим, что объект поддерживает len()


def first_item_duck(obj: Any) -> Any:
    """
    Взять «первый» элемент полиморфно: пробуем итерироваться (iter/next).
    Работает для строк, списков, диапазонов, кортежей, генераторов и т.п.
    """
    it = iter(obj)  # если не итерируемый — здесь упадём с TypeError
    return next(it)  # если пустой — здесь StopIteration


def sum_numbers_duck(values: Iterable[float]) -> float:
    """
    Полиморфная сумма: работает для списков/кортежей/генераторов чисел.
    Никаких type-checks — лишь интерфейс «итерируемое из чисел».
    """
    return float(sum(values))


def main() -> None:
    """Демонстрация примеров из книги"""
    l_obj = [1, 2, 3]
    print("type([1, 2, 3]) ->", get_type(l_obj))
    print("type(type([1, 2, 3])) ->", get_type_of_type(l_obj))

    eq1, eq2, inst = type_eq_examples_for_list(l_obj)
    print("checks (type==type([]), type==list, isinstance) ->", eq1, eq2, inst)

    lens = polymorphic_len(["ab", [1, 2, 3], {"k": 1, "v": 2}])
    print("polymorphic len ->", lens)

    print("first_item('code') ->", first_item_duck("code"))
    print("first_item(range(5)) ->", first_item_duck(range(5)))

    print("sum_numbers_duck([1.5, 2.5]) ->", sum_numbers_duck([1.5, 2.5]))
    print(
        "sum_numbers_duck(i*i for i in range(3)) ->",
        sum_numbers_duck(i * i for i in range(3)),
    )


if __name__ == "__main__":
    main()
