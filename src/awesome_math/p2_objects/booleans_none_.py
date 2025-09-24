from __future__ import annotations

from typing import Any, Tuple

__all__ = [
    "compare_demo",
    "bool_value",
    "list_of_nones",
    "booleans_as_ints",
    "default_if_none",
    "is_none",
    "main",
]


def compare_demo(a: int, b: int) -> Tuple[bool, bool]:
    """Вернуть (a > b, a < b) — простая демонстрация булевых сравнений."""
    return a > b, a < b


def bool_value(obj: Any) -> bool:
    """Булево значение произвольного объекта (правдивость/ложность)."""
    return bool(obj)


def list_of_nones(n: int) -> list[None]:
    """Список из n значений None."""
    return [None] * n


def booleans_as_ints() -> tuple[bool, bool, bool]:
    """Проверка связи bool и int: True == 1, False == 0, isinstance(True, int)."""
    return (True == 1, False == 0, isinstance(True, int))


def default_if_none(x: Any, default: Any) -> Any:
    """Вернуть default, если x is None, иначе вернуть x (None-coalescing)."""
    return x if x is not None else default


def is_none(x: Any) -> bool:
    """Проверка через идентичность: x is None (рекомендовано, а не x == None)."""
    return x is None


def main() -> None:
    """Демонстрация примеров из книги"""
    gt, lt = compare_demo(1, 2)
    print("1 > 2 ->", gt)
    print("1 < 2 ->", lt)

    print("bool('hack') ->", bool_value("hack"))
    x = None
    print("None demo:", x)

    lst = list_of_nones(100)
    print("list_of_none size:", len(lst))

    t_eq1, f_eq0, is_int = booleans_as_ints()
    print("True == 1, False == 0, isinstance(True,int) ->", t_eq1, f_eq0, is_int)

    print("default_if_none(None, 'X') ->", default_if_none(None, "X"))
    print("default_if_none(0, 'X') ->", default_if_none(0, "X"))

    print("is_none(0) ->", is_none(0))
    print("is_none(None) ->", is_none(None))


if __name__ == "__main__":
    main()
