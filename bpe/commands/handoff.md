---
description: Compact the current conversation into a handoff document for another agent to pick up
argument-hint: What will the next session be used for?
---

# Handoff Command

Write a handoff document so a fresh agent can continue the current work without starting from scratch. The handoff is ephemeral and forward-looking — it is not a session summary. For durable, backwards-looking session records, use `/bpe:session-summary` instead.

## Step 1: Generate the Path

Produce an ephemeral path with `mktemp`:

```bash
mktemp -t handoff-XXXXXX.md
```

Read the file (it will be empty) before writing to it.

## Step 2: Tailor to the Next Session's Focus

If the user passed arguments, treat them as a description of what the next session will focus on. Tailor the handoff toward that focus — emphasize the threads of the current conversation that matter for the stated next step, and elide the rest.

If no argument was passed, write a general-purpose handoff covering the live state of the conversation.

## Step 3: Write the Handoff

Include these sections, in this order:

### Current State
- What is done, what is in progress, and what is queued next.
- Branch name, last commit SHA, and whether work is pushed.
- Files in flight — paths to anything created or modified this session, especially uncommitted work.

### Open Decisions and Blockers
- Anything awaiting input from the user or another agent.
- Trade-offs the current session deferred — what was chosen, what was rejected, and why.

### Suggested Skills for the Next Session
- List the specific skills the next agent should invoke before starting work, e.g. `python:python`, `temporal:temporal-developer`, `bpe:session-management`. The current session knows which skills mattered; the next session benefits from the hint.
- Note any project-stack-specific skill that proved especially useful and why.

### Pointers, Not Content
- Reference PRDs, plans, ADRs by path.
- Reference issues and PRs by URL or `gh` invocation.
- Reference commits and diffs by SHA, branch range, or `git log`/`git diff` invocation.
- Reference existing session summaries in `.ai-sessions/` by filename.
- Reference `.ai-sessions/lessons.md` when a relevant cross-session lesson applies — by filename plus the category heading or quoted lesson, not by restating the lesson body.

## Anti-Duplication Rule

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs, prior session summaries). Reference them by path or URL instead. The handoff is a pointer index, not a content store. If a fact lives somewhere durable, link to it; only restate things the next session cannot trivially recover.

## Step 4: Confirm

After writing the handoff, display:

- The full path to the handoff file.
- A one-paragraph summary of what the document covers and the assumed next-session focus.

The next session can be primed by reading the file (e.g. `Read /tmp/handoff-XXXXXX.md`).
