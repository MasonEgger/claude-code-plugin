---
description: Generate session recap in .ai-sessions/ and capture lessons learned
---

# Session Summary Command

Create a complete session summary and capture lessons learned. This command performs two actions:
1. Generates a session summary file in `.ai-sessions/`
2. Appends lessons learned to `.ai-sessions/lessons.md`

## Step 1: Load the Format Reference and Setup

Read the canonical format reference at `${CLAUDE_PLUGIN_ROOT}/references/session-management.md`. Treat that file as the single source of truth for templates, naming conventions, and lesson capture guidance — do not restate or reinterpret its rules in this command.

If `.ai-sessions/` does not exist, create it:
```bash
mkdir -p .ai-sessions
```

Generate the timestamp using this exact command:
```bash
date +%Y%m%d-%H%M
```

## Step 2: Generate Session Summary

Create `.ai-sessions/session-{timestamp}-{slug}.md` per the naming convention and section template in the format reference ("Session Summary Template" section).

Populate every required section. Pull content from this conversation:
- Header metadata (date, duration, conversation turns, estimated cost, model)
- Goal Context (only if a `/goal` ran in this session — see "Goal Context Populating Rule" in the reference; omit the section entirely otherwise)
- Key actions taken
- Prompt inventory (table of user prompts → actions → outcomes)
- Efficiency insights, process improvements, observations
- Suggested skills for next session (which skills the next `/bpe:execute-plan` should invoke at its hardened skill-loading step — see "Suggested Skills Populating Rule" in the reference)

If the session has no clear single focus, use `mixed-work` as the slug.

## Step 3: Capture Lessons Learned

Update `.ai-sessions/lessons.md` per the rules in the format reference ("Capturing Lessons" and "Lessons.md Template" sections). In short:

- If `lessons.md` does not exist, initialize it from the template in the reference.
- Identify specific, actionable lessons from this session — not generic advice.
- Prepend new lessons to the `## Recent` section with a `(YYYY-MM-DD)` date suffix; cap Recent at 10 entries (move overflow into category-only).
- Place each lesson under the most specific applicable category heading per the category guidelines in the reference. Create new category headings on demand.
- Deduplicate against existing entries; update wording and date in place when substantially similar.

## Step 4: Offer to Clean Up Stale Handoffs

Check `.ai-sessions/handoffs/` for any `.md` files (per the "Handoff files" section of the format reference). For each one present, ask the user whether it can be removed now that this session is wrapping up. Default to keep on uncertainty; delete only on explicit confirmation. This prevents stale handoffs from being accidentally committed alongside the session summary.

## Step 5: Confirm

After completing both files, display:
- The path to the session summary file
- How many lessons were captured
- A brief preview of the lessons added
- A note about any handoff files that were deleted (or kept) in step 4

Ask the user if they want to adjust anything before the session ends.
