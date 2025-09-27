# pylint: disable=missing-function-docstring, unused-variable
# pylint: disable=unsupported-assignment-operation, import-outside-toplevel
# ruff: noqa: F841
import sys
import textwrap
from importlib import import_module, reload
from pathlib import Path
from types import ModuleType

from awesome_math.p23.module_coding import (
    get_attr_path,
    list_public_names,
    mutate_shared_list,
    set_module_attr,
)


def write_module(tmp_path: Path, name: str, body: str) -> ModuleType:
    pkg_dir = tmp_path / "pkg_demo"
    pkg_dir.mkdir(exist_ok=True)
    (pkg_dir / "__init__.py").write_text("")
    mod_path = pkg_dir / f"{name}.py"
    mod_path.write_text(textwrap.dedent(body))
    sys.path.insert(0, str(tmp_path))
    try:
        return import_module(f"pkg_demo.{name}")
    finally:
        sys.path.pop(0)


def test_module_namespace_listing():
    import awesome_math.p23.module_coding as mc

    names = list_public_names(mc)
    # есть ключевые утилиты
    assert "list_public_names" in names
    assert "mutate_shared_list" in names
    assert "get_attr_path" in names


def test_from_semantics_copy_vs_shared(tmp_path):
    # Модуль-источник с неизменяемым x и изменяемым y
    share = write_module(
        tmp_path,
        "share",
        """
        x = 1
        y = [1, 2]
        """,
    )

    # Имитация "from share import x, y" — локальные имена-ссылки
    x = share.x
    y = share.y

    # Переназначение x влияет только локально
    x = 23
    assert share.x == 1

    # Изменение списка — общее, видно в модуле
    mutate_shared_list(y)
    assert share.y == ["hack", 2]


def test_import_vs_reload_and_from_pins_old_objects(tmp_path):
    # Стартовая версия
    changer = write_module(
        tmp_path,
        "changer",
        """
        message = 'First version'
        def printer():
            return message
        """,
    )

    # Клиент, использующий "import changer"
    assert changer.printer() == "First version"

    # Клиент, сделавший ранее "from changer import printer"
    copied_printer = changer.printer

    # Обновляем файл и перезагружаем
    pkg_dir = Path(changer.__file__).parent
    (pkg_dir / "changer.py").write_text(
        textwrap.dedent(
            """
            message = 'After editing'
            def printer():
                return 'reloaded: ' + message
            """
        )
    )

    reload(changer)

    # import-клиент видит новую версию
    assert changer.printer() == "reloaded: After editing"
    # а ранее скопированная ссылка осталась старой
    assert copied_printer() == "First version"


def test_attribute_qualification_paths(tmp_path):
    # Создаём связку nest2 -> nest3
    nest3 = write_module(tmp_path, "nest3", "X = 3")
    nest2 = write_module(
        tmp_path,
        "nest2",
        """
        X = 2
        import pkg_demo.nest3 as nest3
        """,
    )

    # Доступ по путям атрибутов
    assert getattr(nest2, "X") == 2
    assert get_attr_path(nest2, ["nest3", "X"]) == 3


def test_cross_file_mutation_requires_module_qualification(tmp_path):
    share = write_module(
        tmp_path,
        "share2",
        """
        x = 1
        """,
    )

    # Локальное имя не меняет модуль
    x = share.x
    x = 99
    assert share.x == 1

    # Изменяем имя непосредственно в модуле
    set_module_attr(share, "x", 42)
    assert share.x == 42
