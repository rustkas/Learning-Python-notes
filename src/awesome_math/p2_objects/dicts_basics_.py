from __future__ import annotations

__all__ = [
    "make_person_literal",
    "fetch_and_change",
    "build_by_assignment",
    "from_keywords",
    "from_zip",
    "insertion_order_demo",
    "nested_record_demo",
    "missing_key_strategies",
    "update_and_union_demo",
    "iteration_materials",
    "loop_formats_examples",
    "main",
]


def make_person_literal() -> dict:
    """Создать словарь литералом."""
    return {"name": "Pat", "job": "dev", "age": 40}


def fetch_and_change() -> tuple[str, dict]:
    """
    Доступ по ключу и изменение значения.
    Возвращает (исходное_name, словарь_после_смены_job->'mgr').
    """
    d = {"name": "Pat", "job": "dev", "age": 40}
    name = d["name"]
    d["job"] = "mgr"
    return name, d


def build_by_assignment() -> dict:
    """Построить словарь поэтапно присваиваниями ключей."""
    d: dict[str, object] = {}
    d["name"] = "Pat"
    d["job"] = "dev"
    d["age"] = 40
    return d


def from_keywords() -> dict:
    """Создать словарь через dict(name=..., ...)."""
    return dict(name="Pat", job="dev", age=40)


def from_zip() -> dict:
    """Создать словарь через dict(zip(keys, values))."""
    keys = ["name", "job", "age"]
    vals = ["Pat", "dev", 40]
    return dict(zip(keys, vals))


def insertion_order_demo() -> list[str]:
    """Показать порядок вставки ключей."""
    d: dict[str, int] = {}
    d["x"] = 1
    d["y"] = 2
    d["z"] = 3
    return list(d.keys())


def nested_record_demo() -> tuple[dict, dict, str, list, str, dict]:
    """
    Вложенные структуры:
    - rec: {'name': {'first': 'Pat', 'last': 'Smith'}, 'jobs': ['dev', 'mgr'], 'age': 40.5}
    - доступ к полям и модификация вложенного списка jobs.
    Возвращает (rec0, name_dict, last, jobs0, last_job, rec_after_append)
    """
    rec = {
        "name": {"first": "Pat", "last": "Smith"},
        "jobs": ["dev", "mgr"],
        "age": 40.5,
    }
    name_dict = rec["name"]
    last = rec["name"]["last"]
    jobs0 = rec["jobs"]
    last_job = rec["jobs"][-1]
    rec["jobs"].append("janitor")
    return rec.copy(), name_dict, last, jobs0, last_job, rec


def missing_key_strategies() -> dict[str, object]:
    """
    Примеры для отсутствующих ключей:
    - 'in' проверка,
    - get с дефолтом,
    - тернарное выражение.
    Также демонстрируем рост словаря при присваивании нового ключа.
    """
    d = {"a": 1, "b": 2, "c": 3}
    d["d"] = 4
    exists_e = "e" in d
    safe_get_e = d.get("e", "missing")
    ternary_e = d["e"] if "e" in d else 0
    return {
        "dict": d,
        "exists_e": exists_e,
        "safe_get_e": safe_get_e,
        "ternary_e": ternary_e,
    }


def update_and_union_demo() -> tuple[dict, dict, dict]:
    """
    Слияние словарей:
    - copy()+update: меняет копию на месте,
    - оператор | : создаёт новый словарь.
    Возвращает (base, updated_copy, union_new).
    """
    base = {"a": 1, "b": 2}
    other = {"b": 200, "c": 3}
    updated = base.copy()
    updated.update(other)  # in-place
    union_new = base | other  # new dict (Python >= 3.9)
    return base, updated, union_new


def iteration_materials() -> tuple[dict, list, list, list]:
    """
    Материалы для итерации:
    - словарь d,
    - списки keys(), values(), items() (для детерминированной проверки).
    """
    d = dict(a=1, b=2, c=3)
    return d, list(d.keys()), list(d.values()), list(d.items())


def loop_formats_examples(d: dict[str, int]) -> tuple[list[str], list[str]]:
    """
    Две формы обхода:
    - по ключам (неявно),
    - по парам items() с распаковкой.
    Возвращает списки строк 'k => v'.
    """
    a = [f"{k} => {d[k]}" for k in d]  # implicit keys()
    b = [f"{k} => {v}" for (k, v) in d.items()]
    return a, b


def main() -> None:
    """Демонстрация примеров из книги"""
    person = make_person_literal()
    print("person =", person)

    name, changed = fetch_and_change()
    print("name =", name)
    print("after change job =", changed)

    print("build by assignment =", build_by_assignment())
    print("from keywords =", from_keywords())
    print("from zip =", from_zip())

    print("insertion order =", insertion_order_demo())

    rec0, name_dict, last, jobs0, last_job, rec1 = nested_record_demo()
    print("rec0 =", rec0)
    print("name dict =", name_dict, "last =", last)
    print("jobs0 =", jobs0, "last_job =", last_job)
    print("rec after append =", rec1)

    miss = missing_key_strategies()
    print("dict after new key =", miss["dict"])
    print("exists_e =", miss["exists_e"])
    print("safe_get_e =", miss["safe_get_e"])
    print("ternary_e =", miss["ternary_e"])

    base, updated, union_new = update_and_union_demo()
    print("base =", base)
    print("updated =", updated)
    print("union_new =", union_new)

    d, k, v, it = iteration_materials()
    print("keys =", k)
    print("values =", v)
    print("items =", it)

    a, b = loop_formats_examples(d)
    print("loop implicit keys =", a)
    print("loop items =", b)


if __name__ == "__main__":
    main()
