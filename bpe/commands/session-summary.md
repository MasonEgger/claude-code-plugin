---
description: Generate session recap in .ai-sessions/ and capture lessons learned
---

# Session Summary Command

Create a complete session summary and capture lessons learned. This command performs two actions:
1. Generates a session summary file in `.ai-sessions/`
2. Appends lessons learned to `.ai-sessions/lessons.md`

## Step 1: Load Skill and Setup

Invoke the `bpe:session-management` skill via the `Skill` tool to load format specifications and capture rules. Treat the skill as the canonical source for templates, naming conventions, and lesson capture guidance — do not restate or reinterpret its rules in this command.

If `.ai-sessions/` does not exist, create it:
```bash
mkdir -p .ai-sessions
```

Generate the timestamp using this exact command:
```bash
date +%Y%m%d-%H%M
```

## Step 2: Generate Session Summary

Create `.ai-sessions/session-{timestamp}-{slug}.md` per the naming convention and section template in the skill (`bpe/skills/session-management/references/formats.md`, "Session Summary Template").

Populate every required section. Pull content from this conversation:
- Header metadata (date, duration, conversation turns, estimated cost, model)
- Key actions taken
- Prompt inventory (table of user prompts → actions → outcomes)
- Efficiency insights, process improvements, observations
- Suggested skills for next session (which skills the next `/bpe:execute-plan` should invoke at its hardened skill-loading step)

If the session has no clear single focus, use `mixed-work` as the slug.

## Step 3: Capture Lessons Learned

Update `.ai-sessions/lessons.md` per the rules in the skill (`SKILL.md` → "Capturing Lessons" and `references/formats.md` → "Lessons.md Template"). In short:

- If `lessons.md` does not exist, initialize it from the template in `references/formats.md`.
- Identify specific, actionable lessons from this session — not generic advice.
- Prepend new lessons to the `## Recent` section with a `(YYYY-MM-DD)` date suffix; cap Recent at 10 entries (move overflow into category-only).
- Place each lesson under the most specific applicable flat top-level category heading (`## Python`, `## Testing`, etc.) — not nested under a `## Categories` parent. Create new category headings on demand.
- Deduplicate against existing entries; update wording and date in place when substantially similar.

## Step 4: Confirm

After completing both files, display:
- The path to the session summary file
- How many lessons were captured
- A brief preview of the lessons added

Ask the user if they want to adjust anything before the session ends.
