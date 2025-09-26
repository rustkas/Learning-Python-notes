# pylint: disable=missing-function-docstring,unnecessary-lambda-assignment
"""
Учебный модуль к главе "Function Basics":

- демонстрация def/return/lambda;
- полиморфизм операций;
- определение функций во время выполнения (внутри if);
- функции как объекты первого класса.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable, List


def times(x: Any, y: Any) -> Any:
    """Полиморфная «произведение/повторение»: работает для чисел и последовательностей."""
    return x * y


def intersect(seq1: Iterable[Any], seq2: Iterable[Any]) -> List[Any]:
    """
    «Почти пересечение»: возвращает список элементов из seq1, встречающихся в seq2,
    сохраняя порядок seq1 и позволяя дубликаты.
    """
    res: List[Any] = []
    for x in seq1:
        if x in seq2:
            res.append(x)
    return res


def select_transform(kind: str) -> Callable[[str], str]:
    """
    Показ того, что def выполняется во время рантайма:
    определяем и возвращаем разную функцию в зависимости от аргумента.
    """
    if kind == "upper":

        def func(s: str) -> str:
            return s.upper()
    else:

        def func(s: str) -> str:
            return s.lower()

    return func


# Анонимная функция (lambda) — одна выраженческая строка.
lambda_cube = lambda x: x**3  # noqa: E731


def returns_none() -> None:
    """Функция без return — возвращает None по умолчанию."""
    x = 1 + 1  # побочный безмолвный расчёт, чтобы линтер не ругался
    _ = x


def alias_call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Вызвать функцию через «псевдоним» (ещё раз: функции — объекты первого класса)."""
    other_name = func
    return other_name(*args, **kwargs)


def set_func_attr(func: Callable[..., Any], **attrs: Any) -> Callable[..., Any]:
    """Навесить пользовательские атрибуты на функцию и вернуть её (чисто демонстрация)."""
    for k, v in attrs.items():
        setattr(func, k, v)
    return func


__all__ = [
    "times",
    "intersect",
    "select_transform",
    "lambda_cube",
    "returns_none",
    "alias_call",
    "set_func_attr",
]
