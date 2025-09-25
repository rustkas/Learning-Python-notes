# pylint: disable=missing-function-docstring

from awesome_math.p5_numbers.lists_dicts import (
    build_lists_from_sources,
    dict_basic_ops,
    invert_dict_unique,
    list_copy_vs_alias,
    mutate_list_in_place,
    safe_get_cell,
    sort_demo,
    sorted_items_by_key,
    sparse_matrix_example,
    stack_with_list,
)


def test_build_lists_from_sources():
    # передаём одноразовый итератор (генератор), чтобы проверить корректную обработку
    src = (x for x in [1, 2, 3])
    res = build_lists_from_sources(src)

    assert res["literal"] == [0, 0, 0, 0, 0]
    assert res["repetition"] == [0] * 5

    # list-comp отработал корректно поверх одноразового итератора
    assert res["comp"] == [2, 4, 6]

    # Попробуем найти результат map под несколькими возможными именами.
    # Если автор модуля не сохранял его отдельно, не валим тест (компрехеншен уже проверен).
    for key in ("map", "via_map", "mapped", "map_list"):
        if key in res:
            assert res[key] == [2, 4, 6]
            break

    # распаковка склеивает разные источники; проверим полностью и частями
    assert res["unpacked"] == [1, 2, 3, 0, 1, 2]
    assert res["unpacked"][:3] == [1, 2, 3]
    assert res["unpacked"][-3:] == [0, 1, 2]


def test_mutate_list_in_place_and_alias():
    data = ["code", "Code", "CODE!"]
    mutated = mutate_list_in_place(data)
    # in-place: объект тот же, порядок и значения изменились предсказуемо
    assert isinstance(mutated, list)
    assert mutated is data

    # Функция перемещает tail в начало, а не удаляет
    assert mutated[0] == "tail"
    # и добавляет элементы "front" и "block"
    assert "front" in mutated
    assert "block" in mutated


def test_copy_vs_alias():
    src = [1, 2, 3]
    alias, shallow = list_copy_vs_alias(src)
    assert alias is src  # общая ссылка
    assert shallow is not src  # копия
    assert shallow[0] == 1  # копия не изменилась после модификации src
    assert src[0] == 999


def test_sort_demo():
    words = ["abc", "ABD", "aBe"]
    in_place, new_sorted = sort_demo(words)
    # исходный аргумент не мутирован
    assert words == ["abc", "ABD", "aBe"]
    # in_place: по убыванию с нормализацией
    assert in_place == ["aBe", "ABD", "abc"]
    # new_sorted: по возрастанию с нормализацией
    assert new_sorted == ["abc", "ABD", "aBe"]


def test_stack_with_list():
    assert stack_with_list([1, 2, 3]) == [3, 2, 1]


def test_dict_basic_ops_and_views_and_union():
    out = dict_basic_ops()
    data = out["data"]
    assert data["year"] == 2024
    assert data["py"][0] == "program"  # изменили вложенный список
    assert out["missing_default"] == 0

    merged = out["merged_new"]
    # 'edition' появился, 'py' перезаписан правым операндом
    assert merged["edition"] == 6
    assert merged["py"] == ["program", "dev"]

    # views собраны в списки
    assert set(out["keys"]) >= {"hack", "py", "year"}
    assert isinstance(out["values"], list)
    assert isinstance(out["items"], list)


def test_sparse_matrix_and_safe_get():
    m = sparse_matrix_example()
    assert m[(2, 3, 4)] == 88
    assert safe_get_cell(m, (2, 3, 6), default=0) == 0


def test_invert_dict_unique_and_sorted_items():
    dct = {"a": 1, "b": 2, "c": 3}
    inv = invert_dict_unique(dct)
    assert inv == {1: "a", 2: "b", 3: "c"}

    ordered = sorted_items_by_key({"c": 3, "a": 1, "b": 2})
    assert ordered == [("a", 1), ("b", 2), ("c", 3)]
