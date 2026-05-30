# Session Summary: Split `/goal` Condition from Orchestrator Instructions

**Date**: 2026-05-30
**Duration**: ~15 minutes
**Conversation Turns**: ~3
**Estimated Cost**: ~$0.50 (Opus 4.7, light file work)
**Model**: claude-opus-4-7

## Key Actions

- Diagnosed two related defects in the v0.4.2 `/bpe:goal` emission, surfaced when the user ran it for a 320-item full plan:
  1. The block emitted by `/bpe:goal` packaged both the `/goal <condition>` invocation AND the ~4400-character orchestrator instructions into a single fenced block. The user pastes it as one slash command, which means the entire orchestrator block becomes the `/goal` condition argument — blowing past `/goal`'s documented 4000-character cap (the actual run hit 4609 chars).
  2. The block (and the README, and the frontmatter description) told the user to run `/auto` first to enable auto-accept mode. **`/auto` doesn't exist as a slash command.** The actual mechanism is `Shift+Tab` to cycle TUI permission modes. The bad instruction came from my earlier `claude-code-guide` research, which I baked into three sites without verifying the command existed locally (my skills list doesn't include it; I could have checked).
- Restructured `bpe/commands/goal.md` Step 3 to emit TWO separate fenced blocks for the user to paste in sequence: Block 1 is the orchestrator instructions (pasted as a normal message, ends with "Standing by for /goal command"); Block 2 is the short `/goal <condition>` activation. The condition itself is ~200 chars — well under the cap.
- Replaced all three `/auto` mentions (description, emitted reminder, README) with neutral "put your session in auto mode" guidance — no client-specific shortcut, no fabricated slash command. User asked for this directly: "Just tell me to put it in auto. I can manually do that."
- Updated README Mermaid diagram and per-step language to reflect the two-block paste flow.
- Bumped version 0.4.2 → 0.4.3.
- Direct-to-main commit + push (third autonomous-mode patch in a row; the meta-lesson about a hardening pass before the next minor release stands).

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| User relayed feedback from another Claude session: `/auto` doesn't exist, actual mechanism is Shift+Tab; also flagged subagent inheritance uncertainty and offered to either verify or build a permission allowlist | Acknowledged the bug; proposed three patch sites; offered to verify subagent inheritance before patching | User chose to skip verification |
| "Just tell me to put it in auto. I can manually do that. Also 'Goal condition is limited to 4000 characters (got 4609)'" | Diagnosed root cause of the 4609 (whole orchestrator embedded in condition); restructured `goal.md` Step 3 to emit two separate blocks; simplified `/auto` guidance to neutral "auto mode"; updated README + frontmatter; bumped 0.4.3 | Patch ready |

## Efficiency Insights

**What went well:**
- Caught the 4000-char defect via the user's run output ("got 4609") — concrete failure data made the diagnosis trivial.
- Two-block split is the architecturally honest fix: `/goal`'s condition is for the evaluator, orchestrator instructions are for the parent session. They were always two separate things; packaging them into one paste was a UX shortcut that hit the cap.

**What could improve:**
- The 4000-char cap was documented in my original Phase 0 research and I still shipped an emitted block that combined condition + instructions — a structural conflict I should have caught when designing the emission format.
- The `/auto` reference came from `claude-code-guide` subagent output. I treated subagent research as authoritative without cross-checking against the visible skills list in my own context. That's the same root cause as the "follow X" defect from 0.4.1 — relying on a single research source without empirical verification.

**Course corrections:**
- None mid-session — the user's diagnosis and direction were clear enough that the fix path was unambiguous.

## Process Improvements

- **Verify subagent research empirically before baking it into emitted output.** Skills list, `/help`, or a quick test dispatch are all cheap. Recurring failure mode across 0.4.1 / 0.4.2 / 0.4.3.
- **When the docs cite a hard cap (4000 chars, 50 dispatches, etc.), design the emission around the cap from day one.** The cap was known; the emission format ignored it.
- **For autonomous-mode patches: dry-read the emitted output asking "if I copy this and paste it into a /goal invocation, what does my session see?"** Would have surfaced both bugs pre-ship.

## Observations

- Three consecutive 0.4.x patches now (0.4.1: slash commands not invokable from autonomous loops / subagents; 0.4.2: commit ritual ownership ambiguity; 0.4.3: condition/instructions packaging + fabricated `/auto`). Each was a real defect, but all three share a meta-cause: under-tested emitted user-facing strings. Pre-ship the autonomous-mode emission should be exercised end-to-end on a toy project, not just read.
- The "research-agent says X" → "ship X verbatim" pipeline has now produced two distinct bugs (the slash command misuse in 0.4.1 and the `/auto` mention in 0.4.3). Treat single-source research output as a hypothesis, not a fact, when it controls user-facing instructions.

## Suggested Skills for Next Session

- None. If the next session is a smoke test against a real Python project, `python:python`.
