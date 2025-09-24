# src/awesome_math/p2_objects/user_objects_.py
# pylint: disable=missing-class-docstring, missing-function-docstring

from __future__ import annotations

from dataclasses import dataclass


class Worker:
    """Простейший пример пользовательского класса."""

    def __init__(self, name: str, pay: float) -> None:
        self.name = name
        self.pay = float(pay)

    def last_name(self) -> str:
        parts = self.name.strip().split()
        return parts[-1] if parts else ""

    def give_raise(self, percent: float) -> None:
        if percent < -1.0:
            raise ValueError("percent is too small; would make pay negative")
        self.pay *= 1.0 + percent

    def __repr__(self) -> str:  # удобный отладочный вид
        # показываем 2 знака после запятой, чтобы тесту было стабильно
        return f"Worker(name={self.name!r}, pay={self.pay:.2f})"


# Небольшая альтернатива на базе dataclass — «заготовка» со сравнениями и repr
@dataclass
class WorkerDC:
    name: str
    pay: float

    def last_name(self) -> str:
        parts = self.name.strip().split()
        return parts[-1] if parts else ""

    def give_raise(self, percent: float) -> None:
        if percent < -1.0:
            raise ValueError("percent is too small; would make pay negative")
        self.pay *= 1.0 + percent


# --- Утилиты для коллекций работников ---


def make_workers() -> list[Worker]:
    return [Worker("Sue Jones", 60000), Worker("Bob Smith", 50000)]


def give_raise_all(workers: list[Worker], percent: float) -> None:
    for w in workers:
        w.give_raise(percent)


def total_pay(workers: list[Worker]) -> float:
    return sum(w.pay for w in workers)


def main() -> None:
    """Демонстрация примеров из книги"""
    workers = make_workers()
    sue, bob = workers
    print("initial:", workers)
    print("sue.last_name() ->", sue.last_name())
    print("bob.last_name() ->", bob.last_name())
    give_raise_all(workers, 0.10)
    print("after 10% raise:", workers)
    print("total pay ->", f"{total_pay(workers):.2f}")

    # dataclass-вариант
    sue_dc = WorkerDC("Sue Jones", 60000)
    sue_dc.give_raise(0.10)
    print("dataclass repr:", sue_dc)


if __name__ == "__main__":
    main()
