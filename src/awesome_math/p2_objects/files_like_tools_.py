from __future__ import annotations

import gzip
import shelve
import sqlite3
import subprocess
import sys
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable

__all__ = [
    "mem_text_roundtrip",
    "mem_bytes_roundtrip",
    "gzip_text_roundtrip",
    "pipe_upper_via_subprocess",
    "shelve_roundtrip",
    "sqlite_roundtrip",
    "main",
]


def mem_text_roundtrip(lines: Iterable[str]) -> list[str]:
    """StringIO: записать строки в памяти и прочитать их построчно."""
    buf = StringIO()
    for line in lines:
        buf.write(line + "\n")
    buf.seek(0)
    return [ln.rstrip() for ln in buf]


def mem_bytes_roundtrip(data: bytes) -> bytes:
    """BytesIO: записать байты в памяти и прочитать обратно."""
    buf = BytesIO()
    buf.write(data)
    return buf.getvalue()


def gzip_text_roundtrip(path: str | Path, lines: Iterable[str]) -> list[str]:
    """Записать/прочитать gz-текстовый файл c UTF-8."""
    p = Path(path)
    with gzip.open(p, "wt", encoding="utf-8", newline="") as f:
        for line in lines:
            f.write(line + "\n")
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return [ln.rstrip() for ln in f]


def pipe_upper_via_subprocess(text: str) -> str:
    """
    Прогоняем текст через дочерний Python-процесс по pipe:
    child читает stdin, пишет upper() в stdout.
    """
    code = "import sys; sys.stdout.write(sys.stdin.read().upper())"
    proc = subprocess.run(
        [sys.executable, "-c", code],
        input=text,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def shelve_roundtrip(path: str | Path) -> dict[str, object]:
    """Создаём shelf, пишем пару ключей, читаем обратно в обычный dict."""
    p = Path(path)
    # shelve.open принимает базовое имя файла без расширения
    with shelve.open(str(p)) as db:
        db["user"] = {"name": "Pat", "roles": ["dev", "mgr"]}
        db["counter"] = 42
    with shelve.open(str(p)) as db:
        return {k: db[k] for k in db.keys()}


def sqlite_roundtrip(path: str | Path) -> list[tuple[int, str]]:
    """Создаём SQLite-БД, вставляем несколько строк и читаем их обратно."""
    p = Path(path)
    con = sqlite3.connect(p)
    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")
        cur.executemany("INSERT INTO items(name) VALUES (?)", [("alpha",), ("beta",), ("gamma",)])
        con.commit()
        cur.execute("SELECT id, name FROM items ORDER BY id")
        return cur.fetchall()
    finally:
        con.close()


def main() -> None:
    """Демонстрация примеров из книги"""
    # 1) In-memory files
    mt = mem_text_roundtrip(["Hello", "world"])
    mb = mem_bytes_roundtrip(b"\x00\x01\x02")
    print("mem_text =", mt)
    print("mem_bytes =", mb)

    # 2) gzip text
    with TemporaryDirectory() as td:
        gz_path = Path(td) / "data.txt.gz"
        gz = gzip_text_roundtrip(gz_path, ["spam", "eggs", "ham"])
        print("gzip_text =", gz)

        # 3) shelve
        shelf_data = shelve_roundtrip(Path(td) / "store")
        print("shelve =", shelf_data)

        # 4) sqlite
        rows = sqlite_roundtrip(Path(td) / "db.sqlite")
        print("sqlite rows =", rows)

    # 5) pipes (subprocess)
    up = pipe_upper_via_subprocess("Hello, pipes!")
    print("pipe_upper =", up)


if __name__ == "__main__":
    main()
