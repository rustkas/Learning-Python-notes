# pylint: disable=missing-function-docstring,unnecessary-pass,consider-using-enumerate
from __future__ import annotations

from typing import Callable, Iterable, List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def evens_desc_while_continue(n: int) -> List[int]:
    """
    Возвращает чётные числа от n-1 до 0 включительно (убывающе),
    демонстрирует while + continue.
    """
    x = n
    out: List[int] = []
    while x:
        x -= 1
        if x % 2 != 0:
            continue
        out.append(x)
    return out


def first_factor_or_prime(num: int) -> Tuple[str, Optional[int]]:
    """
    Ищет делитель числа > 1. Демонстрирует while + break + else.

    Возвращает:
      ("factor", d)   если найден делитель d (2..num//2),
      ("prime", None) если делителей не нашли (нормальный выход из цикла).
    """
    if num <= 3:
        return ("prime", None) if num >= 2 else ("factor", 0)
    x = num // 2
    while x > 1:
        if num % x == 0:
            return "factor", x  # break-эквивалент — ранний возврат
        x -= 1
    # Сработает, только если break/return не выполнился
    return "prime", None


def sum_and_prod(seq: Iterable[int]) -> Tuple[int, int]:
    """
    Демонстрирует for по значениям: считает сумму и произведение.
    """
    s = 0
    p = 1
    for x in seq:
        s += x
        p *= x
    return s, p


def rotate_sequence(seq: Sequence[T]) -> List[List[T]]:
    """
    Возвращает все циклические сдвиги (развороты головы в хвост) исходной последовательности.
    Демонстрирует range + len и срезы.
    """
    res: List[List[T]] = []
    n = len(seq)
    for i in range(n):
        res.append(list(seq[i:] + seq[:i]))  # тот же тип на выходе — список
    return res


def step_slice(seq: Sequence[T], step: int) -> List[T]:
    """
    Возвращает каждый step-й элемент, демонстрирует срез с шагом как альтернативу range(..., step).
    """
    return list(seq[::step])


def pair_sum_zip(a: Iterable[int], b: Iterable[int]) -> List[int]:
    """
    Складывает элементы двух итерируемых параллельно, демонстрируя zip (усечение по кратчайшему).
    """
    return [x + y for x, y in zip(a, b)]


def index_items_enumerate(seq: Iterable[T], start: int = 0) -> List[Tuple[int, T]]:
    """
    Возвращает список пар (index, item), демонстрирует enumerate.
    """
    return [(i, v) for i, v in enumerate(seq, start=start)]


def find_with_for_else(seq: Iterable[T], pred: Callable[[T], bool]) -> Tuple[bool, Optional[T]]:
    """
    Ищет первый элемент, удовлетворяющий предикату.
    Демонстрация for/else:
      - если найден — ранний возврат (по сути break),
      - если не найден — срабатывает ветка после цикла (else-эквивалент).
    """
    for item in seq:
        if pred(item):
            return True, item
    return False, None


def add_one_inplace(lst: List[int]) -> List[int]:
    """
    Модифицирует список на месте, используя range(len(...)) для индексации.
    Демонстрирует ситуацию, где прямой 'for x in lst' не меняет исходный список.
    """
    for i in range(len(lst)):
        lst[i] += 1
    return lst


def nested_cartesian(xs: Iterable[T], ys: Iterable[U]) -> List[Tuple[T, U]]:
    """
    Демонстрирует вложенные for: прямое произведение двух коллекций.
    """
    res: List[Tuple[T, U]] = []
    for x in xs:
        for y in ys:
            res.append((x, y))
    return res


def infinite_noop(limit: int = 3) -> int:
    """
    Демонстрация pass: «делаем ничего» limit раз через while True.
    Возвращает количество «пустых» итераций (для тестируемости).
    """
    count = 0
    while True:
        # Делать нечего...
        pass  # noqa: PIE789 (если применяются дополнительные линтеры)
        count += 1
        if count >= limit:
            break
    return count
