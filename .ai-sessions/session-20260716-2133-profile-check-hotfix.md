# Session Summary: Goal Run A1-F1 and Profile-Check Hook Hotfix

**Date**: 2026-07-16
**Duration**: Spanned 2026-07-04 to 2026-07-16 with long idle gaps; roughly 6 hours of active orchestration plus 1 hour of hotfix work
**Conversation Turns**: ~45
**Estimated Cost**: High (Fable 5 session; ~25 subagent dispatches at 40-100k tokens each during the goal run)
**Model**: Fable 5 (subagents inherited via `model: inherit`)

## Goal Context

- **Condition**: Every item in todo.md is checked off; claude plugin validate ./bpe exits 0; git status --short is empty; all commits are pushed to origin/fable; .ai-sessions/lessons.md contains any new lessons captured during the run.
- **Mode**: full
- **Outcome**: failed: the Step F2 implement dispatch terminated on a Fable 5 usage limit (2026-07-06); the run stopped per the Failure contract. The remaining steps were completed outside this session and merged to main as PR #18.
- **Turn count**: ~35 orchestrator turns
- **Subagent dispatches**: 25 (10 implement, 6 fix, 9 validator) plus 6 finalize dispatches within those steps
- **Steps completed**: 11 of 24 (A1, A2, B1, B2, B3, C1, C2, D1, E1, E2, F1)

## Key Actions

- Set up the `/bpe:goal` full-mode run: pre-flight, gitignore fix for goal.md, `claude plugin validate ./bpe` adopted as the test command (fixed a pre-existing YAML frontmatter error in apply-review.md to green the baseline), plugin-dev skill routing added to the orchestrator playbook.
- Orchestrated steps A1 through F1 through the implement, validate, fix, finalize state machine; every commit SHA-verified with session summary present; two steps needed two fix rounds (B1, C2), one stray out-of-scope edit was parked in a git stash during B2.
- Step F2 dispatch died mid-read on the Fable 5 usage limit; loop stopped per contract.
- On return (2026-07-16): diagnosed the user being locked out of prompting. Root cause: the 0.6.0 `profile-check` prompt-based UserPromptSubmit hook; its judge model intermittently narrates instead of answering bare `{}`, and the harness surfaces that as a prompt block.
- Hotfix on `fix/profile-check-hook`: replaced the prompt-based hook with a deterministic `hooks/profile-check.py` command hook (regex detection, fresh-install fast path, fail-open on bad input), updated `profile-check.json` and `profile-check.md`, bumped the plugin to 0.6.1.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| /bpe:goal full (verify live step-executor) | Pre-flight, verified installed 0.5.0 executor unchanged with model: inherit, wrote goal.md | Ready after gitignore + test-command fixes |
| add goal.md to .gitignore | Edited .gitignore | Done |
| no test suite; use plugin-dev validator | Adopted claude plugin validate + skill routing; fixed apply-review.md YAML | Baseline green |
| have subagents load plugin-dev skills | Baked skill routing into goal.md orchestrator prompt | Done |
| /goal @goal.md | Orchestrated A1-F1 via step-executor/validator dispatches | 11 of 24 steps landed and pushed |
| What on earth is going on? (post-F2 failure, blocked prompts) | Diagnosed quota death + profile-check hook lockout | Hotfix branch + PR; cache hot-patch |

## Efficiency Insights

**What went well:**
- The sub-agent-per-step architecture kept the parent transcript small enough to survive a 12-day session spanning 11 steps and a context summarization.
- SHA-anchored post-dispatch verification caught nothing bad, but the B2 out-of-scope detection (validator caught a stray working-tree edit the executor missed) proved the validator layer earns its cost.

**What could improve:**
- The goal condition referenced todo.md, which the completed run later deleted; a re-fired evaluator would have been unable to verify the condition. Conditions should reference artifacts that survive convergence.
- The F2 quota death produced no orchestrator-side handling; a Failure lands in the transcript but nothing summarizes run state for the returning user.

**Course corrections:**
- User backed out an unintended model change to the live step-executor before the run started; verified the installed 0.5.0 copy stayed pristine.

## Process Improvements

- When a goal run dies on quota, write a one-line state file (steps done, next step, blockers) so the returning user gets the picture without transcript archaeology.
- Prompt-based hooks should never own a branch where the common case must return a bare sentinel; see today's lesson.

## Observations

- The three prompt blocks the user hit were nondeterministic: the same hook let the final (much longer) prompt through, which is consistent with judge-model variance rather than a config error.
- The 0.6.0 work this session helped build (K2's profile-check hook) is what locked the user out; the K2 lesson about prompt-hook input limits was captured but the fail-closed blocking risk was not foreseen.

## Suggested Skills for Next Session

- `plugin-dev:hook-development` — if the PR review surfaces hook protocol questions, or further hook work lands.
- `skill-creator:*` and `plugin-dev:skill-development` — the user's next project is codifying taste/judgment preferences into skills (lessons extraction, python skill audit, higher-level engineering skills).
