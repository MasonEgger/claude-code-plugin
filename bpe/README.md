# BPE Plugin

Brainstorm-Plan-Execute development workflow with session tracking and lessons learned.

## Overview

This plugin packages the BPE loop - a structured workflow for building software with Claude Code using test-driven development. It also includes session management for tracking work history and accumulating lessons across sessions.

## Commands

| Command | Purpose |
|---|---|
| `/bpe:brainstorm` | Iterative Q&A to develop a project specification (`spec.md`) |
| `/bpe:plan` | Transform spec into implementation roadmap (`plan.md` + `todo.md`) |
| `/bpe:execute-plan` | Implement one step at a time following strict TDD |
| `/bpe:gh-issue` | Fetch a GitHub issue and route to brainstorm or plan |
| `/bpe:commit-message` | Generate a commit message explaining what was changed |
| `/bpe:session-summary` | Generate session recap and capture lessons learned |
| `/bpe:handoff` | Compact the current conversation into an ephemeral handoff document for a fresh agent |
| `/bpe:review` | Generate an HTML view of `spec.md` / `plan.md` / `todo.md` and serve it locally for visual review with annotations |
| `/bpe:apply-review` | Load saved review feedback and apply changes to the reviewed artifact |
| `/bpe:lessons` | View, search, and manage accumulated lessons |
| `/bpe:wtf-wid` | WTF was I doing? Tight, fits-on-screen recap of the current session for fast re-entry |
| `/bpe:goal` | Wrap the BPE loop in a `/goal`-driven autonomous run. Pre-flights safety, writes the `/goal` argument to `goal.md` — run with `/goal @goal.md` |

As of 0.6.0, BPE commands are implemented as skills.
Invocation is unchanged: each `/bpe:<name>` above works exactly as before.
The underlying file layout moved from `commands/<name>.md` to `skills/<name>/SKILL.md`.

## The BPE Loop

1. **Brainstorm** - Develop a thorough specification through iterative dialogue
2. **Plan** - Break the spec into right-sized, TDD-structured implementation steps
3. **Execute** - Implement steps one at a time, following the plan exactly
4. **Review & Record** - Summarize the session and capture lessons for next time

## Session Management

Session artifacts live in `.ai-sessions/` at the project root:

- **Session summaries** - Individual markdown files capturing what happened each session
- **lessons.md** - Accumulated cross-session learnings in a hybrid format (recent + categorized)

The execute-plan command automatically reads the most recent session summary for continuity. Format specs and workflow rules live in `references/session-management.md`, which the relevant commands read directly. There is intentionally no Skill registered for this — invocation is always via an explicit slash command.

## Autonomous Mode

Requires Claude Code v2.1.139+.

`/bpe:goal` wraps the BPE loop in Claude Code's `/goal` autonomous-execution primitive. The parent session orchestrates; each step is delegated to the `bpe:step-executor` subagent (fresh context per dispatch, no compaction risk). The parent's transcript stays small, the subagent does the work, and `/goal`'s evaluator watches the parent transcript to decide when the run is complete.

```mermaid
flowchart TD
    A["/bpe:goal [full|section|step]"] --> B["Pre-flight checks<br/>(refuses on main, missing files)"]
    B --> C["Writes /goal argument to goal.md<br/>(condition + trimmed orchestrator playbook)"]
    C --> D["User runs: /goal @goal.md"]
    D --> E["Parent loop: dispatch one step at a time"]
    E --> F["Agent(bpe:step-executor)<br/>fresh context, runs TDD, commits, pushes"]
    F -->|"returns ≤200-word report"| E
    E --> G{"/goal evaluator:<br/>condition met?"}
    G -->|no| E
    G -->|yes| H["Final session-summary + lessons<br/>(parent runs once)"]
```

Modes:

- `full` (default) — converges only when every item in `todo.md` is checked off and tests pass. The main use case.
- `section <name>` — converges after every item in a labeled section is checked off.
- `step` — converges after one item. Rarely useful; for a single interactive step, use `/bpe:execute-plan` instead. `step` is here for the case where you want the autonomous-mode contracts (SHA verification, session-summary-per-commit, push) on one item.

Hard guarantees:

- **Refuses to run on `main`/`master`.** Create a feature branch first.
- The subagent commits with `git commit -S -F commit-msg.md`, then `git push`. If push fails, it stops cleanly with a `Failure:` report.
- Each subagent dispatch is a fresh context — no compaction, no /clear required.
- `/goal clear` is the escape hatch. Subagent reports remain in the transcript for review.

`/bpe:goal` writes the assembled `/goal` argument to `goal.md` at the repo root: the condition followed by a trimmed orchestrator playbook, together under `/goal`'s 4000-character cap. You then run `/goal @goal.md` — Claude Code's `@` expansion inlines the file contents as the `/goal` argument, so no copy-paste is needed. The condition leads (the evaluator focuses on its AND clauses); the playbook follows in the same message and tells the parent session how to drive the loop. `goal.md` is intended to be gitignored — `/bpe:goal` refuses to run if it isn't. The file MUST NOT start with `/goal ` since `@goal.md` already supplies the argument; the command writes the body only.

Three hard contracts the orchestrator enforces:

- **SEQUENTIAL DISPATCHES ONLY.** Exactly one `Agent(subagent_type="bpe:step-executor")` per turn. The Agent tool's standard guidance encourages parallel dispatches for independent work; that guidance does NOT apply here because todo.md items share state (todo.md checkmarks, git state, the test suite). Parallel dispatches corrupt all three. The orchestrator block emitted by `/bpe:goal` explicitly forbids parallel dispatches; the subagent has a defense-in-depth pre-flight that aborts on a non-empty `git status --short` (which a concurrent subagent would leave).
- **Every commit in the loop must include a new `.ai-sessions/session-*.md`.** After each subagent dispatch, the orchestrator parses the `Commit:` SHA from the report and verifies that exact commit (not `HEAD`, which is unreliable if anything raced) contains a session summary. Stops on miss.
- **Exactly one commit per dispatch.** No follow-ups, no fixups, no amends, no `--no-verify`. If a subagent discovers something needs fixing after its commit lands, that's a `Failure:` — the orchestrator does NOT make the follow-up.

Put your session into auto mode before pasting so subagent tool calls don't prompt you mid-loop. The exact mechanism depends on your client (TUI users typically toggle this with a keyboard shortcut).

## Installation

Install via the marketplace registered in this repo:

```
/plugin marketplace add MasonEgger/claude-code-plugin
/plugin install bpe@mmegger-plugins
```

See the [top-level README](../README.md) for the full plugin list and marketplace details.

## Reference

- [How I Actually Use the Damn Thing](https://mason.dev/blog/how-i-actually-use-the-damn-thing/) - The BPE loop explained
- [What I Found Actually Works](https://mason.dev/blog/what-i-found-actually-works-with-ai/) - Prompts as code philosophy
- [Skills, Plugins, and MCP Oh My](https://mason.dev/blog/skills-plugins-and-mcp-oh-my/) - Claude Code customization approach
