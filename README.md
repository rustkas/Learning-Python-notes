Локальная разработка:

# GitHub actions:

```
# rename
git branch -m ch03-script1 ch04
git remote set-url origin git@github.com:rustkas/Learning-Python-notes.git
git push --set-upstream origin ch04
git push -u origin ch04

```
# Python actions:

```
python -m venv .venv
source .venv/bin/activate  # WSL/Ubuntu
```

Поставь пакет в режиме разработки editable и dev-зависимости:
```
pip uninstall -y awesome-math
pip install -e .[dev]
```

Запусти тесты и линтеры:

```
# в VS Code: Task -> `check-all`
# или вручную:
ruff check src tests
mypy src tests
pytest -q tests


```

Собрать:
```
python -m build
twine check dist/*

```

`pytest tests/p1_start/test_script1.py -q`

`python -m awesome_math.p1_start.script1`

`pytest -q tests/p1_start/test_threenames.py`


# Очистка и пересборка

```
# из корня проекта
deactivate 2>/dev/null || true
rm -rf .venv

python3.10 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev]'

# проверка entry points
python - <<'PY'
import importlib.metadata as m
dist = m.distribution("awesome-math")
print("console_scripts:", sorted(ep.name for ep in dist.entry_points if ep.group=="console_scripts"))
for ep in dist.entry_points:
    if ep.group=="console_scripts":
        print(f"  {ep.name} -> {ep.value}")
PY

# файлы должны появиться
ls -l .venv/bin/amath .venv/bin/script1 .venv/bin/cycles

# запуск
script1
cycles
amath

```

```
pytest -q tests/p2_objects/test_numbers.py
pytest -q tests/p2_objects/test_strings_literals.py
pytest -q tests/p2_objects/test_strings_unicode.py
pytest -q tests/p2_objects/test_dicts_basics.py
pytest -q tests/p2_objects/test_tuples_basics.py
pytest -q tests/p2_objects/test_files_basics.py
pytest -q tests/p2_objects/test_files_like_tools.py
pytest -q tests/p2_objects/test_sets_basics.py
pytest -q tests/p2_objects/test_booleans_none.py
pytest -q tests/p2_objects/test_types.py
pytest -q tests/p2_objects/test_type_hinting.py
pytest -q tests/p2_objects/test_user_objects.py
python -m pytest -q tests/p2_objects/test_quiz_ch4.py

pytest -q tests/p5_numbers/test_numbers_expressions.py
pytest -q tests/p5_numbers/test_dynamic_typing.py
pytest -q tests/p5_numbers/test_lists_dicts.py
pytest -q tests/p5_numbers/test_tuples_files.py
# или весь набор
pytest -q
```