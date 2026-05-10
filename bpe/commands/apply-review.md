---
description: Load saved review feedback from /bpe:review and apply changes to the reviewed artifact
---

# Apply Review Command

Consume the feedback JSON written by `/bpe:review` and apply the user's annotations to the reviewed markdown artifact. The user has already reviewed in the browser and clicked Save — this command surfaces their decisions and applies the changes after explicit confirmation.

## Step 1: Find the Most Recent Feedback File

Find the most recent feedback JSON in `/tmp/`:

```bash
ls -t /tmp/bpe-review-*-feedback.json 2>/dev/null | head -1
```

If none exists, tell the user to run `/bpe:review` first and stop.

If one exists but its `saved_at` timestamp is more than 24 hours old, surface that to the user and ask whether they meant to apply this older feedback or run `/bpe:review` again.

## Step 2: Load and Summarize

Read the feedback JSON. Expected shape:

```json
{
  "sections": [
    {
      "id": "section-N",
      "heading": "<heading text>",
      "decision": "approve" | "needs-changes" | "reject" | "unset",
      "comment": "<free-text feedback>"
    }
  ],
  "global_comment": "<free-text>",
  "artifact_path": "<absolute path to the reviewed markdown file>",
  "saved_at": "<ISO timestamp>"
}
```

Display a summary:

- Counts: N approved, N needs-changes, N rejected, N unset.
- For every section that is NOT `approve`, list:
  - The heading.
  - The decision.
  - The comment (verbatim).
- The global comment, if non-empty.
- The artifact path that will be modified.

## Step 3: Confirm Before Mutating

Ask the user explicitly: "Apply these changes to `<artifact_path>`?" Do not proceed without a clear yes.

How to interpret each decision:

- **approve** — leave the section unchanged.
- **needs-changes** — apply the comment as a directive: rewrite the section to incorporate the feedback, preserving structure and surrounding context.
- **reject** — the section should be removed or rewritten. Reject often means "this is wrong, redo" rather than "delete entirely". When ambiguous, ask the user before deleting.
- **unset** — no decision recorded. If the section has a comment, treat it as needs-changes; otherwise leave alone and note that the section had no decision.

Apply the **global_comment** as a holistic directive across the artifact (e.g. "tighten language", "add a glossary", "split into two files").

## Step 4: Apply the Changes

Read the artifact via the Read tool. Make targeted edits via the Edit tool — one Edit per affected section. Do not rewrite the whole file unless the global comment explicitly requests it. Preserve formatting, list styles, and unrelated sections exactly.

## Step 5: Confirm

After applying, show the user:

- A brief diff summary (which sections changed, one line each).
- Any feedback that could not be applied automatically and why.
- Suggested next step: `/bpe:review` again to re-review, `/bpe:plan` to regenerate downstream artifacts (if `spec.md` was edited), or continue.
