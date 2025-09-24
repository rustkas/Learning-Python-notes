# pylint: disable=missing-function-docstring
import subprocess
import sys

from awesome_math.p2_objects.sets_basics_ import (
    basic_ops,
    collection_difference,
    make_sets,
    mutating_demo,
    order_neutral_equality,
    remove_duplicates,
)


def test_basic_ops_sets():
    x, y = make_sets()
    inter, union, diff, is_super = basic_ops(x, y)
    assert x == set("hack")
    assert y == {"a", "p"}
    assert inter == {"a"}
    assert union == set("hackp")
    assert diff == set("hck")
    assert is_super is False


def test_remove_duplicates_and_difference_and_eq():
    assert remove_duplicates([3, 1, 2, 1, 3, 1]) == [1, 2, 3]
    assert collection_difference("code", "hack") == {"d", "o", "e"}
    assert order_neutral_equality("code", "deoc") is True
    assert order_neutral_equality([1, 2, 2, 3], [3, 1, 1, 2]) is True


def test_mutating_demo_changes_set():
    before, after = mutating_demo()
    # 'p' добавлен, 'a' удалён
    assert "p" in after and "a" not in after
    # остальные элементы из "hack" кроме 'a' сохранились
    assert {"h", "c", "k"}.issubset(after)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.sets_basics_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    # так как печатаем отсортированные представления, ожидаемые строки детерминированы
    assert "X(sorted) = ['a', 'c', 'h', 'k']" in out
    assert "Y(sorted) = ['a', 'p']" in out
    assert "X & Y (sorted) = ['a']" in out
    assert "X | Y (sorted) = ['a', 'c', 'h', 'k', 'p']" in out
    assert "X - Y (sorted) = ['c', 'h', 'k']" in out
    assert "dedup = [1, 2, 3]" in out
    assert "diff('code','hack')(sorted) = ['d', 'e', 'o']" in out
    assert "order-neutral equality 'code' vs 'deoc' = True" in out
