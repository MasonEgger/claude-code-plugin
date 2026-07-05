# TODO: BPE 0.6.0 Redesign

Mirror of plan.md. Check off sub-steps as they land. Each top-level `[ ]` is a step; nested `[ ]` are the Scope/Tooling/Do/Verify/Document sub-steps within it.

## Component A: Skill migration

- [ ] Step A1: Migrate all `bpe/commands/*.md` to `bpe/skills/<name>/SKILL.md`
  - [ ] Scope defined (13 skill dirs under bpe/skills/)
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] All 13 skill dirs created with SKILL.md + `disable-model-invocation: true`
  - [ ] Verify: 13 SKILL.md files exist; `/bpe:` autocomplete shows all
  - [ ] Documented (README note about migration)
- [ ] Step A2: Delete legacy `bpe/commands/` files after verification
  - [ ] Scope defined (empty commands/ dir)
  - [ ] Tooling loaded (plugin-dev:plugin-structure)
  - [ ] Files removed; plugin.json checked
  - [ ] Verify: commands/ empty; /bpe:brainstorm still works
  - [ ] Documented (no new docs)

## Component B: Plan template family and Tools block

- [ ] Step B1: Add Task template and heuristic guidance to `/bpe:plan` skill
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Feature/Task sections added; meta-prompting note; heuristic
  - [ ] Verify: greps for Task/Feature/Meta-prompting succeed; skill body loads
  - [ ] Documented (in skill body)
- [ ] Step B2: Add per-section Tools block schema to `/bpe:plan` skill
  - [ ] Scope defined
  - [ ] Tooling loaded
  - [ ] Tools block schema added; per-step override note; backwards-compat note; validator-protocol.md updated
  - [ ] Verify: greps for Tools:, Validator consults, Tools block succeed
  - [ ] Documented (in skill body + validator-protocol.md)
- [ ] Step B3: Make execute-plan skill and step-executor agent template-agnostic
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development, plugin-dev:agent-development)
  - [ ] execute-plan wording changed; step-executor mode=implement step 3 rewritten; step-executor-protocol.md note added
  - [ ] Verify: no "TDD step" remains; "Feature or Task" note added; "sub-steps as written" wording present
  - [ ] Documented (in agent/skill bodies)

## Component C: bpe:cheap-research subagent + tool discovery pass

- [ ] Step C1: Create `bpe:cheap-research` subagent at `bpe/agents/cheap-research.md`
  - [ ] Scope defined (new agent file)
  - [ ] Tooling loaded (plugin-dev:agent-development)
  - [ ] File created with frontmatter (model: haiku, read-only tools) and body
  - [ ] Verify: file exists; frontmatter parses; test dispatch returns shortlist
  - [ ] Documented (README agent inventory updated)
- [ ] Step C2: Wire cheap-research into `/bpe:plan` discovery; add `--no-discover` flag
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Plan skill dispatches cheap-research; --no-discover flag handled; cache to spec.md's External tool candidates section; brainstorm extended
  - [ ] Verify: greps succeed; end-to-end dispatch works; --no-discover skips
  - [ ] Documented (in plan skill body + README)

## Component D: /bpe:retrofit skill

- [ ] Step D1: Create `bpe/skills/retrofit/SKILL.md`
  - [ ] Scope defined (new skill file)
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] SKILL.md created with frontmatter + 5-step procedure; --replace flag; blindspot placeholder cross-referenced to Component E
  - [ ] Verify: file exists; --replace refuses without flag when spec exists; produces spec on spec-less repo
  - [ ] Documented (README command table row added)

## Component E: Blindspot pass in brainstorm and retrofit

- [ ] Step E1: Add Step 0 blindspot pass to `bpe/skills/brainstorm/SKILL.md`
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:skill-development)
  - [ ] Step 0 added; Saving section updated to expect `## Starting context`
  - [ ] Verify: greps succeed; live invocation shows blindspot pass
  - [ ] Documented (in skill body)
- [ ] Step E2: Add Step 0 blindspot pass to `bpe/skills/retrofit/SKILL.md` and canonical doc
  - [ ] Scope defined
  - [ ] Tooling loaded
  - [ ] retrofit skill Step 3 placeholder replaced; session-management.md Starting context doc added
  - [ ] Verify: greps succeed; live invocation runs Step 0
  - [ ] Documented (session-management.md is canonical)

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
