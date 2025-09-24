from __future__ import annotations

from collections import namedtuple
from typing import Any

__all__ = [
    "make_tuple_example",
    "sequence_ops",
    "try_assign_first",
    "rebuild_tuple_replace_first",
    "unpack_a_middle_c",
    "as_dict_key_demo",
    "nested_mutable_demo",
    "namedtuple_point_demo",
    "main",
]


def make_tuple_example() -> tuple[int, str, float]:
    """Учебный кортеж разных типов."""
    return (123, "text", 1.23)


def sequence_ops(t: tuple[Any, ...]) -> tuple[Any, list[Any], tuple[Any, ...], tuple[Any, ...]]:
    """
    Базовые операции последовательностей для кортежа:
    - первый элемент,
    - срез до последнего (списком для наглядности),
    - конкатенация с (4, 5, 6),
    - повторение * 2.
    """
    first = t[0]
    slice_upto_last = list(t[:-1])  # просто показать, что это новая коллекция
    concat_new = t + (4, 5, 6)
    repeat_new = t * 2
    return first, slice_upto_last, concat_new, repeat_new


def try_assign_first(t: tuple[Any, ...]) -> bool:
    """
    Проверяем неизменяемость: попытка t[0] = 'X' должна дать TypeError.
    Возвращаем True, если поймали TypeError.
    """
    try:
        # type: ignore[index]
        t[0] = "X"  # pylint: disable=unsupported-assignment-operation
    except TypeError:
        return True
    return False


def rebuild_tuple_replace_first(t: tuple[Any, ...], new_first: Any) -> tuple[Any, ...]:
    """Как «изменять» кортеж: создаём новый из частей."""
    return (new_first,) + t[1:]


def unpack_a_middle_c(seq: tuple[Any, ...]) -> tuple[Any, list[Any], Any]:
    """Расширенная распаковка: a, *middle, c."""
    a, *middle, c = seq
    return a, middle, c


def as_dict_key_demo() -> tuple[dict[tuple[str, int], str], str]:
    """
    Кортеж как ключ словаря.
    Возвращает (словарь, извлечённое_значение_по_ключу('x',1)).
    """
    d: dict[tuple[str, int], str] = {("x", 1): "point_x1", ("y", 2): "point_y2"}
    return d, d[("x", 1)]


def nested_mutable_demo() -> tuple[tuple[int, list[int]], tuple[int, list[int]]]:
    """
    Кортеж, содержащий список: сам кортеж неизменяем, но список внутри можно менять.
    Возвращает (снимок_до, после_добавления_элемента_в_вложенный_список).
    """
    t = (1, [2, 3])
    before = (t[0], list(t[1]))  # копия внутреннего списка для стабильного "до"
    t[1].append(4)
    after = t
    return before, after


def namedtuple_point_demo() -> tuple[Any, int, int]:
    """
    Пример namedtuple поверх tuple: удобные имена полей.
    Возвращает (p, p.x, p.y).
    """
    Point = namedtuple("Point", "x y")
    p = Point(2, 3)
    return p, p.x, p.y


def main() -> None:
    """Демонстрация примеров из книги"""
    t = make_tuple_example()
    print("t =", t)

    first, upto_last, concat_new, repeat_new = sequence_ops(t)
    print("t[0] =", first)
    print("t[:-1] =", upto_last)
    print("t + (4, 5, 6) =", concat_new)
    print("t * 2 =", repeat_new)
    print("t unchanged =", t)

    print("assign_error =", try_assign_first(t))
    replaced = rebuild_tuple_replace_first(t, "Z")
    print("replaced_first =", replaced)

    a, middle, c = unpack_a_middle_c((1, 2, 3, 4))
    print("unpack a,*middle,c =", (a, middle, c))

    d, fetched = as_dict_key_demo()
    print("dict_by_tuple_key =", d)
    print("dict_by_tuple_key[('x', 1)] =", fetched)

    before, after = nested_mutable_demo()
    print("nested before =", before)
    print("nested after  =", after)

    p, px, py = namedtuple_point_demo()
    print("namedtuple Point =", p, px, py)


if __name__ == "__main__":
    main()
