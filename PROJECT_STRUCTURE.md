# Project Architecture

Automatically generated project structure and Python architecture information.

## Directory Tree

```text
Agentic-POC-Contract-management/
├── .git
│   └── [contents excluded]
├── api
│   ├── routes
│   │   └── __init__.py
│   └── __init__.py
├── scripts
│   ├── __init__.py
│   └── generate_structure.py
├── src
│   ├── app
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger_config.py
│   │   └── main.py
│   ├── app.egg-info
│   │   ├── dependency_links.txt
│   │   ├── PKG-INFO
│   │   ├── SOURCES.txt
│   │   └── top_level.txt
│   └── __init__.py
├── tests
│   └── __init__.py
├── venv
│   └── [contents excluded]
├── .env
├── .env.example
├── .gitignore
├── PROJECT_STRUCTURE.md
├── pyproject.toml
├── readme.md
└── requirements.txt
```

## Python Architecture

### `api\__init__.py`

No classes, functions, or imports detected.

### `api\routes\__init__.py`

No classes, functions, or imports detected.

### `scripts\__init__.py`

No classes, functions, or imports detected.

### `scripts\generate_structure.py`

**Functions:**
- `should_hide()`
- `should_collapse()`
- `generate_tree()`
- `analyze_python_file()`
- `find_python_files()`
- `generate_markdown()`
- `main()`

**Imports:**
- `pathlib`
- `ast`

### `src\__init__.py`

No classes, functions, or imports detected.

### `src\app\__init__.py`

No classes, functions, or imports detected.

### `src\app\config.py`

No classes, functions, or imports detected.

### `src\app\logger_config.py`

No classes, functions, or imports detected.

### `src\app\main.py`

**Imports:**
- `subprocess`

### `tests\__init__.py`

No classes, functions, or imports detected.

## Collapsed Directories

The following directories are intentionally shown in the tree but their contents are not expanded:

- `.env/`
- `.git/`
- `.idea/`
- `.venv/`
- `.vscode/`
- `__pycache__/`
- `env/`
- `node_modules/`
- `venv/`

## Hidden Directories

The following directories are completely excluded from the generated architecture:

- `.coverage/`
- `.mypy_cache/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.tox/`
- `build/`
- `dist/`
