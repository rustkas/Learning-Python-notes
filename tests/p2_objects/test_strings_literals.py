# pylint: disable=missing-function-docstring, unsupported-assignment-operation
import subprocess
import sys

from awesome_math.p2_objects.strings_literals_ import (
    make_escaped,
    quotes_equivalence,
    raw_examples,
    repr_nonprintables,
    triple_quote_message,
)


def test_escaped_lengths_and_repr_zero_byte():
    s_escape, s_zero = make_escaped()
    assert len(s_escape) == 5
    assert len(s_zero) == 5
    # значение включает нулевые байты; repr показывает их как \x00
    r = repr_nonprintables(s_zero)
    assert "\\x00" in r and r.startswith("'A") and r.endswith("C'")


def test_quotes_equivalence_true():
    assert quotes_equivalence() is True


def test_triple_quote_message_shape():
    msg = triple_quote_message()
    assert msg.startswith("\n")
    assert "bbb'''bbb\"\"bbb" in msg
    assert msg.endswith("\n")


def test_raw_examples_lengths_and_content():
    pattern_raw, windows_path, len_raw_n, len_norm_n = raw_examples()
    assert pattern_raw == r"\n\t\\"
    assert windows_path.startswith("C:\\") and windows_path.endswith("\\code")
    assert len_raw_n == 2
    assert len_norm_n == 1


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.strings_literals_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    assert "len(s_escape) = 5" in out
    assert "len(s_zero)   = 5" in out
    assert "repr(s_zero)  = 'A\\x00B\\x00C'" in out
    assert "quotes_equivalence = True" in out
    assert "triple_starts_with_newline = True" in out
    assert "triple_contains_quotes = True" in out
    assert "triple_ends_with_newline = True" in out
    assert "raw_pattern = \\n\\t\\" in out
    assert "windows_path = C:\\Users\\you\\code" in out
    assert "len(r'\\n') = 2 len('\\n') = 1" in out
