# pylint: disable=invalid-name, missing-function-docstring, missing-class-docstring
import sys
from typing import get_type_hints


def func_annotations() -> dict[str, dict[str, object]]:
    """Вернём сырые и разрешённые аннотации функции add."""
    return {
        "raw": add.__annotations__,
        "resolved": get_type_hints(add),
    }


variable_v: int = "anything"


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    return f"Hi {name}"


class User:
    name: str
    age: int


def user_annotations():
    return {
        "raw": User.__annotations__,
        "resolved": get_type_hints(User),
    }


def annotations_of_var() -> dict[str, object]:
    """Вернём тип аннотации переменной variable_v, уже разрешённый до класса."""
    resolved = get_type_hints(sys.modules[__name__])
    return {"type": resolved.get("variable_v")}


def main() -> None:
    """Демонстрация примеров из книги"""
    print(f"add(1, 2) -> {add(1, 2)}")
    print(f"add('1','2') -> {add('1', '2')}")
    print(f"greet(123) -> {greet(123)}")
    print(f"variable_v annotation -> {annotations_of_var()['type']}, value -> {variable_v}")

    ua = user_annotations()
    user_keys = sorted(ua["raw"].keys())
    print(f"User.__annotations__ keys -> {user_keys}")
    print(f"User annotations resolved -> {ua['resolved']}")

    fa = func_annotations()
    print(f"add annotations raw -> {fa['raw']}")
    print(f"add annotations resolved -> {fa['resolved']}")


if __name__ == "__main__":
    main()
