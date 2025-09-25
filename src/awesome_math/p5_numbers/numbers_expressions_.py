# src/awesome_math/p2_objects/numbers_expressions_.py
# pylint: disable=missing-function-docstring, invalid-name
from __future__ import annotations

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction
from statistics import mean, median
from typing import Any


def precedence_examples() -> tuple[int, int, int]:
    return 2 * (3 + 4), 2 * 3 + 4, 2 + 3 * 4


def sqrt_and_square(n: float) -> tuple[float, float, float, float, float]:
    return math.sqrt(n), n**0.5, pow(n, 0.5), n**2, pow(n, 2)


def mixed_type_result_type() -> type:
    return type(1 + 2.0 + 3)


def trunc_round_examples(x: float) -> tuple[int, int, float, float]:
    return int(x), math.trunc(x), round(x), round(x, 2)


def to_float(i: int) -> float:
    return float(i)


def format_bases(n: int) -> tuple[str, str, str, str, str, str]:
    return oct(n), hex(n), bin(n), f"{n:o}", f"{n:x}", f"{n:b}"


def parse_bases(oct_str: str, hex_str: str, bin_str: str) -> tuple[int, int, int]:
    return int(oct_str, 8), int(hex_str, 16), int(bin_str, 2)


def division_examples() -> dict[str, Any]:
    return {
        "true_div": 10 / 4,
        "floor_div_int": 10 // 4,
        "floor_div_float": 10 // 4.0,
        "mod": 10 % 3,
        "divmod": divmod(10, 3),
        "floor_neg": (5 // -2, 5 // -2.0),
    }


def chained_comparisons_demo() -> tuple[bool, bool]:
    x, y, z = 2, 4, 6
    return x < y < z, (1 == 2 < 3)


def float_equality_demo() -> tuple[bool, bool, float]:
    a = 1.1 + 2.2
    return (math.isclose(a, 3.3), round(a, 1) == round(3.3, 1), a)


def bitwise_demo() -> dict[str, int]:
    x = 0b0001
    return {
        "shl2": x << 2,  # 0b0100 -> 4
        "or_3": x | 0b0011,  # 0b0011 -> 3
        "and_3": x & 0b0011,  # 0b0001 -> 1
        "xor_mask": 0xFF ^ 0b10101010,  # 0x55 -> 85
    }


def underscores_demo() -> tuple[bool, bool]:
    return (9999999 == 9_999_999, 0xFF_FF == 65535)


def stats_and_random_demo() -> dict[str, Any]:
    random.seed(0)
    xs = [1, 2, 4, 5, 7]
    return {
        "mean": mean(xs),
        "median": median(xs),
        "rand": (random.random(), random.randint(1, 10)),
    }


def decimals_fractions_demo() -> dict[str, Any]:
    # точность по умолчанию
    d_exact = Decimal("0.1") + Decimal("0.1") + Decimal("0.1") - Decimal("0.3")
    # глобально установим короткую точность и покажем деление
    prev = getcontext().prec
    getcontext().prec = 4
    d_div = Decimal(1) / Decimal(7)
    getcontext().prec = prev

    f_sum = Fraction(1, 10) + Fraction(1, 10) + Fraction(1, 10) - Fraction(3, 10)
    return {"dec_zero": d_exact, "dec_div_1_7": d_div, "frac_zero": f_sum}


def sets_demo() -> dict[str, Any]:
    x = set("abcd")
    y = set("bdxy")
    return {
        "diff": x - y,  # {'a','c'}
        "union": x | y,
        "inter": x & y,  # {'b','d'}
        "symdiff": x ^ y,
        "subset": {"b", "d"} <= x,
        "superset": x >= {"a"},
    }


def booleans_demo() -> tuple[bool, int]:
    return isinstance(True, int), True + 4


def literals_showcase() -> dict[str, Any]:
    return {
        "int": 1234,
        "float": 3.14,
        "complex": 3 + 4j,
        "hex": 0xFF,
        "oct": 0o377,
        "bin": 0b1010,
        "set": {"a", "b"},
        "bool": True,
    }


def main() -> None:
    """Демонстрация ключевых моментов главы про числа и выражения."""
    print("precedence ->", precedence_examples())
    s = sqrt_and_square(144)
    print(f"sqrt/square -> sqrt={s[0]} pow05={s[1]} pow()={s[2]} sq={s[3]} pow2={s[4]}")
    print("mixed_type_result_type ->", mixed_type_result_type().__name__)
    print("division ->", division_examples())
    isclose_ok, rounded_ok, val = float_equality_demo()
    print(f"float eq -> isclose={isclose_ok} rounded={rounded_ok} raw={val}")
    print("chained ->", chained_comparisons_demo())
    print("bases fmt ->", format_bases(64))
    print("bitwise ->", bitwise_demo())
    print("underscores ->", underscores_demo())
    print("stats/random ->", stats_and_random_demo()["mean"])
    print("dec/frac ->", decimals_fractions_demo())
    print("sets ->", sets_demo())
    print("booleans ->", booleans_demo())


if __name__ == "__main__":
    main()
