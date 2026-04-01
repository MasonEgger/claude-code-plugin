---
description: View, search, and manage accumulated lessons from .ai-sessions/lessons.md
argument-hint: "[search term | recent | all | categories | prune | promote]"
---

# Lessons Command

View and manage accumulated lessons from `.ai-sessions/lessons.md`.

## Behavior

1. Read `.ai-sessions/lessons.md`
   - If the file does not exist, inform the user: "No lessons file found. Run `/bpe:session-summary` at the end of a session to start capturing lessons."
   - If the file exists, proceed based on arguments.

2. **No arguments** (`/bpe:lessons`): Display the full `## Recent` section and list available categories with their lesson counts.

3. **With search term** (`/bpe:lessons $ARGUMENTS`): Search the entire lessons.md for entries matching the argument. Display matching lessons grouped by category. If no matches, say so.

4. **Special arguments**:
   - `recent` - Show the Recent section (default if no args)
   - `all` - Display the entire lessons.md file
   - `categories` - List just the category headings with counts
   - `prune` - Review lessons.md for duplicates, outdated entries, or lessons that have already been incorporated elsewhere. Check all of the following for existing coverage:
     - The project's `CLAUDE.md`
     - All global rule files in `~/.claude/rules/*.md`
     - `~/.claude/CLAUDE.md`
     
     For each lesson that is already covered, note where it exists. Present findings to the user grouped by status:
     ```
     ## Already incorporated
     - [lesson] — covered in ~/.claude/rules/python.md
     - [lesson] — covered in project CLAUDE.md
     
     ## Duplicates
     - [lesson] — duplicate of [other lesson] in lessons.md
     
     ## Outdated
     - [lesson] — reason it appears outdated
     ```
     Ask the user to confirm before making changes. Pruned lessons are NOT deleted — they are moved to `.ai-sessions/lessons-pruned.md` with a record of what happened to each one:
     ```
     ## Pruned <date>
     - [lesson] — promoted to ~/.claude/rules/python.md
     - [lesson] — duplicate of [other lesson]
     - [lesson] — outdated: [reason]
     ```
     Append to the file if it already exists. Then remove the pruned lessons from lessons.md.
   - `promote` - Identify lessons that appear broadly applicable or have been validated across multiple sessions. For each promotable lesson, classify its destination:
     1. **Project-local**: Lessons specific to this codebase (architecture decisions, project-specific conventions, repo-specific workflows) → add to the project's `CLAUDE.md`.
     2. **Global**: Lessons that apply across all projects (language standards, tooling preferences, general workflow patterns) → add to the matching file in `~/.claude/rules/`. Read the existing rule files in `~/.claude/rules/*.md` to find the best fit by topic. If no existing rule file is a good fit, suggest creating a new one with appropriate `paths:` frontmatter (e.g., `paths: ["**/*.py"]` for Python-specific rules).
     
     Present the proposed promotions grouped by destination:
     ```
     ## Project CLAUDE.md
     - [lesson] — reason it's project-specific
     
     ## ~/.claude/rules/python.md (existing)
     - [lesson] — reason it fits here
     
     ## ~/.claude/rules/deployment.md (new file)
     - [lesson] — reason a new rule file is needed
     ```
     Ask the user to confirm, adjust destinations, or skip individual lessons before making any changes. After confirmed promotions are applied, remove the promoted lessons from lessons.md.

## Output Format

When displaying lessons, use clean markdown formatting. Group by category when showing search results. Always show the date associated with each lesson.
