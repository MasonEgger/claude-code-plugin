---
description: Generate an HTML view of a BPE artifact and serve it locally for visual review with annotations
argument-hint: spec | plan | todo (defaults to most recent)
---

# Review Command

Generate a styled, interactive HTML view of `spec.md`, `plan.md`, or `todo.md` and serve it on a local HTTP server for human review. The user marks each section approved / needs-changes / rejected, leaves comments, and clicks Save. Feedback is written to JSON for `/bpe:apply-review` to consume.

The server runs in the background — this command does not block the Claude Code terminal. Continue working or wait; either is fine.

## Step 1: Determine the Artifact

Resolve the target artifact:

- If the user passed an argument, map it: `spec` → `spec.md`, `plan` → `plan.md`, `todo` → `todo.md`.
- If no argument was passed, pick the most recently modified of `spec.md`, `plan.md`, `todo.md` in the project root.
- If none exist, tell the user and stop.

## Step 2: Generate the HTML Artifact

Read the chosen markdown file. Generate a self-contained HTML file. Constraints:

**Required structure (the server's injected JavaScript depends on these data attributes):**

- A persistent button at the top right with `id="bpe-save-btn"` and visible label "Save". Make it sticky so it stays in view while scrolling.
- Each meaningful section of the artifact becomes a wrapper element with:
  - `data-section-id="section-N"` (incrementing N starting at 1, unique per section).
  - `data-section-heading="<exact heading text>"`.
  - The rendered section content inside (headings, paragraphs, lists, code blocks, tables — match the markdown faithfully).
- Inside or adjacent to each section, a review controls block containing:
  - Three radio inputs with `name="decision-section-N"`, `data-section-decision="section-N"`, and `value="approve" | "needs-changes" | "reject"`. Label them clearly.
  - A `<textarea data-section-comment="section-N" placeholder="Comments for this section"></textarea>`.
- A global comment textarea at the bottom: `<textarea id="global-comment" placeholder="Anything else?"></textarea>`.

**Do NOT generate the save fetch logic.** The server injects standardized JavaScript that wires up `#bpe-save-btn` to collect feedback from the data attributes above and POST to `/save`. Generating your own save logic will conflict.

**Visual quality:** Take inspiration from Thariq Shihipar's HTML effectiveness examples and Simon Willison's exploit explainer. Priorities:

- Readable typography (system font stack, comfortable line length, ~16-18px base).
- Clear visual hierarchy — headings, sections, callouts.
- Color-code the decision states (green = approve, amber = needs-changes, red = reject).
- Sticky sidebar or sticky save bar so reviewers don't have to scroll back up.
- Light theme is fine; dark theme is fine; pick one and commit.
- For `plan.md` specifically: collapse each step by default, color-code RED/GREEN/REFACTOR labels, surface file paths.
- For `spec.md`: anchored TOC, callout boxes for goals/non-goals/constraints/open-questions if those sections exist.
- For `todo.md`: render as a checklist with grouping by section.

Self-contained: all CSS and any non-server JS inline. No external dependencies, no CDNs.

## Step 3: Write the HTML and Start the Server

Create the HTML file at a unique path:

```bash
mktemp -t bpe-review-XXXXXX.html
```

Compute the feedback path by replacing `.html` with `-feedback.json` on the same path.

Start the server in the background. Use `run_in_background: true` so the terminal returns immediately:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/review-server.py <html-path> <feedback-path> <source-markdown-path>
```

The script:

- Kills any prior `/bpe:review` server via the PID file at `/tmp/bpe-review-server.pid`.
- Binds to the local Tailscale IPv4 if `tailscale` is installed and the daemon is up; otherwise falls back to `127.0.0.1`. Picks a random free port either way. Tailscale binding lets the user review on a phone or second laptop without extra configuration.
- Injects the save JavaScript into the HTML.
- Opens the URL in the user's default browser.
- Writes feedback JSON on `POST /save`, then exits.

## Step 4: Confirm

Tell the user:

- The server URL (read it from the background process's stdout — the script prints `BPE review server: http://127.0.0.1:PORT/`).
- The artifact being reviewed.
- That they should mark each section, leave any comments, then click Save.
- When done, run `/bpe:apply-review` to load the feedback and apply changes.
- If they walk away or close the browser without saving, just re-run `/bpe:review` — it kills the prior server cleanly.
