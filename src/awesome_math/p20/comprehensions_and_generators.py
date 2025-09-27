# src/awesome_math/p5_numbers/comprehensions_and_generators.py
# pylint: disable=missing-function-docstring

"""
Ключевые примеры по comprehensions и генераторам.
Основано на главе о Comprehensions and Generations. (См. учебный файл главы.)
"""

from typing import Callable, Iterable, Iterator, List, Sequence, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def main() -> None:
    """Демонстрация примеров из книги"""
    # Небольшой показ: ротации и квадраты
    print(list(scramble("code")))
    print(list(gen_squares(5)))


# --- Компрехенции и генераторные выражения ---


def ords_list(s: str) -> List[int]:
    """Возвращает коды символов строки (list-comprehension)."""
    return [ord(ch) for ch in s]


def even_squares(n: int) -> List[int]:
    """Квадраты чётных чисел 0..n-1 одной компрехенцией с фильтром."""
    return [x * x for x in range(n) if x % 2 == 0]


def double_gen(it: Iterable[T]) -> Iterator[Tuple[T, T]]:
    """Генераторное выражение: удваиваем каждый элемент как кортеж (x, x)."""
    return ((x, x) for x in it)


# --- Генераторы: функции ---


def gen_squares(n: int) -> Iterator[int]:
    """Генератор квадратов 0..n-1."""
    for i in range(n):
        yield i * i


def scramble(seq: Sequence[T]) -> Iterator[Sequence[T]]:
    """
    Генерирует все циклические сдвиги (ротации) последовательности.
    Пример из главы: N результатов для последовательности длины N.
    """
    for i in range(len(seq)):
        yield seq[i:] + seq[:i]


def permute(seq: Sequence[T]) -> Iterator[Sequence[T]]:
    """
    Рекурсивный генератор перестановок (N! результатов).
    Для больших N возвращает элементы по одному, не создавая огромный список.
    """
    if not seq:
        # Пустая последовательность -> единственная перестановка: пустая
        yield seq
        return
    for i in range(len(seq)):
        head = seq[i : i + 1]
        rest = seq[:i] + seq[i + 1 :]
        for tail in permute(rest):
            yield head + tail


# --- Мини-эмуляции map/zip (ленивые) ---


def mymap_func(func: Callable[..., U], *seqs: Iterable[T]) -> Iterator[U]:
    """
    Ленивая версия map с поддержкой нескольких итерируемых аргументов.
    Транслирует пары/тройки аргументов через zip-подобное объединение.
    """
    for args in zip(*seqs):
        yield func(*args)  # type: ignore[misc]


def myzip_gen(*seqs: Iterable[T]) -> Iterator[Tuple[T, ...]]:
    """
    Ленивая версия zip с усечением по кратчайшей последовательности.
    """
    for args in zip(*seqs):
        yield args


def mymap_pad(*seqs: Sequence[T], pad: U | None = None) -> Iterator[Tuple[T | U, ...]]:
    """
    Пэддящая версия «как map(func=None, ...) из Py2» для наблюдения длиной.
    Возвращает кортежи, выравнивая длины за счёт 'pad'.
    """
    # Требуются последовательности с индексами/len для подсчёта max длины:
    maxlen = max(len(s) for s in seqs) if seqs else 0
    for i in range(maxlen):
        yield tuple((s[i] if i < len(s) else pad) for s in seqs)


# --- Вспомогательные демонстрации single-pass свойства ---


def first_two(it: Iterable[T]) -> Tuple[T, T]:
    """Берёт первые два элемента из любого итерируемого источника."""
    iterator = iter(it)
    a = next(iterator)
    b = next(iterator)
    return a, b


def consume_all(it: Iterable[T]) -> List[T]:
    """Материализует всё в список (для сравнения с повторными проходами)."""
    return list(it)
