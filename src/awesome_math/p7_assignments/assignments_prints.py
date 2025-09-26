# awesome_math/p7_assignments/assignments_prints.py
from __future__ import annotations

import sys
from io import StringIO
from typing import Any, Iterable, List, Tuple


def swap_tuple(a: Any, b: Any) -> Tuple[Any, Any]:
    """Идиоматическая перестановка через распаковку."""
    a, b = b, a
    return a, b


def split_first_rest(seq: Iterable[Any]) -> Tuple[Any, List[Any]]:
    """Расширенная распаковка: первый и «хвост»."""
    first, *rest = seq
    return first, rest


def split_rest_last(seq: Iterable[Any]) -> Tuple[List[Any], Any]:
    """Расширенная распаковка: «всё кроме последнего» и последний."""
    *rest, last = seq
    return rest, last


def nested_unpacking(s: str) -> Tuple[str, str, str]:
    """Вложенная распаковка по форме."""
    (a, b), c = s[:2], s[2:]
    return a, b, c


def multi_target_shared_list_demo() -> Tuple[List[int], List[int]]:
    """
    Демонстрация shared reference при множественном присваивании.
    Возвращает (a, b), где обе ссылки указывают на один список.
    """
    a = b = []
    b.append(42)  # in-place отражается в a
    return a, b


def separate_mutables_demo() -> Tuple[List[int], List[int]]:
    """Правильная инициализация двух разных списков одним выражением."""
    a, b = [], []  # создаём ДВА объекта
    b.append(42)
    return a, b


def augmented_list_inplace_shared() -> Tuple[List[int], List[int]]:
    """
    Показать, что L += [...] меняет на месте и видно через все ссылки.
    В отличие от L = L + [...], которое создаёт новый объект.
    """
    L = [1, 2]
    M = L
    L += [3, 4]  # эквивалентно L.extend(...)
    return L, M  # обе ссылки видят изменения


def concatenation_makes_new_object() -> Tuple[List[int], List[int]]:
    """Показать, что L = L + [...] создаёт новый объект, M не меняется."""
    L = [1, 2]
    M = L
    L = L + [3, 4]
    return L, M


def append_sort_gotcha(lst: List[int]) -> Tuple[List[int], Any]:
    """
    Возвращает (после append, результат sort()) — второй элемент будет None.
    (Модифицирует входной список.)
    """
    lst.append(99)
    sort_result = lst.sort()  # типичная ловушка: возвращает None
    return lst, sort_result


def read_until_stop(file_like, stop_line: str = "STOP\n") -> List[str]:
    """
    Читает строки до стоп-маркера, используя оператор := в заголовке while.
    Возвращает список строк без переводов строк.
    """
    lines: List[str] = []
    while (line := file_like.readline()) and line != stop_line:
        lines.append(line.rstrip("\n"))
    return lines


def print_pack(*objects: Any, sep: str = " ", end: str = "\n", file=sys.stdout) -> None:
    """Тонкая обёртка вокруг print для явной демонстрации параметров."""
    print(*objects, sep=sep, end=end, file=file)


def redirect_stdout_demo(text: str) -> str:
    """
    Временно переназначает sys.stdout на StringIO, печатает text и восстанавливает stdout.
    Возвращает захваченный вывод.
    """
    original = sys.stdout
    try:
        sink = StringIO()
        sys.stdout = sink
        print(text)
        return sink.getvalue()
    finally:
        sys.stdout = original


def named_assignment_math_repeat(base: str, n: int) -> Tuple[str, int]:
    """
    Демонстрация := как выражения: строит base * (k := n) и возвращает (строка, k).
    """
    s = base * (k := n)
    return s, k


# -------------------- ДОПОЛНЕНИЯ -------------------- #


def for_star_unpack(items: Iterable[Iterable[Any]]) -> List[Tuple[Any, List[Any], Any]]:
    """
    Расширенная распаковка в заголовке for: для каждого итерируемого
    элемента вида (a, ..., c) вернуть кортеж (a, список-середина, c).
    Пример входа: [(1,2,3,4), (5,6,7,8)] -> [(1,[2,3],4), (5,[6,7],8)].
    """
    acc: List[Tuple[Any, List[Any], Any]] = []
    for a, *b, c in items:
        acc.append((a, b, c))
    return acc


class _FlushSpy:
    """Фальш-объект файла для проверки, что flush был вызван при print(..., flush=True)."""

    def __init__(self) -> None:
        self.buf = StringIO()
        self.flush_called = False

    def write(self, s: str) -> int:
        return self.buf.write(s)

    def flush(self) -> None:
        self.flush_called = True

    def getvalue(self) -> str:
        return self.buf.getvalue()


def print_with_flush(text: str) -> Tuple[str, bool]:
    """
    Печатает в «файл» с обязательным flush=True; возвращает (накопленный_текст, flush_был_вызван).
    """
    spy = _FlushSpy()
    print(text, file=spy, flush=True)
    return spy.getvalue(), spy.flush_called


def capture_stderr_of_print(text: str) -> str:
    """
    Перехватывает вывод print(..., file=sys.stderr) через временную замену sys.stderr.
    Возвращает строку, ушедшую в stderr.
    """
    original = sys.stderr
    try:
        sink = StringIO()
        sys.stderr = sink
        print(text, file=sys.stderr)
        return sink.getvalue()
    finally:
        sys.stderr = original


def plus_equal_vs_plus_with_str_sequence() -> Tuple[List[str], str]:
    """
    Демонстрация различий:
    - L += 'abc' допустимо (список расширится отдельными символами);
    - L = L + 'abc' => TypeError (нельзя конкатенировать list и str).
    Возвращает (результат после +=, имя типа исключения при +).
    """
    L: List[str] = []
    L += "abc"  # работает как extend
    err = "NO_ERROR"
    try:
        _ = L + "xyz"  # ожидаем TypeError
    except Exception as e:  # noqa: BLE001 (нам важно имя)
        err = type(e).__name__
    return L, err


def named_assignment_illegal_targets() -> Tuple[bool, bool]:
    """
    Проверяет, что конструкции с := на не-именованных целях не компилируются:
    (a[0] := 1) и (obj.attr := 1) должны давать SyntaxError на стадии compile().
    Возвращает пару булевых: (поймали_SyntaxError_для_индекса, ..._для_атрибута).
    """
    src_index = "(lambda a: (a[0] := 1))([0])"
    src_attr = "class X: pass\nx=X()\n(x.y := 1)"
    ok_index = ok_attr = False
    try:
        compile(src_index, "<mem>", "exec")
    except SyntaxError:
        ok_index = True
    try:
        compile(src_attr, "<mem>", "exec")
    except SyntaxError:
        ok_attr = True
    return ok_index, ok_attr
