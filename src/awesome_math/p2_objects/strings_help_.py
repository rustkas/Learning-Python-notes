from __future__ import annotations

import inspect
import pydoc

__all__ = [
    "list_string_attrs",
    "dunder_add_equivalence",
    "method_doc",
    "type_name",
    "help_snippet_for_replace",
    "main",
]


def list_string_attrs(s: str) -> list[str]:
    """Вернуть список имён атрибутов/методов строки (dir)."""
    return dir(s)


def dunder_add_equivalence(s: str, tail: str) -> tuple[str, str]:
    """Показать эквивалентность s + tail и s.__add__(tail)."""
    return s + tail, s.__add__(tail)


def method_doc(obj: object, method_name: str) -> str:
    """Вернуть docstring метода (через inspect.getdoc)."""
    method = getattr(obj, method_name)
    return inspect.getdoc(method) or ""


def type_name(obj: object) -> str:
    """Имя типа объекта, эквивалент help(type(obj)) на уровне заголовка."""
    return type(obj).__name__


def help_snippet_for_replace() -> str:
    """Короткий снэпшот help-текста для str.replace (через pydoc.render_doc)."""
    # pydoc.render_doc форматирует «жирный» через backspace-оверстайл.
    # plain() очищает эти управляющие символы → получаем обычный текст.
    raw = pydoc.render_doc(str.replace)
    text = pydoc.plain(raw)
    return "\n".join(text.splitlines()[:3])  # первые строки для демонстрации


def main() -> None:
    """Демонстрация примеров из книги"""
    s = "Code"
    print("s =", s)

    attrs = list_string_attrs(s)
    print("attr_count =", len(attrs))
    print("'upper' in dir? ", "upper" in attrs)
    print("'__add__' in dir? ", "__add__" in attrs)

    res_plus, res_dunder = dunder_add_equivalence(s, "head!")
    print("s + 'head!' =", res_plus)
    print("s.__add__('head!') =", res_dunder)

    doc = method_doc(str, "replace")
    print("replace doc has 'old' and 'new'? ", ("old" in doc and "new" in doc))

    print("type_name(s) =", type_name(s))

    snippet = help_snippet_for_replace()
    print("help snippet first line:", snippet.splitlines()[0])


if __name__ == "__main__":
    main()
