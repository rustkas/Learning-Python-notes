# pylint: disable=missing-function-docstring
import subprocess
import sys
from pathlib import Path

from awesome_math.p2_objects.files_basics_ import (
    append_line,
    iter_lines_stripped,
    read_all,
    read_by_size,
    read_one_line,
    seek_and_read,
    write_lines,
)


def test_write_and_read_roundtrip(tmp_path: Path):
    path = tmp_path / "data.txt"
    _ = write_lines(path, ["Hello", "world!"])
    content = read_all(path)
    assert content == "Hello\nworld!\n"
    assert content.split() == ["Hello", "world!"]  # файл читается как строка


def test_read_by_size_and_readline(tmp_path: Path):
    path = tmp_path / "data.txt"
    write_lines(path, ["Hello", "world!"])
    assert read_by_size(path, 5) == "Hello"
    assert read_one_line(path) == "Hello\n"


def test_iteration_protocol(tmp_path: Path):
    path = tmp_path / "data.txt"
    write_lines(path, ["Hello", "world!"])
    assert iter_lines_stripped(path) == ["Hello", "world!"]


def test_seek_and_read_word(tmp_path: Path):
    path = tmp_path / "data.txt"
    write_lines(path, ["Hello", "world!"])
    # смещение 6 — после "Hello\n", читаем 5 символов "world"
    assert seek_and_read(path, 6, 5) == "world"


def test_append_and_read(tmp_path: Path):
    path = tmp_path / "data.txt"
    write_lines(path, ["Hello", "world!"])
    append_line(path, "Again")
    assert read_all(path) == "Hello\nworld!\nAgain\n"


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.files_basics_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    # ключевые фрагменты демонстрации
    assert "read_all: 'Hello\\nworld!\\n'" in out
    assert "Hello\nworld!\n" in out  # прямой вывод текста
    assert "iter_lines: ['Hello', 'world!']" in out
    assert "read_by_size(5): Hello" in out
    assert "read_one_line(): 'Hello\\n'" in out
    assert "seek_and_read(6,5): world" in out
    assert "after append: 'Hello\\nworld!\\nAgain\\n'" in out
