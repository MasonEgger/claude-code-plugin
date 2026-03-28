# Session Management Format Templates

## Session Summary Template

```markdown
# Session Summary: {Descriptive Title}

**Date**: {YYYY-MM-DD}
**Duration**: {approximate duration}
**Conversation Turns**: {count}
**Estimated Cost**: {estimate based on token usage}
**Model**: {model used}

## Key Actions

- {Action 1 with brief description of outcome}
- {Action 2 with brief description of outcome}
- ...

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| {User's prompt or command} | {What Claude did} | {Result} |
| ... | ... | ... |

## Efficiency Insights

**What went well:**
- {Efficient approach or good tool usage}

**What could improve:**
- {Missed opportunity or inefficiency}

**Course corrections:**
- {Any mid-session changes in approach}

## Process Improvements

- {Specific, actionable suggestion for future sessions}
- ...

## Observations

- {Interesting patterns, noteworthy moments, or highlights}
- ...
```

## Lessons.md Template

```markdown
# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- {Most recent lesson} ({YYYY-MM-DD})
- {Second most recent} ({YYYY-MM-DD})
- ...

## Python
- {Python-specific lesson} ({YYYY-MM-DD})

## Testing
- {Testing-specific lesson} ({YYYY-MM-DD})

## Git
- {Git-specific lesson} ({YYYY-MM-DD})

## Tooling
- {Tooling-specific lesson} ({YYYY-MM-DD})

## Architecture
- {Architecture-specific lesson} ({YYYY-MM-DD})

## Workflow
- {Workflow-specific lesson} ({YYYY-MM-DD})

## Debugging
- {Debugging-specific lesson} ({YYYY-MM-DD})
```

### Category Guidelines

- Create categories as needed - the list above is a starting point, not exhaustive
- A lesson belongs in the most specific applicable category
- If a lesson fits multiple categories, pick one - avoid duplicating across categories
- Categories with zero entries can be omitted from the file
- Common additional categories: Infrastructure, Documentation, Performance, Security, DevOps

### Lesson Quality Examples

**Good lessons (specific, actionable):**
- Use `uv run --script` for standalone Python scripts - no virtualenv needed (2026-02-24)
- The ruff formatter handles import sorting - no need to configure isort separately (2026-02-25)
- Always read the most recent .ai-sessions/ summary before starting execute-plan (2026-02-25)
- Ansible `--check` flag prevents accidental changes during testing (2026-02-24)

**Bad lessons (too generic, not actionable):**
- Python is good for scripting
- Always write tests
- Use version control
- Read documentation
