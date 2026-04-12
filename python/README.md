# Python Development Standards Plugin

Enforces modern Python coding conventions and provides reference documentation for toolchain configuration, TDD workflows, CLI script development, and documentation patterns.

## What's Included

### Skill: python

Triggers when working with `.py` files, `pyproject.toml`, or any Python tooling configuration.

**Core requirements** (always enforced):
- Type hints on all functions, parameters, and return types
- RST docstrings on public interfaces
- Absolute imports only
- Modern Python idioms
- Descriptive variable names (no single-letter names)
- PEP 604 union syntax (`X | None` over `Optional[X]`)

**Reference docs** (loaded on demand):
- `toolchain.md` — uv, ruff, mypy, pytest, nox, just configuration
- `cli-scripts.md` — PEP 723 inline metadata for standalone scripts
- `documentation.md` — Docstring and doctest patterns
- `tdd-workflow.md` — Red-green-refactor cycle with verification commands
