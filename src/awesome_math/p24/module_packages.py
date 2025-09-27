# src/awesome_math/p5_numbers/module_packages.py
# pylint: disable=missing-function-docstring,line-too-long
"""
Демонстрация примеров из книги
"""

from __future__ import annotations

import importlib
import sys
import types
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def push_sys_path(path: Path | str):
    """Временно добавляет путь в sys.path (в начало), затем восстанавливает."""
    p = str(path)
    sys.path.insert(0, p)
    try:
        yield
    finally:
        # убрать только первое вхождение, если пользователю вдруг дублировали
        if p in sys.path:
            sys.path.remove(p)


def import_fresh(module_name: str) -> types.ModuleType:
    """
    Импортирует модуль 'с нуля' — удаляя цепочку родительских пакетов из sys.modules.
    Удобно для тестов импорта пакетов.
    """
    # удалить сам модуль
    sys.modules.pop(module_name, None)
    # удалить родителей (pkg.sub.mod -> pkg, pkg.sub)
    parts = module_name.split(".")
    for i in range(1, len(parts)):
        sys.modules.pop(".".join(parts[:i]), None)
    return importlib.import_module(module_name)


def is_namespace_package(mod: types.ModuleType) -> bool:
    """
    True, если это namespace-пакет: у него нет __file__, но есть __path__ (iterable).
    """
    has_path = hasattr(mod, "__path__")
    has_file = hasattr(mod, "__file__")
    return bool(has_path) and not has_file


def write_tree(root: Path, tree: dict) -> None:
    """
    Утилита для тестов: создаёт файловое дерево из словаря вида:
    {
      "pkg": {
        "__init__.py": "content",
        "sub": {
          "mod.py": "content"
        }
      }
    }
    Значение-строка -> файл с содержимым, значение-словарь -> папка.
    """
    for name, value in tree.items():
        target = root / name
        if isinstance(value, dict):
            target.mkdir(parents=True, exist_ok=True)
            write_tree(target, value)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value, encoding="utf-8")


def module_attr(mod: types.ModuleType, name: str):
    """Безопасно получить атрибут модуля (для тестов)."""
    return getattr(mod, name)


def main():
    """Демонстрация примеров из книги"""
    print(
        "Модульные пакеты можно импортировать, объединять (namespace) и управлять приоритетом поиска."
    )
    print("Смотрите тесты для подробных примеров использования.")


if __name__ == "__main__":
    main()
