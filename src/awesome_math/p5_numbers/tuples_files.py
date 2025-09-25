# awesome_math/p5_numbers/tuples_files.py
from __future__ import annotations

import json
import pickle
from collections import namedtuple
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


def tuple_basics(seq: Sequence[int]) -> Dict[str, Any]:
    """Демонстрация базовых операций с кортежами и *-распаковкой."""
    t = tuple(seq)
    replaced_first = (999,) + t[1:] if t else t
    repeated = t * 2
    concatenated = t + (0, 1)
    unpacked_literal = (*t, -1, *range(3))
    return {
        "t": t,
        "len": len(t),
        "slice": t[1:-1] if len(t) >= 2 else (),
        "replaced_first": replaced_first,
        "repeated": repeated,
        "concatenated": concatenated,
        "unpacked_literal": unpacked_literal,
        "count_0": t.count(0),
        "index_first": (t.index(t[0]) if t else None),
    }


def replace_first_in_tuple(t: Tuple[Any, ...], value: Any) -> Tuple[Any, ...]:
    """Возвращает новый кортеж с заменённым первым элементом."""
    return (value,) + t[1:] if t else (value,)


Rec = namedtuple("Rec", ["name", "age", "jobs"])


def make_namedtuple_record(name: str, age: float, jobs: List[str]) -> Dict[str, Any]:
    """Создаёт namedtuple и даёт доступ по позиции и по имени."""
    rec = Rec(name=name, age=age, jobs=list(jobs))
    return {
        "rec": rec,
        "by_pos": (rec[0], rec[2]),
        "by_attr": (rec.name, rec.jobs),
        "as_dict": rec._asdict(),
    }


def shallow_vs_deep_copy() -> Dict[str, Any]:
    """Показывает разницу между поверхностной и глубокой копией."""
    original = {"a": [1, 2], "b": {"x": 10}}
    shallow = original.copy()  # верхний уровень
    deep = deepcopy(original)  # полностью
    # модифицируем вложенное
    original["a"][0] = 999
    original["b"]["x"] = 42
    return {
        "original": original,
        "shallow": shallow,  # изменится вместе с original по вложенным ссылкам
        "deep": deep,  # останется прежним
    }


def truthiness(values: Iterable[Any]) -> List[bool]:
    """Истинность объектов через bool()."""
    return [bool(v) for v in values]


def compare_dicts_by_items(left: Dict[Any, Any], right: Dict[Any, Any]) -> Dict[str, Any]:
    """Равенство словарей и сравнение 'по величине' через сортировку items()."""
    left_sorted = sorted(left.items())
    right_sorted = sorted(right.items())
    return {
        "eq": left == right,
        "lt_by_items": left_sorted < right_sorted,
        "gt_by_items": left_sorted > right_sorted,
    }


def none_preallocate(size: int) -> List[Any]:
    """Предзаполнение None и запись в последний элемент."""
    lst = [None] * size
    if size:
        lst[-1] = "OK"
    return lst


def repetition_gotcha_demo() -> Dict[str, Any]:
    """Иллюстрирует общий вложенный список при [L]*N и способ избежать этого."""
    base = [4, 5, 6]
    y_shared = [base] * 3
    base[1] = 0  # повлияет на все в y_shared
    # уникальные копии
    base2 = [4, 5, 6]
    y_isolated = [list(base2) for _ in range(3)]
    y_isolated[0][1] = 99
    return {"y_shared": y_shared, "y_isolated": y_isolated}


def cyclic_structure_repr() -> str:
    """Создаёт циклическую структуру и возвращает её repr/str (ожидаем '...')."""
    data = ["stuff"]
    data.append(data)
    return str(data)


def write_text_lines(path: Path, lines: Iterable[str]) -> Path:
    """Запись строк в текстовый файл через менеджер контекста."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        for line in lines:
            # write не добавляет \n — добавим сами
            f.write(line)
            if not line.endswith("\n"):
                f.write("\n")
    return path


def read_text_lines(path: Path) -> List[str]:
    """Чтение файла построчно итератором, без завершающих переводов строк."""
    out: List[str] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            out.append(line.rstrip("\n"))
    return out


def write_binary(path: Path, data: bytes) -> Path:
    """Запись байтов в бинарный файл."""
    path = Path(path)
    with path.open("wb") as f:
        f.write(data)
    return path


def read_binary(path: Path) -> bytes:
    """Чтение байтов из бинарного файла."""
    with Path(path).open("rb") as f:
        return f.read()


def pickle_roundtrip(obj: Any, path: Path) -> Any:
    """Сериализация/десериализация через pickle в бинарный файл."""
    p = Path(path)
    with p.open("wb") as f:
        pickle.dump(obj, f)
    with p.open("rb") as f:
        return pickle.load(f)


def json_roundtrip(obj: Any, path: Path) -> Any:
    """Сериализация/десериализация через JSON (текстовый файл)."""
    p = Path(path)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
