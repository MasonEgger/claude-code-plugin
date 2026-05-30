---
description: Autonomous-mode BPE run via /goal. Modes — step (default, safest) | section <name> | full. Pre-flights branch safety (refuses on main), detects the project test runner, builds a verifiable completion condition, and emits a single copy-paste /goal block (condition + trimmed orchestrator playbook + per-commit verification) that dispatches the bpe:step-executor subagent per todo.md item. Requires Claude Code v2.1.139+; put your session in auto mode before pasting for unattended execution.
argument-hint: [step | section <name> | full]
---

# BPE Autonomous Goal

Set up a `/goal`-driven autonomous BPE run. The parent session orchestrates; each step is executed by the `bpe:step-executor` subagent (fresh context per step, no compaction risk). The parent's transcript stays tiny, and the `/goal` evaluator watches it for completion.

**Requires Claude Code v2.1.139+.** Pairs well with `/auto`. The `/goal` command itself must still be run by the user — slash commands cannot invoke other slash commands programmatically, so this command builds the full `/goal` invocation and prints it in a fenced block for one-keystroke copy-paste.

## Mode Routing

Parse `$ARGUMENTS`:

- `step` (or empty) — autonomous through ONE step. Safest. Default.
- `section <name>` — autonomous through one labeled section of `todo.md`. A section is a top-level Markdown heading or an explicit comment block like `<!-- section: foo -->`.
- `full` — autonomous to the end of `todo.md`. Use only when you fully trust the plan and have plenty of time / quota.

State the routed mode in user-facing text before pre-flight.

## Step 1: Pre-Flight Checks (refuse on any failure)

Run these in parallel and surface results in user-facing text:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
test -f plan.md && echo "plan: yes" || echo "plan: NO"
test -f todo.md && echo "todo: yes" || echo "todo: NO"
grep -c '^- \[ \]' todo.md 2>/dev/null || echo 0
grep -q '^commit-msg\.md$' .gitignore && echo "gitignore: ok" || echo "gitignore: MISSING commit-msg.md"
```

Then detect the test runner:

- `pyproject.toml` present → `pytest -q`
- `package.json` present → `npm test --silent`
- `Cargo.toml` present → `cargo test --quiet`
- `go.mod` present → `go test ./...`
- Otherwise → ask the user for the exact test command and use what they provide.

**Refuse and stop if any of these are true:**

- Branch is `main` or `master`. Tell the user: "Refusing to run autonomous mode on main. Create a feature branch first: `git checkout -b <branch-name>`."
- `plan.md` or `todo.md` is missing.
- Zero unchecked items in `todo.md`.
- `commit-msg.md` is not gitignored. Tell the user to add it and re-run.
- Test runner can't be detected AND the user didn't supply one.

Do NOT auto-create branches, auto-edit `.gitignore`, or auto-anything in pre-flight. These are deliberate decisions for the user.

## Step 2: Build the Goal Condition

Mode determines the condition. Substitute `<test-cmd>` with the detected runner, `<branch>` with the current branch.

**step:**
```
The next unchecked item in todo.md at the start of this run is now checked off; <test-cmd> exits 0 with no failing tests; git status --short is empty; the commit for the step is pushed to origin/<branch>.
```

**section <name>:**
```
Every item under the "<name>" section of todo.md is checked off; <test-cmd> exits 0; git status --short is empty; all commits for that section are pushed to origin/<branch>.
```

**full:**
```
Every item in todo.md is checked off; <test-cmd> exits 0 with no failing tests; git status --short is empty; all commits are pushed to origin/<branch>; .ai-sessions/lessons.md contains any new lessons captured during the run.
```

## Step 3: Emit the Combined `/goal` Block

The orchestrator instructions are trimmed to ~1500 chars so they fit alongside the ~250-char condition inside `/goal`'s 4000-character cap. The user pastes ONE block. The condition leads (the evaluator focuses on its AND clauses); the orchestrator playbook follows in the same message.

Print exactly this block inside one fenced code block so it can be copied in one motion. Substitute `<condition>`, `<mode>`, `<test-cmd>`, and `<branch>` from steps 1–2.

````
/goal <condition from step 2>

You're the orchestrator for an autonomous BPE run. Loop until the goal condition above is met.

CRITICAL CONTRACT — every commit in this loop MUST include a new `.ai-sessions/session-*.md` file. The subagent generates it; you verify it landed. Pre-commit hooks reject commits without one, and the file is how the user re-enters this work later — non-negotiable.

CRITICAL CONTRACT — each dispatch produces EXACTLY ONE commit. No follow-ups, no fixups, no amends, no `--no-verify`. If a subagent reports needing a follow-up to fix something it discovered post-commit, that's a `Failure:` — do NOT make the follow-up on its behalf, do NOT re-dispatch for cleanup. Stop the loop; the user resolves.

Per loop:

1. `git rev-parse --abbrev-ref HEAD` — abort if `main` or `master`.
2. Read the first `- [ ]` in `todo.md`. If none remain, run final wrap-up: `<test-cmd>`, then echo `git log <branch>..HEAD`, then stop.
3. Dispatch `Agent(subagent_type="bpe:step-executor")` with this prompt: "Execute the next unchecked `todo.md` item per your system prompt. CRITICAL: (a) you MUST generate a new `.ai-sessions/session-*.md` for this step and stage it in your commit, (b) you MUST regenerate `commit-msg.md` fresh — never reuse stale content from a prior commit, (c) you get EXACTLY ONE commit per dispatch — fold any fixes into the main commit before committing; once `git commit` succeeds you cannot fix anything in this dispatch. Return the structured report only after pushing successfully — otherwise return a `Failure:` block."
4. Parse the report. `Failure:` → echo verbatim, stop.
5. VERIFY: run `git show --stat --name-only HEAD | grep -E '^\.ai-sessions/session-.*\.md$'`. If grep returns nothing, the subagent's commit is missing its session summary — echo "BPE rule violation: commit missing .ai-sessions/session-*.md" and stop the loop.
6. Echo `git log -1 --format="%h %s"` and `git status --short` in user-facing text (the /goal evaluator only sees the parent transcript). Loop to step 2.

Hard rules:
- NEVER `/clear` or `/compact` — kills the active /goal.
- NEVER commit on the subagent's behalf, even on `Failure:`.
- Stop after 50 successful dispatches with "dispatch cap reached".

Mode: <mode>. Test: <test-cmd>. Branch: <branch>.
````

After the block, print this single-line reminder:

```
Put your session into auto mode before pasting, so subagent tool calls don't prompt you mid-loop.
```

## Step 4: Do NOT Run It Yourself

This command builds and emits the autonomous prompt — it does not execute it. The user must paste the emitted `/goal …` block themselves. If the user asks you to "just run it," remind them they need to paste it so the `/goal` evaluator owns the session loop.
