# pylint: disable=missing-function-docstring
from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import reduce, wraps
from typing import Any, List, Tuple

# ---------- РЕКУРСИИ И АЛЬТЕРНАТИВЫ ----------


def mysum_recursive(seq: Iterable[Any]) -> Any:
    """Сумма последовательности рекурсией (предполагаем, что seq конечен)."""
    seq = list(seq)
    if not seq:
        return 0
    head, *tail = seq
    return head if not tail else head + mysum_recursive(tail)


def sumtree_recursive(tree: List[Any], *, trace: bool = False) -> int:
    """Сумма всех чисел в произвольно вложенных списках (depth-first, рекурсия)."""
    total = 0
    for item in tree:
        if isinstance(item, list):
            total += sumtree_recursive(item, trace=trace)
        else:
            if trace:
                print(item, end=", ")
            total += item
    return total


def sumtree_queue(tree: List[Any], *, trace: bool = False) -> int:
    """Сумма через явную очередь (breadth-first)."""
    total = 0
    items: List[Any] = list(tree)
    while items:
        front = items.pop(0)
        if isinstance(front, list):
            items.extend(front)
        else:
            if trace:
                print(front, end=", ")
            total += front
    return total


def sumtree_stack(tree: List[Any], *, trace: bool = False) -> int:
    """Сумма через явный стек (depth-first, порядок как у рекурсии)."""
    total = 0
    items: List[Any] = list(tree)
    while items:
        front = items.pop(0)
        if isinstance(front, list):
            items[:0] = front  # prepend — LIFO
        else:
            if trace:
                print(front, end=", ")
            total += front
    return total


# ---------- ФУНКЦИИ КАК ОБЪЕКТЫ, АТРИБУТЫ, АННОТАЦИИ, ДЕКОРАТОРЫ ----------


def make_attr_counter(start: int = 0) -> Callable[[], int]:
    """Счётчик со state в атрибуте функции (аналог static local)."""

    def inner() -> int:
        inner.count += 1  # type: ignore[attr-defined]
        return inner.count  # type: ignore[attr-defined]

    inner.count = start  # type: ignore[attr-defined]
    return inner


def annotated_sum(a: int, b: int, c: int = 0) -> int:
    """Просто сумма; аннотации отражены в __annotations__."""
    return a + b + c


# (аннотации заданы через сигнатуру; Python сам заполнит __annotations__)


def echo_decorator(prefix: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Простейший декоратор с сообщением перед вызовом."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"{prefix}{func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ---------- LAMBDA И ДИСПЕТЧЕРИ ----------


def build_actions() -> List[Callable[[int], int]]:
    """Таблица из 3 простых действий: *2, **2, //2."""
    return [
        (lambda x: x * 2),
        (lambda x: x**2),
        (lambda x: x // 2),
    ]


def apply_dispatch(key: str, text: str) -> str:
    """Словарь-«switch» с lambda-ми."""
    table = {
        "upper": (lambda s: s.upper()),
        "lower": (lambda s: s.lower()),
        "repeat4": (lambda s: f"{s * 4}!"),
    }
    return table[key](text)


def make_adder(x: int) -> Callable[[int], int]:
    """Замыкание из lambda — добавляет запомненное x."""
    return lambda y: x + y


# ---------- MAP/FILTER/REDUCE И УТИЛИТЫ ----------


def map_add(seq: Iterable[int], inc: int) -> List[int]:
    return list(map(lambda x: x + inc, seq))


def filter_positive(seq: Iterable[int]) -> List[int]:
    return list(filter(lambda x: x > 0, seq))


def reduce_sum(seq: Iterable[int]) -> int:
    return reduce(lambda acc, x: acc + x, seq)


def reduce_product(seq: Iterable[int]) -> int:
    return reduce(lambda acc, x: acc * x, seq)


# ---------- ПРИМЕР «ФУНКЦИИ КАК ДАННЫЕ» ----------


def exclaim(message: str) -> str:
    return f"{message}!"


def run_schedule(schedule: Iterable[Tuple[Callable[[str], str], str]]) -> List[str]:
    """Выполнить список (функция, аргумент) и вернуть результаты."""
    return [func(arg) for func, arg in schedule]
