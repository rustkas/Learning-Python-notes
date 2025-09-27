# tests/p5_numbers/test_module_packages.py
# pylint: disable=missing-function-docstring
# pylint: disable=unsupported-assignment-operation

from __future__ import annotations

import importlib
from pathlib import Path

from awesome_math.p24.module_packages import (
    import_fresh,
    is_namespace_package,
    module_attr,
    push_sys_path,
    write_tree,
)


def test_basic_package_import(tmp_path: Path):
    """
    Проверяем обычный импорт пакета: pkg/sub/mod.py и доступ к атрибутам.
    """
    root = tmp_path / "root"
    write_tree(
        root,
        {
            "dir1": {
                "dir2": {
                    "mod.py": "var = 'code'\n",
                }
            }
        },
    )

    with push_sys_path(root):
        m = import_fresh("dir1.dir2.mod")
        assert module_attr(m, "var") == "code"

        # повторный импорт не перезапускает код — импорт идемпотентен
        m2 = importlib.import_module("dir1.dir2.mod")
        assert m2 is m


def test_init_py_sets_namespace_and_precedence(tmp_path: Path):
    """
    __init__.py создаёт атрибуты пространства имен и повышает приоритет
    по сравнению с namespace-папками без __init__.py.
    """
    root = tmp_path / "root"
    write_tree(
        root,
        {
            "pkg": {
                "__init__.py": "name = 'Python'\n",
                "sub": {
                    "__init__.py": "value = 3.12\n",
                    "mod.py": "x = 42\n",
                },
            }
        },
    )

    with push_sys_path(root):
        pkg = import_fresh("pkg")
        assert module_attr(pkg, "name") == "Python"

        sub = importlib.import_module("pkg.sub")
        assert module_attr(sub, "value") == 3.12

        mod = importlib.import_module("pkg.sub.mod")
        assert module_attr(mod, "x") == 42

        # обычный пакет имеет __file__
        assert hasattr(pkg, "__file__")
        assert hasattr(sub, "__file__")


def test_relative_imports_inside_package(tmp_path: Path):
    """
    Относительные импорты в файле пакета: from . import b / from .b import val
    """
    root = tmp_path / "root"
    write_tree(
        root,
        {
            "pack": {
                "__init__.py": "",
                "a.py": "from . import b\nVAL = b.val.upper()\n",
                "b.py": "val = 'hack'\n",
            }
        },
    )

    with push_sys_path(root):
        a = import_fresh("pack.a")
        assert module_attr(a, "VAL") == "HACK"


def test_absolute_imports_skip_enclosing_package(tmp_path: Path):
    """
    Абсолютный импорт пропускает текущий пакет и ищет по sys.path.
    Создаём внешний модуль 'extmod' и внутри пакета пытаемся делать 'import extmod'.
    """
    root = tmp_path / "root"
    external = tmp_path / "external"

    write_tree(external, {"extmod.py": "answer = 7\n"})

    write_tree(
        root,
        {
            "pp": {
                "__init__.py": "",
                "inner.py": "import extmod\nANS = extmod.answer\n",
            }
        },
    )

    with push_sys_path(external), push_sys_path(root):
        inner = import_fresh("pp.inner")
        assert module_attr(inner, "ANS") == 7


def test_namespace_package_spanning_multiple_dirs(tmp_path: Path):
    """
    Namespace-пакет: две папки sub/ в разных корнях sys.path объединяются.
    """
    part1 = tmp_path / "part1"
    part2 = tmp_path / "part2"

    write_tree(
        part1,
        {"sub": {"mod1.py": "v1 = 'one'\n"}},
    )
    write_tree(
        part2,
        {"sub": {"mod2.py": "v2 = 'two'\n"}},
    )

    with push_sys_path(part1), push_sys_path(part2):
        # сам пакет 'sub' — namespace: есть __path__, нет __file__
        sub = import_fresh("sub")
        assert is_namespace_package(sub)

        mod1 = importlib.import_module("sub.mod1")
        mod2 = importlib.import_module("sub.mod2")
        assert module_attr(mod1, "v1") == "one"
        assert module_attr(mod2, "v2") == "two"


def test_regular_package_takes_precedence_over_namespace(tmp_path: Path):
    """
    Если на sys.path есть и обычный пакет (с __init__.py), и папка без __init__.py
    с тем же именем, выигрывает обычный пакет.
    """
    part_ns = tmp_path / "ns_part"
    part_reg = tmp_path / "reg_part"

    # namespace-контент (без __init__.py)
    write_tree(part_ns, {"tool": {"util.py": "flag = 'ns'\n"}})

    # обычный пакет того же имени (с __init__.py)
    write_tree(part_reg, {"tool": {"__init__.py": "kind = 'regular'\n"}})

    with push_sys_path(part_ns), push_sys_path(part_reg):
        tool = import_fresh("tool")
        # обычный пакет имеет __file__ и атрибуты из __init__.py
        assert hasattr(tool, "__file__")
        assert module_attr(tool, "kind") == "regular"
        # а namespace-модуль 'tool.util' не должен подмешиваться автоматически
        assert not hasattr(tool, "util")


def test_reload_chain_is_clean(tmp_path: Path):
    """
    Проверяем, что import_fresh очищает цепочку пакетов в sys.modules,
    чтобы можно было честно переимпортировать пакет другой версии.
    """
    root = tmp_path / "root"
    write_tree(root, {"a": {"b": {"c.py": "x = 1\n"}}})

    with push_sys_path(root):
        c1 = import_fresh("a.b.c")
        assert c1.x == 1

        # Заменим файл и убедимся, что новый импорт видит новые данные
        (root / "a" / "b" / "c.py").write_text("x = 2\n", encoding="utf-8")
        c2 = import_fresh("a.b.c")
        assert c2.x == 2
