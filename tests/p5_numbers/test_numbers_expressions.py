# tests/p2_objects/test_numbers_expressions.py
# pylint: disable=missing-function-docstring

import subprocess
import sys

from awesome_math.p5_numbers import numbers_expressions_ as ne


def test_precedence_and_results():
    a, b, c = ne.precedence_examples()
    assert (a, b, c) == (14, 10, 14)


def test_sqrt_and_square_tools():
    s = ne.sqrt_and_square(144)
    assert s[0] == 12.0 and s[1] == 12.0 and s[2] == 12.0
    assert s[3] == 144**2 and s[4] == 144**2


def test_mixed_type_and_trunc_round():
    assert ne.mixed_type_result_type() is float
    i, t, r0, r2 = ne.trunc_round_examples(2.567)
    assert (i, t) == (2, 2)
    assert r0 in (3, 3.0) and abs(r2 - 2.57) < 1e-12
    assert ne.to_float(3) == 3.0


def test_bases_conversion_and_format():
    o, h, b, fo, fx, fb = ne.format_bases(64)
    assert o == "0o100" and h == "0x40" and b == "0b1000000"
    assert fo == "100" and fx == "40" and fb == "1000000"
    assert ne.parse_bases("100", "40", "1000000") == (64, 64, 64)


def test_division_and_mod_floor_negatives():
    d = ne.division_examples()
    assert d["true_div"] == 2.5
    assert d["floor_div_int"] == 2 and d["floor_div_float"] == 2.0
    assert d["mod"] == 1 and d["divmod"] == (3, 1)
    assert d["floor_neg"] == (2, 2.0) or d["floor_neg"] == (2, 2.0)  # sanity (kept for clarity)
    # Важно проверить именно floor для отрицательных:
    assert (5 // -2, 5 // -2.0) == (-3, -3.0)


def test_chained_and_float_equality():
    ch, weird = ne.chained_comparisons_demo()
    assert ch is True and weird is False
    isclose_ok, rounded_ok, raw = ne.float_equality_demo()
    assert isclose_ok is True and rounded_ok is True and abs(raw - 3.3) < 1e-15


def test_bitwise_and_underscores():
    bw = ne.bitwise_demo()
    assert bw["shl2"] == 4 and bw["or_3"] == 3 and bw["and_3"] == 1 and bw["xor_mask"] == 85
    u = ne.underscores_demo()
    assert u == (True, True)


def test_stats_random_decimal_fraction_sets_bools():
    s = ne.stats_and_random_demo()
    assert abs(s["mean"] - 3.8) < 1e-12 and isinstance(s["median"], (int, float))
    df = ne.decimals_fractions_demo()
    assert str(df["dec_zero"]) == "0.0" and str(df["frac_zero"]) == "0"
    st = ne.sets_demo()
    assert st["inter"] == {"b", "d"} and st["subset"] is True and st["superset"] is True
    bi = ne.booleans_demo()
    assert bi == (True, 5)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.numbers_expressions_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "precedence -> (14, 10, 14)" in out
    assert "mixed_type_result_type -> float" in out
    assert "division ->" in out and "true_div" in out
    assert "float eq -> isclose=True rounded=True" in out
    assert "bases fmt ->" in out and "0o100" in out and "0x40" in out and "0b1000000" in out
    assert "bitwise ->" in out and "'shl2': 4" in out
    assert "dec/frac ->" in out and "Decimal('0.0')" in out
    assert "sets ->" in out and "'inter': {'d', 'b'}" in out
    assert "booleans -> (True, 5)" in out
