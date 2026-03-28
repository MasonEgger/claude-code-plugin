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
   - `prune` - Review lessons.md for duplicates, outdated entries, or lessons that have been incorporated into CLAUDE.md. Suggest removals and ask user for confirmation before editing.
   - `promote` - Identify lessons that appear broadly applicable or have been validated across multiple sessions. Suggest adding them to the project's CLAUDE.md. Show the proposed additions and ask for confirmation.

## Output Format

When displaying lessons, use clean markdown formatting. Group by category when showing search results. Always show the date associated with each lesson.
