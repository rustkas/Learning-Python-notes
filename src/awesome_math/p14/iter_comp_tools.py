# pylint: disable=missing-function-docstring, missing-class-docstring
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, TypeVar

T = TypeVar("T")
U = TypeVar("U")


# ---------- Базовые примеры: for vs. list-comprehension ----------


def squares_with_for(seq: Iterable[int]) -> List[int]:
    out: List[int] = []
    for x in seq:
        out.append(x * x)
    return out


def squares_with_list_comp(seq: Iterable[int]) -> List[int]:
    return [x * x for x in seq]


# ---------- Фильтрация и постобработка строк ----------


def rstrip_lines(lines: Iterable[str]) -> List[str]:
    return [line.rstrip() for line in lines]


def count_nonblank(lines: Iterable[str]) -> int:
    # считаем непустые (после strip) строки
    return len([line for line in lines if line.strip() != ""])


# ---------- Картизианское произведение (вложенные for) ----------


def cartesian_concat(a: Iterable[str], b: Iterable[str]) -> List[str]:
    return [x + y for x in a for y in b]


# ---------- zip и enumerate вместе ----------


def zip_enumerate_demo(a: Iterable[Any], b: Iterable[Any]) -> List[str]:
    return [f"{i}:{x}+{y}" for i, (x, y) in enumerate(zip(a, b))]


# ---------- map/filter и их эквиваленты на компрехеншенах ----------


def map_ord(s: str) -> List[int]:
    # map возвращает итератор — приводим к list для удобства тестов
    return list(map(ord, s))


def map_ord_comp(s: str) -> List[int]:
    return [ord(ch) for ch in s]


def filter_digit(strings: Iterable[str]) -> List[str]:
    # оставим только строки, состоящие из цифр
    return list(filter(str.isdigit, strings))


def filter_digit_comp(strings: Iterable[str]) -> List[str]:
    return [x for x in strings if x.isdigit()]


# ---------- Ручная итерация по протоколу iter/next ----------


def manual_collect(iterable: Iterable[T]) -> List[T]:
    it = iter(iterable)
    out: List[T] = []
    while True:
        try:
            item = next(it)
        except StopIteration:
            break
        out.append(item)
    return out


# ---------- Диагностика одно-/многопроходности ----------


@dataclass
class IterabilityInfo:
    is_self_iterator: bool
    independent_iters: Optional[bool]  # None — если объект сам итератор (один проход)


def inspect_iterable(iterable: Iterable[T]) -> IterabilityInfo:
    it1 = iter(iterable)
    # Если объект сам является итератором, iter(obj) is obj
    is_self = it1 is iterable  # type: ignore[comparison-overlap]

    if is_self:
        # Нельзя корректно проверить независимость двух итераторов: их нет
        return IterabilityInfo(is_self_iterator=True, independent_iters=None)

    # Для многопроходных формируем два итератора и продвигаем один
    it2 = iter(iterable)
    try:
        first1 = next(it1)
    except StopIteration:
        # пустой итерируемый — но это тоже «многопроходность»: итераторы независимы,
        # хотя оба уже исчерпаны. Считаем independent_iters=True.
        return IterabilityInfo(is_self_iterator=False, independent_iters=True)

    try:
        first2 = next(it2)
    except StopIteration:
        return IterabilityInfo(is_self_iterator=False, independent_iters=False)

    # Независимы, если стартовые элементы совпадают: у обоих позиция "с нуля".
    independent = first1 == first2
    return IterabilityInfo(is_self_iterator=False, independent_iters=independent)


# ---------- Однопроходный и многопроходный примеры ----------


class SinglePassRange:
    """
    Однопроходный «диапазон»: сам себе итератор.
    Поведение как у map/zip/enumerate/file: второй проход продолжает первый.
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.i = 0

    def __iter__(self) -> "SinglePassRange":
        return self

    def __next__(self) -> int:
        if self.i >= self.n:
            raise StopIteration
        val = self.i
        self.i += 1
        return val


class MultiPassListWrapper:
    """
    Многопроходная обёртка: каждый __iter__ даёт *независимый* итератор.
    """

    def __init__(self, data: Sequence[T]) -> None:
        self._data = list(data)

    def __iter__(self) -> Iterator[T]:
        # Возвращаем новый итератор списка
        return iter(self._data)


# ---------- Генераторное выражение и dict/set компрехеншены ----------


def genexpr_upper(lines: Iterable[str]) -> List[str]:
    # генератор даёт по одному; list собирает всё
    return list(line.upper() for line in lines)


def dict_comp_index(lines: Iterable[str]) -> Dict[int, str]:
    # оставим только строки, начинающиеся на 'L' или 'P'
    return {ix: line for ix, line in enumerate(lines) if line[:1] in ("L", "P")}
