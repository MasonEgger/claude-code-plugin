---
description: "End-of-day brain dump — syncs Todoist tasks, processes voice transcript, and routes info across the Obsidian vault"
argument-hint: "[MM-DD-YYYY]"
---

## End of Day Brain Dump — Voice-First Journal & Vault Router

You are processing Mason's end-of-day voice transcript and routing information across his Obsidian vault.

### Required Checks
You MUST perform these checks and they must ALL be true before you proceed:

- Check to see if the directory you are working in is an Obsidian Vault. If it isn't, tell the user this command is only for use in an Obsidian Vault and do NO MORE WORK.
- Calculate the year using `date +%Y` and save as {year}. Calculate today's date using `date +%m-%d-%Y` and save as {today}.
- If $ARGUMENTS is provided, use that as {date}. Otherwise, use {today} as {date}. This allows the user to run `/productivity:eod` for today or `/productivity:eod 03-15-2026` for a specific date.
- Check to see if there is a Journal entry in @Journal/{year}/current/{date}.md. If there isn't, tell the user to create the journal entry for that day and do NO MORE WORK.
- Look for a @transcript.md file. If it doesn't exist, tell the user to create a transcript.md file with their voice recording transcript and do NO MORE WORK.

### Step 1: Sync Todoist Tasks (Optional)
Before processing the transcript, sync today's Todoist tasks into the journal.

- Check if `todo` CLI is available by running `todo project list --json --limit 1`.
- If available, follow the steps in /productivity:todoist-sync for {date}: fetch completed and pending tasks, organize by project, and write to the Completed Tasks section.
- If `todo` is not available or fails, skip this step silently and note in the final summary that Todoist sync was skipped.
- This runs BEFORE transcript processing so the blog narrative can reference completed tasks.

### Step 2: Read Context (do this even if Step 1 was skipped)
- Read @CLAUDE.md for Mason's writing voice and vault conventions.
- Read the journal entry at Journal/{year}/current/{date}.md
- Read @transcript.md — this is a voice transcript of Mason talking about his day.
- Scan the vault structure so you understand what cross-links are available.

### Step 3: Process the Transcript
Parse the transcript and extract the following categories of information:

1. **Narrative content** — what happened today, how Mason feels about it, decisions made, context for future Mason. This becomes the Blog section.
2. **People mentioned** — anyone Mason talked about, met with, or interacted with. Note what was discussed or relevant context about them.
3. **Customer/work updates** — any customer meetings, outcomes, action items, or account changes.
4. **Ideas** — app ideas, blog post ideas, business ideas, project ideas. Anything forward-looking and creative.
5. **Highlights and lowlights** — things that went well or poorly. Often expressed through tone (excitement = highlight, frustration = lowlight).
6. **Learning** — anything Mason explicitly says he learned or researched.

### Step 4: Write the Journal Entry
Write the cleaned-up narrative to the **Blog** section of {date}.md.

Rules for the Blog section (same as transcript-2-journal):
- Mason's writing tone/voice is in @CLAUDE.md. Match it. Clean up filler words and make it coherent, but keep his voice.
- Remove conversational filler ("um", "uh", "like", "you know") but preserve his natural directness and casual tone.
- Put things in chronological order. If he says "Oh before that we did X", rewrite so it flows organically.
- Use sub-headers (###) for different sections: Personal, Work, PyTexas, or whatever categories fit the content.
- Add Obsidian `[[cross-links]]` to people, places, projects, and concepts that exist or should exist in the vault.
  - Before adding a cross link, check if a matching file already exists and use that exact link.
  - If no file exists but it's the kind of thing Mason tracks (people, places, events, projects), create the cross-link anyway.
- Write to Highlights/Lowlights section based on tone and content.

Do **NOT** write to Ideas & Insights or Learning sections directly. Instead, tell Mason what you would put there and let him decide.

### Step 5: Route to Person Files
For each person mentioned in the transcript:

1. Check if a person file already exists anywhere in Reference/People/ (search by name).
2. **If the file exists**: Append a brief interaction note under the "## Notes" or similar section with today's date and context. Don't overwrite existing content.
3. **If no file exists but Mason had a meaningful interaction**: Create a new person file in the appropriate subfolder using the Person template. Fill in what you know from the transcript (organization, role, how they met, context). Use these subfolder rules:
   - Temporal co-workers → `Reference/People/Co-Workers/Temporal/`
   - Community/Python people → `Reference/People/Community/Python/` or `Reference/People/Community/PyTexas/`
   - Customers → `Reference/People/Customers/Temporal/`
   - Friends → `Reference/People/Friends/`
   - If unclear, use `Reference/People/`
4. **If the person is just casually mentioned** (not a meaningful interaction), just use the `[[cross-link]]` in the journal — don't create or update a person file.

### Step 6: Route to Customer Notes
If Mason discussed a customer meeting or customer-related work:

1. Find the customer company file in `Active/Work/Temporal/Customers/`.
2. Append a meeting history entry with today's date and a summary of what was discussed, decisions made, and action items.
3. If a customer contact was mentioned, check/update their file in `Reference/People/Customers/Temporal/` too.

### Step 7: Create Idea Files
If Mason mentioned app ideas, blog post ideas, business ideas, or project ideas:

1. Tell Mason about each idea you extracted and ask if he wants them captured.
2. For approved ideas, create a note in `Inbox/` with the idea title and any context from the transcript.
   - These are intentional captures, not junk. They should have enough context to be useful later.

### Step 8: Summary
After all updates, give Mason a brief summary:
- What was written to the journal
- Which person files were created or updated (with links)
- Which customer files were updated
- Any ideas extracted (pending his approval)
- Suggestions for Ideas & Insights or Learning sections

Keep the summary concise. Mason is tired at EOD — just the facts.
