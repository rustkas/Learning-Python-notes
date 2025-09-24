from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable

__all__ = [
    "write_lines",
    "read_all",
    "read_by_size",
    "read_one_line",
    "iter_lines_stripped",
    "seek_and_read",
    "append_line",
    "main",
]


def write_lines(path: str | Path, lines: Iterable[str]) -> int:
    """Записать строки по одной, добавляя '\\n' после каждой. Возвращает кол-во символов."""
    p = Path(path)
    written = 0
    with p.open("w", encoding="utf-8", newline="") as f:
        for line in lines:
            written += f.write(line + "\n")
    return written


def read_all(path: str | Path) -> str:
    """Прочитать весь файл как одну строку."""
    with Path(path).open("r", encoding="utf-8") as f:
        return f.read()


def read_by_size(path: str | Path, size: int) -> str:
    """Прочитать первые size символов файла."""
    with Path(path).open("r", encoding="utf-8") as f:
        return f.read(size)


def read_one_line(path: str | Path) -> str:
    """Прочитать первую строку целиком (включая завершающий '\\n', если есть)."""
    with Path(path).open("r", encoding="utf-8") as f:
        return f.readline()


def iter_lines_stripped(path: str | Path) -> list[str]:
    """Итеративно прочитать файл построчно, обрезая завершающие пробелы/переводы строк."""
    out: list[str] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            out.append(line.rstrip())
    return out


def seek_and_read(path: str | Path, offset: int, size: int) -> str:
    """Переместить указатель в offset и прочитать size символов."""
    with Path(path).open("r", encoding="utf-8") as f:
        f.seek(offset)
        return f.read(size)


def append_line(path: str | Path, line: str) -> int:
    """Дописать строку в конец (с переводом строки).Возвращает кол-во символов, записанных сейчас"""
    with Path(path).open("a", encoding="utf-8", newline="") as f:
        return f.write(line + "\n")


def main() -> None:
    """Демонстрация примеров из книги"""
    with TemporaryDirectory() as td:
        p = Path(td) / "data.txt"
        n = write_lines(p, ["Hello", "world!"])
        print("wrote chars:", n)

        text = read_all(p)
        print("read_all:", repr(text))
        # как в книге: печать «распознаёт» управляющие символы
        print(text)

        print("split:", text.split())
        print("iter_lines:", iter_lines_stripped(p))

        print("read_by_size(5):", read_by_size(p, 5))
        print("read_one_line():", repr(read_one_line(p)))
        print("seek_and_read(6,5):", seek_and_read(p, 6, 5))  # после 'Hello\n' начинается 'world'

        append_line(p, "Again")
        print("after append:", repr(read_all(p)))


if __name__ == "__main__":
    main()
