# pylint: disable=missing-function-docstring
import subprocess
import sys
from pathlib import Path

from awesome_math.p2_objects.files_like_tools_ import (
    gzip_text_roundtrip,
    mem_bytes_roundtrip,
    mem_text_roundtrip,
    pipe_upper_via_subprocess,
    shelve_roundtrip,
    sqlite_roundtrip,
)


def test_mem_text_and_bytes():
    assert mem_text_roundtrip(["a", "b"]) == ["a", "b"]
    assert mem_bytes_roundtrip(b"\x00\xff") == b"\x00\xff"


def test_gzip_text_roundtrip(tmp_path: Path):
    path = tmp_path / "sample.txt.gz"
    lines = ["spam", "eggs", "ham"]
    assert gzip_text_roundtrip(path, lines) == lines


def test_pipe_upper_via_subprocess():
    assert pipe_upper_via_subprocess("Abc!") == "ABC!"


def test_shelve_roundtrip(tmp_path: Path):
    data = shelve_roundtrip(tmp_path / "store")
    assert data["counter"] == 42
    assert data["user"]["name"] == "Pat"
    assert "dev" in data["user"]["roles"]


def test_sqlite_roundtrip(tmp_path: Path):
    rows = sqlite_roundtrip(tmp_path / "db.sqlite")
    # три строки, имена по порядку
    assert [name for _, name in rows] == ["alpha", "beta", "gamma"]


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.files_like_tools_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "mem_text = ['Hello', 'world']" in out
    assert "mem_bytes = b'\\x00\\x01\\x02'" in out
    assert "gzip_text = ['spam', 'eggs', 'ham']" in out
    assert "shelve = {'user': {'name': 'Pat', 'roles': ['dev', 'mgr']}, 'counter': 42}" in out
    assert "sqlite rows = [(1, 'alpha'), (2, 'beta'), (3, 'gamma')]" in out
    assert "pipe_upper = HELLO, PIPES!" in out
