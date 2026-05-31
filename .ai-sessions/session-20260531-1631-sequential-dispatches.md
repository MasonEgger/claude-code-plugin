# Session Summary: Enforce SEQUENTIAL DISPATCHES ONLY in /goal Orchestrator

**Date**: 2026-05-31
**Duration**: ~25 minutes
**Conversation Turns**: ~3
**Estimated Cost**: ~$1.00 (Opus 4.7, focused file edits)
**Model**: claude-opus-4-7

## Key Actions

- Diagnosed a cataclysmic failure of the v0.4.4 autonomous-mode loop on the user's protobuf project. The orchestrator dispatched roughly twelve `bpe:step-executor` subagents in a single batched message (Steps 4–15) instead of sequentially. Result: per-step verification ran against `HEAD` (whichever commit landed last, not the dispatched one); subagents raced on `todo.md` checkmarks; multiple commits with RED test suites landed and pushed to `origin/v1` before any gate fired. Net state: a chain of 7 broken commits on the user's feature branch, with 0cf3ee7 as failing HEAD.
- Root cause: the orchestrator block said "Per loop:" with numbered steps, but never explicitly forbade firing multiple `Agent()` calls in a single message. The Agent tool's standing guidance encourages parallel dispatches for "independent work" — a model reading the unchecked todo list as N independent items can plausibly batch-dispatch. The serialization that the entire safety model relied on (verify → gate → next dispatch) collapsed because all dispatches ran concurrently.
- Three structural fixes in v0.4.5:
  - **New CRITICAL CONTRACT at the top of the orchestrator block: SEQUENTIAL DISPATCHES ONLY.** Explicit "exactly ONE `Agent` call per turn", "NEVER fire in parallel", "YOUR TURN ENDS HERE" at step 6, with the rationale spelled out (todo.md / git state / test suite are NOT independent across items). Also added "SERIALIZATION IS THE SAFETY MODEL — do not optimize it away" to override the Agent tool's default parallelism guidance.
  - **Verify against the subagent's reported SHA, not `HEAD`.** Step 5 of the orchestrator loop now: (a) parses the `Commit:` field from the subagent's report, (b) confirms `git rev-parse HEAD == reported-sha` (stops on mismatch, which catches the racing scenario directly), (c) runs the session-summary grep against the reported SHA, (d) parses the `Tests:` field and stops if it doesn't show exit code 0 (catches red-test commits directly, which was the actual harm in the protobuf failure).
  - **Subagent-side clean-tree pre-flight.** Updated the `step-executor.md` "Pre-flight" Hard Invariant: BEFORE any work, run `git status --short` along with the branch check; abort with `Failure:` on any non-empty output. A dirty tree at dispatch start strongly implies a concurrent subagent (or incomplete prior cleanup). Defense in depth — catches a parallel dispatch from the inside.
- Updated `README.md` "Autonomous Mode" section to list three hard contracts (SEQUENTIAL, summary-per-commit, one-commit-per-dispatch) instead of two.
- Bumped version 0.4.4 → 0.4.5.
- Fifth 0.4.x patch driven by emitted-string defects, but this one is qualitatively worse — the prior four were correctness issues; this one was a safety-model collapse that pushed broken code to a feature branch. The pre-ship dry-read pattern is now clearly insufficient; an adversarial test harness against a throwaway repo is needed before any 0.5.0.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| User shared the failed subagent's diagnosis: orchestrator fired ~12 dispatches in parallel, verification couldn't gate anything, subagents raced on todo.md, multiple RED commits landed and pushed | Diagnosed root cause (no "sequential only" rule, no verify-against-reported-SHA, no Tests: field check); proposed three structural fixes; flagged the broader pattern of 5 consecutive emitted-string defects and recommended an adversarial test harness before 0.5.0 | Fix plan agreed |
| "We should absolutely enforce only one of these running at a time. ... lets do it and land it as 0.4.5" | Applied: SEQUENTIAL DISPATCHES contract, verify-against-reported-SHA, Tests:-field check, subagent clean-tree pre-flight, README update; bumped version; session summary + lessons + commit-msg; signed commit to main; pushed | Patch landed |

## Efficiency Insights

**What went well:**
- Multi-layer defense (orchestrator-side contract + verify-against-SHA + subagent-side clean-tree check) addresses both prevention and detection — if the orchestrator slips, the subagent catches it on entry; if a subagent's TDD slips, verify catches the commit before the loop continues.
- The verify-against-reported-SHA change is the structural fix; the SEQUENTIAL CONTRACT is the language fix. Both shipped together because language alone wouldn't have caught what slipped in 0.4.4 (the model could still be tempted to parallel-dispatch and the verification was too weak to catch the consequences).

**What could improve:**
- This is the FIFTH consecutive autonomous-mode patch on emitted strings. The cost is now visible: a real production failure on the user's protobuf project, broken commits pushed to a feature branch, and the user having to manually clean up. The pre-ship reading discipline didn't catch it; reading-aloud doesn't surface "what would a model with parallel-dispatch instincts do here?"
- The orchestrator block has grown by ~600 chars across these patches. Still well under the 4000 cap, but trending toward bloat. Future patches may need to be net-zero (replace, not add).

**Course corrections:**
- The 0.4.4 verification step (`git show HEAD | grep .ai-sessions`) was wrong in the parallel-dispatch case because HEAD was the last-finished commit, not the one being verified. Fixed by parsing the reported SHA from the subagent's report and verifying THAT commit. This generalizes: post-dispatch verification must be anchored to what the subagent says it did, not to whatever the global state happens to be.

## Process Improvements

- **Before any 0.5.0 release, build an adversarial test harness** against a throwaway repo with N todo items. Run `/bpe:goal` with mode=section (or full), observe whether dispatches are serial, whether verification catches injected failures (red tests, missing session summary, parallel HEAD movement), and whether the loop stops cleanly on each. Five emitted-string defects in a row makes "read the output" demonstrably insufficient.
- **When an orchestration pattern relies on a serializability guarantee, write the guarantee as an explicit CRITICAL CONTRACT at the top of the prompt AND build a check that fires if the guarantee was violated.** Language alone won't override the Agent tool's standing guidance. Both layers (declared contract + run-time detection) are needed.
- **For autonomous-mode failures, "what would the model interpret this as?" must be asked from a model-instincts perspective, not a human-reader perspective.** A human reading "Per loop: 1. ... 2. ... 3. dispatch ..." sees a sequential algorithm. A model sees a recipe whose dispatch step could be batched.

## Observations

- The Agent tool's documentation actively works AGAINST safety in this scenario: "When you launch multiple agents for independent work, send them in a single message with multiple tool uses so they run concurrently." That advice is correct for genuinely independent work; it's catastrophic for an orchestrator whose dispatched units share mutable state. The fix has to live in the orchestrator prompt (since we can't modify the Agent tool's docs) — strong override language plus run-time detection.
- The verification flaw (checking HEAD instead of the reported SHA) was a real architectural mistake in 0.4.4, not just an omission. Anchoring verification to the artifact's reported identity rather than the global state is a generalizable principle for any orchestration pattern with concurrent writers.
- The user's protobuf project now has a real cleanup burden (7 broken commits on origin/v1). The plugin can't help with that directly, but every future /goal user will benefit from the v0.4.5 hardening.

## Suggested Skills for Next Session

- None for the next plugin-side session. For the adversarial test harness work, no specific skills needed beyond shell and basic git.
