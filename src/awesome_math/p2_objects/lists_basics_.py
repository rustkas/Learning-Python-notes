from __future__ import annotations

__all__ = [
    "make_list_example",
    "sequence_ops",
    "list_mutations",
    "sort_and_reverse_demo",
    "bounds_demo",
    "make_matrix_3x3",
    "comprehensions_demo",
    "make_row_sums_generator",
    "row_sums_three",
    "set_and_dict_comprehensions",
    "main",
]


def make_list_example() -> list:
    """Создать учебный список разных типов."""
    return [123, "text", 1.23]


def sequence_ops(lst: list) -> tuple[object, list, list, list]:
    """
    Базовые операции последовательностей:
    - первый элемент,
    - срез до последнего (lst[:-1]),
    - конкатенация с [4,5,6],
    - повторение * 2.
    """
    first = lst[0]
    slice_upto_last = lst[:-1]
    concat_new = lst + [4, 5, 6]
    repeat_new = lst * 2
    return first, slice_upto_last, concat_new, repeat_new


def list_mutations() -> tuple[list, float, list]:
    """
    Демонстрация изменяемости:
    - append добавляет в конец,
    - pop удаляет по индексу и возвращает элемент (здесь индекс 2).
    """
    lst = [123, "text", 1.23]
    lst.append("Py")
    after_append = lst.copy()
    popped = lst.pop(2)
    after_pop = lst
    return after_append, popped, after_pop


def sort_and_reverse_demo() -> tuple[list, list]:
    """
    Сортировка и разворот in-place.
    Возвращаем копии после сортировки и после reverse.
    """
    m = ["bb", "aa", "cc"]
    m.sort()
    after_sort = m.copy()
    m.reverse()
    after_reverse = m.copy()
    return after_sort, after_reverse


def bounds_demo(lst: list) -> tuple[bool, bool]:
    """
    Попытки выйти за границы индекса и присвоить по несуществующему индексу.
    Возвращает (index_error, assign_error).
    """
    index_error = False
    assign_error = False
    try:
        _ = lst[99]
    except IndexError:
        index_error = True
    try:
        lst[99] = 1  # pylint: disable=unsupported-assignment-operation
    except IndexError:
        assign_error = True
    return index_error, assign_error


def make_matrix_3x3() -> tuple[list[list[int]], list[int], int]:
    """Создать 3×3 матрицу (список списков), вернуть (M, вторая строка, элемент [1][2])."""
    m = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    row2 = m[1]
    item_1_2 = m[1][2]
    return m, row2, item_1_2


def comprehensions_demo(m: list[list[int]]) -> dict[str, object]:
    """
    Демонстрация list comprehensions на матрице:
    - второй столбец,
    - второй столбец +1,
    - только чётные из второго столбца,
    - диагональ,
    - удвоение символов строки 'hack',
    - несколько значений: [x**2, x**3] для x=0..3,
    - положительные с шагом 2: [x, x//2, x*2] для x>-0.
    """
    col2 = [row[1] for row in m]
    col2_plus1 = [row[1] + 1 for row in m]
    col2_evens = [row[1] for row in m if row[1] % 2 == 0]
    diag = [m[i][i] for i in [0, 1, 2]]
    doubles = [c * 2 for c in "hack"]
    squares_cubes = [[x**2, x**3] for x in range(4)]
    positives = [[x, x // 2, x * 2] for x in range(-6, 7, 2) if x > 0]
    return {
        "col2": col2,
        "col2_plus1": col2_plus1,
        "col2_evens": col2_evens,
        "diag": diag,
        "doubles": doubles,
        "squares_cubes": squares_cubes,
        "positives": positives,
    }


def make_row_sums_generator(m: list[list[int]]):
    """Генератор сумм строк матрицы (generator expression)."""
    return (sum(row) for row in m)


def row_sums_three(m: list[list[int]]) -> list[int]:
    """Взять первые три значения из генератора сумм строк (удобно для тестов)."""
    g = make_row_sums_generator(m)
    return [next(g), next(g), next(g)]


def set_and_dict_comprehensions(m: list[list[int]]) -> tuple[set[int], dict[int, int]]:
    """
    Построить:
    - множество сумм строк,
    - словарь {индекс_строки: сумма}.
    """
    sums_set = {sum(row) for row in m}
    sums_dict = {i: sum(m[i]) for i in range(len(m))}
    return sums_set, sums_dict


def main() -> None:
    """Демонстрация примеров из книги"""
    lst = make_list_example()
    print("L =", lst)
    first, upto_last, concat_new, repeat_new = sequence_ops(lst)
    print("first =", first)
    print("L[:-1] =", upto_last)
    print("L + [4,5,6] =", concat_new)
    print("L * 2 =", repeat_new)
    print("L unchanged =", lst)

    after_append, popped, after_pop = list_mutations()
    print("after append =", after_append)
    print("popped =", popped)
    print("after pop =", after_pop)

    after_sort, after_reverse = sort_and_reverse_demo()
    print("sorted =", after_sort)
    print("reversed =", after_reverse)

    index_error, assign_error = bounds_demo(lst)
    print("index_error =", index_error, "assign_error =", assign_error)

    m, row2, item = make_matrix_3x3()
    print("M =", m)
    print("row2 =", row2, "item[1][2] =", item)

    comp = comprehensions_demo(m)
    print("col2 =", comp["col2"])
    print("col2_plus1 =", comp["col2_plus1"])
    print("col2_evens =", comp["col2_evens"])
    print("diag =", comp["diag"])
    print("doubles =", comp["doubles"])
    print("squares_cubes =", comp["squares_cubes"])
    print("positives =", comp["positives"])

    print("row sums (first 3) =", row_sums_three(m))

    sums_set, sums_dict = set_and_dict_comprehensions(m)
    print("sums_set =", sums_set)
    print("sums_dict =", sums_dict)


if __name__ == "__main__":
    main()
