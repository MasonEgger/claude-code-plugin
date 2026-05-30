# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- Inside an autonomous `/goal` loop (parent session) or any subagent dispatch, slash commands cannot be invoked — there is no user-input channel. The model's natural "I'll run `/bpe:session-summary` now" silently fails and the loop exits without converging. Procedures intended for autonomous or subagent contexts must say "Read the command file with the Read tool, then execute its procedure inline," not "follow /bpe:X" — which is ambiguous and the model interprets as a slash-command call. (2026-05-29)
- The `/goal` evaluator sees only the parent transcript — not subagent tool calls. When designing autonomous loops with subagents, every fact needed to verify the goal condition (test output, git status, todo.md delta, commit SHA) must be echoed in user-facing text by either the subagent's final report or the parent orchestrator's verification calls. (2026-05-24)
- Plugin subagents inherit auto-mode from the parent session — `permissionMode` in plugin agent frontmatter is explicitly IGNORED. There is no per-agent way to enable auto mode. Tell users to run `/auto` first in the parent session. The classifier auto-pauses after 3 consecutive or 20 total blocked tool calls, so a runaway loop can't silently spam destructive calls. (2026-05-24)
- Subagents CAN invoke the `Skill` tool at runtime (empirically verified, undocumented). `Skill(skill="plugin:name")` works with the fully-qualified form; bare-name form not yet tested. Skill body arrives as an injected human-role message in the subagent's context — treat as binding instructions for the remainder of that subagent turn. (2026-05-24)
- `/goal` is cleared by `/clear`; auto-compaction behavior with `/goal` is undocumented. Architect around it via sub-agent isolation: one subagent dispatch per step, fresh context each time, parent context grows ~500 tokens per step (50k for 100 steps), compaction never triggered in normal operation. Don't try to fight compaction with /compact or /clear inside an active goal. (2026-05-24)
- When testing undocumented features empirically via subagents, have the subagent write evidence to a verifiable file (e.g. `/tmp/test/result.txt`) — do not trust the subagent's spoken summary alone. Read the file back yourself to confirm it contains real tool output, not hallucination. (2026-05-24)
- The skill-creator skill's "be pushy about triggering" rule applies to auto-fired skills only. For slash commands (user-typed, shown in menu) and explicitly-dispatched plugin agents (`subagent_type: ...`), the rules shift to clarity, what+when, and disambiguation. Don't write commands or agents with skill-style triggering rhetoric. (2026-05-24)
- Before bumping a plugin version, check the live committed version with `git show HEAD:<manifest>`. One uncommitted working set should bump once, not per-file or per-feature. Easy to double-bump when adding multiple components in the same session. (2026-05-24)
- When edits happen outside the user's CWD (e.g. a sibling repo), state the absolute path of the parent repo on every file change — not just once. Quiet single mentions get lost in long sessions and the user ends up running `git status` in the wrong dir and concluding nothing happened. (2026-05-24)
- Don't bulk-apply a user-articulated rule before confirming target scope. If the user says "we should not X in the skill" without naming a skill, ask which one — the prompt may have been misrouted from another session, or apply only to a specific artifact. Building memory files, rule files, and audit subagents before clarification wastes ~thousands of tokens and gets reverted. (2026-05-24)
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
- Plugin subagents inherit auto-mode from the parent — `permissionMode` is ignored in plugin agent frontmatter. Run `/auto` in the parent session; classifier auto-pauses after 3 consecutive or 20 total blocks. (2026-05-24)
- Subagents can invoke the `Skill` tool at runtime (undocumented but empirically verified). Use fully-qualified `plugin:name` form. Skill body arrives as injected human-role message. (2026-05-24)
- The `/goal` evaluator sees only the parent transcript — subagent tool calls are invisible. Subagent reports must surface every verification fact (test output, git status, commit SHA) in user-facing text. (2026-05-24)
- `/goal` is cleared by `/clear`; auto-compaction with `/goal` is undocumented. Sub-agent-per-step architecture sidesteps both: fresh context per dispatch, parent stays tiny, compaction never triggers. (2026-05-24)
- Triggering rules for skills (auto-fire, be "pushy") do not apply to slash commands (user-typed, slash menu) or plugin agents (explicit dispatch). Commands and agents need clarity and disambiguation, not push. (2026-05-24)
- Inside an autonomous `/goal` loop or any subagent dispatch, slash commands cannot be invoked — there is no user-input channel. Procedures must say "Read the command file and execute its procedure inline," not "follow /bpe:X." Otherwise the model attempts the slash invocation, it silently fails, and the loop exits. (2026-05-29)

## Tooling

- `chrome-headless-shell --virtual-time-budget=Nms` deterministically advances JS timers during a screenshot — use it to capture transient UI states and async-rendered content. (2026-05-24)
- For Python f-strings embedding JS object literals, double every JS brace `{{ }}` to escape. (2026-05-24)

## Design

- Use color severity gradients (green → amber → violet → red) for ordered choices; reserve discrete-category palettes for unordered ones. (2026-05-24)
- WCAG 1.4.1 status indicators: always color + text label + glyph/shape, not just color + label. (2026-05-24)
