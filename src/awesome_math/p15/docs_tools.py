# pylint: disable=missing-function-docstring
"""
docs_tools: мини-утилиты для демонстрации документации в Python.

Содержит:
- docstring’и у модуля, функций, классов и методов;
- фильтрацию атрибутов через dir();
- извлечение docstring’ов и Pydoc-текста.
"""

from __future__ import annotations

import pydoc
from typing import List


def public_attrs(obj: object) -> List[str]:
    """
    Вернуть отсортированный список «публичных» атрибутов объекта:
    без имён, начинающихся с '_' (включая '__dunder__').
    """
    return sorted([name for name in dir(obj) if not name.startswith("_")])


def get_doc(obj: object) -> str:
    """
    Вернуть docstring объекта (или пустую строку, если его нет).
    """
    return obj.__doc__ or ""


def pydoc_text(obj: object) -> str:
    """
    Вернуть текстовую справку Pydoc по объекту (как даёт help()).
    Удобно для автотестов, т.к. это просто строка.
    """
    return pydoc.render_doc(obj, "Help on %s")


def square(x: int | float) -> int | float:
    r"""
    Возвращает квадрат числового аргумента.

    Пример:
    >>> square(3)
    9
    """
    return x**2


class Demo:
    """Пример класса с docstring и методом."""

    def shout(self, text: str) -> str:
        """Вернуть текст В ВЕРХНЕМ РЕГИСТРЕ."""
        return text.upper()


__all__ = [
    "public_attrs",
    "get_doc",
    "pydoc_text",
    "square",
    "Demo",
]
