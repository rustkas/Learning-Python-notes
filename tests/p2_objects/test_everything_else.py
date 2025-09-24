# tests/p2_objects/test_everything_else.py
# pylint: disable=missing-function-docstring
# pylint: disable=consider-using-f-string

import subprocess
import sys

from awesome_math.p2_objects import everything_else_ as ee


def test_function_object_demo():
    name, is_call, sq3, tag = ee.function_object_demo()
    assert name == "sq"
    assert is_call is True and sq3 == 9 and tag == "demo"


def test_module_object_demo():
    mod_name, has_sqrt, sqrt9 = ee.module_object_demo()
    assert mod_name == "math" and has_sqrt is True and sqrt9 == 3


def test_class_object_demo():
    cls_name, is_type, inst_ok = ee.class_object_demo()
    assert cls_name == "WorkerLite" and is_type is True and inst_ok is True


def test_compile_exec_demo():
    is_code, expr_val, y_val = ee.compile_exec_demo()
    assert is_code is True and expr_val == 5 and y_val == 20


def test_noncore_objects_demo():
    kind, matched, sum_val = ee.noncore_objects_demo()
    assert kind in {"Pattern", "Pattern[int]"} or "Pattern" in kind  # Py>=3.12 may parametrize repr
    assert matched is True and sum_val == 2


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.everything_else_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "function object: name=sq" in out
    assert "module object: name=math" in out
    assert "class object: name=WorkerLite" in out
    assert "code object: isinstance(CodeType)=True" in out
    assert "noncore objects: re kind=" in out and "sqlite 1+1=2" in out
