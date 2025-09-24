import re
import sys
import subprocess

def test_script1_runs_and_outputs():
    # Запускаем как модуль, чтобы не зависеть от относительных путей
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p1_start.script1"],
        capture_output=True, text=True, check=True
    )
    lines = proc.stdout.strip().splitlines()
    assert len(lines) == 3

    # 1-я строка — платформа (допускаем linux/win32/darwin)
    assert re.match(r"^(linux|win32|darwin)", lines[0])

    # 2-я строка — 2**100
    assert lines[1] == "1267650600228229401496703205376"

    # 3-я строка — повтор строки
    assert lines[2] == "Hack!" * 8
