# tests/p2_objects/test_user_objects.py
# pylint: disable=missing-function-docstring
import subprocess
import sys

from awesome_math.p2_objects.user_objects_ import (
    Worker,
    WorkerDC,
    give_raise_all,
    make_workers,
    total_pay,
)


def test_worker_basics_and_raise():
    sue = Worker("Sue Jones", 60000)
    bob = Worker("Bob Smith", 50000)

    assert sue.last_name() == "Jones"
    assert bob.last_name() == "Smith"

    sue.give_raise(0.10)
    assert round(sue.pay, 2) == 66000.00

    # repr стабилен по формату
    r = repr(sue)
    assert "Worker(name='Sue Jones', pay=66000.00)" in r


def test_utils_on_collections():
    ws = make_workers()
    assert [w.last_name() for w in ws] == ["Jones", "Smith"]

    give_raise_all(ws, 0.10)
    assert round(ws[0].pay, 2) == 66000.00
    assert round(ws[1].pay, 2) == 55000.00

    assert round(total_pay(ws), 2) == 121000.00


def test_dataclass_variant_behaves_similarly():
    sue_dc = WorkerDC("Sue Jones", 60000)
    assert sue_dc.last_name() == "Jones"
    sue_dc.give_raise(0.10)
    assert round(sue_dc.pay, 2) == 66000.00
    # dataclass даёт удобный repr автоматически
    assert "WorkerDC" in repr(sue_dc)


def test_run_as_module_prints_expected_fragments():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.user_objects_"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout
    # несколько характерных маркеров
    assert "initial: [Worker(name='Sue Jones', pay=60000.00)" in out
    assert "sue.last_name() -> Jones" in out
    assert "bob.last_name() -> Smith" in out
    assert "after 10% raise:" in out
    assert "total pay -> 121000.00" in out
    assert "dataclass repr: WorkerDC" in out
