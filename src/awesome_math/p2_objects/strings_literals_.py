from __future__ import annotations

__all__ = [
    "make_escaped",
    "repr_nonprintables",
    "quotes_equivalence",
    "triple_quote_message",
    "raw_examples",
    "main",
]


def make_escaped() -> tuple[str, str]:
    """
    Вернёт две строки:
    - s_escape: 'A\\nB\\tC'  (перевод строки + таб)
    - s_zero:   'A\\0B\\0C'  (нулевой байт внутри строки)
    """
    s_escape = "A\nB\tC"
    s_zero = "A\0B\0C"
    return s_escape, s_zero


def repr_nonprintables(s: str) -> str:
    """repr() строки: непечатаемые символы будут показаны как \\xNN и т.п."""
    return repr(s)


def quotes_equivalence() -> bool:
    """
    Один и тот же текст можно записать разными кавычками, избегая экранирования.
    Здесь обе формы дают одинаковую строку: He said "hi"
    """
    s_single = 'He said "hi"'
    s_double_escaped = 'He said "hi"'
    return s_single == s_double_escaped


def triple_quote_message() -> str:
    """
    Многострочный литерал в тройных кавычках (как в книге):
    первая строка пустая (начинается с \n), внутри есть как ''' так и "".
    """
    msg = """
aaaaaaaaaaaa
bbb'''bbb""bbb
cccccccc
"""
    return msg


def raw_examples() -> tuple[str, str, int, int]:
    """
    Показываем raw-строки:
    - pattern_raw = r'\\n\\t\\\\' — два символа на последовательность \n (в отличие от обычной строки)
    - windows_path = r'C:\\Users\\you\\code' — без удвоения обратных слэшей
    Возвращаем также длины: len(r'\\n') == 2, len('\\n') == 1.
    """
    pattern_raw = r"\n\t\\"
    windows_path = r"C:\Users\you\code"
    len_raw_n = len(r"\n")
    len_norm_n = len("\n")
    return pattern_raw, windows_path, len_raw_n, len_norm_n


def main() -> None:
    """Демонстрация примеров из книги"""
    s_escape, s_zero = make_escaped()
    print("len(s_escape) =", len(s_escape))  # 5
    print("len(s_zero)   =", len(s_zero))  # 5
    print("repr(s_zero)  =", repr_nonprintables(s_zero))  # 'A\\x00B\\x00C'

    print("quotes_equivalence =", quotes_equivalence())  # True

    msg = triple_quote_message()
    print("triple_starts_with_newline =", msg.startswith("\n"))
    print("triple_contains_quotes =", "bbb'''bbb\"\"bbb" in msg)
    print("triple_ends_with_newline =", msg.endswith("\n"))

    pattern_raw, windows_path, len_raw_n, len_norm_n = raw_examples()
    print("raw_pattern =", pattern_raw)  # \n\t\
    print("windows_path =", windows_path)  # C:\Users\you\code
    print("len(r'\\n') =", len_raw_n, "len('\\n') =", len_norm_n)


if __name__ == "__main__":
    main()
