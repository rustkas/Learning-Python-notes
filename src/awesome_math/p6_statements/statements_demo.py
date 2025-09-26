# awesome_math/p6_statements/statements_demo.py
from __future__ import annotations

from typing import Any, Iterable, List


def interactive_echo(inputs: Iterable[str]) -> List[str]:
    """
    Классический read–eval–print цикл без ввода с клавиатуры:
    читает строки до 'stop' и возвращает ответы (upper()).
    """
    out: List[str] = []
    for s in inputs:
        if s == "stop":
            break  # демонстрация break
        out.append(s.upper())
    return out


def interactive_square_int(inputs: Iterable[str]) -> List[Any]:
    """
    Версия с проверкой ввода: целые -> квадрат; иначе 'Bad!'*8.
    После выхода добавляем 'Bye' (как в примере из главы).
    """
    out: List[Any] = []
    for s in inputs:
        if s == "stop":
            break
        if not s.isdigit():
            out.append("Bad!" * 8)
        else:
            out.append(int(s) ** 2)
    out.append("Bye")
    return out


def interactive_square_float_try(inputs: Iterable[str]) -> List[Any]:
    """
    Версия через try/except: парсим float, иначе ловим исключение.
    """
    out: List[Any] = []
    for s in inputs:
        if s == "stop":
            break
        try:
            out.append(float(s) ** 2)
        except Exception:
            out.append("Bad!" * 8)
    out.append("Bye")
    return out


def multiline_sum(a: int, b: int, c: int, d: int) -> int:
    """
    Многострочное выражение через скобки (демонстрация переноса).
    """
    total = a + b + c + d
    return total


def semicolon_chain() -> int:
    """
    Несколько простых операторов в одной строке, разделённых ';'.
    """
    a = 1
    b = 2
    c = a + b  # noqa: E702 - демонстрация разрешённого стиля
    return c


def single_line_if(x: int, y: int) -> str:
    """
    Однострочный if: тело после ':'. (else на новой строке.)
    """
    res = None
    if x > y:
        res = "gt"  # noqa: E701 - демонстрация синтаксиса из главы
    else:
        res = "le"
    return res  # type: ignore[return-value]


def bracketed_list() -> list[int]:
    """
    Продолжение литерала списка на нескольких строках внутри [].
    """
    data = [
        1111,
        2222,
        3333,
    ]
    return data


def nested_if_demo(text: str) -> str:
    """
    Вложенные блоки: если цифры -> проверяем порог, иначе Bad!*8.
    """
    if text.isdigit():
        num = int(text)
        if num < 20:
            return "low"
        else:
            return str(num**2)
    else:
        return "Bad!" * 8


def break_continue_demo(n: int) -> list[int]:
    """
    Собираем нечётные числа от 0 до n-1; прекращаем после > 10 (показ break/continue).
    """
    acc: list[int] = []
    i = 0
    while i < n:
        i += 1
        if i % 2 == 0:
            continue
        acc.append(i)
        if i > 10:
            break
    return acc


def match_case_demo(value: object) -> str:
    """
    Пример match/case (Python 3.10+). Возвращаем человека читаемую метку.
    """
    # match — «мягкое» ключевое слово: зарезервировано только в этом контексте
    match value:
        case 0:
            return "zero"
        case int() as x if x > 0:
            return "positive-int"
        case float() as f if f < 0:
            return "negative-float"
        case str() as s:
            return f"string:{s}"
        case _:
            return "other"
