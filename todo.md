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

- [x] Step F1: Extend `step-executor` mode=implement to write deviations
  - [x] Scope defined (bpe/agents/step-executor.md + .gitignore; repo working copy only, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:agent-development)
  - [x] Deviations-log step inserted into Mode: implement between Tree snapshot and Implement-Report emission, renumbered to whole numbers (new step 7; report emission became step 8; Bundled cross-reference updated to "steps 1-7"); entry format per plan (`## Step N` heading with `- Plan said:` / `- Deviated:` / `- Impact:` lines, skip when no deviation, create file if absent); `.ai-sessions/implementation-notes.md` appended to .gitignore
  - [x] Verify: greps succeed (step-executor implementation-notes.md 1, .gitignore implementation-notes.md 1); step position and renumbering confirmed by reading the section; `claude plugin validate ./bpe` exits 0 (live test dispatch that writes an entry deferred to a reloaded session, same as A1/B1/C1/C2/D1/E1/E2; updated agents don't take effect until plugin reload)
  - [x] Documented (in agent body)
- [x] Step F2: Extend mode=finalize to absorb deviations into session summary and clear
  - [x] Scope defined
  - [x] Tooling loaded (skills not reloaded; finished a half-applied F2 edit inline, conventions matched from F1 and existing sections)
  - [x] session-summary Step 2 substep added; step-executor finalize note added; session-management.md format section added (plus a directory-structure bullet for the file)
  - [x] Verify: greps succeed (session-summary "Deviations from Plan" 1, session-management implementation-notes 4, step-executor implementation-notes 2); `claude plugin validate ./bpe` exits 0; end-to-end implement+finalize round trip deferred to a reloaded session, same as F1
  - [x] Documented (session-management.md canonical)
- [x] Step F3: Extend `validator` to read implementation-notes.md as diff context
  - [x] Scope defined (bpe/agents/validator.md only; repo working copy, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:agent-development)
  - [x] Procedure step 3 substep added: read `.ai-sessions/implementation-notes.md` if present, treat `## Step N` sections as accepted deviation context rather than findings; format referenced to the "implementation-notes.md Format" section of session-management.md instead of restated
  - [x] Verify: grep succeeds (validator implementation-notes.md 1); `claude plugin validate ./bpe` exits 0
  - [x] Documented (in agent body)

## Component G: Plan archive lifecycle

- [x] Step G1: Add `--archive` and `--regen` flags to `/bpe:plan` with refuse-without-flag
  - [x] Scope defined (bpe/skills/plan/SKILL.md + README row; repo working copy, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Flag handling section added at top of procedure (absent → fresh; present + no flag → refuse with date and N/M; `--archive` → archive routine placeholder, filled by G2; `--regen` → delete + regenerate); argument-hint merged with C2's flag to `"[--archive | --regen] [--no-discover]"`
  - [x] Verify: greps succeed (`--archive` 6, `--regen` 5); frontmatter parses as YAML; `claude plugin validate ./bpe` exits 0; interactive refuse/regen tests deferred to a reloaded session, same as A1-F2
  - [x] Documented (in skill body + README /bpe:plan row)
- [x] Step G2: Implement archive routine and design accomplishment.md template
  - [x] Scope defined (bpe/skills/plan/SKILL.md + bpe/references/session-management.md; repo working copy, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Archive routine steps added to plan skill (slug propose + user confirm, mkdir, mv plan.md/todo.md, write accomplishment.md, then fresh plan); accomplishment.md template + archive layout section added to session-management.md with a Directory Structure bullet
  - [x] Verify: greps succeed (Archive routine 2, accomplishment.md 7); frontmatter parses as YAML; `claude plugin validate ./bpe` exits 0; end-to-end `--archive` run with stub files deferred to a reloaded session, same as A1-G1
  - [x] Documented (session-management.md canonical)
- [x] Step G3: Wire archive prompt into `/bpe:session-summary` at end of `/goal` loop
  - [x] Scope defined (bpe/skills/session-summary/SKILL.md; repo working copy, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Archive prompt section added as new Step 5 (Confirm renumbered to Step 6, same precedent as F1); guards: skip inside step-executor mode=finalize dispatches, prompt only after the goal loop ends with todo.md present and non-zero checked items; yes-path follows the plan skill's Archive routine inline (slug confirmation included) but stops before fresh-plan generation; no-path notes /bpe:plan will refuse until archived
  - [x] Verify: `grep -i "archive prompt"` hits 3 (heading is Title Case per house style, so the plan's exact-case grep needs -i); frontmatter parses as YAML; `claude plugin validate ./bpe` exits 0; end-to-end goal-loop-to-archive-prompt run deferred to a reloaded session, same as A1-G2
  - [x] Documented (in skill body; Step 6 Confirm now reports the archive outcome)

## Component H: Autonomous mode for non-code

- [x] Step H1: Extend `/bpe:goal` pre-flight with verification_command cascade
  - [x] Scope defined (bpe/skills/goal/SKILL.md, bpe/skills/brainstorm/SKILL.md, bpe/skills/retrofit/SKILL.md, bpe/references/session-management.md; repo working copy, installed cache untouched)
  - [x] Tooling loaded (plugin-dev:skill-development)
  - [x] Pre-Flight cascade added (manifest autodetect → spec.md `**Verification command:**` field → ask user); goal Step 2 wording now covers non-test commands like `vale docs/` (drop the "with no failing tests" clause; exit 0 is the whole signal) and the refusal bullet names the full cascade; brainstorm Tool discovery gained step 5 prompting for the command when no manifest matches (field goes between **Skills:** and **Notes:**); retrofit step 4 tooling bullet asks the same; session-management.md gained "Available Tooling Section (spec.md)" documenting the section format including the field, intro line updated per G2 precedent
  - [x] Verify: `grep "Verification command"` hits in goal SKILL (2 lines) and session-management.md (2 lines), plus brainstorm and retrofit; all three touched SKILL.md frontmatters parse as YAML; `claude plugin validate ./bpe` exits 0; end-to-end vale-on-a-prose-repo run deferred to a reloaded session, same as A1-G3
  - [x] Documented (session-management.md canonical)

## Component I: Validator linter integration

- [x] Step I1: Extend `bpe/agents/validator.md` to run Linters from Tools block
  - [x] Scope defined (bpe/agents/validator.md only)
  - [x] Tooling loaded (plugin-dev:agent-development)
  - [x] Procedure step 4 extended (Linters read from Tools block, legacy/none handling); new step 5 runs linters via Bash and parses output into schema findings with severity mapping and linter check ID as `rule`; linter-fails-to-run recorded in `notes`, not a hard failure; downstream steps renumbered 6-9
  - [x] Verify: greps succeed (`Linters` 3 hits, `linter check ID` 1 hit); frontmatter parses as YAML and tools already include Bash; `claude plugin validate ./bpe` exits 0 (end-to-end vale-on-a-prose-diff dispatch deferred to a reloaded session, same as A1/B1/C1/F1; updated agents don't take effect until plugin reload)
  - [x] Documented (in agent body)
- [x] Step I2: Update validator-protocol.md and validate-findings.py for linter findings note
  - [x] Scope defined (bpe/references/validator-protocol.md only; validate-findings.py evaluated, unchanged)
  - [x] Tooling loaded (python:python)
  - [x] Linter-sourced findings section added to protocol (same schema for all sources, `rule` carries linter check ID, severity mapping matches validator.md step 5, cross-ref to Tools block, failed-to-run linters land in `notes`); validate-findings.py verified against sample linter JSON
  - [x] Verify: grep hits (`Linter-sourced findings` at line 101); script accepts linter-shaped finding (verdict warn, rule vale.OverusedPhrases) with exit 0, so validate-findings.py needed no changes (schema is source-agnostic: linter fields are covered by the existing required + optional finding keys); `claude plugin validate ./bpe` exits 0
  - [x] Documented (validator-protocol.md canonical)

## Component J: Model tier enforcement wiring

- [x] Step J1: Add `model:` field to all subagent and skill frontmatter per Goal 11 tables
  - [x] Scope defined (3 agents + 13 SKILL.md files; cheap-research already `model: haiku` from C1, no edit)
  - [x] Tooling loaded (plugin-dev:agent-development, plugin-dev:skill-development)
  - [x] step-executor: sonnet, validator: opus, cheap-research: haiku (from C1); skills per Goal 11 table (`model:` placed directly above `disable-model-invocation: true` in all 13)
  - [x] Verify: greps for each tier count check out (5 opus skills, 8 sonnet skills); agents have model fields (plan's literal `grep -A1 "^---" | grep "^model:"` pipeline can't match due to multi-file filename prefixes; direct `grep "^model:" bpe/agents/*.md` shows all 3); all 16 frontmatters parse as YAML; `claude plugin validate ./bpe` exits 0; live tier verification deferred to plugin reload per A1-I2 precedent
  - [x] Documented (spec.md Goal 11 IS the doc)

## Component K: Per-user profile system

- [x] Step K1: Design profile schema and create `bpe/references/model-profiles.md`
  - [x] Scope defined
  - [x] Tooling loaded (plugin-dev:plugin-settings)
  - [x] Schema documented with active_profile, per-profile overrides, precedence rules, concrete example
  - [x] Verify: file exists; greps succeed; YAML example parses (both fenced examples validated via PyYAML; concrete example asserted against Goal 11 values); `claude plugin validate ./bpe` exits 0
  - [x] Documented (this file IS the doc; cross-reference added to spec.md Goal 11)
- [x] Step K2: Create `bpe/hooks/profile-check.md` UserPromptSubmit warning hook
  - [x] Scope defined
  - [x] Tooling loaded (plugin-dev:hook-development, plugin-dev:plugin-settings)
  - [x] Hook created; registered in plugin.json (prompt hook config in `bpe/hooks/profile-check.json`, referenced via plugin.json `hooks` field; `.md` is the canonical body/doc since hook configs are JSON)
  - [x] Verify: file exists; registered; plugin.json and profile-check.json parse; embedded response JSON parses with warning wording; `claude plugin validate ./bpe` exits 0; end-to-end hook-firing tests (warning on mismatch, silence absent bpe.local.md) deferred to a reloaded interactive session per A1-K1 precedent
  - [x] Documented (hook body + cross-reference from model-profiles.md)
- [ ] Step K3: Ship example profile file and update README
  - [ ] Scope defined
  - [ ] Tooling loaded (plugin-dev:plugin-settings)
  - [ ] .claude/bpe.local.md.example created; README section added
  - [ ] Verify: files exist; example YAML parses; README section present
  - [ ] Documented (README IS user-facing)

## Component L: Version bump to 0.6.0

- [x] Step L1: Bump `bpe/.claude-plugin/plugin.json` version to 0.6.0
  - [x] Scope defined
  - [x] Tooling loaded (plugin-dev:plugin-structure)
  - [x] Version string changed
  - [x] Verify: grep shows 0.6.0; JSON parses
  - [x] Documented (no docs change; landed early at Mason's direction on 2026-07-15 to ship the completed components, while F2-K remain open)
