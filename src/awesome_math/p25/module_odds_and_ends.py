# src/awesome_math/p5_numbers/module_odds_and_ends.py
# pylint: disable=invalid-name,missing-function-docstring

"""
Примеры «модульных мелочей»: __all__/_, dual-mode, алиасы, динамический импорт,
интроспекция, __getattr__/__dir__, безопасная транзитивная перезагрузка.
"""

from __future__ import annotations

from importlib import import_module
from importlib import reload as _reload
from types import ModuleType
from typing import Iterable

# --- Экспорт и "приватность" -------------------------------------------------

__all__ = ["public_a", "listing", "import_by_name", "reload_all", "dual_mode_title"]

public_a = 1
_internal_b = 2  # скроется из from * (и не в __all__)

# --- Управляемый доступ к атрибутам модуля -----------------------------------


def __getattr__(name: str):
    # Виртуальные атрибуты для демонстрации
    if name == "virtual_times_two":
        return public_a * 2
    raise AttributeError(f"{name} is undefined")


def __dir__() -> list[str]:
    # Красивая выдача для dir(module)
    base = set(globals().keys()).union({"virtual_times_two"})
    return sorted(base)


# --- Интроспекция -------------------------------------------------------------


def listing(module: ModuleType, *, show_dunder: bool = False) -> list[tuple[str, type]]:
    """
    Вернёт (имя, тип) атрибутов модуля, отсортированных по имени.
    """
    items = []
    for k, v in module.__dict__.items():
        if not show_dunder and k.startswith("__"):
            continue
        items.append((k, type(v)))
    items.sort(key=lambda p: p[0])
    return items


# --- Динамический импорт ------------------------------------------------------


def import_by_name(name: str) -> ModuleType:
    """
    Импортирует модуль по строковому имени и возвращает объект модуля.
    """
    return import_module(name)


# --- Безопасная транзитивная перезагрузка ------------------------------------


def _iter_nested_modules(mod: ModuleType) -> Iterable[ModuleType]:
    for obj in mod.__dict__.values():
        if isinstance(obj, ModuleType):
            yield obj


def reload_all(*modules: ModuleType) -> set[str]:
    """
    Транзитивно перезагружает переданные модули и их зависимости.
    Возвращает множество имён модулей, которые были перезагружены.

    Безопасности ради пропускает "built-in" модули без __file__.
    """
    visited: set[ModuleType] = set()
    reloaded_names: set[str] = set()

    def walk(m: ModuleType):
        if m in visited:
            return
        visited.add(m)
        # пропускаем встроенные и sentinel-модули
        if getattr(m, "__file__", None):
            _reload(m)
            reloaded_names.add(m.__name__)
        for child in _iter_nested_modules(m):
            walk(child)

    for root in modules:
        if isinstance(root, ModuleType):
            walk(root)
    return reloaded_names


# --- Dual-mode ---------------------------------------------------------------


def dual_mode_title() -> str:
    return "Learning Python — Dual Mode Demo"


def main() -> None:
    """Демонстрация примеров из книги"""
    print(dual_mode_title())


if __name__ == "__main__":
    main()
