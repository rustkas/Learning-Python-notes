# src/awesome_math/p2_objects/everything_else_.py
# pylint: disable=missing-function-docstring, invalid-name

from __future__ import annotations

import math
import re
import sqlite3
from types import CodeType
from typing import Any


def function_object_demo() -> tuple[str, bool, int, str]:
    def sq(x: int) -> int:
        return x * x

    # функции — объекты: можно добавить атрибут
    sq.tag = "demo"  # type: ignore[attr-defined]
    return (sq.__name__, callable(sq), sq(3), sq.tag)  # type: ignore[attr-defined]


def module_object_demo() -> tuple[str, bool, int]:
    mod = math
    return (mod.__name__, hasattr(mod, "sqrt"), int(round(mod.sqrt(9))))


def class_object_demo() -> tuple[str, bool, bool]:
    class WorkerLite:
        def __init__(self, name: str) -> None:
            self.name = name

    cls = WorkerLite
    inst = cls("Pat")
    return (cls.__name__, isinstance(cls, type), isinstance(inst, WorkerLite))


def compile_exec_demo() -> tuple[bool, int, int]:
    expr = compile("a + b", "<expr>", "eval")
    assert isinstance(expr, CodeType)
    res = eval(expr, {}, {"a": 2, "b": 3})  # noqa: S307 (осознанная демо)

    stmt = compile("x = 10\ny = x * 2", "<stmt>", "exec")
    ns: dict[str, Any] = {}
    exec(stmt, {}, ns)  # noqa: S102 (осознанная демо)
    return (isinstance(expr, CodeType), int(res), int(ns["y"]))


def noncore_objects_demo() -> tuple[str, bool, int]:
    # re.Pattern — объект из модуля, не ядерный тип
    pattern = re.compile(r"\w+")
    ok = pattern.fullmatch("abc123") is not None

    # sqlite3.Connection — объект интерфейса к БД (здесь :memory:)
    con = sqlite3.connect(":memory:")
    try:
        cur = con.cursor()
        cur.execute("select 1 + 1")
        (val,) = cur.fetchone()  # type: ignore[misc]
    finally:
        con.close()
    return (type(pattern).__name__, ok, int(val))


def main() -> None:
    """Демонстрация примеров из книги"""
    fn_name, is_call, sq3, tag = function_object_demo()
    print(f"function object: name={fn_name}, callable={is_call}, sq(3)={sq3}, tag={tag}")

    mod_name, has_sqrt, sqrt9 = module_object_demo()
    print(f"module object: name={mod_name}, has sqrt={has_sqrt}, sqrt(9)={sqrt9}")

    cls_name, is_type, inst_ok = class_object_demo()
    print(f"class object: name={cls_name}, is type={is_type}, instance ok={inst_ok}")

    is_code, expr_val, y_val = compile_exec_demo()
    print(f"code object: isinstance(CodeType)={is_code}, eval= {expr_val}, exec y={y_val}")

    kind, matched, sum_val = noncore_objects_demo()
    print(f"noncore objects: re kind={kind}, matched={matched}, sqlite 1+1={sum_val}")


if __name__ == "__main__":
    main()
