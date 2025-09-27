# src/awesome_math/p5_numbers/modules_big_picture.py
# pylint: disable=missing-function-docstring

from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any, List, Tuple


def main() -> None:
    """Демонстрация примеров из книги"""
    # Небольшая демонстрация: импорт math и печать его файла/атрибутов
    m = import_module("math")
    print(get_module_file(m))
    print("sqrt" in list_module_attributes(m))


# --- Основные утилиты вокруг модулей и импорта ---


def import_module(name: str) -> ModuleType:
    """Импортирует модуль (или возвращает уже загруженный) и отдаёт объект модуля."""
    return importlib.import_module(name)


def is_module_loaded(name: str) -> bool:
    """Проверяет, присутствует ли модуль в sys.modules (уже загружен)."""
    return name in sys.modules


def import_and_get_attr(module_name: str, attr_name: str) -> Any:
    """Импортирует модуль и возвращает значение его атрибута (или возбуждает AttributeError)."""
    mod = import_module(module_name)
    return getattr(mod, attr_name)


def reload_module(mod: ModuleType) -> ModuleType:
    """Перезагружает модуль (повторно выполняет код файла)."""
    return importlib.reload(mod)


def list_module_attributes(mod: ModuleType) -> List[str]:
    """Список атрибутов модуля (его «пространство имён»)."""
    return sorted(dir(mod))


def get_module_file(mod: ModuleType) -> str | None:
    """
    Возвращает путь к файлу модуля или None для встроенных (например, sys),
    у которых нет __file__.
    """
    return getattr(mod, "__file__", None)


# --- Путь поиска и выбор файла ---


def get_sys_path() -> List[str]:
    """Копия текущего sys.path (путь поиска модулей)."""
    return list(sys.path)


def ensure_path_appended(path: str) -> None:
    """
    Добаляет путь в конец sys.path (на время процесса).
    Идёмпотентно: если уже есть — ничего не делаем.
    """
    if path not in sys.path:
        sys.path.append(path)


def find_first_on_sys_path(module_basename: str) -> Tuple[str | None, str]:
    """
    Пытается определить, откуда был загружен модуль с данным base-name:
    возвращает (module_file, picked_from_dir). Если модуль уже импортирован —
    его __file__ (или None для built-in) и каталог, где найдено первое совпадение.
    """
    # Где бы Python стал искать: первая директория из sys.path, где есть имя без расширения.
    picked_dir = next((p for p in sys.path if p), "")
    # Если модуль уже загружен, можно вернуть его файл.
    mod = sys.modules.get(module_basename)
    return (get_module_file(mod) if isinstance(mod, ModuleType) else None, picked_dir)


if __name__ == "__main__":
    main()
