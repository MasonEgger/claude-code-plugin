---
name: Session Management
description: This skill should be used when the user asks to "check session history", "what happened last session", "review previous sessions", "resume previous work", "what did we do last time", "pick up where we left off", "where did we leave off", "catch me up", "what's the status of this project", "load prior context", "continuing prior work", or "update lessons.md", or when referencing ".ai-sessions", "lessons.md", or "previous session". Provides format specifications and workflow guidance for session tracking and cross-session lessons accumulation. Session summary creation is handled by the /bpe:session-summary command, which loads this skill explicitly for format guidance.
version: 0.1.0
---

# Session Management

## Purpose

Track structured session history and accumulated lessons in the project's `.ai-sessions/` directory. Write session summaries after each work session. Maintain `lessons.md` with reusable insights organized in a hybrid chronological/categorical format.

## Directory Structure

All session artifacts live in `.ai-sessions/` at the project root:

- `.ai-sessions/lessons.md` — accumulated cross-session learnings
- `.ai-sessions/session-{YYYYMMDD}-{HHMM}-{slug}.md` — individual session summaries (e.g. `session-20260225-1430-plugin-setup.md`)

Create the directory with `mkdir -p .ai-sessions` if it does not exist.

## Session Summary Files

### Naming Convention

Files follow the pattern: `session-{timestamp}-{slug}.md`

- **Timestamp**: Generate via `date +%Y%m%d-%H%M`. Do not substitute `date` invocations or shell time variables.
- **Slug**: 2-3 word kebab-case description of the session's primary focus. When a session has no clear single focus, use `mixed-work`.

### Required Sections, Format Templates, and Lesson Quality Examples

Consult **`references/formats.md`** for the full session summary template, the `lessons.md` template, category guidelines, and good/bad lesson examples.

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

Before beginning work in `/bpe:execute-plan`, check whether `.ai-sessions/` exists. If it does, identify the most recent session summary by sorting filenames (the embedded `{YYYYMMDD}-{HHMM}` timestamp makes lexicographic order equal chronological order) — do not rely on filesystem mtime, which can be misleading after edits or git operations. Read that summary in full before beginning implementation.

If the latest summary contains a "Suggested Skills for Next Session" section, treat its entries as inputs to step 3 of `/bpe:execute-plan` (the hardened skill-loading step). Invoke those skills in addition to any the agent identifies from the current tech stack — the previous session's recommendation is a hint, not a cap.

For mid-session, forward-looking baton passes (handing the conversation to a fresh agent without finishing the current work), use `/bpe:handoff` instead. Handoff documents are ephemeral (`mktemp`-based) and live outside `.ai-sessions/`. They are not durable artifacts and are not auto-read by `/bpe:execute-plan` — the next agent must be pointed at the handoff path explicitly (e.g. `Read /tmp/handoff-XXXXXX.md`).

