# Session Summary: One-Commit-Per-Dispatch Rule + Orchestrator Verification

**Date**: 2026-05-30
**Duration**: ~30 minutes
**Conversation Turns**: ~6
**Estimated Cost**: ~$1.50 (Opus 4.7, multiple file rewrites + diagnosis)
**Model**: claude-opus-4-7

## Key Actions

- Diagnosed a real autonomous-mode failure on the user's RSS feeds project (v1 branch). The subagent's `Failure:` report initially looked like "session summary missing", but the user's hands-on investigation revealed the actual sequence: the scaffold commit (`bd3a620`) DID include its `.ai-sessions/session-*.md` — the hook rejection was on a SECOND, follow-up commit (a test fix for `Test2::V0` → `Test::More`) that legitimately had no new summary because it wasn't a new BPE step.
- Also surfaced: the scaffold commit landed with a stale message ("Add design spec and TDD implementation roadmap" — leftover from the planning phase) because the subagent reused an existing `commit-msg.md` instead of regenerating it.
- The user's resolution was decisive: "Don't do follow-up/fixup commits. Only commit when you're finally done and ready and proud of it." This resolves the architectural conflict between BPE's one-summary-per-step rule and the global pre-commit hook's one-summary-per-commit enforcement.
- Bundled three changes into v0.4.4 (also a UX simplification the user requested in the prior turn — single-paste `/goal` block instead of two):
  - **`step-executor.md`** — added Hard Invariant: "Exactly ONE commit per dispatch. No follow-ups, no fixups, no amends, no `--no-verify`." Tightened step 5 to require `commit-msg.md` regeneration even if a stale file exists. Tightened step 6 with a pre-commit test-run + `git diff --staged` visual confirmation, plus an explicit "do NOT make a follow-up fix commit" on hook rejection.
  - **`goal.md` Step 3** — replaced the two-block emission (introduced in 0.4.3) with a single combined `/goal` block. The orchestrator playbook trimmed to ~1500 chars by dropping redundancy with the subagent's system prompt; condition (~250 chars) + playbook total ~1750, well under the 4000-char cap. Added two CRITICAL CONTRACT call-outs at the top (session-summary mandatory; one-commit-per-dispatch). New step 5 in the orchestrator loop: verify via `git show --stat --name-only HEAD | grep -E '^\.ai-sessions/session-.*\.md$'` that the subagent's commit actually contains the summary; stop on miss.
  - **`README.md`** — Mermaid diagram updated for single-block emission; Autonomous Mode prose now describes the two hard contracts the orchestrator enforces.
- Bumped version 0.4.3 → 0.4.4.
- Direct-to-main commit + push (fourth autonomous-mode patch in a row — the meta-pattern of "under-tested emitted user-facing strings" continues to bite, despite hardening passes).

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| "Why can't this just be one block and you limit to 4000? Do you need that many characters?" | Counted what's actually load-bearing in the orchestrator; proposed trim from ~4400 → ~1100 chars; showed mock-up of single-paste version | User agreed in principle |
| "Dont forget you MUST do the .ai-session summary. My pre-commit hook will nail you on that" | Initially read as a workflow reminder; verified no hook on this repo; was about to apply the trim when user interrupted | Interrupted |
| "No I mean in the goal. YOu have to state that. I keep watching the subagents fail. The instructions need to be in the goal" | Reinterpreted: user wants session-summary mandate MORE visible in the orchestrator's dispatch prompt; added CRITICAL CONTRACT, MUST language, orchestrator-side verification step | Mock-up shown |
| User shared the failed subagent's actual diagnosis showing (a) session summary DID land, (b) hook trip was on a follow-up commit, (c) scaffold commit had stale message; codified working rule "Don't do follow-up/fixup commits. Only commit when you're finally done and ready and proud of it." | Bundled the new rule into v0.4.4 alongside the single-paste trim, the CRITICAL CONTRACT call-outs, the orchestrator verification step, and a fix for stale `commit-msg.md` reuse | All applied |

## Efficiency Insights

**What went well:**
- The architectural fix (one-commit-per-dispatch) resolves the hook conflict cleanly. The original instinct to disable the global hook would have masked a real BPE discipline issue; the user's resolution turned the hook into a feature.
- Trimming the orchestrator to ~1500 chars while STRENGTHENING the session-summary contract proved both things were possible at once — emphasis isn't a function of length.
- Adding orchestrator-side verification (`git show --stat | grep .ai-sessions`) is a cheap defense-in-depth that catches the subagent if it ever slips again, regardless of how well its system prompt is written.

**What could improve:**
- I almost shipped the trim WITHOUT addressing the subagent's actual failure mode because the user's first reminder ("MUST do the .ai-session summary") read like a workflow nudge. The follow-up ("I keep watching the subagents fail. The instructions need to be in the goal") was the correction. Cost: one round-trip.
- This is the fourth 0.4.x patch in a row. Every single one was a defect in emitted user-facing strings discoverable by reading them end-to-end as a user would. The pre-ship dry-read is still not happening.

**Course corrections:**
- Re-scoped from "trim the orchestrator" to "trim AND emphasize AND verify AND fix the follow-up-commit class entirely" after the user's diagnosis landed. The single PR is now substantive enough to qualify as the autonomous-mode hardening pass, not just a UX patch.

## Process Improvements

- **For autonomous-mode patches, run the emitted output mentally as a user pasting it into a fresh Claude Code session.** Would have caught: the 4000-char overflow (0.4.3), the stale `commit-msg.md` reuse pattern (0.4.4), the silent-failure mode of skipped session summaries (0.4.4 verification step).
- **When the user reports a real failed run, distinguish symptom from cause before fixing.** The subagent's `Failure:` report blamed the session summary; the actual cause was a follow-up commit + a stale commit message. The user's hands-on diagnosis was essential.
- **When two artifacts both enforce a rule (the subagent's system prompt AND the orchestrator's dispatch prompt), they reinforce — they don't substitute.** Strong language in step-executor.md wasn't enough; the orchestrator needs to verify post-commit. Defense in depth wins.

## Observations

- The user's "Don't do follow-up/fixup commits. Only commit when you're finally done and ready and proud of it" is a generalizable software discipline statement that happens to also resolve a specific architectural conflict. It deserves to be a Plugin Development lesson at the category level — applies beyond autonomous mode.
- Four 0.4.x patches now (slash commands not invokable in loops, commit ritual ambiguity, condition packaging + fake `/auto`, one-commit-per-dispatch + verification). Each is a real defect, but the pattern is clear: emitted user-facing strings need empirical end-to-end testing before shipping. The README already calls out "smoke test on a small real project" in the test plan; that needs to happen BEFORE the next minor release.
- The global pre-commit hook that requires one new `.ai-sessions/session-*.md` per commit is actually an excellent forcing function — it turns the "should I make a follow-up commit?" question into a hard wall. Plugins that aim to be commit-discipline-aware should consider this hook a feature, not an obstacle.

## Suggested Skills for Next Session

- None. If the next session is a smoke test on a real Python or Perl project: `python:python` if Python.
