# pylint: disable=missing-function-docstring
import subprocess
import sys
from pathlib import Path

from awesome_math.p2_objects.files_unicode_ import (
    binary_write_read_roundtrip,
    manual_encode_decode,
    text_write_read_utf8,
)


def test_binary_roundtrip(tmp_path: Path):
    p = tmp_path / "data.bin"
    got = binary_write_read_roundtrip(p)
    assert got == b"h\xffa\xeec\xddk\n"  # точное совпадение сырых байт


def test_text_utf8_roundtrip_and_sizes(tmp_path: Path):
    p = tmp_path / "unidata.txt"
    s = " 🐍hÄck👏 "
    text_back, raw = text_write_read_utf8(p, s)
    assert text_back == s
    assert raw == s.encode("utf-8")
    # в UTF-8 emoji и 'Ä' занимают больше 1 байта
    assert len(raw) > len(s)


def test_manual_encode_decode_utf8():
    b, back = manual_encode_decode("hÄck", "utf-8")
    assert b == b"h\xc3\x84ck"
    assert back == "hÄck"


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.files_unicode_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    # бинарная часть
    assert "binary bytes = b'h\\xffa\\xeec\\xddk\\n'" in out
    # текстовая часть
    s = " 🐍hÄck👏 "
    expected_bytes_repr = repr(s.encode("utf-8"))
    assert "text utf8 = " + repr(s) in out
    assert "bytes utf8 = " + expected_bytes_repr in out
    # ручной encode/decode
    assert "manual utf8 encode/decode = b'h\\xc3\\x84ck' hÄck" in out
