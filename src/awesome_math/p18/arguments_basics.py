# pylint: disable=missing-function-docstring, import-outside-toplevel,unused-argument
# ruff: noqa: F841
from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

# --- Базовая модель передачи аргументов -------------------------------------


def rebind_local(a: int) -> int:
    """Локальное переназначение имени (на вызывающего не влияет)."""
    a = 99
    return a


def mutate_first_item(a: int, b: List[Any]) -> None:
    """Меняем изменяемый аргумент на месте: эффект виден снаружи."""
    a = 2  # не влияет на вызывающего
    b[0] = "mod"  # видно снаружи


def multiple_results(x: int, y: List[int]) -> Tuple[int, List[int]]:
    """Возвращаем несколько значений одним кортежем."""
    x = 2
    y = [3, 4]
    return x, y


# --- Ключевые, умолчания, сборщики, распаковка -------------------------------


def kw_defaults(a: int, b: int = 2, c: int = 3) -> Tuple[int, int, int]:
    return a, b, c


def collect_positional(*args: Any) -> Tuple[Any, ...]:
    """Собрать произвольно много позиционных."""
    return args


def collect_keyword(**kwargs: Any) -> Dict[str, Any]:
    """Собрать произвольно много ключевых."""
    return kwargs


def mix_collect(a: Any, *pargs: Any, **kargs: Any) -> Tuple[Any, Tuple[Any, ...], Dict[str, Any]]:
    return a, pargs, kargs


def sum4(a: int, b: int, c: int, d: int) -> int:
    return a + b + c + d


def call_with_unpack(pargs: Sequence[int], kargs: Mapping[str, int]) -> int:
    """Распаковать * и ** при вызове."""
    return sum4(*pargs, **kargs)


# --- keyword-only и positional-only -----------------------------------------


def kwonly(a: int, *, sep: str = " ", end: str = "\n") -> Tuple[int, str, str]:
    """sep и end обязательно передавать по имени (или использовать умолчания)."""
    return a, sep, end


def posonly(a: int, b: int, /, c: int) -> Tuple[int, int, int]:
    """a, b — только позиционно (Python ≥3.8), c можно по имени."""
    return a, b, c


# --- Примеры обобщённых функций ---------------------------------------------


def min_varargs(*args: Any) -> Any:
    """Минимум среди произвольного числа аргументов (сравнимых типов)."""
    if not args:
        raise ValueError("no arguments")
    it = iter(args)
    best = next(it)
    for x in it:
        if x < best:
            best = x
    return best


def minmax(test: Callable[[Any, Any], bool], *args: Any) -> Any:
    if not args:
        raise ValueError("no arguments")
    best = args[0]
    for x in args[1:]:
        if test(x, best):
            best = x
    return best


def less(x: Any, y: Any) -> bool:  # для minmax
    return x < y


def greater(x: Any, y: Any) -> bool:  # для minmax
    return x > y


def intersect(*args: Iterable[Any]) -> List[Any]:
    """Пересечение для ≥1 итерируемых; без дубликатов в результате."""
    if not args:
        return []
    res: List[Any] = []
    first, *rest = args
    for x in first:
        if x in res:
            continue
        if all(x in other for other in rest):
            res.append(x)
    return res


def union(*args: Iterable[Any]) -> List[Any]:
    """Объединение для ≥0 итерируемых; без дубликатов; сохраняет порядок первого появления."""
    res: List[Any] = []
    for seq in args:
        for x in seq:
            if x not in res:
                res.append(x)
    return res


# --- Эмуляция print с keyword-only опциями ----------------------------------


def print3(*args: Any, sep: str = " ", end: str = "\n", file=None) -> None:
    """Мини-версия print: все позиционные печатаются, опции — keyword-only."""
    import sys

    if file is None:
        file = sys.stdout
    out = sep.join(map(str, args)) + end
    file.write(out)
