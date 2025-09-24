from __future__ import annotations

import math
import random
import secrets
import sys
from decimal import ROUND_HALF_UP, Decimal, localcontext  # getcontext
from fractions import Fraction
from typing import Iterable, Optional

__all__ = [
    "big_pow_digits",
    "divisions",
    "isclosef",
    "money_sum_decimal",
    "rational_add",
    "random_sample",
    "secure_token_hex",
    "bit_info",
    "pow_mod",
]


def big_pow_digits(exp: int) -> int:
    """
    Считает количество цифр у 2**exp.
    На Python 3.11+ временно повышает лимит для str(очень_большого_int).
    """
    if hasattr(sys, "set_int_max_str_digits"):
        prev = sys.get_int_max_str_digits()
        try:
            # поднимем лимит разумно под задачу
            sys.set_int_max_str_digits(max(prev, exp + 100))
            return len(str(2**exp))
        finally:
            sys.set_int_max_str_digits(prev)
    else:
        return len(str(2**exp))


def divisions(a: int, b: int) -> tuple[float, int, int]:
    """Возвращает (a/b как float, a//b, a%b) — демонстрация /, // и %."""
    return (a / b, a // b, a % b)


def isclosef(a: float, b: float, rel: float = 1e-12, abs_: float = 0.0) -> bool:
    """Корректное сравнение float."""
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# def money_sum_decimal(amounts: Iterable[str], quant: str = "0.01") -> Decimal:
#     """
#     Суммирует денежные строки с фиксированной точностью.
#     Пример: money_sum_decimal(["0.10", "0.20"]) -> Decimal("0.30")
#     """
#     getcontext().prec = 28
#     total = sum(Decimal(x) for x in amounts)
#     return total.quantize(Decimal(quant), rounding=ROUND_HALF_UP)


def money_sum_decimal(
    amounts: Iterable[str],
    quant: str = "0.01",
    *,
    prec: int = 28,
    rounding=ROUND_HALF_UP,
) -> Decimal:
    """
    Суммирует денежные строки с локальным Decimal-контекстом.
    - amounts: строки, а не float (избегаем двоичной погрешности).
    - quant: шаг округления (копейка по умолчанию).
    - prec: рабочая точность (локальная, не глобальная).
    - rounding: правило округления (по умолчанию "обычное" HALF_UP).
    """
    with localcontext() as ctx:
        ctx.prec = prec
        ctx.rounding = rounding
        total = sum(Decimal(x) for x in amounts)
        # Можно положиться на ctx.rounding и НЕ передавать rounding в quantize.
        return total.quantize(Decimal(quant))


def rational_add(a_num: int, a_den: int, b_num: int, b_den: int) -> Fraction:
    """Точное сложение рациональных: (a_num/a_den) + (b_num/b_den)."""
    return Fraction(a_num, a_den) + Fraction(b_num, b_den)


def random_sample(seed: int, k: int = 3, rng: Optional[random.Random] = None) -> list[float]:
    """
    Возвращает k равномерных float в [0, 1). Если передан rng — используем его (удобно для DI).
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    r = rng or random.Random(seed)
    return [r.random() for _ in range(k)]


def secure_token_hex(nbytes: int = 16) -> str:
    """Криптостойкий токен: используем secrets, не random."""
    return secrets.token_hex(nbytes)


def bit_info(n: int) -> dict[str, int | str]:
    """Сводка по числу: битовая длина, hex/bin строки (без префикса)."""
    return {
        "bit_length": n.bit_length(),
        "hex": format(n, "x"),
        "bin": format(n, "b"),
    }


def pow_mod(a: int, b: int, m: int) -> int:
    """Быстрое возведение в степень по модулю (встроенный pow с 3 аргументами)."""
    return pow(a, b, m)


def main() -> None:
    """Короткая демонстрация для запуска: python -m awesome_math.p2_objects.numbers_"""
    print("digits(2**12345) =", big_pow_digits(12345))
    print("divisions(5,2) =", divisions(5, 2))
    print("float close? 0.1+0.2 vs 0.3 ->", isclosef(0.1 + 0.2, 0.3))
    print("money sum:", money_sum_decimal(["0.10", "0.20"]))
    print("fraction:", rational_add(1, 3, 1, 6))
    print("random sample:", random_sample(42, 3))
    print("secure token len:", len(secure_token_hex(8)))
    print("bit info 2**100:", bit_info(2**100))
    print("pow_mod(2,10,17):", pow_mod(2, 10, 17))


if __name__ == "__main__":
    main()
