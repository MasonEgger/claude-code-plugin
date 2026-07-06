# TODO: BPE 0.6.0 Redesign

Mirror of plan.md. Check off sub-steps as they land. Each top-level `[ ]` is a step; nested `[ ]` are the Scope/Tooling/Do/Verify/Document sub-steps within it.

## Component A: Skill migration

- [x] Step A1: Migrate all `bpe/commands/*.md` to `bpe/skills/<name>/SKILL.md`
  - [x] Scope defined (12 skill dirs under bpe/skills/; plan said 13 but enumerates 12 and 12 command files exist)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] All 12 skill dirs created with SKILL.md + `disable-model-invocation: true`
  - [x] Verify: 12 SKILL.md files exist; frontmatter YAML parses; `claude plugin validate` passes (live `/bpe:` autocomplete check deferred to a reloaded interactive session)
  - [x] Documented (README note about migration)
- [x] Step A2: Delete legacy `bpe/commands/` files after verification
  - [x] Scope defined (empty commands/ dir; plan said 13 files but 12 existed, per the A1 discrepancy note)
  - [x] Tooling loaded (plugin-dev:plugin-structure)
  - [x] Files removed; directory removed; plugin.json checked (no `commands:` field present); dangling `commands/` path references updated to `skills/<name>/SKILL.md` in step-executor.md, goal/SKILL.md, step-executor-protocol.md
  - [x] Verify: commands/ removed; brainstorm SKILL.md frontmatter parses and `claude plugin validate ./bpe` exits 0 (interactive /bpe:brainstorm check deferred to a reloaded session, same as A1)
  - [x] Documented (no new docs; README migration note from A1 stands)

## Component B: Plan template family and Tools block

- [x] Step B1: Add Task template and heuristic guidance to `/bpe:plan` skill
  - [x] Scope defined (bpe/skills/plan/SKILL.md only)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Feature/Task sections added; meta-prompting note; heuristic; two consistency edits (intro line + Prompt Generation Requirement 4) so the body no longer claims every prompt is RED-GREEN-REFACTOR
  - [x] Verify: greps for Task/Feature/Meta-prompting succeed (3/1/2); frontmatter YAML parses; `claude plugin validate ./bpe` exits 0 (interactive /bpe:plan invocation deferred to a reloaded session, same as A1/A2)
  - [x] Documented (in skill body)
- [x] Step B2: Add per-section Tools block schema to `/bpe:plan` skill
  - [x] Scope defined (bpe/skills/plan/SKILL.md, bpe/references/validator-protocol.md)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Tools block schema added (section replaced, Output Format bullet updated); per-step override note; backwards-compat note; validator-protocol.md "Tools block" section + Tool-list propagation aligned
  - [x] Verify: greps for Tools:, Validator consults, Tools block succeed; `claude plugin validate ./bpe` exits 0
  - [x] Documented (in skill body + validator-protocol.md)
- [x] Step B3: Make execute-plan skill and step-executor agent template-agnostic
  - [x] Scope defined (bpe/skills/execute-plan/SKILL.md, bpe/agents/step-executor.md, bpe/references/step-executor-protocol.md)
  - [x] Tooling loaded (plugin-dev:skill-development, plugin-dev:agent-development)
  - [x] execute-plan step 7 wording changed + mixed-template note added; step-executor mode=implement step 3 rewritten; step-executor-protocol.md Mode contracts note added; consistency touches (Key Requirements line, agent frontmatter description, protocol Role bullet) so no TDD-only wording contradicts the templates
  - [x] Verify: "TDD step" count 0 in step-executor.md; "Feature or Task" count 1 in step-executor-protocol.md; "sub-steps as written" count 1 in execute-plan SKILL.md; `claude plugin validate ./bpe` exits 0
  - [x] Documented (in agent/skill bodies)

## Component C: bpe:cheap-research subagent + tool discovery pass

- [x] Step C1: Create `bpe:cheap-research` subagent at `bpe/agents/cheap-research.md`
  - [x] Scope defined (new agent file)
  - [x] Tooling loaded (plugin-dev:agent-development)
  - [x] File created with frontmatter (model: haiku, read-only tools; `color: green` added per agent-development skill, matching existing agents) and body (input/output contracts, read-only invariant, typical dispatches)
  - [x] Verify: file exists; frontmatter YAML parses and name/description/model/tools match plan exactly; `claude plugin validate ./bpe` exits 0 (live Agent-tool test dispatch deferred to a reloaded session, same as A1/B1; new agents don't register until plugin reload)
  - [x] Documented (README "Agents" inventory section added listing step-executor, validator, cheap-research)
- [x] Step C2: Wire cheap-research into `/bpe:plan` discovery; add `--no-discover` flag
  - [x] Scope defined (bpe/skills/plan/SKILL.md, bpe/skills/brainstorm/SKILL.md, README row)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Plan skill Tool discovery section added (Pass 1 session enumeration + Pass 2 cheap-research dispatch with sample prompt matching the C1 agent's input/output contract); --no-discover flag handled (plus `argument-hint` frontmatter consistency touch); cache to spec.md's External tool candidates section with skip-when-populated and --refresh-discover noted as future work; brainstorm Tool discovery step 4 added with old record step renumbered to 5
  - [x] Verify: greps succeed (cheap-research count 2, no-discover shown, External tool candidates shown); both frontmatters parse as YAML; `claude plugin validate ./bpe` exits 0 (end-to-end `/bpe:plan` and `/bpe:plan --no-discover` runs deferred to a reloaded session, same as A1/B1/C1; updated skills don't take effect until plugin reload and slash commands aren't invocable from a subagent)
  - [x] Documented (in plan skill body + README /bpe:plan row noting --no-discover)

## Component D: /bpe:retrofit skill

- [x] Step D1: Create `bpe/skills/retrofit/SKILL.md`
  - [x] Scope defined (new skill file)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] SKILL.md created with frontmatter (name, description, disable-model-invocation, argument-hint "[--replace]") + 5-step procedure; --replace refuse-unless guard; blindspot placeholder cross-referenced to Component E; tooling Q&A shares Component C's discovery pass incl. bpe:cheap-research dispatch; spec.md output matches brainstorm's Available tooling format
  - [x] Verify: file exists; frontmatter parses as YAML with all four fields asserted; `claude plugin validate ./bpe` exits 0 (live `/bpe:retrofit` refuse/produce-spec invocations deferred to a reloaded session, same as A1/B1/C1/C2; new skills don't register until plugin reload)
  - [x] Documented (README command table row added for /bpe:retrofit)

## Component E: Blindspot pass in brainstorm and retrofit

- [x] Step E1: Add Step 0 blindspot pass to `bpe/skills/brainstorm/SKILL.md`
  - [x] Scope defined (bpe/skills/brainstorm/SKILL.md only; retrofit stays on its D1 placeholder until E2)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Step 0 added before the substantive Q&A (one starting-context question; 3-5 unknown-unknowns framed "you may want to consider"; verbatim `## Starting context` record; proceed to standard Q&A); Saving section updated to place `## Starting context` between `# <title>` and `## Project overview`, matching D1's retrofit ordering
  - [x] Verify: greps succeed (Blindspot pass 1, Starting context 2); frontmatter parses as YAML; `claude plugin validate ./bpe` exits 0 (live `/bpe:brainstorm` blindspot-pass check deferred to a reloaded session, same as A1/B1/C1/C2/D1; updated skills don't take effect until plugin reload)
  - [x] Documented (in skill body)
- [x] Step E2: Add Step 0 blindspot pass to `bpe/skills/retrofit/SKILL.md` and canonical doc
  - [x] Scope defined (bpe/skills/retrofit/SKILL.md + bpe/references/session-management.md)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] retrofit skill Step 3 placeholder replaced with the full blindspot pass mirroring brainstorm's E1 Step 0 (one starting-context question informed by repo state; 3-5 unknown-unknowns framed "you may want to consider"; verbatim answer kept for step 5's `## Starting context`; proceed to shortened Q&A); stale "Component E adds the full blindspot pass" cross-reference from D1 removed; session-management.md gained a "Starting Context Section (spec.md)" doc covering format (H2, verbatim), placement (between `# <title>` and `## Project overview`), and purpose (calibrates plan writer and validator), plus an intro pointer
  - [x] Verify: greps succeed (retrofit "Blindspot pass" 1, session-management "Starting context" 2, retrofit "placeholder" 0); frontmatter parses as YAML with all four fields asserted; `claude plugin validate ./bpe` exits 0 (live `/bpe:retrofit` Step 0 check deferred to a reloaded session, same as A1/B1/C1/C2/D1/E1; updated skills don't take effect until plugin reload)
  - [x] Documented (session-management.md is the canonical doc; retrofit step 3 points to it)

## Component F: implementation-notes.md deviations log

- [ ] Step F1: Extend `step-executor` mode=implement to write deviations
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:agent-development)
  - [ ] Step 6.5 added to mode=implement; gitignore entry added
  - [ ] Verify: greps succeed; test dispatch writes entry
  - [ ] Documented (in agent body)
- [ ] Step F2: Extend mode=finalize to absorb deviations into session summary and clear
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:agent-development, plugin-dev:skill-development)
  - [ ] session-summary Step 2 substep added; step-executor finalize note added; session-management.md format section added
  - [ ] Verify: greps succeed; end-to-end absorbs deviations
  - [ ] Documented (session-management.md canonical)
- [ ] Step F3: Extend `validator` to read implementation-notes.md as diff context
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:agent-development)
  - [ ] Procedure step 3 substep added
  - [ ] Verify: grep succeeds
  - [ ] Documented (in agent body)

## Component G: Plan archive lifecycle

- [ ] Step G1: Add `--archive` and `--regen` flags to `/bpe:plan` with refuse-without-flag
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Flag handling section added; argument-hint updated
  - [ ] Verify: greps succeed; refuse and regen tests pass
  - [ ] Documented (in skill body + README)
- [ ] Step G2: Implement archive routine and design accomplishment.md template
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Archive routine steps added to plan skill; accomplishment.md template added to session-management.md
  - [ ] Verify: greps succeed; end-to-end archives to .ai-sessions/<slug>/
  - [ ] Documented (session-management.md canonical)
- [ ] Step G3: Wire archive prompt into `/bpe:session-summary` at end of `/goal` loop
  - [ ] Scope defined
  - [ ] Tooling loaded
  - [ ] Archive prompt section added to session-summary skill
  - [ ] Verify: end-to-end goal loop fires archive prompt
  - [ ] Documented (in skill body)

## Component H: Autonomous mode for non-code

- [ ] Step H1: Extend `/bpe:goal` pre-flight with verification_command cascade
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Pre-Flight cascade added; brainstorm+retrofit prompt for verification_command when needed; session-management.md format doc added
  - [ ] Verify: greps succeed; end-to-end runs vale on a prose project
  - [ ] Documented (session-management.md canonical)

## Component I: Validator linter integration

- [ ] Step I1: Extend `bpe/agents/validator.md` to run Linters from Tools block
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:agent-development)
  - [ ] Procedure step 4 extended; new subprocess+parse step added; failure handling noted
  - [ ] Verify: greps succeed; vale findings appear in test dispatch
  - [ ] Documented (in agent body)
- [ ] Step I2: Update validator-protocol.md and validate-findings.py for linter findings note
  - [ ] Scope defined
  - [ ] Tooling loaded (python:python)
  - [ ] Linter-sourced findings section added to protocol; validate-findings.py verified against sample linter JSON
  - [ ] Verify: grep succeeds; script accepts linter finding
  - [ ] Documented (validator-protocol.md canonical)

## Component J: Model tier enforcement wiring

- [ ] Step J1: Add `model:` field to all subagent and skill frontmatter per Goal 11 tables
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:agent-development, plugin-dev:skill-development)
  - [ ] step-executor: sonnet, validator: opus, cheap-research: haiku (from C1); skills per Goal 11 table
  - [ ] Verify: greps for each tier count check out (5 opus skills, 8 sonnet skills); agents have model fields
  - [ ] Documented (spec.md Goal 11 IS the doc)

## Component K: Per-user profile system

- [ ] Step K1: Design profile schema and create `bpe/references/model-profiles.md`
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:plugin-settings)
  - [ ] Schema documented with active_profile, per-profile overrides, precedence rules, concrete example
  - [ ] Verify: file exists; greps succeed; YAML example parses
  - [ ] Documented (this file IS the doc)
- [ ] Step K2: Create `bpe/hooks/profile-check.md` UserPromptSubmit warning hook
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:hook-development, plugin-dev:plugin-settings)
  - [ ] Hook created; registered in plugin.json
  - [ ] Verify: file exists; registered; warning fires on mismatch; absent profile fires no warning
  - [ ] Documented (hook body + cross-reference from model-profiles.md)
- [ ] Step K3: Ship example profile file and update README
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:plugin-settings)
  - [ ] .claude/bpe.local.md.example created; README section added
  - [ ] Verify: files exist; example YAML parses; README section present
  - [ ] Documented (README IS user-facing)

## Component L: Version bump to 0.6.0

- [ ] Step L1: Bump `bpe/.claude-plugin/plugin.json` version to 0.6.0
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:plugin-structure)
  - [ ] Version string changed
  - [ ] Verify: grep shows 0.6.0; JSON parses
  - [ ] Documented (no docs change)
