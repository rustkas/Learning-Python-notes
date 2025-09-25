"""
Учебный модуль о динамической типизации и ссылках в Python.
"""

from __future__ import annotations

import gc
import weakref
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


def rebind_vs_mutate_demo() -> Tuple[List[int], List[int], List[int]]:
    """
    Показывает разницу между перепривязкой имени и мутацией объекта.
    Возвращает (L1_final, L2_final, L3_final):
    - L1 и L2 изначально ссылаются на один список; затем L1 мутируется "на месте"
      (эффект виден через L2).
    - L3 — независимая копия исходного списка; её мутация не влияет на L2.
    """
    base = [1, 2, 3]
    l1 = base
    l2 = base  # shared reference
    l1[0] = 99  # in-place -> видно в L2
    l3 = base[:]  # копия
    l3.append(4)  # меняем только L3
    return l1, l2, l3


def func_args_binding(lst: List[int], x: Any) -> Tuple[List[int], Any]:
    """
    Демонстрация передачи аргументов по ссылке:
    - мутируем lst (эффект виден снаружи),
    - перепривязываем имя x внутри функции (снаружи не видно).
    Возвращаем фактические локальные значения после операций.
    """
    lst.append(42)  # мутация исходного списка
    x = "rebound"  # локальная перепривязка, аргумент снаружи не меняется
    return lst, x


def eq_vs_is(a: Any, b: Any) -> Tuple[bool, bool]:
    """
    Возвращает (a == b, a is b). Полезно для иллюстрации различий
    между равенством значений и тождественностью объектов.
    """
    return a == b, a is b


def shallow_vs_deep_copy(data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Возвращает (shallow, deep) копии словаря data.
    """
    return copy(data), deepcopy(data)


@dataclass
class Holder:
    """Простой класс для weakref-демо."""

    value: int


def weakref_demo() -> Tuple[weakref.ReferenceType[Holder], int]:
    """
    Создаёт объект Holder, делает на него слабую ссылку, удаляет сильную ссылку
    и форсирует сборку мусора. Возвращает (weakref, steps), где steps — количество
    вызовов gc.collect() до обнуления слабой ссылки (обычно 0..1).
    """
    obj = Holder(123)
    w = weakref.ref(obj)
    # Снимаем сильную ссылку и просим GC прибраться:
    del obj
    steps = 0
    for _ in range(3):
        steps += 1
        gc.collect()
        if w() is None:
            break
    return w, steps


def type_hint_is_optional(a: "int | str") -> str:
    """
    Псевдо-демо: аннотация 'int | str' никак не ограничивает тип.
    Функция просто возвращает строковое представление аргумента.
    """
    return f"value={a!r}; type={type(a).__name__}"
