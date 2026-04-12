# Python Toolchain Configuration

## Tool Summary

| Tool | Purpose |
|------|---------|
| `uv` | Package/dependency management, virtual environments |
| `ruff` | Linting + formatting (replaces black, flake8, isort) |
| `mypy` | Type checking (always use `--strict`) |
| `pytest` | Testing |
| `nox` | Test automation across environments |
| `just` | Task runner (alternative to make) |

## uv Commands

```bash
uv run script.py      # Run with automatic environment
uv add package        # Add dependency
uv sync               # Sync dependencies from pyproject.toml
uv venv               # Create virtual environment
```

Avoid `uv pip` commands—use `uv add` instead.

## pyproject.toml Example

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = []

[dependency-groups]
dev = [
    "ruff",
    "mypy",
    "pytest",
    "nox",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 120
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
strict = true
python_version = "3.14"
```

## justfile Example

```just
default:
    @just --list

check:
    ruff check .
    mypy .

fmt:
    ruff format .
    ruff check --fix .

test:
    pytest

all: fmt check test
```

## noxfile.py Example

```python
import nox

@nox.session(python=["3.11", "3.12"])
def tests(session: nox.Session) -> None:
    session.install(".", "-e", ".[dev]")
    session.run("pytest")

@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", ".")
```
