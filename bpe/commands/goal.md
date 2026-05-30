---
description: Autonomous-mode BPE run via /goal. Modes — step (default, safest) | section <name> | full. Pre-flights branch safety (refuses on main), detects the project test runner, builds a verifiable completion condition, and emits two paste-blocks (orchestrator instructions + /goal activation) that dispatch the bpe:step-executor subagent per todo.md item. Requires Claude Code v2.1.139+; put your session in auto mode before pasting for unattended execution.
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

## Step 3: Emit Two Blocks (Orchestrator + Goal)

The `/goal` command has a documented 4000-character cap on the condition argument. The orchestrator instructions are ~4400 chars on their own, so they CANNOT ride along inside a single `/goal` call. Emit TWO separate fenced blocks for the user to paste in sequence:

1. **Block 1 (orchestrator instructions)** — pasted first as a normal message. Tells the parent session what to do, then waits for `/goal` activation.
2. **Block 2 (`/goal` activation)** — pasted second as a slash command. Sets the short condition and kicks off autonomous cycling.

Print Block 1 first inside its own fenced code block, then Block 2 inside a separate fenced block.

**Block 1 — paste this first as a normal message:**

````
You are about to be put into a /goal-driven autonomous BPE run. Read these orchestrator instructions and acknowledge briefly, but WAIT — do not start any work until I send the /goal command in my next message.

You cannot invoke slash commands from inside an autonomous /goal loop — there is no user-input channel. When a step below tells you to "execute the procedure in commands/X.md", that means: Read the markdown file at that path with the Read tool, then execute its numbered procedure inline as your own work. Do NOT try to type `/bpe:session-summary` (or any other slash command) — it will not fire and you may exit the loop.

Until the goal condition is met, repeat this micro-loop:

1. Run `git rev-parse --abbrev-ref HEAD` and echo the output. Abort if the branch is `main` or `master`.
2. Read the first unchecked `- [ ]` item in todo.md. If none remain, run the final wrap-up (step 6) and stop.
3. Dispatch `Agent(subagent_type="bpe:step-executor")` with this prompt: "Execute the next unchecked item in todo.md. Follow your system prompt's procedure exactly — that includes reading commands/execute-plan.md, commands/session-summary.md, and commands/commit-message.md and executing their procedures inline rather than trying to invoke them as slash commands. You own the full commit ritual: per-step session summary (mandatory, stage it), commit-message, commit, and push. The orchestrator does NOT commit on your behalf. Return the structured report only after pushing successfully — otherwise return a Failure: block."
4. Parse the report. If it is a `Failure:` block, echo the failure verbatim and stop — the user will intervene. Do NOT attempt to commit or push yourself; the subagent owns that work and any retry should also be the subagent's (or the user's) call.
5. After a successful report, echo `git log -1 --format="%h %s"` and `git status --short` in user-facing text so the /goal evaluator can verify. Then loop to step 2.
6. Final wrap-up (only when no unchecked items remain): run `<test-cmd>` once more and echo the result; read `${CLAUDE_PLUGIN_ROOT}/commands/session-summary.md` and execute its procedure inline to capture the overall goal-driven session (do NOT type `/bpe:session-summary`); echo `git log <branch>..HEAD` to show what landed.

Mode: <mode>. Test command: <test-cmd>. Branch: <branch>.

Hard rules for you, the orchestrator:
- NEVER run `/clear` or `/compact`. Both kill the active /goal session. You don't need them — the subagent architecture keeps your context tiny (one report per step).
- If 50 successful dispatches have completed and the goal is still unmet, stop with an explicit "dispatch cap reached" message — something is probably looping.
- If you notice your own context climbing unexpectedly (a subagent returned far more than the 200-word report cap, or you've been forced to echo huge git diffs), stop and tell the user to re-fire with a tighter scope. Do not attempt to compact your way out.

Escape hatch: the user can type `/goal clear` at any time to stop the autonomous loop. Subagent reports remain in the transcript for later review.

Reply with: "Orchestrator instructions received. Standing by for /goal command."
````

**Block 2 — paste this second to activate the loop:**

````
/goal <condition from step 2>
````

After both blocks, print this single-line reminder:

```
Put your session into auto mode before pasting Block 1, so subagent tool calls don't prompt you mid-loop.
```

## Step 4: Do NOT Run It Yourself

This command builds and emits the autonomous prompt — it does not execute it. The user must paste the emitted `/goal …` block themselves. If the user asks you to "just run it," remind them they need to paste it so the `/goal` evaluator owns the session loop.
