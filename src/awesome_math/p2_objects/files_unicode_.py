from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

__all__ = [
    "binary_write_read_roundtrip",
    "text_write_read_utf8",
    "manual_encode_decode",
    "main",
]


def binary_write_read_roundtrip(path: str | Path) -> bytes:
    """
    Демонстрация бинарного файла: пишем сырые байты и читаем их обратно.
    Никаких Unicode-преобразований.
    """
    p = Path(path)
    sample = b"h\xffa\xeec\xddk\n"
    with p.open("wb") as f:
        f.write(sample)
    with p.open("rb") as f:
        data = f.read()
    return data


def text_write_read_utf8(path: str | Path, text: str) -> tuple[str, bytes]:
    """
    Демонстрация текстового файла: пишем Unicode-строку в UTF-8 и
    читаем (1) как текст (получаем исходные кодпоинты), (2) как сырые байты.
    """
    p = Path(path)
    with p.open("w", encoding="utf-8", newline="") as f:
        _ = f.write(text)
    with p.open("r", encoding="utf-8") as f:
        text_back = f.read()
    with p.open("rb") as f:
        raw = f.read()
    return text_back, raw


def manual_encode_decode(s: str, encoding: str = "utf-8") -> tuple[bytes, str]:
    """Ручная кодировка/декодировка."""
    b = s.encode(encoding)
    back = b.decode(encoding)
    return b, back


def main() -> None:
    """Демонстрация примеров из книги"""
    with TemporaryDirectory() as td:
        # 1) Бинарный файл
        bin_path = Path(td) / "data.bin"
        bdata = binary_write_read_roundtrip(bin_path)
        print("binary bytes =", repr(bdata))

        # 2) Текстовый файл (Unicode, UTF-8)
        txt_path = Path(td) / "unidata.txt"
        demo_text = " 🐍h\u00c4ck👏 "
        text_back, raw = text_write_read_utf8(txt_path, demo_text)
        print("text utf8 =", repr(text_back))
        print("bytes utf8 =", repr(raw))
        print("sizes:", len(text_back), len(raw))  # символы vs байты

        # 3) Вручную encode/decode
        enc, dec = manual_encode_decode("hÄck")
        print("manual utf8 encode/decode =", repr(enc), dec)


if __name__ == "__main__":
    main()
