---
description: "Pull completed and pending Todoist tasks into today's Obsidian journal entry, grouped by project"
argument-hint: "[MM-DD-YYYY]"
---

## Todoist Daily Sync — Pull completed & pending tasks into Obsidian journal

You are syncing Mason's Todoist tasks into his Obsidian daily journal using the `todo` CLI (aliased to `/opt/homebrew/bin/td`).

### Required Checks
You MUST perform these checks and they must ALL be true before you proceed:

- Check to see if the directory you are working in is an Obsidian Vault. If it isn't, tell the user this command is only for use in an Obsidian Vault and do NO MORE WORK.
- Verify `todo` works by running `todo project list --json --limit 1`. If it fails, tell the user to set up the Todoist CLI (`/opt/homebrew/bin/td`) aliased as `todo` and authenticate with `todo auth login`. Do NO MORE WORK.
- Calculate the year using `date +%Y` and save as {year}. Calculate today's date using `date +%m-%d-%Y` and save as {today}.
- If $ARGUMENTS is provided, use that as {date}. Otherwise, use {today} as {date}.
- Check to see if there is a Journal entry in Journal/{year}/current/{date}.md. If there isn't, tell the user to create the journal entry for that day and do NO MORE WORK.

### Step 1: Fetch Data
Run these three commands and parse the JSON output:

1. **Projects map**: `todo project list --json --all`
   Build a map of project `id` → `name` from the results array.

2. **Completed tasks**: `todo completed --since {YYYY-MM-DD} --until {YYYY-MM-DD+1} --json --full --all`
   Convert {date} from MM-DD-YYYY to YYYY-MM-DD for the `--since` param. Set `--until` to the next day.
   Each result has: `content`, `completedAt`, `projectId`, `labels`, `description`.

3. **Pending tasks for today**: `todo task list --due today --json --full --all`
   Each result has: `content`, `projectId`, `labels`, `due`, `priority`.

### Step 2: Organize by Project
Group completed tasks by project name (resolved from the project map).
Group pending tasks by project name.

For each task:
- Use the `content` field as the task text.
- Resolve `projectId` to a project name using the map from Step 1.
- If the project name matches something in the vault (e.g., PyTexas, Temporal), use an Obsidian `[[cross-link]]` for the project header.
  - Before cross-linking, check if a file exists in the vault for that project name.
- If a task has time-estimate labels (5min, 15min, 30min, 1hr, 2hr, half-day, full-day), include them as a subtle note.

Omit projects with zero completed tasks from the completed section.
Omit the pending section entirely if there are no pending tasks.
Order projects alphabetically. Within each project, order tasks by completion time.

### Step 3: Write to Journal
Read the journal entry at Journal/{year}/current/{date}.md.

Find the `## Completed Tasks` section. Write the organized content between `## Completed Tasks` and the next `##` section.

**Idempotency check**: If the Completed Tasks section already has content beyond the HTML comment, ask Mason whether to overwrite or skip. Do NOT silently overwrite.

Format:

```
## Completed Tasks
<!-- Auto-populated from Todoist via /productivity:eod -->

**Summary:** {N} completed | {M} still pending

#### [[ProjectName]]
- [x] Task content
- [x] Another task

#### ProjectName
- [x] Task without vault match

#### ⏳ Still Pending
- [ ] Task content — *[[ProjectName]]*
- [ ] Another task — *ProjectName*
```

Rules:
- Use `[x]` for completed, `[ ]` for pending.
- Project headers for completed tasks use `####` with the project name (cross-linked if vault file exists).
- Pending tasks are grouped under a single `#### ⏳ Still Pending` header with project name in italics after an em dash.
- The summary line shows total completed and total pending counts.
- If "Inbox" is the project name, use "Inbox" as-is (no cross-link).

### Step 4: Summary
Tell Mason:
- How many tasks were synced (completed + pending)
- Which projects had completed tasks
- Any issues encountered

Keep it to 2-3 lines.
