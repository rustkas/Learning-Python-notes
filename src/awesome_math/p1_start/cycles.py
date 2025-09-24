# Cyclic list demo: [1, 2, <self>]

from __future__ import annotations

def make_cycle() -> list:
    L: list = [1, 2]
    L.append(L)      # L[-1] is L
    return L

def main() -> None:
    L = make_cycle()
    # repr у самоссылочных контейнеров показывает [...] вместо бесконечной печати
    print(repr(L))

if __name__ == "__main__":
    main()
