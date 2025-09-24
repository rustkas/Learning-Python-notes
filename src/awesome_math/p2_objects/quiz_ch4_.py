# src/awesome_math/p2_objects/quiz_ch4_.py
# pylint: disable=missing-function-docstring, invalid-name

from __future__ import annotations


def core_types() -> list[str]:
    """П.1: перечислить core-типы."""
    return [
        "numbers",
        "strings",
        "lists",
        "dicts",
        "tuples",
        "files",
        "sets",
        "bool",
        "none",
        "type",
    ]


def why_core() -> str:
    """П.2: почему «core»?"""
    return (
        "они встроены в язык и всегда доступны; для них есть синтаксис литералов "
        "('text', [..], {..}, (..)); другие объекты обычно создаются через импорт и вызовы "
        "функций (например, open для файлов)"
    )


def immutable_definition() -> tuple[str, list[str]]:
    """П.3: что значит immutable и какие типы такие?"""
    return (
        "нельзя менять на месте; создаём новые объекты выражениями",
        ["numbers", "strings", "tuples"],
    )


def sequence_and_iterable() -> dict[str, object]:
    """П.4: что такое sequence и как связано с iterable?"""
    return {
        "sequence_def": "позиционно упорядоченная коллекция; поддерживает indexing/slicing/concat",
        "sequence_examples": ["strings", "lists", "tuples"],
        "iterable_def": "физическая или виртуальная последовательность, выдающая элементы по требованию",
        "iterable_examples": ["sequences", "range", "files", "generators", "dict_keys"],
    }


def mapping_info() -> dict[str, object]:
    """П.5: что такое mapping и какой core-тип mapping?"""
    return {
        "mapping_def": "отображение ключ -> значение",
        "core_mapping": "dict",
        "notes": "сохраняет порядок вставки ключей (с Python 3.7), есть методы для тестов ключей и итерации",
    }


def polymorphism_definition() -> str:
    """П.6: что такое полиморфизм и зачем он?"""
    return (
        "смысл операции зависит от операндов (например, + у чисел — сложение, у строк — конкатенация); "
        "пишем код к интерфейсу, а не к конкретному типу, и получаем гибкость"
    )


def main() -> None:
    """Демонстрация примеров из книги"""
    print("Q1 core types ->", ", ".join(core_types()))
    print("Q2 why core   ->", why_core())
    imm_def, imm_list = immutable_definition()
    print("Q3 immutable  ->", imm_def, "; kinds:", ", ".join(imm_list))
    seq = sequence_and_iterable()
    print("Q4 sequence   ->", seq["sequence_def"], "; kinds:", ", ".join(seq["sequence_examples"]))  # type: ignore[index]
    print("   iterable   ->", seq["iterable_def"], "; kinds:", ", ".join(seq["iterable_examples"]))  # type: ignore[index]
    m = mapping_info()
    print("Q5 mapping    ->", m["mapping_def"], "; core:", m["core_mapping"])  # type: ignore[index]
    print("Q6 polymorph  ->", polymorphism_definition())


if __name__ == "__main__":
    main()
