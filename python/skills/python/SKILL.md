---
name: python
description: Python development standards and toolchain preferences. Use when (1) writing ANY Python code, (2) setting up Python projects with pyproject.toml, (3) creating standalone CLI scripts, (4) configuring Python tooling (ruff, mypy, pytest, nox, uv), (5) reviewing or refactoring Python code, or (6) advising on Python best practices. Enforces modern Pythonic style, strict type hints, and uv-based workflows. Make sure to use this skill whenever the user is working with .py files, pyproject.toml, noxfile.py, justfiles for Python projects, or any Python packaging — even if they don't explicitly mention Python standards.
---

# Python Development Standards

## Before Writing Any Code

**For applications and multi-file projects:** Read [references/tdd-workflow.md](references/tdd-workflow.md) first. Follow TDD with mandatory verification after every change.

**For CLI scripts and one-off utilities:** Skip TDD workflow. Focus on working code.

## Core Requirements

These requirements apply to all Python code without exception:

1. **Type hints everywhere** - all functions, all parameters, all return types. No `Any`.
2. **Docstrings on all public interfaces** - RST format for Sphinx compatibility.
3. **Absolute imports only** - never use relative imports.
4. **Modern Python idioms** - use latest features appropriate for target version.
5. **Empty `__init__.py`** - never add anything to `__init__.py`.
6. **Descriptive variable names** - single-letter names (`i`, `j`, `k`, `m`, `x`, etc.) are NEVER allowed. Use names that convey meaning: `line_index`, `inner_index`, `label_match`.
7. **`X | None` over `Optional[X]`** - for projects targeting Python 3.10+, use PEP 604 union syntax (`str | None`) instead of `typing.Optional[str]`. Ruff UP007 enforces this.

## Packaging

- **Dev dependencies**: Use `[dependency-groups]` in pyproject.toml, not `[project.optional-dependencies]`. Optional deps require explicit `uv sync --extra dev`, while dependency groups sync by default.
- **Hatchling build backend**: The correct string is `hatchling.build`, not `hatchling.backends`.

## Reference Files

Read based on task:

- [references/toolchain.md](references/toolchain.md) - Project setup and tool configuration (uv, ruff, mypy, pytest, nox, just)
- [references/cli-scripts.md](references/cli-scripts.md) - CLI tool development with PEP 723
- [references/documentation.md](references/documentation.md) - Docstring and doctest patterns
- [references/tdd-workflow.md](references/tdd-workflow.md) - Red-green-refactor cycle and verification commands
