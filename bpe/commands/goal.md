---
description: Autonomous-mode BPE run via /goal. Modes — full (default) | section <name> | step. Pre-flights branch safety (refuses on main), detects the project test runner, builds a verifiable completion condition, and writes the assembled /goal block (condition + trimmed orchestrator playbook + per-commit verification) to goal.md at the repo root for you to paste. Requires Claude Code v2.1.139+; put your session in auto mode before pasting for unattended execution.
argument-hint: [full | section <name> | step]
---

# BPE Autonomous Goal

Set up a `/goal`-driven autonomous BPE run. The parent session orchestrates; each step is executed by the `bpe:step-executor` subagent (fresh context per step, no compaction risk). The parent's transcript stays tiny, and the `/goal` evaluator watches it for completion.

**Requires Claude Code v2.1.139+.** Pairs well with `/auto`. The `/goal` command itself must still be run by the user — slash commands cannot invoke other slash commands programmatically, so this command writes the assembled `/goal` invocation to `goal.md` at the repo root and you paste it from there.

## Mode Routing

Parse `$ARGUMENTS`:

- empty or `full` — autonomous to the end of `todo.md`. **Default.** Use when you trust the plan and have time / quota.
- `section <name>` — autonomous through one labeled section of `todo.md`. A section is a top-level Markdown heading or an explicit comment block like `<!-- section: foo -->`.
- `step` — autonomous through ONE step. Rarely the right tool — for a single interactive step, `/bpe:execute-plan` is simpler. Use `step` only when you want the autonomous-mode contracts (SHA verification, session-summary-per-commit, push) on a single item without driving it yourself.

State the routed mode in user-facing text before pre-flight.

## Step 1: Pre-Flight Checks (refuse on any failure)

Run these in parallel and surface results in user-facing text:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
test -f plan.md && echo "plan: yes" || echo "plan: NO"
test -f todo.md && echo "todo: yes" || echo "todo: NO"
grep -c '^- \[ \]' todo.md 2>/dev/null || echo 0
grep -q '^commit-msg\.md$' .gitignore && echo "gitignore commit-msg.md: ok" || echo "gitignore commit-msg.md: MISSING"
grep -q '^goal\.md$' .gitignore && echo "gitignore goal.md: ok" || echo "gitignore goal.md: MISSING"
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
- `goal.md` is not gitignored. Tell the user to add it and re-run — this command writes the `/goal` block there as a working artifact.
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

## Step 3: Write the `/goal` Argument to `goal.md`

`/goal` enforces a hard **4000-character cap** on its argument. STRICTLY enforce it: after substituting every placeholder, count the characters of the assembled file content from the condition line through the final `Mode:` line. If the count exceeds 4000, trim the orchestrator prose — NEVER the safety contracts, the per-turn steps, or the verification rules — and recount. NEVER write content over 4000 characters to `goal.md`. The condition leads (the evaluator focuses on its AND clauses); the orchestrator playbook follows in the same message.

The user will run `/goal @goal.md`. Claude Code's `@` expansion inlines the file contents as the `/goal` argument, so `goal.md` must contain ONLY the argument body — **the file MUST NOT start with `/goal `** or the expansion would produce `/goal /goal …`.

Use the Write tool to overwrite `goal.md` at the repo root with exactly the content below. Substitute `<condition>`, `<mode>`, `<test-cmd>`, and `<branch>` from steps 1–2. **Plain text only — no fenced code block, no surrounding ruler lines, no leading `/goal `.** The file contents ARE the `/goal` argument:

```
<condition from step 2>

You're the orchestrator for an autonomous BPE run. Loop until the goal condition above is met.

SEQUENTIAL DISPATCHES ONLY — this is the safety model; do not optimize it away. Dispatch EXACTLY ONE `Agent(subagent_type="bpe:step-executor")` per turn. Never fire multiple or parallel dispatches. Despite the Agent tool's usual parallel-for-independent-work guidance, todo.md items are NOT independent: they share todo.md state, git state, and the test suite. Parallel dispatches race on checkmarks, land commits out of order, and defeat red-test gating (HEAD becomes whichever finished last). After one dispatch returns and you verify it, YOUR TURN ENDS — the /goal evaluator runs; if the condition isn't met, a new turn begins with one new dispatch.

EVERY commit MUST include a new `.ai-sessions/session-*.md`. The subagent generates it; you verify it landed. Pre-commit hooks reject commits without one, and it's how the user re-enters this work — non-negotiable.

EACH dispatch produces EXACTLY ONE commit — no follow-ups, fixups, amends, or `--no-verify`. If a subagent reports needing a post-commit fix, that's a `Failure:` — do NOT fix it yourself or re-dispatch for cleanup. Stop the loop; the user resolves.

Per turn (one dispatch only):
1. `git rev-parse --abbrev-ref HEAD` — abort if `main` or `master`.
2. Read the first `- [ ]` in `todo.md`. If none remain, wrap up: run `<test-cmd>`, echo `git log <branch>..HEAD`, then stop.
3. Dispatch EXACTLY ONE `Agent(subagent_type="bpe:step-executor")` with: "Execute the next unchecked todo.md item per your system prompt. CRITICAL: (a) generate a new `.ai-sessions/session-*.md` and stage it in your commit; (b) regenerate `commit-msg.md` fresh — never reuse stale content; (c) you get EXACTLY ONE commit — fold every fix in before committing; once `git commit` succeeds you cannot fix anything in this dispatch; (d) verify the test suite exits 0 IMMEDIATELY before staging — never commit a red suite. Return the structured report only after pushing successfully — otherwise return a `Failure:` block."
4. Parse the report. `Failure:` → echo verbatim, stop the loop.
5. VERIFY against the SHA in the report — NOT HEAD, which is unreliable if anything raced:
   a. Parse `Commit:` → `<sha>`.
   b. `git rev-parse HEAD` must equal `<sha>`. If not, echo `BPE rule violation: HEAD moved during verification (HEAD=<actual>, reported=<sha>)` and STOP.
   c. `git show --stat --name-only <sha> | grep -E '^\.ai-sessions/session-.*\.md$'` — if empty, echo `BPE rule violation: commit <sha> missing .ai-sessions/session-*.md` and STOP.
   d. Parse `Tests:`. If it isn't exit 0 (e.g. `pytest -q → 0 (12 passed)`), echo `BPE rule violation: commit <sha> shipped non-green tests: <tests-field>` and STOP.
6. Echo `git log -1 --format="%h %s"` and `git status --short` (the evaluator only sees the parent transcript). YOUR TURN ENDS — dispatch nothing else.

Hard rules: SEQUENTIAL only, never parallel. Never `/clear` or `/compact` (kills the active /goal). Never commit on the subagent's behalf, even on `Failure:`. Stop after 50 successful dispatches with "dispatch cap reached".

Mode: <mode>. Test: <test-cmd>. Branch: <branch>.
```

After writing the file, print this in user-facing text — concise, no fenced /goal block, no tilde rulers, no inlined contents:

```
Wrote /goal argument to goal.md (Mode: <mode>, Test: <test-cmd>, Branch: <branch>, length: <N>/4000 chars).
Run with: /goal @goal.md
Put your session into auto mode first, so subagent tool calls don't prompt you mid-loop.
```

Do NOT paste the contents of `goal.md` inline. The whole point of writing to a file is to avoid dumping a multi-thousand-character block into the transcript every invocation — and the user no longer needs to copy anything, since `@goal.md` will inline the file at invocation time.

## Step 4: Do NOT Run It Yourself

This command writes the `/goal` argument to disk — it does not execute it. The user must run `/goal @goal.md` themselves; slash commands can't invoke other slash commands programmatically. If the user asks you to "just run it," remind them they need to type `/goal @goal.md` so the `/goal` evaluator owns the session loop.
