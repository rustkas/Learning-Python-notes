# pylint: disable=consider-using-f-string
from __future__ import annotations

__all__ = [
    "find_substring",
    "replace_substring",
    "split_csv",
    "upper_and_isalpha",
    "rstrip_line",
    "strip_then_split",
    "format_three_ways",
    "advanced_formats",
    "main",
]


def find_substring(s: str, sub: str) -> int:
    """Вернёт смещение подстроки sub в s или -1, если не нашлось."""
    return s.find(sub)


def replace_substring(s: str, old: str, new: str) -> str:
    """Заменит все вхождения old на new и вернёт НОВУЮ строку (s не меняется)."""
    return s.replace(old, new)


def split_csv(line: str) -> list[str]:
    """Разобьёт строку по запятой в список подстрок."""
    return line.split(",")


def upper_and_isalpha(s: str) -> tuple[str, bool]:
    """Вернёт (верхний_регистр(s), только_буквы?)."""
    return s.upper(), s.isalpha()


def rstrip_line(line: str) -> str:
    """Обрезает пробельные символы справа (включая \\n, \\t, пробел)."""
    return line.rstrip()


def strip_then_split(line: str) -> list[str]:
    """Обрезает справа и затем делит по запятой (цепочка вызовов)."""
    return line.rstrip().split(",")


def format_three_ways(tool: str, major: int, minor: int) -> tuple[str, str, str]:
    """Демонстрация трёх способов форматирования (minor + 9 — как в книге)."""
    fmt_expr = "Using %s version %s.%s" % (tool, major, minor + 9)
    fmt_method = "Using {} version {}.{}".format(tool, major, minor + 9)
    fmt_f = f"Using {tool} version {major}.{minor + 9}"
    return fmt_expr, fmt_method, fmt_f


def advanced_formats() -> tuple[str, str, str]:
    """Расширенные форматы: точность/знаки/заполнение/разделители."""
    a = "%.2f | %+05d" % (3.14159, -62)  # -> '3.14 | -0062'
    b = "{1:,.2f} | {0}".format("sapp"[1:], 296_999.256)  # -> '296,999.26 | app'
    c = f"{296_999.256:,.2f} | {'sapp'[1:]}"  # -> '296,999.26 | app'
    return a, b, c


def main() -> None:
    """Демонстрация примеров из книги"""
    # неизменяемость: методы создают НОВЫЕ строки
    s = "Code"
    print("s =", s)
    print("s.find('od') =", find_substring(s, "od"))  # 1
    print("s.replace('od','abl') =", replace_substring(s, "od", "abl"))  # 'Cable'
    print("s (unchanged) =", s)  # 'Code'

    # split / rstrip / цепочки
    line = "aaa,bbb,ccccc,dd\n"
    print("line.rstrip() =", rstrip_line(line))  # 'aaa,bbb,ccccc,dd'
    print("line.rstrip().split(',') =", strip_then_split(line))  # ['aaa', 'bbb', 'ccccc', 'dd']

    # регистры и тесты содержания
    s2 = "code"
    up, is_alpha = upper_and_isalpha(s2)
    print("s2.upper() =", up)  # 'CODE'
    print("s2.isalpha() =", is_alpha)  # True

    # три способа форматирования
    tool, major, minor = "Python", 3, 3
    f1, f2, f3 = format_three_ways(tool, major, minor)
    print("format %  =", f1)
    print("format() =", f2)
    print("f-string =", f3)

    # расширенные форматы
    a, b, c = advanced_formats()
    print("advanced1 =", a)
    print("advanced2 =", b)
    print("advanced3 =", c)


if __name__ == "__main__":
    main()
