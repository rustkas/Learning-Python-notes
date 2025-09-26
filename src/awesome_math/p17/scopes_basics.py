# ruff: noqa: F401
# pylint: disable=missing-function-docstring,redefined-outer-name,global-statement,invalid-name
from __future__ import annotations

from typing import Callable, List, Tuple

# --- Global vs local ---------------------------------------------------------

X_GLOBAL = "Hack"  # <- стиль UPPER_CASE


def read_global() -> str:
    return X_GLOBAL


def write_local_shadow() -> str:
    # Локальная тень глобального имени: глобал не меняется
    X_GLOBAL = "Py!"  # noqa: F841  # локальная переменная, не глобальная
    return X_GLOBAL


def set_global(value: str) -> str:
    global X_GLOBAL
    X_GLOBAL = value
    return X_GLOBAL


def reset_global() -> str:
    return set_global("Hack")


# --- Enclosing / closures ----------------------------------------------------


def closure_read() -> str:
    x = "Py!"

    def inner() -> str:
        return x  # берётся из охватывающей функции

    return inner()


def make_counter(start: int) -> Callable[[str], Tuple[str, int]]:
    """Накопительный счётчик на nonlocal-состоянии (пер-вызов)."""
    state = start

    def inner(label: str) -> Tuple[str, int]:
        nonlocal state
        state += 1
        return (label, state)

    return inner


class _Counter:
    def __init__(self, start: int) -> None:
        self.state = start

    def __call__(self, label: str) -> Tuple[str, int]:
        self.state += 1
        return (label, self.state)


def make_counter_attr(start: int) -> _Counter:
    return _Counter(start)


def outer_bad(start: int) -> Callable[[str], Tuple[str, int]]:
    """Демонстрация ошибки без nonlocal: вызов вернёт UnboundLocalError."""
    state = start

    def inner(label: str) -> Tuple[str, int]:
        # Намеренный анти-пример: читаем state до присваивания.
        state += 1  # noqa: F823  # Ruff: undefined-local (намеренно)
        return (label, state)

    return inner


# --- Loop + closures: bad vs good capture -----------------------------------


def make_actions_bad() -> List:
    """Все замыкания схватят одно и то же (последнее) i."""
    # pylint: disable=cell-var-from-loop  # намеренно показываем анти-пример
    acts = []
    for i in range(5):
        acts.append(lambda x: i**x)
    return acts


def make_actions_good() -> List:
    """Фиксация текущего i через значение по умолчанию аргумента."""
    return [(lambda x, i=i: i**x) for i in range(5)]
