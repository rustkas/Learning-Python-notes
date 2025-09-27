# src/awesome_math/p5_numbers/module_coding.py
# pylint: disable=missing-function-docstring, unnecessary-pass

"""
Демонстрация примеров из книги
"""

from types import ModuleType
from typing import Iterable, List

__all__ = [
    "list_public_names",
    "set_module_attr",
    "mutate_shared_list",
    "get_attr_path",
]


def list_public_names(module: ModuleType) -> List[str]:
    names = [n for n in dir(module) if not n.startswith("__")]
    return sorted(names)


def set_module_attr(module: ModuleType, name: str, value):
    setattr(module, name, value)
    return getattr(module, name)


def mutate_shared_list(items: list) -> list:
    if items:
        items[0] = "hack"
    return items


def get_attr_path(obj, path: Iterable[str]):
    cur = obj
    for part in path:
        cur = getattr(cur, part)
    return cur


def main():
    """
    Демонстрация примеров из книги
    """
    pass


if __name__ == "__main__":
    main()
