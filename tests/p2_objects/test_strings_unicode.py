# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.strings_unicode_ import (
    a_diaeresis_variants,
    code_point_hex,
    encode_sizes,
    latin1_roundtrip,
    len_and_encoded_sizes,
    sample_text_and_bytes,
)


def test_sample_text_and_bytes_types_and_values():
    text, blob = sample_text_and_bytes()
    assert isinstance(text, str) and text == "hÄck"
    assert isinstance(blob, (bytes, bytearray)) and blob == b"a\x01c"


def test_encode_sizes_for_code_are_4_and_10():
    u8, u16 = encode_sizes("Code")
    assert (u8, u16) == (4, 10)  # utf-16 содержит BOM


def test_code_point_hex_for_snake():
    assert code_point_hex("🐍") == "0x1f40d"


def test_len_and_encoded_sizes_for_emoji():
    lc, b8, b16 = len_and_encoded_sizes("🐍")
    assert lc == 1
    assert b8 == 4
    assert b16 == 6  # 4 байта суррогатной пары + 2 байта BOM


def test_a_diaeresis_variants_all_equal():
    v1, v2, v3, v4, v5 = a_diaeresis_variants()
    for s in (v2, v3, v4, v5):
        assert v1 == s == "hÄÄÄÄck"


def test_latin1_roundtrip_pounds():
    sym, by, back = latin1_roundtrip()
    assert sym == "£" and by == b"\xa3" and back == "£"


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_unicode_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "text = hÄck" in out
    assert "bytes = b'a\\x01c'" in out
    assert "sizes('Code') utf-8/utf-16 = 4 10" in out
    assert "hex(ord('🐍')) = 0x1f40d" in out
    assert "len/utf8/utf16 for '🐍' = 1 4 6" in out
    assert "variants equal to 'hÄÄÄÄck' = True" in out
    assert "latin1 roundtrip = £ b'\\xa3' £" in out
