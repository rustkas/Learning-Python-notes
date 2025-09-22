def add(a: float, b: float) -> float:
    return a + b

def mul(a: float, b: float) -> float:
    return a * b

def main() -> None:
    # entry point для console_script
    import sys
    a, b = map(float, sys.argv[1:3])
    print(add(a, b))
