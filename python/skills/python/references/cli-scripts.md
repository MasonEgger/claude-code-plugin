# CLI Script Development with PEP 723

Use PEP 723 inline metadata for standalone, self-contained Python scripts.

## Script Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

"""Brief description of what this script does."""

import argparse


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    # Add arguments here
    args = parser.parse_args()
    # Implementation here


if __name__ == "__main__":
    main()
```

## Key Points

- Shebang: `#!/usr/bin/env -S uv run --script`
- Metadata block starts with `# /// script` and ends with `# ///`
- Specify `requires-python` for minimum Python version
- List dependencies with version constraints
- Make executable: `chmod +x script.py`
- Run directly (`./script.py`) or via `uv run script.py`
- `uv` creates disposable virtual environments automatically

## When NOT to Use PEP 723

- Multi-file projects → use `pyproject.toml`
- Shared libraries → use proper packaging
- Scripts needing complex dependency resolution → use full project structure
