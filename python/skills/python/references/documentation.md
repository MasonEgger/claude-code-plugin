# Documentation Standards

Use RST-style docstrings formatted for Sphinx.

## Docstring Template

```python
def process_data(data: list[str], threshold: int = 10) -> dict[str, int]:
    """
    Process a list of strings and count occurrences above threshold.

    Args:
        data: List of strings to process
        threshold: Minimum count to include in results (default: 10)

    Returns:
        Dictionary mapping strings to their counts, filtered by threshold

    Raises:
        ValueError: If threshold is negative

    Examples:
        >>> process_data(["a", "a", "b"], threshold=2)
        {"a": 2}
    """
```

## Doctest Guidelines

Include 2-4 examples per function showing typical use and edge cases:

```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the arithmetic mean.

    Examples:
        >>> calculate_average([1.0, 2.0, 3.0])
        2.0
        >>> calculate_average([])
        Traceback (most recent call last):
            ...
        ValueError: Cannot calculate average of empty list
    """
```

**Use doctests for:** Simple examples, quick sanity checks, self-documenting code

**Use pytest for:** Complex scenarios, fixtures, mocks, external dependencies

## Running Doctests

```bash
python -m doctest module.py -v    # Single module
pytest --doctest-modules          # All modules via pytest
```
