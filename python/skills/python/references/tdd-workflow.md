# TDD Workflow for Python

## The Cycle

For every change, follow this cycle:

1. **Write a failing test** — Define expected behavior before implementation
2. **Write minimal code to pass** — Only enough to make the test green
3. **Verify** — Run the full check suite (see below)
4. **Refactor** — Clean up while keeping tests green
5. **Verify again** — Ensure refactoring didn't break anything

## Verification Commands

After EVERY code change, run the full suite:

```bash
just check   # or run manually:
ruff check . && ruff format --check . && mypy --strict . && pytest
```

All four must pass before moving on:
- `ruff check .` — Linting
- `ruff format --check .` — Formatting verification
- `mypy --strict .` — Type checking
- `pytest` — Tests

## Test Structure

```python
def test_function_does_expected_thing() -> None:
    """Describe what behavior is being verified."""
    # Arrange
    input_data = create_test_input()

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_output
```

## What to Test

**Test:**
- Your application logic
- Edge cases and error conditions
- Integration points you control

**Don't test:**
- Framework/library behavior
- Trivial code (getters, setters, simple assignments)
- Implementation details (test outcomes, not internals)

## Red-Green-Refactor Discipline

```
┌─────────────────────────────────────────────────────┐
│  RED: Write failing test                            │
│    ↓                                                │
│  GREEN: Minimal code to pass                        │
│    ↓                                                │
│  VERIFY: ruff + mypy --strict + pytest (all pass)  │
│    ↓                                                │
│  REFACTOR: Clean up code                            │
│    ↓                                                │
│  VERIFY: ruff + mypy --strict + pytest (all pass)  │
│    ↓                                                │
│  REPEAT                                             │
└─────────────────────────────────────────────────────┘
```

## Key Rules

- Never skip verification steps
- Fix failures immediately—don't accumulate tech debt
- If tests fail after refactoring, undo and try again
- Type errors are bugs—treat them with same urgency as test failures
- Module-level mutable state (dicts, lists, caches) needs an `autouse` fixture that clears it between tests. Write the fixture during RED, not as a REFACTOR afterthought.
