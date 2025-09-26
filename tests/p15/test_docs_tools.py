# pylint: disable=missing-function-docstring,import-outside-toplevel,missing-class-docstring
import re

import pytest

import awesome_math.p15.docs_tools as docs_tools


def test_module_has_docstring():
    assert isinstance(docs_tools.__doc__, str)
    assert "docs_tools" in docs_tools.__doc__


def test_function_docstring_and_behavior():
    # docstring есть и содержит ключевые слова
    doc = docs_tools.get_doc(docs_tools.square)
    assert "квадрат" in doc.lower()
    # функция работает
    assert docs_tools.square(4) == 16
    assert docs_tools.square(2.5) == pytest.approx(6.25)


def test_class_and_method_docstrings():
    assert "docstring" in docs_tools.Demo.__doc__.lower()
    assert "верхнем" in docs_tools.Demo.shout.__doc__.lower()
    assert docs_tools.Demo().shout("ok") == "OK"


def test_public_attrs_filters_private_and_dunder():
    names = docs_tools.public_attrs([])
    # обычные методы списка видны
    assert "append" in names
    # dunder-методы скрыты
    assert not any(n.startswith("__") for n in names)
    # одиночное подчеркивание тоже скрыто
    assert "_ipython_canary_method_should_not_exist_" not in names


def test_pydoc_text_on_user_function_contains_signature_or_keywords():
    text = docs_tools.pydoc_text(docs_tools.square)
    # В тексте есть имя объекта и краткое описание (из docstring)
    assert "square" in text
    assert re.search(r"возвращает.*квадрат", text.lower()) is not None


def test_pydoc_text_on_builtin_contains_known_phrase():
    text = docs_tools.pydoc_text(ord)
    # Док Pydoc по ord почти всегда содержит эту фразу
    assert "Return the Unicode code point" in text


def test_public_attrs_works_for_modules_too():
    import math

    names = docs_tools.public_attrs(math)
    assert "sin" in names and "cos" in names
    assert "__dict__" not in names


def test_get_doc_empty_for_objects_without_docstrings():
    class NoDoc:
        pass

    assert docs_tools.get_doc(NoDoc()) == ""


def test_docs_tools_all_exports():
    exported = set(docs_tools.__all__)
    assert {"public_attrs", "get_doc", "pydoc_text", "square", "Demo"} <= exported
