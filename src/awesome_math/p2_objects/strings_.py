from __future__ import annotations

from typing import Optional

__all__ = [
    "seq_len",
    "char_at",
    "first_char",
    "last_char",
    "index_from_end",
    "slice_between",
    "slice_from",
    "slice_to",
    "everything_but_last",
    "copy_string",
    "concat",
    "repeat",
    "neg_index_equivalence",
    "main",
]


def seq_len(s: str) -> int:
    """Длина строки (обёртка над len для симметрии интерфейса)."""
    return len(s)


def char_at(s: str, i: int) -> str:
    """Символ по индексу i (может быть отрицательным). Может бросить IndexError."""
    return s[i]


def first_char(s: str) -> str:
    """Первый символ."""
    return s[0]


def last_char(s: str) -> str:
    """Последний символ."""
    return s[-1]


def index_from_end(s: str, k: int) -> str:
    """k-й с конца (k>=1): 1 -> последний, 2 -> предпоследний..."""
    if k <= 0:
        raise ValueError("k must be >= 1")
    return s[-k]


def slice_between(s: str, i: Optional[int], j: Optional[int]) -> str:
    """Срез s[i:j] (None значит отсутствующую границу)."""
    return s[i:j]  # Python сам корректно обрабатывает None


def slice_from(s: str, i: int) -> str:
    """Срез от i до конца."""
    return s[i:]


def slice_to(s: str, j: int) -> str:
    """Срез от начала до j (не включая j)."""
    return s[:j]


def everything_but_last(s: str) -> str:
    """Всё, кроме последнего символа."""
    return s[:-1]


def copy_string(s: str) -> str:
    """Полная копия строки (для строк не нужна, но полезно для других последовательностей)."""
    return s[:]


def concat(s: str, t: str) -> str:
    """Конкатенация."""
    return s + t


def repeat(s: str, n: int) -> str:
    """Повторение строки n раз."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return s * n


def neg_index_equivalence(s: str, i_neg: int) -> tuple[str, str]:
    """
    Показывает эквивалентность отрицательного индекса и положительного:
    s[i_neg]  vs  s[len(s)+i_neg]
    """
    return (s[i_neg], s[len(s) + i_neg])


def main() -> None:
    """Демонстрация примеров из книги"""
    s = "Code"
    print("s =", s)
    print("len(s) =", seq_len(s))
    print("s[0] =", char_at(s, 0))
    print("s[1] =", char_at(s, 1))
    print("s[-1] =", char_at(s, -1))
    print("s[-2] =", char_at(s, -2))
    print("s[1:3] =", slice_between(s, 1, 3))
    print("s[1:]  =", slice_from(s, 1))
    print("s[0:3] =", slice_between(s, 0, 3))
    print("s[:3]  =", slice_to(s, 3))
    print("s[:-1] =", everything_but_last(s))
    print("s[:]   =", copy_string(s))
    print("s + 'xyz' =", concat(s, "xyz"))
    print("s * 8    =", repeat(s, 8))


if __name__ == "__main__":
    main()
