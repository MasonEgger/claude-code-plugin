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

`/goal` enforces a hard **4000-character cap** on its argument. STRICTLY enforce it: after substituting every placeholder, count the characters of the assembled block — the `/goal` line through the final `Mode:` line, i.e. everything inside the fenced block that gets pasted (the tilde rulers below are display-only and do NOT count). If the count exceeds 4000, trim the orchestrator prose — NEVER the safety contracts, the per-turn steps, or the verification rules — and recount. NEVER emit a block over 4000 characters. The user pastes ONE block. The condition leads (the evaluator focuses on its AND clauses); the orchestrator playbook follows in the same message.

Print the `/goal` block inside one fenced code block so it can be copied in one motion, framed by a tilde ruler above and below. Substitute `<condition>`, `<mode>`, `<test-cmd>`, and `<branch>` from steps 1–2.

First print this ruler line **exactly as written**, wrapped in single backticks — it is inline code, so the markdown renderer prints the 80 tildes literally instead of treating the line as a tilde code-fence (a bare `~~~~…` line at column 0 gets swallowed as fence syntax):

`~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

Then the `/goal` block:

````
/goal <condition from step 2>

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
````

Then print the same ruler line again (inline code, exactly as written):

`~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

The tilde rulers are display-only frames so the `/goal` block is easy to spot in the transcript — they are NOT part of the `/goal` command. Keep them OUTSIDE the fenced block; the user copies only what's inside the fence.

After the block, print this single-line reminder:

```
Put your session into auto mode before pasting, so subagent tool calls don't prompt you mid-loop.
```

## Step 4: Do NOT Run It Yourself

This command builds and emits the autonomous prompt — it does not execute it. The user must paste the emitted `/goal …` block themselves. If the user asks you to "just run it," remind them they need to paste it so the `/goal` evaluator owns the session loop.
