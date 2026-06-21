# Session Summary: BPE validator agent system

**Date**: 2026-06-21
**Duration**: ~90 minutes
**Conversation Turns**: ~10
**Estimated Cost**: ~$8
**Model**: claude-opus-4-7

## Key Actions

- Diagnosed a real misunderstanding about subagent tool access. Subagents inherit only the tools listed in their frontmatter `tools:` field; the parent's tool inventory does not propagate. The `bpe:step-executor` agent's `tools: Read, Edit, Write, Bash, Grep, Glob, Skill` was the gate that excluded `ToolSearch` and therefore all MCP tools.
- Designed a generic QA-agent pattern. Instead of N domain-specific validators (`validator-temporal`, `validator-python`, ...), one `bpe:validator` agent receives MCP and skill lists from the orchestrator and consults them. The orchestrator decides which tools the validator consults per plan.md section. Auto-discovery fallback exists for ad-hoc human use; the loop always passes lists explicitly.
- Established the QA-team architectural principle. The orchestrator (`/bpe:goal`) dispatches the validator, not the executor. Mason: "If you let devs decide whether something should be tested they'll say no."
- Settled the pre-commit fix loop. Validator runs after `mode=implement` and before `mode=finalize`. Up to 3 iterations of executor `mode=fix` to resolve `block`/`warn` findings; `info` findings record only and ride along in the commit message body. Hard cap stops the loop with a Failure surfaced to the `/goal` evaluator.
- Implemented Phase 1: created `bpe/scripts/validate-findings.py` (canonical schema check, std-lib only, 150 lines), `bpe/references/validator-protocol.md` (single source of truth for the dispatch state machine, severity ladder, and findings schema), and `bpe/agents/validator.md` (the generic validator with read-only tools: `Read, Grep, Glob, Bash, Skill, ToolSearch`).
- Implemented Phase 2: refactored `bpe/agents/step-executor.md` into three modes (`implement`, `fix`, `finalize`) with mode-specific invariants. `mode=fix` is the only mode that may start with a dirty tree; `mode=finalize` is the only mode that commits or pushes. Backwards-compatible default flow preserved for legacy `/goal` runs in flight that do not pass `Mode:`.
- Implemented Phase 3: `bpe/commands/brainstorm.md` gained a tool discovery step that writes spec.md's `## Available tooling` section. `bpe/commands/plan.md` gained per-section `**Validator consults:**` declarations sourced from spec.md. `bpe/commands/goal.md` rewrote the orchestrator playbook to delegate the per-step state machine to `validator-protocol.md` (keeping the assembled `/goal` block at 3198 chars, comfortably under the 4000 cap).
- Smoke-tested the schema validator with six fixture cases (well-formed, clean, verdict mismatch, bad severity, missing field, unknown key, malformed JSON, stdin pipe). All passed.
- Scanned all new and modified files for AI-tells per `~/.claude/rules/writing-style.md`. Zero em-dashes, zero banned vocab, zero sentence-initial Additionally.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| "Got this from an agent ... Is this true about the subagent?" | Verified `bpe:step-executor` frontmatter; confirmed the tools allowlist is the gate; explained three options to broaden access (`*` wildcard, explicit MCP list, `ToolSearch` alone) | User accepted; chose to design a validator pattern instead of widening the executor |
| "Should we create a step-validator?" | Recommended yes; raised the pre-commit-vs-post-commit decision as the core design call | User chose pre-commit |
| "Pre-commit ... stop bad code from being committed" | Outlined three guardrails (iteration cap, severity tiers, declarative validator selection); recommended executor dispatches validator | User accepted iteration cap and severity model; overrode dispatch ownership ("Orchestrator dispatches. If you let devs decide whether something should be tested they'll say no.") |
| "Generic validator that knows to reach for MCP and Skills, args optional" | Revised plan to one generic agent with parameterized dispatch; orchestrator always passes explicit lists; auto-discovery is fallback for human use | User accepted |
| "What would a validate-findings.py do?" | Explained schema/enum/consistency/canonicalize roles; explicitly scoped out semantic correctness, dedup, severity interpretation | User accepted; "sounds good, implement it all" |
| "Implement it all" | Created feature branch `validator-agent-system`; wrote 3 Phase 1 files; refactored step-executor for 3 modes; updated brainstorm/plan/goal; smoke-tested schema validator; style-scanned everything | Ready for commit |

## Efficiency Insights

**What went well:**
- Reflecting the plan back before each major decision caught real preferences early. Asking "executor dispatches or orchestrator dispatches?" surfaced the QA-team principle that drove the rest of the architecture.
- The schema validator script is small enough to smoke-test by hand in two minutes. Six fixture cases caught zero bugs, which suggests the script is right; if it had been larger I would have needed proper tests.
- Delegating the per-step state machine to `validator-protocol.md` kept the inline `/goal` block at 3198 chars (cap is 4000). Without delegation the block would have blown past the cap and forced ugly trimming of safety contracts.

**What could improve:**
- I drafted the wrong dispatch ownership first (executor dispatches validators), then had to revise. The QA-team analogy was hiding in plain sight; I could have led with "treat this like CI, not like a TODO checker" and arrived at orchestrator-dispatches from the first pass.
- The `validate-findings.py` could be a uv-installable CLI rather than a script invoked by path, but the path-based invocation matches the rest of `bpe/scripts/` and avoids a packaging dependency. Worth revisiting if other scripts join.

**Course corrections:**
- Switched from "one validator agent per domain" to "one generic validator parameterized per section" mid-design when Mason pushed back on hardcoding Temporal. The generic version is now the only version; no domain validators exist.

## Process Improvements

- When a subagent reports a tool-access issue, read the agent's frontmatter `tools:` field FIRST before guessing. The gate is in the frontmatter, not in the parent session.
- When designing a multi-agent loop with token-cost sensitivity, count the dispatches per unit of user work explicitly. This step's loop is up to 5 dispatches per todo item (implement, validator x3 iter, finalize); compared to the legacy 1 dispatch per item, that's a 5x token-cost ceiling. Mason needs to be aware so they can declare `Validator consults: none` for cheap sections.
- For commands that emit `/goal` blocks, always check the substituted character count of the inline block against the 4000 cap. The check is `awk` + `sed` + `wc -c`, takes 5 seconds, catches future bloat.

## Observations

- The single biggest design call in this work was Mason's "orchestrator dispatches validators, not executor" call. It chose the QA-team-as-separate-team model over an embedded-quality-checks model. Worth recording: when the user can articulate a clear social analogy ("if you let devs decide whether something should be tested they'll say no"), trust it over the technically-cleaner-on-paper option.
- The findings JSON schema is small and stable. Adding new fields is cheap; changing field semantics is not. The validator agent and the executor's `mode=fix` both consume the schema, so any change ripples to both. The protocol doc (`validator-protocol.md`) is intentionally the single point of truth so the two agents stay aligned.
- The auto-discovery fallback path in `bpe:validator` is technically optional. It exists for humans invoking the validator standalone for ad-hoc review of a diff. The automated loop never uses it.

## Suggested Skills for Next Session

- `python:python` — if the next session touches `validate-findings.py` or adds test coverage to it, the toolchain standards apply.
- `plugin-dev:agent-development` — if iterating on agent frontmatter (description quality, tool minimization, color picks).
- `plugin-dev:command-development` — if iterating on the goal/brainstorm/plan command frontmatter or argument-hint patterns.
