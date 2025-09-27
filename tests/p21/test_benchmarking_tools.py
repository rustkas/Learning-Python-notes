# tests/p21/test_benchmarking_tools.py
# pylint: disable=missing-function-docstring
from __future__ import annotations

import math

from awesome_math.p21.benchmarking_tools import (
    bestof,
    bestoftotal,
    build_range_list,
    for_loop_abs,
    gen_expr_abs,
    gen_func_abs,
    list_comp_abs,
    map_abs,
    once,
    total,
)


def test_once_and_total_return_shapes_and_results():
    t1, r1 = once(pow, 2, 5)
    assert r1 == 32
    assert t1 >= 0.0

    t2, r2 = total(pow, 2, 5, _reps=1000)
    assert r2 == 32
    assert t2 > 0.0  # должно быть измеримое положительное время


def test_bestof_and_bestoftotal_identity_when_reps1_is_one():
    # свойство: bestoftotal(..., _reps1=1) == total(...) по времени и результату
    t_tot, res_tot = total(pow, 2, 10, _reps=1234)
    t_best, res_best = bestoftotal(pow, 2, 10, _reps1=1, _reps=1234)
    # допускаем крошечную погрешность из-за измерения
    assert abs(t_tot - t_best) <= max(1e-12, t_tot * 1e-12)
    assert res_tot == res_best == 1024


def test_kwargs_supported_by_timers():
    def f(a: int, *, scale: int = 2) -> int:
        return a * scale

    t, r = bestof(f, 7, scale=3, _reps=10)
    assert r == 21
    assert t >= 0.0


def test_iteration_variants_produce_same_output():
    data = build_range_list(1000)
    ref = list_comp_abs(data)
    assert ref == for_loop_abs(data)
    assert ref == map_abs(data)
    assert ref == gen_expr_abs(data)
    assert ref == gen_func_abs(data)


def test_compare_math_sqrt_and_pow_result_equality():
    # функционально эквивалентные способы — результат одинаковый
    t1, r1 = bestoftotal(math.sqrt, 144.0, _reps1=3, _reps=5000)
    t2, r2 = bestoftotal(pow, 144.0, 0.5, _reps1=3, _reps=5000)
    assert r1 == r2 == 12.0
    # времена не сравниваем жёстко — бенчмарки шумные по определению
    assert t1 > 0.0 and t2 > 0.0
