# Session Management

This file is the single source of truth for the format and workflow of session artifacts in `.ai-sessions/`. The `/bpe:session-summary`, `/bpe:execute-plan`, and `/bpe:handoff` commands all read it directly via `${CLAUDE_PLUGIN_ROOT}/references/session-management.md`.

## Purpose

Track structured session history and accumulated lessons in the project's `.ai-sessions/` directory. Write session summaries after each work session. Maintain `lessons.md` with reusable insights organized in a hybrid chronological/categorical format.

## Directory Structure

All session artifacts live in `.ai-sessions/` at the project root:

- `.ai-sessions/lessons.md` — accumulated cross-session learnings
- `.ai-sessions/session-{YYYYMMDD}-{HHMM}-{slug}.md` — individual session summaries (e.g. `session-20260101-0900-plugin-setup.md`)

Create the directory with `mkdir -p .ai-sessions` if it does not exist.

## Session Summary Files

### Naming Convention

Files follow the pattern: `session-{timestamp}-{slug}.md`

- **Timestamp**: Generate via `date +%Y%m%d-%H%M`. Do not substitute `date` invocations or shell time variables.
- **Slug**: 2-3 word kebab-case description of the session's primary focus. When a session has no clear single focus, use `mixed-work`.

### Session Summary Template

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

## Suggested Skills for Next Session

- {Skill name (e.g. `python:python`) — one-line note on why it matters for the likely next step}
- ...
```

### Suggested Skills Populating Rule

The "Suggested Skills for Next Session" section gives the next `/bpe:execute-plan` run an explicit hint about which skills to invoke at its hardened skill-loading step. Populate it based on what the *next* step needs — not a log of what the current session loaded. Include a skill if the next step will need it (whether or not the current session used it); omit a skill the current session used incidentally if the next step will not need it. For example, if the current session edited Python tooling but the next step is documentation cleanup, omit `python:python` and include only the docs-relevant skills. Omit the section entirely only if the next session genuinely needs no skills.

## Lessons Learned (lessons.md)

### Hybrid Format

The `lessons.md` file uses a hybrid structure combining chronological and categorical organization:

- **Recent section**: The 10 most recent lessons, newest first. Provides quick access to fresh insights.
- **Category sections**: Lessons organized by topic (Python, Testing, Git, Tooling, Architecture, Workflow, Debugging, etc.). Provides lookup by domain.

Each lesson entry includes a date in parentheses: `- Lesson text (YYYY-MM-DD)`

### Lessons.md Template

Use this skeleton when initializing a new `lessons.md`. Category sections are created on demand — the template intentionally does not prescribe a fixed set. Categories are flat top-level (`##`) headings; do not nest them under a `## Categories` parent.

```markdown
# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- {Most recent lesson} ({YYYY-MM-DD})

<!--
Category sections live below. Create each one only when at least one
lesson belongs to it. Use the most specific applicable category.
Common starting points: Python, Testing, Git, Tooling, Architecture,
Workflow, Debugging. Other valid examples: Infrastructure,
Documentation, Performance, Security, DevOps, Plugin Development.
Omit categories with zero entries.
-->

## {Category}
- {Lesson} ({YYYY-MM-DD})
```

### Capturing Lessons

When identifying lessons from a session:

1. Focus on **specific, actionable insights** — not generic advice.
2. Prefer concrete over abstract: "Use `just check` instead of running linters individually" beats "Run linters efficiently".
3. **Deduplicate** against existing entries — update wording and date if substantially similar.
4. Keep the Recent section to 10 entries maximum — move older entries to categories only.
5. Create new category headings as needed — use judgment for the most specific fit.

### Category Guidelines

- Create categories as needed — the list above is a starting point, not exhaustive.
- A lesson belongs in the most specific applicable category.
- If a lesson fits multiple categories, pick one — avoid duplicating across categories.
- Categories with zero entries can be omitted from the file.
- Common additional categories: Infrastructure, Documentation, Performance, Security, DevOps, Plugin Development.

### Lesson Quality Examples

**Good lessons (specific, actionable):**
- Use `uv run --script` for standalone Python scripts — no virtualenv needed (2026-02-24)
- The ruff formatter handles import sorting — no need to configure isort separately (2026-02-25)
- Always read the most recent `.ai-sessions/` summary before starting execute-plan (2026-02-25)
- Ansible `--check` flag prevents accidental changes during testing (2026-02-24)

**Bad lessons (too generic, not actionable):**
- Python is good for scripting
- Always write tests
- Use version control
- Read documentation

## Integration with BPE Workflow

### `/bpe:execute-plan` Step 2 — Find the Most Recent Summary

Before beginning work in `/bpe:execute-plan`, check whether `.ai-sessions/` exists. If it does, identify the most recent session summary by sorting filenames lexicographically — the embedded `{YYYYMMDD}-{HHMM}` timestamp makes lexicographic order equal chronological order. Do not rely on filesystem mtime, which can be misleading after edits or git operations. Read that summary in full before beginning implementation.

### `/bpe:execute-plan` Step 3 — Honor "Suggested Skills for Next Session"

If the latest summary contains a "Suggested Skills for Next Session" section, treat its entries as inputs to the hardened skill-loading step. Invoke those skills in addition to any the agent identifies from the current tech stack — the previous session's recommendation is a hint, not a cap.

### Relationship to `/bpe:handoff`

For mid-session, forward-looking baton passes (handing the conversation to a fresh agent without finishing the current work), use `/bpe:handoff` instead of writing a session summary. Handoff documents are ephemeral (`mktemp`-based) and live outside `.ai-sessions/`. They are not durable artifacts and are not auto-read by `/bpe:execute-plan` — the next agent must be pointed at the handoff path explicitly (e.g. `Read /tmp/handoff-XXXXXX.md`).
