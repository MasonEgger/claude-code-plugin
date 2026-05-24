# Lessons Learned

## Recent
<!-- 10 most recent lessons, newest first -->
- When edits happen outside the user's CWD (e.g. a sibling repo), state the absolute path of the parent repo on every file change — not just once. Quiet single mentions get lost in long sessions and the user ends up running `git status` in the wrong dir and concluding nothing happened. (2026-05-24)
- Don't bulk-apply a user-articulated rule before confirming target scope. If the user says "we should not X in the skill" without naming a skill, ask which one — the prompt may have been misrouted from another session, or apply only to a specific artifact. Building memory files, rule files, and audit subagents before clarification wastes ~thousands of tokens and gets reverted. (2026-05-24)
- `chrome-headless-shell --virtual-time-budget=Nms` advances setTimeout/setInterval clocks deterministically during a screenshot, so transient UI states (warning labels that reset after a timeout, async-rendered Mermaid diagrams, scroll-spy-triggered classes) can be captured at exact moments without race conditions. Pair with `--no-sandbox --disable-gpu` on Linux. (2026-05-24)
- For Python f-strings that embed JavaScript object/function-body literals, double every JS brace `{{ }}` to escape. Tedious but works; the alternative (template string concat) is uglier. (2026-05-24)
- A two-level table-of-contents (group heading divider + nested decision units) collapses to "exactly two levels" — pin that as a hard rule in the contract because the CSS doesn't style `ol ol ol`, and future contributors won't notice the styling gap until they need it. (2026-05-24)
- Decision-color severity gradients (green → amber → violet → red) carry ordering information that discrete category colors don't. When designing a 3-or-more-option choice, pick a gradient first and use it; if a new option appears later, the gradient is the right place to slot it. (2026-05-24)
- For sub-agent audit workflows: bucket findings into 3-4 user-facing decision groups (accept/reject as a batch) rather than flat per-item questions. One multi-select AskUserQuestion handles 13 findings in one round; flat questions cause fatigue and selection errors. (2026-05-24)
- When a skill should produce consistent output, lift invariants (CSS, schema, structure) into version-controlled assets and let the LLM fill in content. "Freehand the layout from prose guidance" reliably drifts; "fill in this skeleton" doesn't. (2026-05-24)
- WCAG 1.4.1 ("not by color alone") for status indicators: always pair color with both a text label AND a glyph/shape change. Color + label alone passes a strict reading, but color + label + glyph (✓ ✎ ↪ ✕) is far more scannable and survives colorblind users + grayscale renders. (2026-05-24)
- Inline `<style>` injection (server reads CSS file, wraps in `<style>` tag, replaces `</head>`) keeps a served HTML page fully self-contained without requiring the LLM to inline the CSS itself or maintain a separate static-file route. (2026-05-24)

## Workflow

- When edits happen outside the user's CWD (e.g. a sibling repo), state the absolute path of the parent repo on every file change — not just once. (2026-05-24)
- Don't bulk-apply a user-articulated rule before confirming target scope; misrouted prompts and ambiguous "the skill" references are common. (2026-05-24)
- Bucket subagent audit findings into 3-4 user-facing decision groups for one multi-select AskUserQuestion rather than flat per-item questions. (2026-05-24)

## Plugin Development

- For consistent skill/command output, lift invariants (CSS, schema, structure) into version-controlled assets; let the LLM fill in content, not invent layout. (2026-05-24)
- Inline `<style>` injection from the server keeps a served HTML page self-contained without forcing the LLM to inline CSS or maintain a separate static route. (2026-05-24)
- A two-level TOC (group divider + nested units) should be pinned as a hard rule in the contract; CSS rarely styles deeper, and the gap isn't visible until needed. (2026-05-24)

## Tooling

- `chrome-headless-shell --virtual-time-budget=Nms` deterministically advances JS timers during a screenshot — use it to capture transient UI states and async-rendered content. (2026-05-24)
- For Python f-strings embedding JS object literals, double every JS brace `{{ }}` to escape. (2026-05-24)

## Design

- Use color severity gradients (green → amber → violet → red) for ordered choices; reserve discrete-category palettes for unordered ones. (2026-05-24)
- WCAG 1.4.1 status indicators: always color + text label + glyph/shape, not just color + label. (2026-05-24)
