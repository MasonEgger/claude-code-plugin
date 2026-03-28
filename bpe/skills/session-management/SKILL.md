---
name: Session Management
description: This skill should be used when the user asks to "write a session summary", "save lessons learned", "create a session recap", "check session history", "update lessons.md", "what happened last session", "review previous sessions", "start execute-plan", or when referencing ".ai-sessions", "lessons.md", or "previous session". Provides format specifications and workflow guidance for session tracking and cross-session lessons accumulation.
version: 0.1.0
---

# Session Management

## Purpose

Track structured session history and accumulated lessons in the project's `.ai-sessions/` directory. Write session summaries after each work session. Maintain `lessons.md` with reusable insights organized in a hybrid chronological/categorical format.

## Directory Structure

All session artifacts live in `.ai-sessions/` at the project root:

```
.ai-sessions/
├── lessons.md                              # Accumulated cross-session learnings
├── session-20260225-1430-plugin-setup.md   # Individual session summaries
├── session-20260224-0900-api-refactor.md
└── ...
```

Create the directory with `mkdir -p .ai-sessions` if it does not exist.

## Session Summary Files

### Naming Convention

Files follow the pattern: `session-{timestamp}-{slug}.md`

- **Timestamp**: Generated via `date +%Y%m%d-%H%M` (always use this command)
- **Slug**: 2-3 word kebab-case description of the session's primary focus

### Required Sections

Every session summary includes:

1. **Header** - Date, duration, conversation turns, estimated cost, model
2. **Key Actions** - Bulleted recap organized by task or phase
3. **Prompt Inventory** - Table mapping prompts to actions and outcomes
4. **Efficiency Insights** - What went well, what could improve
5. **Process Improvements** - Actionable suggestions for future sessions
6. **Observations** - Patterns, highlights, noteworthy moments

For detailed format templates, category guidelines, and lesson quality examples, consult **`references/formats.md`**.

## Lessons Learned (lessons.md)

### Hybrid Format

The `lessons.md` file uses a hybrid structure combining chronological and categorical organization:

- **Recent section**: The 10 most recent lessons, newest first. Provides quick access to fresh insights.
- **Category sections**: Lessons organized by topic (Python, Testing, Git, Tooling, Architecture, Workflow, Debugging, etc.). Provides lookup by domain.

Each lesson entry includes a date in parentheses: `- Lesson text (YYYY-MM-DD)`

### Capturing Lessons

When identifying lessons from a session:

1. Focus on **specific, actionable insights** - not generic advice
2. Prefer concrete over abstract: "Use `just check` instead of running linters individually" beats "Run linters efficiently"
3. **Deduplicate** against existing entries - update wording and date if substantially similar
4. Keep the Recent section to 10 entries maximum - move older entries to categories only
5. Create new category headings as needed - use judgment for the most specific fit

### Integration with BPE Workflow

When running `/bpe:execute-plan`, check for `.ai-sessions/` and read the latest summary for prior context before beginning work.

