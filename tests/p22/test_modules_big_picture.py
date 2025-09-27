# tests/p5_numbers/test_modules_big_picture.py
# pylint: disable=missing-function-docstring
# pylint: disable=unsupported-assignment-operation

from types import ModuleType

from awesome_math.p22.modules_big_picture import (
    ensure_path_appended,
    find_first_on_sys_path,
    get_module_file,
    get_sys_path,
    import_and_get_attr,
    import_module,
    is_module_loaded,
    list_module_attributes,
    reload_module,
)


def test_import_module_and_attr_access():
    m = import_module("math")
    assert isinstance(m, ModuleType)
    # доступ к атрибуту через нашу обёртку
    name = import_and_get_attr("math", "__name__")
    assert name == "math"
    # атрибут функции присутствует в пространстве имён
    attrs = list_module_attributes(m)
    assert "sqrt" in attrs


def test_is_module_loaded_after_import():
    _ = import_module("math")
    assert is_module_loaded("math") is True


def test_reload_module_roundtrip():
    m = import_module("math")
    m2 = reload_module(m)
    assert m2 is m  # reload возвращает тот же объект (перевыполненный)


def test_get_module_file_for_stdlib_and_builtin():
    # stdlib: у большинства модулей есть __file__
    m_os = import_module("os")
    assert get_module_file(m_os) is not None

    # built-in: у sys обычно нет __file__
    m_sys = import_module("sys")
    assert get_module_file(m_sys) is None


def test_sys_path_introspection_and_append_idempotent(tmp_path):
    path_list = get_sys_path()
    assert isinstance(path_list, list)
    assert len(path_list) > 0

    # Добавление нового пути в sys.path
    new_dir = str(tmp_path)
    ensure_path_appended(new_dir)
    path_list2 = get_sys_path()
    assert new_dir in path_list2

    # Повторное добавление не плодит дубликаты
    ensure_path_appended(new_dir)
    path_list3 = get_sys_path()
    assert path_list3.count(new_dir) == 1


def test_find_first_on_sys_path_reports_loaded_location():
    # Загружаем модуль и спрашиваем, откуда он (или что выбрано как первая директория)
    _ = import_module("math")
    mod_file, picked_dir = find_first_on_sys_path("math")
    # picked_dir — первая директория поиска, mod_file — реальный файл (или None для built-in)
    assert isinstance(picked_dir, str)
    # Для math обычно есть файл .so/.pyd/.py — допускаем None на нестандартных сборках
    assert mod_file is None or isinstance(mod_file, str)
