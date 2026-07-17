# Accomplishment: BPE 0.6.0 Redesign

**Archived**: 2026-07-16
**Convergence**: converged

## Spec Slice

The full spec.md: redesign BPE from a TDD-only code workflow into a template-aware pipeline that handles non-code projects, with a validator QA loop, deviation tracking, plan archiving, explicit model tiers, and per-user model profiles.
24 steps across 12 components (A through L).

## What Got Done

- Component A: all 12 commands migrated to `bpe/skills/<name>/SKILL.md`; legacy `commands/` deleted; `/bpe:` invocation unchanged.
- Component B: Feature (TDD) and Task (Scope/Tooling/Do/Verify/Document) plan templates with a selection heuristic; per-section Tools block schema; executor made template-agnostic.
- Component C: `bpe:cheap-research` subagent (haiku, read-only); two-pass tool discovery in `/bpe:plan` with `--no-discover` and spec.md caching.
- Component D: `/bpe:retrofit` produces spec.md for existing projects, guarded by `--replace`.
- Component E: Step 0 blindspot pass in brainstorm and retrofit; verbatim `## Starting context` record consumed by plan and validator.
- Component F: implementation-notes.md deviations log; written by mode=implement, absorbed into session summaries by mode=finalize, read by the validator as accepted diff context.
- Component G: `/bpe:plan` refuses over an existing plan without `--archive`/`--regen`; archive routine with slug confirmation and accomplishment.md; end-of-goal archive prompt in session-summary.
- Component H: verification-command cascade (manifest autodetect, spec.md field, ask) so non-code projects get first-class goal conditions.
- Component I: validator runs Tools-block linters as subprocesses and folds output into the findings schema; protocol doc gained the Linter-sourced findings section; validate-findings.py needed no changes.
- Component J: explicit `model:` tiers in all 3 agents and 13 skills (opus for judgment-heavy, sonnet for mechanical, haiku for cheap-research).
- Component K: `.claude/bpe.local.md` profile system with single-pass resolution (model-profiles.md), profile-check UserPromptSubmit hook, shipped example file and README section.
- Component L: version bump to 0.6.0.
- Ride-alongs: Ship It comment lock and decision tooltips (issue #16); `mktemp -u` collision fix in the review skill.

## Deferred or Dropped

- Live end-to-end checks for every component (skill invocation, hook firing, model tiers, archive flag flow) deferred to a reloaded plugin session; the 0.5.0 cache ran this whole goal loop.
- Per-step linter overrides: the validator resolves Linters at section level only, because dispatches carry a Section but no step identifier (recorded as an info finding on I1).
- Family-alias comparison semantics for the profile-check hook live only in the hook body, not in model-profiles.md (info finding on K2).

## Notable Decisions

- L1 (version bump) landed early on 2026-07-15 at Mason's direction to ship the completed components; F2 through K then converged the same day, so the shipped 0.6.0 matches the finished plan.
- Prompt-based hooks cannot see process env vars and a `.md` file cannot be a hook registration, so K2 split into profile-check.md (canonical body) plus profile-check.json (registration) with session-agent delegation for BPE_PROFILE (documented deviation).
- Cross-file active_profile resolution was made explicitly single-pass after a K1 warn: the name resolves once (env, per-project, user-global) and governs lookups in both files.
- G1 merged the plan's literal argument-hint with C2's pre-existing `--no-discover` flag rather than replacing it.
- G3's archive prompt got an executor-dispatch guard beyond the plan's wording, since session-summary also runs inline on every finalize where prompting is impossible.
- The plan was hand-written rather than generated (bootstrap paradox: the templates it created did not exist yet), noted in spec.md.

## Files Touched

63 files versus main (+4340/-271) across 31 commits on `fable`, shipped as PR #18.
Highlights: `bpe/skills/*` (13 SKILL.md files, 12 migrated + retrofit), `bpe/agents/{step-executor,validator,cheap-research}.md`, `bpe/references/{session-management,validator-protocol,step-executor-protocol,model-profiles}.md`, `bpe/hooks/profile-check.{md,json}`, `bpe/scripts/{review-server.py,review.css}`, `bpe/.claude-plugin/plugin.json`, `.claude/bpe.local.md.example`, `bpe/README.md`.

## Lessons Cross-Reference

- "X is the only Y" claims in agent docs get contradicted by the doc's own procedure (2026-07-15, from the I1 warn).
- Prompt hooks see only hook-input JSON and cannot be registered as `.md` (2026-07-15, from K2).
- Sweep for content regressions with greppable tokens before shipping a branch containing a rewrite (2026-07-15).
- Point fixes on files a rewrite touches must land as commits (2026-07-15, the mktemp revert).
- Stale-claim grep after contract-changing edits (2026-07-05, from the A2/B1 warns).
- Meta-project bootstrap paradox: hand-write the plan, note it in spec.md (2026-07-04).
