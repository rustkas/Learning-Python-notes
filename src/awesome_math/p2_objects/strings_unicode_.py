from __future__ import annotations

__all__ = [
    "sample_text_and_bytes",
    "encode_sizes",
    "code_point_hex",
    "len_and_encoded_sizes",
    "a_diaeresis_variants",
    "latin1_roundtrip",
    "main",
]


def sample_text_and_bytes() -> tuple[str, bytes]:
    """Пример: Unicode-строка и байтовая строка."""
    return "hÄck", b"a\x01c"


def encode_sizes(s: str) -> tuple[int, int]:
    """Размеры s в байтах при utf-8 и utf-16 (с BOM)."""
    return len(s.encode("utf-8")), len(s.encode("utf-16"))


def code_point_hex(ch: str) -> str:
    """Кодовая позиция символа в шестн. виде, напр. '🐍' -> '0x1f40d'."""
    return hex(ord(ch))


def len_and_encoded_sizes(s: str) -> tuple[int, int, int]:
    """
    (длина в символах, длина в utf-8 байтах, длина в utf-16 байтах).
    Удобно показывать различие для '🐍', 'Ä', смешанных строк и т.д.
    """
    return len(s), len(s.encode("utf-8")), len(s.encode("utf-16"))


def a_diaeresis_variants() -> tuple[str, str, str, str, str]:
    """
    Пять эквивалентных способов получить 'hÄÄÄÄck':
    - смешанный вариант: \xc4, \u00c4, \U000000c4, литерал 'Ä';
    - только \\x-экраны;
    - только \\u-экраны;
    - только \\U-экраны;
    - буквальный литерал.
    """
    s_mixed = "h\xc4\u00c4\U000000c4Äck"
    s_x = "h" + "\xc4" * 4 + "ck"
    s_u = "h" + "\u00c4" * 4 + "ck"
    s_u = "h" + "\U000000c4" * 4 + "ck"
    s_lit = "hÄÄÄÄck"
    return s_mixed, s_x, s_u, s_u, s_lit


def latin1_roundtrip() -> tuple[str, bytes, str]:
    """
    Пример кодировки/декодировки на latin1: '£' <-> b'\\xA3'.
    Возвращает (символ, байты, символ_после_decode).
    """
    symbol = "\u00a3"  # '£'
    as_bytes = symbol.encode("latin1")  # b'\xA3'
    back = as_bytes.decode("latin1")  # '£'
    return symbol, as_bytes, back


def main() -> None:
    """Демонстрация примеров из книги"""
    # str vs bytes
    text, blob = sample_text_and_bytes()
    print("text =", text)  # hÄck
    print("bytes =", blob)  # b'a\x01c'

    # размеры в разных кодировках
    u8, u16 = encode_sizes("Code")
    print("sizes('Code') utf-8/utf-16 =", u8, u16)  # 4, 10

    # кодовая позиция символа-эмодзи
    print("hex(ord('🐍')) =", code_point_hex("🐍"))  # 0x1f40d

    # сравнение длины в символах и байтах
    lc, b8, b16 = len_and_encoded_sizes("🐍")
    print("len/utf8/utf16 for '🐍' =", lc, b8, b16)  # 1, 4, 6

    # варианты записи 'Ä'
    v1, v2, v3, v4, v5 = a_diaeresis_variants()
    print("variants equal to 'hÄÄÄÄck' =", (v1 == v5 == v2 == v3 == v4))

    # latin1 roundtrip
    sym, by, back = latin1_roundtrip()
    print("latin1 roundtrip =", sym, by, back)


if __name__ == "__main__":
    main()
