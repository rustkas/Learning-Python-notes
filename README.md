Локальная разработка:

```
python -m venv .venv
source .venv/bin/activate  # WSL/Ubuntu
```

Поставь пакет в режиме разработки editable и dev-зависимости:
```
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
