# awesome_math/p5_numbers/lists_dicts.py
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def build_lists_from_sources(src: Iterable[int]) -> Dict[str, List[int]]:
    """Показывает разные способы сборки списка из iterable, безопасно и для генераторов."""
    # Замораживаем источник, чтобы его можно было проходить многократно
    src_list = list(src)

    literal = [0, 0, 0, 0, 0]
    repetition = [0] * 5
    comp = [x * 2 for x in src_list]
    via_map1 = list(map(lambda x: x * 2, src_list))
    via_map2 = list(map(lambda x: x * 2, src_list))
    via_map3 = list(map(lambda x: x * 2, src_list))
    unpacked = [*src_list, *range(3)]

    return {
        "literal": literal,
        "repetition": repetition,
        "comp": comp,
        "map1": via_map1,
        "map2": via_map2,
        "map3": via_map3,
        "unpacked": unpacked,
    }


def mutate_list_in_place(items: List[Any]) -> List[Any]:
    """Демонстрирует in-place операции списка."""
    items.append("tail")
    items.extend([1, 2])
    items.insert(1, "mid")
    items[0:0] = ["front"]  # вставка срезом в начало
    items[2:4] = ["block"]  # замена среза
    items.pop()  # удалить последний
    items.remove(1)  # удалить по значению
    items.reverse()
    return items


def list_copy_vs_alias(src: List[int]) -> Tuple[List[int], List[int]]:
    """Возвращает (alias, copy) после мутаций src, чтобы показать различие ссылок."""
    alias = src  # общая ссылка
    shallow = src[:]  # копия верхнего уровня
    src[0] = 999  # изменяем исходный
    return alias, shallow


def sort_demo(words: List[str]) -> Tuple[List[str], List[str]]:
    """Возвращает (in_place, new_sorted) — разные способы сортировки."""
    in_place = words[:]  # не мутируем аргумент
    in_place.sort(key=str.lower, reverse=True)
    new_sorted = sorted(words, key=str.lower, reverse=False)
    return in_place, new_sorted


def stack_with_list(seq: Iterable[int]) -> List[int]:
    """LIFO стек на списке: push=append, pop=pop."""
    stack: List[int] = []
    for x in seq:
        stack.append(x)
    popped = []
    while stack:
        popped.append(stack.pop())
    return popped


def dict_basic_ops() -> Dict[str, Any]:
    """Базовые операции со словарём, включая get/update/union и views."""
    data: Dict[str, Any] = {"hack": 1, "py": ["app", "dev"]}
    # доступ/создание/изменение
    data["year"] = 2024
    data["py"][0] = "program"

    # безопасные чтения
    missing = data.get("missing", 0)

    # merge: update (in-place) и | (новый словарь)
    other = {"py": ["program", "dev"], "edition": 6}
    merged_new = data | other  # Python >= 3.9 — копия + update

    # представления (views)
    keys_view = list(data.keys())
    values_view = list(data.values())
    items_view = list(data.items())

    return {
        "data": data,
        "missing_default": missing,
        "merged_new": merged_new,
        "keys": keys_view,
        "values": values_view,
        "items": items_view,
    }


def sparse_matrix_example() -> Dict[Tuple[int, int, int], int]:
    """Разрежённая матрица — dict с ключами-кортежами координат."""
    matrix: Dict[Tuple[int, int, int], int] = {}
    matrix[(2, 3, 4)] = 88
    matrix[(7, 8, 9)] = 99
    return matrix


def safe_get_cell(
    matrix: Dict[Tuple[int, int, int], int], coord: Tuple[int, int, int], default: int = 0
) -> int:
    """Безопасное чтение ячейки разрежённой матрицы — через get()."""
    return matrix.get(coord, default)


def invert_dict_unique(dct: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Инверсия словаря (value -> key). Работает корректно, если значения хешируемые и уникальны.
    """
    return {v: k for k, v in dct.items()}


def sorted_items_by_key(dct: Dict[str, int]) -> List[Tuple[str, int]]:
    """Возвращает пары (k, v), отсортированные по ключам, без мутации словаря."""
    return sorted(dct.items(), key=lambda kv: kv[0])
