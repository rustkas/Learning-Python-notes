from __future__ import annotations

import string
from typing import Iterable, Optional

__all__ = [
    "starts_and_ends",
    "safe_find",
    "index_or_raise",
    "count_sub",
    "strip_variants",
    "normalize_casefold",
    "partition_once",
    "rpartition_once",
    "split_lines",
    "join_with_sep",
    "remove_punctuation",
    "align_variants",
    "main",
]


def starts_and_ends(s: str, prefix: str, suffix: str) -> tuple[bool, bool]:
    """Проверить начало/конец строки."""
    return s.startswith(prefix), s.endswith(suffix)


def safe_find(s: str, sub: str) -> int:
    """Безопасный поиск: возвращает индекс или -1 (в отличие от index())."""
    return s.find(sub)


def index_or_raise(s: str, sub: str) -> int:
    """Строгий поиск: как str.index — бросает ValueError, если нет."""
    return s.index(sub)  # пусть исключение поднимет сама строка


def count_sub(s: str, sub: str) -> int:
    """Подсчитать количество неперекрывающихся вхождений подстроки."""
    return s.count(sub)


def strip_variants(s: str, chars: Optional[str] = None) -> tuple[str, str, str]:
    """
    Вернёт (strip, lstrip, rstrip).
    chars=None означает пробельные символы; иначе — удалить набор chars.
    """
    return s.strip(chars), s.lstrip(chars), s.rstrip(chars)


def normalize_casefold(s: str) -> str:
    """
    Нормализовать регистр для сравнения (лучше, чем .lower() для некоторых языков).
    Пример: 'straße'.casefold() -> 'strasse'
    """
    return s.casefold()


def partition_once(s: str, sep: str) -> tuple[str, str, str]:
    """Один раз разделить слева (всегда возвращает тройку)."""
    return s.partition(sep)


def rpartition_once(s: str, sep: str) -> tuple[str, str, str]:
    """Один раз разделить справа (всегда возвращает тройку)."""
    return s.rpartition(sep)


def split_lines(s: str, keepends: bool = False) -> list[str]:
    """Разбить по переводам строк; можно сохранить разделители."""
    return s.splitlines(keepends=keepends)


def join_with_sep(parts: Iterable[str], sep: str = " ") -> str:
    """Собрать строки через разделитель (предпочтительнее, чем + в цикле)."""
    return sep.join(parts)


def remove_punctuation(s: str) -> str:
    """Удалить всю ASCII-пунктуацию через translate/maketrans."""
    table = str.maketrans("", "", string.punctuation)
    return s.translate(table)


def align_variants(s: str, width: int, fillchar: str = " ") -> tuple[str, str, str]:
    """Вернёт (ljust, rjust, center)."""
    return s.ljust(width, fillchar), s.rjust(width, fillchar), s.center(width, fillchar)


def main() -> None:
    """Демонстрация примеров из книги"""
    s = "Python,strings\n"
    print("s =", s.rstrip("\n"))

    # startswith/endswith
    print("starts/ends:", starts_and_ends(s, "Py", "\n"))

    # find vs index, count
    print("find(',') =", safe_find(s, ","))
    print("count('n') =", count_sub(s, "n"))

    # strip/lstrip/rstrip
    print("strip ws =", strip_variants("  *hello*  "))
    print("strip *  =", strip_variants("**hello**", "*"))

    # casefold
    print("casefold('straße') =", normalize_casefold("straße"))

    # partition / rpartition
    print("partition(',')  =", partition_once("a,b,c", ","))
    print("rpartition(',') =", rpartition_once("a,b,c", ","))

    # splitlines
    print("splitlines keep=False =", split_lines("x\ny\r\nz", keepends=False))
    print("splitlines keep=True  =", split_lines("x\ny\r\nz", keepends=True))

    # join
    print("join with '-' =", join_with_sep(["code", "more", "fun"], "-"))

    # translate/maketrans
    print("remove punctuation =", remove_punctuation("Hello, world! (v2)"))

    # alignment
    print("align '.' width=5 =", align_variants("hi", 5, "."))


if __name__ == "__main__":
    main()
