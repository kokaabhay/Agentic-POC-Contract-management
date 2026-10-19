# Project Architecture

Automatically generated project structure and Python architecture information.

## Directory Tree

```text
Agentic-POC-Contract-management/
├── .git
│   └── [contents excluded]
├── api
│   ├── __pycache__
│   │   └── [contents excluded]
│   ├── routes
│   │   ├── __pycache__
│   │   │   └── [contents excluded]
│   │   ├── __init__.py
│   │   └── contracts.py
│   └── __init__.py
├── scripts
│   ├── __init__.py
│   └── generate_structure.py
├── src
│   ├── __pycache__
│   │   └── [contents excluded]
│   ├── app
│   │   ├── __pycache__
│   │   │   └── [contents excluded]
│   │   ├── services
│   │   │   ├── __pycache__
│   │   │   │   └── [contents excluded]
│   │   │   ├── blob_storage.py
│   │   │   └── doc_processor.py
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
├── streamlit
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

### `api\routes\contracts.py`

**Functions:**
- `normalize_batch_name()`
- `get_batch_prefix()`
- `upload_contract_batch()`
- `process_contract_batch()`

**Imports:**
- `re`
- `pathlib`
- `uuid`
- `fastapi`
- `starlette.concurrency`
- `src.app.config`
- `src.app.services.blob_storage`
- `src.app.services.doc_processor`

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

**Classes:**
- `Settings`

**Functions:**
- `allowed_extension_set()`

**Imports:**
- `pathlib`
- `pydantic_settings`

### `src\app\logger_config.py`

No classes, functions, or imports detected.

### `src\app\main.py`

**Functions:**
- `health_check()`

**Imports:**
- `api.routes.contracts`
- `src.app.config`
- `subprocess`
- `fastapi`

### `src\app\services\blob_storage.py`

**Functions:**
- `upload_bytes()`
- `download_bytes()`
- `list_blob_names()`
- `blob_exists()`
- `save_json()`
- `read_json()`

**Imports:**
- `json`
- `typing`
- `azure.storage.blob`
- `src.app.config`

### `src\app\services\doc_processor.py`

**Functions:**
- `extract_document()`

**Imports:**
- `tempfile`
- `pathlib`
- `docling.document_converter`

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
