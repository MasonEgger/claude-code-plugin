# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- `/goal`'s condition argument is capped at 4000 chars. If an autonomous-mode wrapper packages orchestrator instructions inline (`/goal <condition>\n\n<orchestrator block>`), the whole multi-line block becomes the condition and blows the cap. Split into two pastes: orchestrator instructions as a normal message first (ends with "Standing by for /goal command"), then `/goal <short condition>` as a separate slash invocation. Design around documented caps from day one. (2026-05-30)
- Verify any slash command exists locally (skills list, `/help`, dispatch test) before baking it into emitted user-facing instructions. Single-source research output (e.g. `claude-code-guide` subagent) can fabricate plausible commands — `/auto` doesn't exist in Claude Code (the actual auto-accept toggle is `Shift+Tab`), but a research call returned it as authoritative and it shipped in three sites of a v0.4.x release. Treat research output as a hypothesis when it controls user-facing strings. (2026-05-30)
- Default to **enumerated stage lists** in any procedure that asks a model to `git add` selectively in an autonomous context. "Stage the files this step touched" gets read differently by different models — and a missing file (like a mandatory `.ai-sessions/session-*.md`) silently fails the commit when a pre-commit hook enforces "one summary per commit." Spell it out: `(a)` code/test files, `(b)` `todo.md`, `(c)` the new session summary, `(d)` `lessons.md` if appended. (2026-05-30)
- For autonomous `/goal` runs, keep the commit ritual (per-step session summary + commit message + commit + push) **in the subagent**, not the orchestrator. Moving it to the orchestrator inflates parent context ~10x per step (reading `session-summary.md` + `commit-message.md` + generating their outputs in the parent each iteration), which defeats the sub-agent-per-step architecture and pushes a 100-step run toward compaction. The subagent's contract must be hardened — "returning a report without having committed is a `Failure:`" — so the model can't plausibly skip it. (2026-05-30)
- Inside an autonomous `/goal` loop (parent session) or any subagent dispatch, slash commands cannot be invoked — there is no user-input channel. The model's natural "I'll run `/bpe:session-summary` now" silently fails and the loop exits without converging. Procedures intended for autonomous or subagent contexts must say "Read the command file with the Read tool, then execute its procedure inline," not "follow /bpe:X" — which is ambiguous and the model interprets as a slash-command call. (2026-05-29)
- The `/goal` evaluator sees only the parent transcript — not subagent tool calls. When designing autonomous loops with subagents, every fact needed to verify the goal condition (test output, git status, todo.md delta, commit SHA) must be echoed in user-facing text by either the subagent's final report or the parent orchestrator's verification calls. (2026-05-24)
- Plugin subagents inherit auto-mode from the parent session — `permissionMode` in plugin agent frontmatter is explicitly IGNORED. There is no per-agent way to enable auto mode. Tell users to put their parent session in auto mode (the exact mechanism is client-specific — TUI users toggle it via keyboard shortcut, not a slash command; `/auto` does not exist despite what some research sources claim). The classifier auto-pauses after 3 consecutive or 20 total blocked tool calls, so a runaway loop can't silently spam destructive calls. (2026-05-24, corrected 2026-05-30)
- Subagents CAN invoke the `Skill` tool at runtime (empirically verified, undocumented). `Skill(skill="plugin:name")` works with the fully-qualified form; bare-name form not yet tested. Skill body arrives as an injected human-role message in the subagent's context — treat as binding instructions for the remainder of that subagent turn. (2026-05-24)
- `/goal` is cleared by `/clear`; auto-compaction behavior with `/goal` is undocumented. Architect around it via sub-agent isolation: one subagent dispatch per step, fresh context each time, parent context grows ~500 tokens per step (50k for 100 steps), compaction never triggered in normal operation. Don't try to fight compaction with /compact or /clear inside an active goal. (2026-05-24)
- When testing undocumented features empirically via subagents, have the subagent write evidence to a verifiable file (e.g. `/tmp/test/result.txt`) — do not trust the subagent's spoken summary alone. Read the file back yourself to confirm it contains real tool output, not hallucination. (2026-05-24)
<!--
Category sections live below. Create each one only when at least one
lesson belongs to it. Use the most specific applicable category.
Common starting points: Python, Testing, Git, Tooling, Architecture,
Workflow, Debugging. Other valid examples: Infrastructure,
Documentation, Performance, Security, DevOps, Plugin Development.
Omit categories with zero entries.
-->

## Workflow

- When edits happen outside the user's CWD (e.g. a sibling repo), state the absolute path of the parent repo on every file change — not just once. (2026-05-24)
- Don't bulk-apply a user-articulated rule before confirming target scope; misrouted prompts and ambiguous "the skill" references are common. (2026-05-24)
- Bucket subagent audit findings into 3-4 user-facing decision groups for one multi-select AskUserQuestion rather than flat per-item questions. (2026-05-24)
- Before bumping a plugin version, check the live committed version with `git show HEAD:<manifest>` — one uncommitted working set bumps once, not per-file. (2026-05-24)
- When testing undocumented features via subagents, have the subagent write evidence to a file you can Read back — don't trust the spoken summary alone. (2026-05-24)

## Plugin Development

- For consistent skill/command output, lift invariants (CSS, schema, structure) into version-controlled assets; let the LLM fill in content, not invent layout. (2026-05-24)
- Inline `<style>` injection from the server keeps a served HTML page self-contained without forcing the LLM to inline CSS or maintain a separate static route. (2026-05-24)
- A two-level TOC (group divider + nested units) should be pinned as a hard rule in the contract; CSS rarely styles deeper, and the gap isn't visible until needed. (2026-05-24)
- Plugin subagents inherit auto-mode from the parent — `permissionMode` is ignored in plugin agent frontmatter. Put the parent session in auto mode via the client's mechanism (TUI: keyboard shortcut, NOT a slash command; `/auto` does not exist). Classifier auto-pauses after 3 consecutive or 20 total blocks. (2026-05-24, corrected 2026-05-30)
- `/goal`'s condition is capped at 4000 chars. Autonomous-mode wrappers must split orchestrator instructions (normal message) from `/goal <condition>` (separate slash invocation) — packaging them inline blows the cap. (2026-05-30)
- Verify slash commands exist locally before baking them into user-facing emitted strings — single-source research output can fabricate. Cross-check against the skills list or `/help`. (2026-05-30)
- Subagents can invoke the `Skill` tool at runtime (undocumented but empirically verified). Use fully-qualified `plugin:name` form. Skill body arrives as injected human-role message. (2026-05-24)
- The `/goal` evaluator sees only the parent transcript — subagent tool calls are invisible. Subagent reports must surface every verification fact (test output, git status, commit SHA) in user-facing text. (2026-05-24)
- `/goal` is cleared by `/clear`; auto-compaction with `/goal` is undocumented. Sub-agent-per-step architecture sidesteps both: fresh context per dispatch, parent stays tiny, compaction never triggers. (2026-05-24)
- Triggering rules for skills (auto-fire, be "pushy") do not apply to slash commands (user-typed, slash menu) or plugin agents (explicit dispatch). Commands and agents need clarity and disambiguation, not push. (2026-05-24)
- Inside an autonomous `/goal` loop or any subagent dispatch, slash commands cannot be invoked — there is no user-input channel. Procedures must say "Read the command file and execute its procedure inline," not "follow /bpe:X." Otherwise the model attempts the slash invocation, it silently fails, and the loop exits. (2026-05-29)
- Default to enumerated stage lists (`(a)` code, `(b)` `todo.md`, `(c)` session summary, `(d)` lessons.md if appended) in any autonomous-mode `git add` step. "Files this step touched" is ambiguous and the missing file silently fails the commit under pre-commit hook enforcement. (2026-05-30)
- Keep the autonomous-mode commit ritual (session-summary + commit-message + commit + push) in the subagent, not the orchestrator. Moving it to the orchestrator inflates parent context ~10x per step and defeats the sub-agent-per-step architecture. Harden the subagent's contract — "returning without committing is a `Failure:`" — so the model can't plausibly skip it. (2026-05-30)

## Tooling

- `chrome-headless-shell --virtual-time-budget=Nms` deterministically advances JS timers during a screenshot — use it to capture transient UI states and async-rendered content. (2026-05-24)
- For Python f-strings embedding JS object literals, double every JS brace `{{ }}` to escape. (2026-05-24)

## Design

- Use color severity gradients (green → amber → violet → red) for ordered choices; reserve discrete-category palettes for unordered ones. (2026-05-24)
- WCAG 1.4.1 status indicators: always color + text label + glyph/shape, not just color + label. (2026-05-24)
