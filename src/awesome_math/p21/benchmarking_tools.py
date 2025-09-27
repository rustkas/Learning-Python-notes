# awesome_math/p21/benchmarking_tools.py
# pylint: disable=missing-function-docstring
from __future__ import annotations

import time
from typing import Any, Callable, Dict, Iterable, List, Tuple

timer = time.perf_counter


def once(func: Callable[..., Any], /, *args, **kwargs) -> Tuple[float, Any]:
    start = timer()
    result = func(*args, **kwargs)
    return (timer() - start, result)


def total(func: Callable[..., Any], /, *args, _reps: int = 100_000, **kwargs) -> Tuple[float, Any]:
    elapsed_sum = 0.0
    last_result: Any = None
    for _ in range(_reps):
        dt, last_result = once(func, *args, **kwargs)
        elapsed_sum += dt
    return (elapsed_sum, last_result)


def bestof(func: Callable[..., Any], /, *args, _reps: int = 5, **kwargs) -> Tuple[float, Any]:
    return min(once(func, *args, **kwargs) for _ in range(_reps))


def bestoftotal(
    func: Callable[..., Any], /, *args, _reps1: int = 50, _reps: int = 100_000, **kwargs
) -> Tuple[float, Any]:
    return min(total(func, *args, _reps=_reps, **kwargs) for _ in range(_reps1))


# ---------- Небольшой набор «тестовых нагрузок» (итерации) ----------


def build_range_list(n: int = 10_000) -> List[int]:
    # выносим создание range->list за пределы измерений
    return list(range(n))


def for_loop_abs(source: Iterable[int]) -> List[int]:
    res: List[int] = []
    for x in source:
        res.append(abs(x))
    return res


def list_comp_abs(source: Iterable[int]) -> List[int]:
    return [abs(x) for x in source]


def map_abs(source: Iterable[int]) -> List[int]:
    # map с встроенной функцией — быстрый случай на CPython
    return list(map(abs, source))


def gen_expr_abs(source: Iterable[int]) -> List[int]:
    # генератор + list — обычно медленнее comprehension
    return list(abs(x) for x in source)


def gen_func_abs(source: Iterable[int]) -> List[int]:
    def gen():
        for x in source:
            yield abs(x)

    return list(gen())


# Утилита для мини-бенчей (не используется в тестах, удобно в REPL/скрипте)
def micro_bench_funcs(
    funcs: Dict[str, Callable[[Iterable[int]], List[int]]],
    data: Iterable[int],
    *,
    _reps1: int = 10,
    _reps: int = 1000,
) -> Dict[str, float]:
    results: Dict[str, float] = {}
    for name, fn in funcs.items():
        t, out = bestoftotal(fn, data, _reps1=_reps1, _reps=_reps)
        # потребляем результат, чтобы избежать «мертвого кода»
        if not out or out[0] != 0 and out[0] != abs(next(iter(data), 0)):
            pass
        results[name] = t
    return results
