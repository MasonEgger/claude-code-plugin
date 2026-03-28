---
description: Generate session recap in .ai-sessions/ and capture lessons learned
---

# Session Summary Command

Create a complete session summary and capture lessons learned. This command performs two actions:
1. Generates a session summary file in `.ai-sessions/`
2. Appends lessons learned to `.ai-sessions/lessons.md`

## Step 1: Setup

If `.ai-sessions/` does not exist, create it:
```bash
mkdir -p .ai-sessions
```

Generate the timestamp using this exact command:
```bash
date +%Y%m%d-%H%M
```

## Step 2: Generate Session Summary

Create `.ai-sessions/session-{timestamp}-{slug}.md` where `{slug}` is a 2-3 word kebab-case description of the session's primary focus.

The summary MUST include ALL of the following sections:

### Header
```markdown
# Session Summary: {Descriptive Title}
**Date**: {YYYY-MM-DD}
**Duration**: {approximate duration}
**Conversation Turns**: {count}
**Estimated Cost**: {estimate based on token usage}
**Model**: {model used}
```

### Key Actions
A brief, bulleted recap of what was accomplished. Organize by task or phase if the session covered multiple areas.

### Prompt Inventory
A table mapping the user's main prompts/commands to the actions taken:

| Prompt/Command | Action Taken | Outcome |
|---|---|---|

### Efficiency Insights
- What went well (efficient approaches, good tool usage)
- What could have been more efficient
- Any corrections or course changes mid-session

### Process Improvements
Specific, actionable suggestions for future sessions.

### Observations
Any other interesting highlights, patterns noticed, or noteworthy moments.

## Step 3: Capture Lessons Learned

After creating the session summary, update `.ai-sessions/lessons.md` with lessons from this session.

### If `lessons.md` does not exist, create it with this structure:

```markdown
# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->

## Categories
<!-- Lessons organized by topic -->
```

### Updating lessons.md

1. **Identify lessons**: Review the session for reusable insights - things that would help future sessions go more smoothly. These should be specific and actionable, not generic advice. Examples:
   - "The ruff formatter handles import sorting - no need to configure isort separately"
   - "Always check for existing .ai-sessions/ before starting execute-plan"
   - "Use `just check` instead of running linters individually"

2. **Add to Recent section**: Prepend each lesson to the `## Recent` section with a date:
   ```markdown
   - {lesson text} ({YYYY-MM-DD})
   ```
   Keep only the 10 most recent entries. Move older ones to their category only.

3. **Add to appropriate category**: Place each lesson under a topic heading (create the heading if it doesn't exist). Common categories include:
   - Python
   - Testing
   - Git
   - Tooling
   - Architecture
   - Workflow
   - Debugging

   Use your judgment for categories. If a lesson fits multiple categories, pick the most specific one. Include the date:
   ```markdown
   - {lesson text} ({YYYY-MM-DD})
   ```

4. **Deduplicate**: If a lesson is substantially similar to an existing one, update the existing entry with the newer/better wording and date rather than adding a duplicate.

## Step 4: Confirm

After completing both files, display:
- The path to the session summary file
- How many lessons were captured
- A brief preview of the lessons added

Ask the user if they want to adjust anything before the session ends.
