# pylint: disable=missing-function-docstring

import math
import random
import re
import subprocess
import sys
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, getcontext

import pytest

from awesome_math.p2_objects.numbers_ import (
    big_pow_digits,
    bit_info,
    divisions,
    isclosef,
    money_sum_decimal,
    pow_mod,
    random_sample,
    rational_add,
    secure_token_hex,
)


def test_big_pow_digits_small():
    assert big_pow_digits(10) == len(str(2**10)) == 4
    assert big_pow_digits(100) == len(str(2**100))


def test_divisions_floor_and_mod():
    f, flo, rem = divisions(-3, 2)
    assert f == -1.5
    assert flo == -2  # floor деление
    assert rem == 1  # модуль с положительным результатом


def test_float_isclose_vs_equality():
    assert (0.1 + 0.2) != 0.3  # ловушка
    assert isclosef(0.1 + 0.2, 0.3)


def test_money_decimal_vs_float():
    assert money_sum_decimal(["0.10", "0.20"]) == Decimal("0.30")


def test_fraction_arithmetic():
    frac = rational_add(1, 3, 1, 6)  # 1/3 + 1/6 = 1/2
    assert frac == Decimal(1) / 2  # проверка через Decimal


def test_random_reproducible():
    assert random_sample(123, 3) == random_sample(123, 3)


def test_secrets_token_hex_length_and_hex():
    tok = secure_token_hex(8)
    assert len(tok) == 16
    assert re.fullmatch(r"[0-9a-f]+", tok)


def test_bit_info_and_formats():
    info = bit_info(2**100)
    assert info["bit_length"] == 101
    assert info["bin"].startswith("1") and set(info["bin"]) <= {"0", "1"}
    assert info["hex"].startswith("1")


def test_pow_mod():
    assert pow_mod(2, 10, 17) == (2**10) % 17 == 4


def test_math_module_basics():
    assert math.isclose(math.sqrt(85) ** 2, 85, rel_tol=1e-12)
    assert math.isfinite(math.pi)


def test_run_as_module():
    # проверим, что демонстрация запускается
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.numbers_"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "digits(2**12345)" in proc.stdout


def test_random_rng_overrides_seed():
    """rng должен определять последовательность, seed игнорируется."""
    seed = 123
    rng_for_func = random.Random(seed)  # этот пойдёт внутрь функции
    rng_for_expected = random.Random(seed)  # этим считаем ожидаемое

    expected = [rng_for_expected.random() for _ in range(3)]
    got = random_sample(seed=999, k=3, rng=rng_for_func)  # seed игнорируется
    assert got == expected


def test_random_k_validation_and_empty():
    """Проверяем валидацию k и пустой результат для k=0."""
    assert random_sample(1, k=0) == []
    with pytest.raises(ValueError):
        random_sample(1, k=-1)


def test_money_localcontext_rounding_modes():
    """Проверяем разные правила округления на 0.005."""
    up = money_sum_decimal(["0.005"], quant="0.01", rounding=ROUND_HALF_UP)
    even = money_sum_decimal(["0.005"], quant="0.01", rounding=ROUND_HALF_EVEN)
    assert up == Decimal("0.01")  # обычное округление "вверх от 0.5"
    assert even == Decimal("0.00")  # банковское округление к чётному


def test_money_localcontext_does_not_leak_global_context():
    """Локальный контекст не должен менять глобальные настройки Decimal."""
    global_ctx_before = (getcontext().prec, getcontext().rounding)
    _ = money_sum_decimal(["0.10", "0.20"], prec=50, rounding=ROUND_HALF_EVEN)
    global_ctx_after = (getcontext().prec, getcontext().rounding)
    assert global_ctx_after == global_ctx_before
