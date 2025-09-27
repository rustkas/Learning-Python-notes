# tests/p25/test_module_odds_and_ends.py
# pylint: disable=missing-function-docstring,unused-argument,line-too-long
# pylint: disable=unsupported-assignment-operation,exec-used

import io
import runpy
from contextlib import redirect_stdout
from importlib import import_module


def test_all_and_private_and_from_star_behavior(monkeypatch):
    # Импортируем модуль «обычно»
    mod = import_module("awesome_math.p25.module_odds_and_ends")

    # _internal_b не должен попадать в from * (т.к. не в __all__)
    # Выполним from * в отдельном пространстве имён
    ns = {}
    exec("from awesome_math.p25.module_odds_and_ends import *", {}, ns)  # noqa: S102
    assert "public_a" in ns
    assert "listing" in ns
    assert "import_by_name" in ns
    assert "reload_all" in ns
    assert "_internal_b" not in ns

    # При обычном import доступен _internal_b через квалификацию
    assert getattr(mod, "_internal_b") == 2


def test_module_level_getattr_and_dir():
    mod = import_module("awesome_math.p25.module_odds_and_ends")
    # виртуальный атрибут
    assert getattr(mod, "virtual_times_two") == mod.public_a * 2
    # неизвестный атрибут -> AttributeError
    try:
        getattr(mod, "nope")
        assert False, "Expected AttributeError"
    except AttributeError:
        pass
    # __dir__ добавляет виртуал
    d = dir(mod)
    assert "virtual_times_two" in d


def test_listing_introspection_returns_sorted_tuples():
    mod = import_module("awesome_math.p25.module_odds_and_ends")
    pairs = mod.listing(mod)
    assert isinstance(pairs, list)
    # список отсортирован по имени
    names = [k for k, _ in pairs]
    assert names == sorted(names)
    # присутствуют наши публичные функции
    assert any(k == "listing" for k, _ in pairs)
    assert any(k == "import_by_name" for k, _ in pairs)


def test_import_by_name_loads_stdlib_module():
    mod = import_module("awesome_math.p25.module_odds_and_ends")
    m_math = mod.import_by_name("math")
    assert m_math.sqrt(9) == 3


def test_reload_all_returns_set_of_names():
    mod = import_module("awesome_math.p25.module_odds_and_ends")
    names = mod.reload_all(mod)  # перезагрузим сам модуль и его зависимости
    # Должно как минимум содержать наш модуль (он имеет __file__)
    assert "awesome_math.p25.module_odds_and_ends" in names


def test_dual_mode_main_runs_when_as_script(tmp_path, monkeypatch):
    # Запуск модуля как скрипта через runpy с run_name="__main__"
    buf = io.StringIO()
    with redirect_stdout(buf):
        runpy.run_module("awesome_math.p25.module_odds_and_ends", run_name="__main__")
    out = buf.getvalue()
    assert "Dual Mode Demo" in out
