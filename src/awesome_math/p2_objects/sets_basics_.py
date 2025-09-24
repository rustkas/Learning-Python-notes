from __future__ import annotations

from typing import Iterable

__all__ = [
    "make_sets",
    "basic_ops",
    "remove_duplicates",
    "collection_difference",
    "order_neutral_equality",
    "mutating_demo",
    "main",
]


def make_sets() -> tuple[set[str], set[str]]:
    """Создаём множества из последовательностей."""
    x = set("hack")  # {'h','a','c','k'}
    y = {"a", "p", "p"}  # литерал множества; дубликаты отбрасываются -> {'a','p'}
    return x, y


def basic_ops(x: set[str], y: set[str]) -> tuple[set[str], set[str], set[str], bool]:
    """Пересечение, объединение, разность, проверка надмножества."""
    inter = x & y
    union = x | y
    diff = x - y
    is_super = x > y
    return inter, union, diff, is_super


def remove_duplicates(seq: Iterable[int]) -> list[int]:
    """Удаление дубликатов: возвращаем отсортированный список уникальных значений."""
    return sorted(set(seq))


def collection_difference(a: str, b: str) -> set[str]:
    """Разность символов двух строк как множеств: set(a) - set(b)."""
    return set(a) - set(b)


def order_neutral_equality(a: Iterable, b: Iterable) -> bool:
    """Проверка равенства без учёта порядка и дубликатов: set(a) == set(b)."""
    return set(a) == set(b)


def mutating_demo() -> tuple[set[str], set[str]]:
    """
    Демонстрация изменяемости множества:
    добавим 'p', удалим 'a', 'discard' игнорирует отсутствие элемента.
    """
    s = set("hack")
    before = set(s)
    s.add("p")  # добавили новый элемент
    s.discard("x")  # безопасно: нет ошибки, если 'x' отсутствует
    s.remove("a")  # удалим существующий элемент
    after = s
    return before, after


def main() -> None:
    """Демонстрация примеров из книги"""
    x, y = make_sets()
    inter, union, diff, is_super = basic_ops(x, y)

    print("X(sorted) =", sorted(x))
    print("Y(sorted) =", sorted(y))
    print("X & Y (sorted) =", sorted(inter))
    print("X | Y (sorted) =", sorted(union))
    print("X - Y (sorted) =", sorted(diff))
    print("X > Y =", is_super)

    seq = [3, 1, 2, 1, 3, 1]
    print("dedup =", remove_duplicates(seq))

    diff2 = collection_difference("code", "hack")
    print("diff('code','hack')(sorted) =", sorted(diff2))

    print("order-neutral equality 'code' vs 'deoc' =", order_neutral_equality("code", "deoc"))

    before, after = mutating_demo()
    print("mutating before(sorted) =", sorted(before))
    print("mutating after(sorted)  =", sorted(after))


if __name__ == "__main__":
    main()
