# awesome_math/p8_selections/if_match.py
from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple

# --- if / dict / match: множественный выбор ---


def os_year_if(choice: str) -> int | str:
    """Каскад if/elif/else."""
    if choice == "macos":
        return 2001
    elif choice == "Linux":
        return 1991
    elif choice == "Windows":
        return 1985
    else:
        return "Bad choice"


def os_year_dict(choice: str) -> int | str:
    """Словарный 'switch' с get по умолчанию."""
    table: Dict[str, int] = dict(macos=2001, Linux=1991, Windows=1985)
    return table.get(choice, "Bad choice")


def os_color_match(state: str) -> str:
    """
    Базовый match: 'go'|'proceed'|'start' -> green; 'stop'|'halt' -> red; иначе yellow.
    """
    # Требует Python 3.10+
    match state:
        case "go" | "proceed" | "start":
            return "green"
        case "stop" | "halt":
            return "red"
        case _:
            return "yellow"


def categorize_stmt_match(stmts: Iterable[str]) -> Tuple[List[str], str, str]:
    """
    Для ['if','while','try'] вернёт (категории, which, other),
    где which = 'while', other = 'try' после сопоставления.
    """
    categories: List[str] = []
    which = None
    other = None
    for stmt in stmts:
        match stmt:
            case "if" | "match":
                categories.append("logic")
            case "for" | "while" as which:
                categories.append("loop")
            case other:
                categories.append("tbd")
    return categories, which, other  # type: ignore[return-value]


# --- Расширенные паттерны match ---


def pattern_demo(state: Any) -> Tuple[str, Any]:
    """
    Демонстрация: литералы, последовательности, отображения, _, as, *, **.
    Возвращает ('тип', what).
    """
    match state:
        case 1 | 2 | 3 as what:
            return "or", what
        case [1, 2, what]:
            return "list", what
        case [0, *what]:
            return "list", what
        case {"a": 1, "b": 2, "c": what}:
            return "dict", what
        case {"a": 0, **what}:
            return "dict", what
        case (1, 2, what):
            return "tuple", what
        case (0, *what):
            return "tuple", what
        case _ as what:
            return "other", what


def guard_demo(state: Any, guard1: bool) -> Tuple[str, Tuple[Any, ...]]:
    """
    Guard-паттерны: выбирает case по структуре и guard.
    state ожидается как ((1,2), 3) или совместимое.
    """
    match state:
        case ((a, 2), b) if guard1:
            return "case1", (a, b)
        case (a, 3) as what:
            return "case2", (a, what)
        case [a, (3 | 4)] as what if guard1:
            return "case3", (a, what)
        case _:
            return "other", (state,)


# --- Булева логика, short-circuit, тернарный оператор ---


def bool_operands(x: Any, y: Any) -> Tuple[Any, Any]:
    """Возвращает (x or y, x and y) — демонстрация возврата операндов."""
    return (x or y, x and y)


def short_circuit_or(f1: Callable[[], Any], f2: Callable[[], Any]) -> Tuple[Any, Tuple[bool, bool]]:
    """
    Вызывает f1() or f2(); возвращает (результат, (f1_called, f2_called)).
    Удобно тестировать short-circuit: если f1 истинен, f2 не вызывается.
    """
    called = [False, False]

    def w1():
        called[0] = True
        return f1()

    def w2():
        called[1] = True
        return f2()

    result = w1() or w2()
    return result, (called[0], called[1])


def ternary_if_expr(x: Any, y: Any, z: Any) -> Any:
    """Классический тернарный if-выражение."""
    return y if x else z


def and_or_equivalent(x: Any, y: Any, z: Any) -> Any:
    """Эквивалент через ((X and Y) or Z) — корректен, когда Y истинен."""
    return (x and y) or z


def first_truthy(*values: Any, default: Any = None) -> Any:
    """Возвращает первый истинный среди values (или default)."""
    acc = default
    for v in values:
        acc = v or acc
    return acc


# --- Утилиты для тестов/демонстраций ---


def lines_to_color(states: Sequence[str]) -> List[str]:
    """Пример пакетной обработки через match."""
    return [os_color_match(s) for s in states]
