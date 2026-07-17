# Implementation Plan: BPE 0.6.0 Redesign

Task-shape plan (per spec.md's Plan generation approach). No TDD ritual. Every step is Scope / Tooling / Do / Verify / Document. Verification is concrete: file exists, slash command resolves, YAML parses, hook fires, etc.

## Current Status

- [ ] Component A: Skill migration (2 steps)
- [ ] Component B: Plan template family and Tools block (3 steps)
- [ ] Component C: bpe:cheap-research subagent + tool discovery pass (2 steps)
- [ ] Component D: /bpe:retrofit skill (1 step)
- [ ] Component E: Blindspot pass in brainstorm and retrofit (2 steps)
- [ ] Component F: implementation-notes.md deviations log (3 steps)
- [ ] Component G: Plan archive lifecycle (3 steps)
- [ ] Component H: Autonomous mode for non-code (1 step)
- [ ] Component I: Validator linter integration (2 steps)
- [ ] Component J: Model tier enforcement wiring (1 step)
- [ ] Component K: Per-user profile system (3 steps)
- [ ] Component L: Version bump to 0.6.0 (1 step)

Total: 24 steps across 12 components. Component A is bootstrap; B-K proceed largely in parallel afterward per spec's ordering constraint (`A → B → C → D → E → F → G → H → I → J → K`). Component L (version bump) lands last after convergence.

## Component A: Skill migration

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development, plugin-dev:plugin-structure, plugin-dev:command-development

### Step A1: Migrate all `bpe/commands/*.md` to `bpe/skills/<name>/SKILL.md` (task)

**NOTE**: Mechanical migration. Commands and skills are unified in Claude Code — same `/bpe:<name>` invocation surface. This step ONLY moves files and adds baseline frontmatter (`disable-model-invocation: true`). Model tier assignments land in Component J.

```text
1. Scope:
   - Artifact(s): bpe/commands/*.md (13 files) → bpe/skills/<name>/SKILL.md
   - Bundled asset: bpe/scripts/review-server.py and review.css stay at bpe/scripts/ (referenced by the review skill via ${CLAUDE_PLUGIN_ROOT}/scripts/).
   - Desired end state: 13 skill directories exist under bpe/skills/, each with a SKILL.md containing the original command content plus `disable-model-invocation: true` in frontmatter. Old bpe/commands/ files remain (deleted in A2 after verification).

2. Tooling:
   - Skills: plugin-dev:skill-development (invoke via Skill tool for canonical SKILL.md format)
   - MCPs: none
   - External: none

3. Do the work:
   - Create bpe/skills/ directory.
   - For each command file in bpe/commands/{brainstorm,plan,execute-plan,gh-issue,commit-message,review,apply-review,handoff,session-summary,lessons,wtf-wid,goal}.md:
     a. Create directory bpe/skills/<name>/
     b. Copy the command file's body to bpe/skills/<name>/SKILL.md
     c. Preserve the existing frontmatter fields (description, argument-hint, allowed-tools)
     d. Add `disable-model-invocation: true` to the frontmatter
     e. Add `name: <name>` field to the frontmatter (Claude Code uses directory name by default; explicit for clarity)
   - Do NOT change any body content in this step. Body edits per component happen later.

4. Verify:
   - Run `ls bpe/skills/*/SKILL.md | wc -l` → expect 13.
   - Run `grep -l "disable-model-invocation: true" bpe/skills/*/SKILL.md | wc -l` → expect 13.
   - Reload the plugin (or restart Claude Code) and type `/bpe:` — expect the same 13 commands to autocomplete under the `bpe:` namespace.
   - Invoke `/bpe:wtf-wid` and confirm the skill body renders in the session (no error about missing skill).

5. Document:
   - Add a note to bpe/README.md that BPE commands migrated to skills in 0.6.0. Explain that `/bpe:<name>` invocation is unchanged; the underlying file layout moved from `commands/` to `skills/<name>/SKILL.md`.
```

### Step A2: Delete legacy `bpe/commands/` files after verification (task)

**NOTE**: Only after A1's verification passes cleanly. Deletion is a discrete step so it can be rolled back if any invocation regressions surface.

```text
1. Scope:
   - Artifact(s): bpe/commands/*.md (13 files)
   - Desired end state: bpe/commands/ directory is empty or removed. All BPE commands invoke as skills.

2. Tooling:
   - Skills: plugin-dev:plugin-structure
   - MCPs: none
   - External: none

3. Do the work:
   - Run `rm bpe/commands/*.md` to delete all migrated command files.
   - Run `rmdir bpe/commands` to remove the now-empty directory. (Leave it if `rmdir` fails because of hidden files.)
   - Check bpe/.claude-plugin/plugin.json for any `commands:` field or path reference. If present, remove; skills are auto-discovered from the skills/ subdirectory.

4. Verify:
   - Run `ls bpe/commands/ 2>&1 || echo removed` → expect "removed" or empty.
   - Run `/bpe:brainstorm` and confirm it works (invoke it and observe the Q&A start).
   - Run `git status` and confirm the deletions appear as expected.

5. Document:
   - No user-facing docs need changes beyond the A1 README note.
```

## Component B: Plan template family and Tools block

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development

### Step B1: Add Task template and heuristic guidance to `/bpe:plan` skill (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/plan/SKILL.md
   - Desired end state: SKILL.md contains a new "Task template" section alongside the existing "Feature template" (renamed from the current unlabeled default). Task template shape matches spec.md's Goal 1: Scope / Tooling / Do / Verify / Document. Marker `(task)` in step title. Executor is template-agnostic.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Read bpe/skills/plan/SKILL.md.
   - Rename the current "Format for Each Step Prompt" section to "Feature template (TDD RED/GREEN/REFACTOR)".
   - Add a new "Task template (non-TDD generic)" section below it with the sub-step shape from spec.md Goal 1: Scope / Tooling / Do / Verify / Document.
   - Add the plan-writer heuristic: use Feature when a bug could hide (new logic, custom validation, novel algorithm); use Task for wiring, renames, config, dependency management, docs, scaffolding, refactors with no behavior change, or non-code work. Fallback: if uncertain, use Feature.
   - Add the meta-prompting note from spec.md Goal 1: numbered sub-steps ARE prompts the executor follows literally, applies to both templates.

4. Verify:
   - Run `grep -c "Task template" bpe/skills/plan/SKILL.md` → expect ≥1.
   - Run `grep -c "Feature template" bpe/skills/plan/SKILL.md` → expect ≥1.
   - Run `grep -c "Meta-prompting" bpe/skills/plan/SKILL.md` → expect ≥1.
   - Invoke `/bpe:plan` in a test session and confirm the skill body loads without YAML parse error.

5. Document:
   - The plan skill's own body documents both templates. No additional docs update.
```

### Step B2: Add per-section Tools block schema to `/bpe:plan` skill (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/plan/SKILL.md, bpe/references/validator-protocol.md
   - Desired end state: plan skill instructs the plan writer to emit `**Tools:**` per section with Skills / MCPs / Linters sub-fields. Transitional read: validator honors legacy `**Validator consults:**` block name.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/plan/SKILL.md "Per-section validator declarations" section (or replace it with a "Per-section Tools block" section) using spec.md Goal 2's format:
     ```
     **Tools:**
     - Skills: <comma-separated>
     - MCPs: <comma-separated>
     - Linters: <comma-separated shell commands>
     ```
   - Add a note that a `**Tools:**` block per section shadows the section default; a `**Tools:**` block per step shadows the section default further.
   - Add a "Backwards compatibility" note that existing plans with `**Validator consults:**` still work — validator honors the old block name and treats it as Skills+MCPs with empty Linters.
   - Edit bpe/references/validator-protocol.md to add a "Tools block" section documenting the schema (Skills / MCPs / Linters) and the transitional read.

4. Verify:
   - Run `grep -A5 "Tools:" bpe/skills/plan/SKILL.md | head -20` → shows the new block schema.
   - Run `grep "Validator consults" bpe/skills/plan/SKILL.md` → shows the backwards-compat note.
   - Run `grep "Tools block" bpe/references/validator-protocol.md` → shows the schema note.

5. Document:
   - Updates to plan skill body and validator-protocol.md are the docs. No additional README changes.
```

### Step B3: Make execute-plan skill and step-executor agent template-agnostic (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/execute-plan/SKILL.md, bpe/agents/step-executor.md, bpe/references/step-executor-protocol.md
   - Desired end state: execute-plan and step-executor mode=implement instructions no longer say "TDD step" or "Failing test, minimal code to pass, refactor". Instead: "Execute the numbered sub-steps for the current todo item as written in plan.md." Both templates supported implicitly by literal sub-step execution.

2. Tooling:
   - Skills: plugin-dev:skill-development, plugin-dev:agent-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/execute-plan/SKILL.md step 7. Change "Follow strict TDD procedures (RED-GREEN-REFACTOR as specified)" to "Follow the specified sub-steps as written in plan.md (RED/GREEN/REFACTOR for Feature steps; Scope/Tooling/Do/Verify/Document for Task steps)."
   - Add a note near step 7 that plan.md may mix Feature and Task steps; executor honors whichever shape is present.
   - Edit bpe/agents/step-executor.md Mode: implement section, step 3. Change "TDD step. Read execute-plan.md... Failing test, minimal code to pass, refactor" to "Execute the sub-steps for the current todo item as written in plan.md. Read execute-plan.md and follow its numbered procedure inline."
   - Edit bpe/references/step-executor-protocol.md to add a note under "Mode contracts" that mode=implement executes whichever template shape plan.md declares (Feature or Task).

4. Verify:
   - Run `grep -c "TDD step" bpe/agents/step-executor.md` → expect 0 (removed).
   - Run `grep -c "Feature or Task" bpe/references/step-executor-protocol.md` → expect ≥1.
   - Run `grep -c "sub-steps as written" bpe/skills/execute-plan/SKILL.md` → expect ≥1.

5. Document:
   - Updates to skill and agent bodies are the docs. No README changes.
```

## Component C: bpe:cheap-research subagent + tool discovery pass

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:agent-development, plugin-dev:skill-development

### Step C1: Create `bpe:cheap-research` subagent at `bpe/agents/cheap-research.md` (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/cheap-research.md (new)
   - Desired end state: New subagent file with `model: haiku`, read-only tools (WebFetch, WebSearch, Read, Grep, Glob), and a contract spec for structured input/output.

2. Tooling:
   - Skills: plugin-dev:agent-development
   - MCPs: none
   - External: none

3. Do the work:
   - Create bpe/agents/cheap-research.md with frontmatter per spec.md Goal 10:
     ```yaml
     ---
     name: cheap-research
     description: Fast, cheap external research subagent for tool discovery, docs lookup, quick fact-checks. Dispatched by /bpe:plan, /bpe:brainstorm, /bpe:retrofit when they need external info.
     model: haiku
     tools: WebFetch, WebSearch, Read, Grep, Glob
     ---
     ```
   - Write the agent body with: role statement, input contract (research question + return-shape spec), output contract (structured data matching spec, or "no relevant results"), read-only invariant (no writes), examples of typical dispatches (tool discovery, docs lookup, fact-check).

4. Verify:
   - Run `ls bpe/agents/cheap-research.md` → file exists.
   - Run `head -20 bpe/agents/cheap-research.md` → frontmatter parses; name/model/tools correct.
   - Manually dispatch the subagent via Agent tool with a test research question ("find Claude Code plugins related to Ansible"); confirm structured shortlist returns.

5. Document:
   - Update bpe/README.md to list bpe:cheap-research alongside step-executor and validator in the agent inventory.
```

### Step C2: Wire cheap-research into `/bpe:plan` discovery pass; add `--no-discover` flag (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/plan/SKILL.md, bpe/skills/brainstorm/SKILL.md
   - Desired end state: `/bpe:plan` dispatches cheap-research for external tool discovery by default. Flag `--no-discover` skips Pass 2. Results cache to spec.md under `## External tool candidates`. brainstorm skill optionally dispatches cheap-research at user's request during Available tooling Q&A.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/plan/SKILL.md to add a "Tool discovery" section describing Pass 1 (session enumeration, existing) and Pass 2 (cheap-research dispatch, new). Include the sample dispatch prompt for cheap-research: "Given the project domain in spec.md's Project overview, find installed marketplace skills and public plugins that could apply. Rank by relevance. Return up to 10."
   - Add `--no-discover` flag handling: if present in $ARGUMENTS, skip Pass 2.
   - Add cache handling: after Pass 2 returns, append results to spec.md under `## External tool candidates` (if section absent, create it). Skip Pass 2 on subsequent runs when the section is already populated (or the user re-runs with `--refresh-discover`, future work).
   - Edit bpe/skills/brainstorm/SKILL.md's Tool discovery step to add: "If the user wants suggestions for external tools not in the session, dispatch the bpe:cheap-research subagent with the project domain; present the shortlist for user confirmation."

4. Verify:
   - Run `grep -c "cheap-research" bpe/skills/plan/SKILL.md` → expect ≥2.
   - Run `grep "no-discover" bpe/skills/plan/SKILL.md` → shows flag documentation.
   - Run `grep "External tool candidates" bpe/skills/plan/SKILL.md` → shows cache section.
   - End-to-end: run `/bpe:plan` on a test spec.md and confirm Pass 2 dispatches (transcript shows cheap-research invocation).
   - Run `/bpe:plan --no-discover` on the same and confirm Pass 2 is skipped.

5. Document:
   - Plan skill body documents the new behavior. Add a bullet to bpe/README.md's /bpe:plan row about `--no-discover`.
```

## Component D: /bpe:retrofit skill

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development

### Step D1: Create `bpe/skills/retrofit/SKILL.md` (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/retrofit/SKILL.md (new)
   - Desired end state: New skill for adding a BPE-compatible spec.md to an existing project that lacks one. Reads repo state, runs shortened Q&A, writes spec.md.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Create bpe/skills/retrofit/SKILL.md with frontmatter: name: retrofit, disable-model-invocation: true, description: "Retrofit a BPE-compatible spec.md onto an existing project that lacks one. Reads repo state and runs a shortened Q&A focused on gaps.", argument-hint: "[--replace]".
   - Body procedure (numbered):
     1. Refuse if spec.md already exists at repo root, unless `--replace` in $ARGUMENTS.
     2. Read repo state: `ls`, `cat README.md` (if present), `cat CLAUDE.md` (if present), manifest files (package.json / pyproject.toml / go.mod / Cargo.toml), top-level module docstrings if language-detectable.
     3. Run blindspot pass (placeholder for Component E; short version: ask user's starting context, surface 3-5 unknown-unknowns).
     4. Run shortened Q&A: project goal, currently in-place vs planned, tooling to declare (share Component C's discovery pass), out of scope.
     5. Write spec.md at repo root matching the format /bpe:plan consumes (Project overview, Starting context, Available tooling, Goals, Non-goals, Component boundaries, Success criteria).
   - Cross-reference: mention that Component E adds the full blindspot pass; this skill uses the placeholder version until E lands.

4. Verify:
   - Run `ls bpe/skills/retrofit/SKILL.md` → file exists.
   - Invoke `/bpe:retrofit` on a test repo without spec.md → produces spec.md.
   - Invoke `/bpe:retrofit` on a repo with existing spec.md → refuses; `/bpe:retrofit --replace` proceeds.

5. Document:
   - Add row to bpe/README.md command table for /bpe:retrofit.
```

## Component E: Blindspot pass in brainstorm and retrofit

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development

### Step E1: Add Step 0 blindspot pass to `bpe/skills/brainstorm/SKILL.md` (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/brainstorm/SKILL.md
   - Desired end state: Brainstorm skill runs a blindspot pass as Step 0 before the substantive Q&A. Records user's starting context verbatim in spec.md under `## Starting context`.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/brainstorm/SKILL.md to add a "Step 0: Blindspot pass" section before the substantive Q&A:
     1. Ask ONE question about starting context (domain familiarity, prior attempts, codebase experience).
     2. Given the answer, surface 3-5 unknown-unknowns as questions the user probably doesn't know to ask. Frame as "you may want to consider" rather than "you must answer".
     3. Record the user's context answer verbatim in spec.md under `## Starting context` (create the section if it doesn't exist).
     4. Proceed to the standard Q&A.
   - Update the "Saving" section to note that `## Starting context` is now expected in spec.md between `# <title>` and `## Project overview`.

4. Verify:
   - Run `grep "Blindspot pass" bpe/skills/brainstorm/SKILL.md` → shows section.
   - Run `grep "Starting context" bpe/skills/brainstorm/SKILL.md` → shows section reference.
   - Invoke `/bpe:brainstorm` and confirm turn 1 asks a starting-context question then surfaces unknown-unknowns.

5. Document:
   - Brainstorm skill body documents Step 0. No README changes.
```

### Step E2: Add same Step 0 blindspot pass to `bpe/skills/retrofit/SKILL.md` (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/retrofit/SKILL.md, bpe/references/session-management.md
   - Desired end state: Retrofit skill runs the same blindspot pass Step 0. session-management.md documents the `## Starting context` section format canonically.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/retrofit/SKILL.md to replace the Step 3 blindspot-pass placeholder from Component D with the full blindspot pass (same shape as Component E1's Step 0).
   - Add a "Starting context section" doc to bpe/references/session-management.md: format (H2 heading, verbatim user context), placement (between `# <title>` and `## Project overview`), purpose (calibrates plan writer and validator).

4. Verify:
   - Run `grep "Blindspot pass" bpe/skills/retrofit/SKILL.md` → shows section.
   - Run `grep "Starting context" bpe/references/session-management.md` → shows the doc.
   - Invoke `/bpe:retrofit` on a fresh test repo and confirm Step 0 runs.

5. Document:
   - session-management.md is the canonical doc.
```

## Component F: implementation-notes.md deviations log

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:agent-development

### Step F1: Extend `bpe/agents/step-executor.md` mode=implement to write deviations (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/step-executor.md, .gitignore
   - Desired end state: mode=implement appends deviations to .ai-sessions/implementation-notes.md before emitting Implement-Report. File is gitignored.

2. Tooling:
   - Skills: plugin-dev:agent-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/agents/step-executor.md Mode: implement section, add a new step between existing 6 (Tree snapshot) and 7 (Emit Implement-Report):
     "6.5. Deviations log. If your work in step 3 deviated from plan.md's prescription for this step (edge case, blocked path, better approach found mid-work), append a one-line entry to .ai-sessions/implementation-notes.md under a `## Step N` heading. Format: `- Plan said: <what>` / `- Deviated: <what actually happened>` / `- Impact: <consequence>`. If no deviation, skip. Create the file if it doesn't exist."
   - Renumber subsequent steps (Emit Implement-Report becomes step 8).
   - Add `.ai-sessions/implementation-notes.md` to .gitignore (append if section for .ai-sessions/ exists, else add).

4. Verify:
   - Run `grep "implementation-notes.md" bpe/agents/step-executor.md` → shows the new step.
   - Run `grep "implementation-notes.md" .gitignore` → gitignored.
   - Dispatch step-executor mode=implement on a test todo item where you know a deviation is likely; confirm .ai-sessions/implementation-notes.md gets an entry.

5. Document:
   - Agent body documents the behavior.
```

### Step F2: Extend mode=finalize to absorb deviations into session summary and clear (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/step-executor.md, bpe/skills/session-summary/SKILL.md, bpe/references/session-management.md
   - Desired end state: mode=finalize's session-summary step reads implementation-notes.md, extracts the step's `## Step N` section, adds a `## Deviations from Plan` section to the session summary, then clears the step's section from implementation-notes.md.

2. Tooling:
   - Skills: plugin-dev:agent-development, plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/session-summary/SKILL.md Step 2 (Generate Session Summary): add substep "If .ai-sessions/implementation-notes.md exists and contains a `## Step <current step N>` section, extract its bullets and add a `## Deviations from Plan` section to the session summary with them. Then remove the `## Step N` section from implementation-notes.md (keep the file if other sections remain, else delete the file)."
   - Edit bpe/agents/step-executor.md Mode: finalize section, step 3 (Session summary). Add: "The session summary skill's procedure now absorbs deviations from .ai-sessions/implementation-notes.md; follow it inline as before."
   - Edit bpe/references/session-management.md to add an "implementation-notes.md format" section documenting: purpose (mid-step deviation tracking), format (`## Step N` heading + bullet list with `Plan said:` / `Deviated:` / `Impact:`), lifecycle (created by mode=implement, absorbed by mode=finalize, gitignored).

4. Verify:
   - Run `grep "Deviations from Plan" bpe/skills/session-summary/SKILL.md` → shows section.
   - Run `grep "implementation-notes.md" bpe/references/session-management.md` → shows the doc.
   - End-to-end: run a full mode=implement + mode=finalize on a step with a deviation; confirm the resulting session summary contains the deviations and implementation-notes.md no longer contains that step's section.

5. Document:
   - session-management.md is the canonical doc.
```

### Step F3: Extend `bpe/agents/validator.md` to read implementation-notes.md as diff context (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/validator.md
   - Desired end state: Validator dispatch reads .ai-sessions/implementation-notes.md before reviewing the diff. Uses recorded deviations to contextualize findings (does not fire on a "suspicious" diff when the deviation is documented).

2. Tooling:
   - Skills: plugin-dev:agent-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/agents/validator.md Procedure step 3 (Obtain the diff). Add substep: "Also read .ai-sessions/implementation-notes.md if it exists. Any `## Step N` section corresponds to a documented mid-step deviation; treat those as accepted context when evaluating the diff, not as findings to flag."

4. Verify:
   - Run `grep "implementation-notes.md" bpe/agents/validator.md` → shows the read step.

5. Document:
   - Agent body documents behavior.
```

## Component G: Plan archive lifecycle

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development

### Step G1: Add `--archive` and `--regen` flags to `/bpe:plan` with refuse-without-flag behavior (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/plan/SKILL.md
   - Desired end state: /bpe:plan (no flags) refuses when plan.md exists at repo root with a message pointing at the flags. `--archive` migrates existing plan.md + todo.md to .ai-sessions/<slug>/ then regenerates. `--regen` discards existing plan.md + todo.md and regenerates.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/plan/SKILL.md to add a "Flag handling" section at the top of the procedure:
     - Check for plan.md at repo root.
     - If absent: proceed to generate fresh plan.
     - If present and no flag: refuse with message "plan.md exists (last modified <date>, N/M items checked). Use `--archive` to preserve it in .ai-sessions before regenerating, or `--regen` to discard and regenerate."
     - If present and `--archive`: run the archive routine (Step G2) then generate fresh plan.
     - If present and `--regen`: delete plan.md and todo.md, then generate fresh plan.
   - Add argument-hint update in frontmatter: `argument-hint: "[--archive | --regen]"`.

4. Verify:
   - Run `grep -- "--archive" bpe/skills/plan/SKILL.md` → shows flag handling.
   - Run `grep -- "--regen" bpe/skills/plan/SKILL.md` → shows flag handling.
   - Manual test: create a stub plan.md, invoke /bpe:plan without flags → refuses.
   - Invoke /bpe:plan --regen → regenerates.

5. Document:
   - Plan skill body documents flags. Add flag row to bpe/README.md.
```

### Step G2: Implement the archive routine and design accomplishment.md template (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/plan/SKILL.md, bpe/references/session-management.md
   - Desired end state: --archive flag routine defined: propose slug from what was accomplished, ask user to confirm/edit, mkdir .ai-sessions/<slug>/, move plan.md and todo.md into it, write accomplishment.md with the template from session-management.md.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Add archive routine steps to bpe/skills/plan/SKILL.md (referenced by --archive):
     1. Propose a slug based on plan.md's stated goals and completed todo items (e.g., "init", "v1", "add-user-auth"). Ask user to confirm or edit.
     2. mkdir -p .ai-sessions/<slug>/
     3. mv plan.md .ai-sessions/<slug>/plan.md
     4. mv todo.md .ai-sessions/<slug>/todo.md
     5. Write .ai-sessions/<slug>/accomplishment.md per the template in session-management.md.
     6. Proceed to generate fresh plan.md.
   - Add "accomplishment.md template" section to bpe/references/session-management.md with the format from spec.md Goal 7: archive date, convergence status, spec slice, what got done, what was deferred, notable decisions, files touched, cross-reference to lessons.

4. Verify:
   - Run `grep "Archive routine" bpe/skills/plan/SKILL.md` → shows section.
   - Run `grep "accomplishment.md" bpe/references/session-management.md` → shows template.
   - End-to-end: with a stub plan.md and todo.md, run /bpe:plan --archive; confirm .ai-sessions/<slug>/ contains all three files.

5. Document:
   - session-management.md is the canonical doc for the archive layout.
```

### Step G3: Wire archive prompt into `/bpe:session-summary` at end of `/goal` loop (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/session-summary/SKILL.md
   - Desired end state: session-summary skill, when detected as the last dispatch of a /goal loop, offers an archive prompt: "Archive plan.md and todo.md?" If user confirms, invoke /bpe:plan --archive via inline execution.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/session-summary/SKILL.md to add a "Step 5: Archive prompt (end of /goal only)" section:
     - Detect if this session was driven by /goal (see "Goal Context Populating Rule" in session-management.md).
     - If yes AND todo.md exists at repo root AND has non-zero checked items, ask: "Archive plan.md and todo.md to .ai-sessions/<slug>/?"
     - On yes: follow the archive routine inline (from Component G2). Ask user for slug confirmation.
     - On no: leave plan.md and todo.md at repo root; next /bpe:plan invocation will refuse until archive happens.

4. Verify:
   - Run `grep "Archive prompt" bpe/skills/session-summary/SKILL.md` → shows section.
   - End-to-end: run a /goal loop through convergence, then session-summary; confirm archive prompt fires.

5. Document:
   - session-summary skill body documents behavior.
```

## Component H: Autonomous mode for non-code

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:skill-development

### Step H1: Extend `/bpe:goal` pre-flight with verification_command cascade (task)

```text
1. Scope:
   - Artifact(s): bpe/skills/goal/SKILL.md, bpe/skills/brainstorm/SKILL.md, bpe/skills/retrofit/SKILL.md, bpe/references/session-management.md
   - Desired end state: /bpe:goal pre-flight cascades: autodetected test runner (existing) → spec.md `**Verification command:**` field (new) → user prompt. Goal condition uses resolved command's exit-0 as success signal. brainstorm and retrofit prompt for verification_command when no test runner is autodetectable.

2. Tooling:
   - Skills: plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/skills/goal/SKILL.md Step 1 (Pre-Flight Checks) to add the cascade:
     ```
     Detect the verification command:
     - pyproject.toml present → pytest -q
     - package.json present → npm test --silent
     - Cargo.toml present → cargo test --quiet
     - go.mod present → go test ./...
     - Otherwise: read spec.md's `## Available tooling` section for `**Verification command:**` field. If present, use it.
     - Otherwise: ask the user for the exact verification command.
     ```
   - Edit bpe/skills/brainstorm/SKILL.md's Tool discovery section: if the project's tech stack doesn't match a known test runner, prompt for a verification command and record it under `## Available tooling` `**Verification command:**`.
   - Edit bpe/skills/retrofit/SKILL.md's Q&A step to prompt for verification command in the same case.
   - Edit bpe/references/session-management.md to document the `## Available tooling` section format including the `**Verification command:**` field.

4. Verify:
   - Run `grep "Verification command" bpe/skills/goal/SKILL.md` → shows cascade.
   - Run `grep "Verification command" bpe/references/session-management.md` → shows format.
   - End-to-end: on a test repo with no test runner but with `**Verification command:** vale docs/` in spec.md, run /bpe:goal; confirm it uses vale.

5. Document:
   - session-management.md is the canonical doc.
```

## Component I: Validator linter integration

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:agent-development, python:python

### Step I1: Extend `bpe/agents/validator.md` to run Linters from Tools block (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/validator.md
   - Desired end state: Validator reads the current section's `Linters:` list from plan.md's Tools block. For each linter, runs as subprocess (via Bash tool), parses output into findings JSON. Emits alongside skill/MCP-sourced findings.

2. Tooling:
   - Skills: plugin-dev:agent-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/agents/validator.md Procedure step 4 (Load consultation tools) to add: "Also read the section's `Linters:` list from plan.md. Each entry is a shell command."
   - Add a new Procedure step between 4 and 5 (Review): "Run each linter as a subprocess via Bash. Capture stdout+stderr. Parse into findings JSON per the schema in validator-protocol.md:
     - severity: block for errors, warn for warnings, info for suggestions (map from linter's own severity levels; if the linter emits errors-only, treat all as block).
     - file: path from the linter's output.
     - line: line number if emitted.
     - rule: linter check ID (e.g., vale.OverusedPhrases, ansible-lint.no-changed-when).
     - message: one-line description from the linter.
     - reference: linter config path or documentation URL if available.
     Emit these findings alongside the skill/MCP-sourced findings in the same block."
   - Add a note that if a linter fails to run (not installed, config missing), record it in `notes` and continue with the rest.

4. Verify:
   - Run `grep "Linters" bpe/agents/validator.md` → shows the new section.
   - Run `grep "linter check ID" bpe/agents/validator.md` → shows schema.
   - End-to-end: with a test plan.md section declaring `Linters: vale --config=.vale.ini` on a prose diff, dispatch validator; confirm vale findings appear.

5. Document:
   - Agent body documents behavior.
```

### Step I2: Update validator-protocol.md and validate-findings.py for linter-sourced findings note (task)

```text
1. Scope:
   - Artifact(s): bpe/references/validator-protocol.md, bpe/scripts/validate-findings.py (only if schema changes)
   - Desired end state: Protocol doc has a "Linter-sourced findings" section explaining the pattern. Schema in validate-findings.py handles linter findings correctly (probably already does, since the schema is source-agnostic).

2. Tooling:
   - Skills: python:python
   - MCPs: none
   - External: none

3. Do the work:
   - Add a "Linter-sourced findings" section to bpe/references/validator-protocol.md. Explain: linter findings use the same JSON schema as skill/MCP findings; `rule` field carries the linter check ID; severity maps from linter output. Cross-reference the Tools block schema for how linters get declared.
   - Read bpe/scripts/validate-findings.py. Verify the schema accepts linter-shaped findings (no linter-specific fields required beyond the existing schema). If the schema needs any changes, make them and re-run the script against a synthetic linter-findings JSON to confirm it validates.

4. Verify:
   - Run `grep "Linter-sourced findings" bpe/references/validator-protocol.md` → shows section.
   - Run `bpe/scripts/validate-findings.py` against a test JSON containing a linter-shaped finding (severity: warn, rule: vale.OverusedPhrases, file: docs/intro.md, line: 12, message: "'leverage' overused"). Expect exit 0.

5. Document:
   - validator-protocol.md is the canonical doc.
```

## Component J: Model tier enforcement wiring

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:agent-development, plugin-dev:skill-development

### Step J1: Add `model:` field to all subagent and skill frontmatter per Goal 11 tables (task)

```text
1. Scope:
   - Artifact(s): bpe/agents/step-executor.md, bpe/agents/validator.md, bpe/agents/cheap-research.md, and all bpe/skills/<name>/SKILL.md files
   - Desired end state: Every subagent and every skill has an explicit `model:` field in frontmatter per spec.md Goal 11's tables. Aliases (opus/sonnet/haiku) resolve to latest-in-family automatically.

2. Tooling:
   - Skills: plugin-dev:agent-development, plugin-dev:skill-development
   - MCPs: none
   - External: none

3. Do the work:
   - Edit bpe/agents/step-executor.md frontmatter: change `model: inherit` to `model: sonnet`.
   - Edit bpe/agents/validator.md frontmatter: change `model: inherit` to `model: opus`.
   - Confirm bpe/agents/cheap-research.md frontmatter has `model: haiku` (set in Component C1).
   - Edit each bpe/skills/<name>/SKILL.md frontmatter per Goal 11's skill tier table:
     - brainstorm, retrofit, plan, review, apply-review: `model: opus`
     - execute-plan, commit-message, session-summary, handoff, wtf-wid, lessons, goal, gh-issue: `model: sonnet`

4. Verify:
   - Run `grep -A1 "^---" bpe/agents/*.md | grep "^model:"` → shows model for all 3 agents.
   - Run `for f in bpe/skills/*/SKILL.md; do grep "^model:" $f || echo "$f missing model:"; done` → all skills have model field.
   - Run `grep -l "model: opus" bpe/skills/*/SKILL.md | wc -l` → expect 5 (brainstorm, retrofit, plan, review, apply-review).
   - Run `grep -l "model: sonnet" bpe/skills/*/SKILL.md | wc -l` → expect 8.

5. Document:
   - No user-facing docs change beyond spec.md's Goal 11 tables which already document the mapping.
```

## Component K: Per-user profile system

**Validator consults:**
- MCPs: none
- Skills: plugin-dev:hook-development, plugin-dev:plugin-settings

### Step K1: Design profile schema and create `bpe/references/model-profiles.md` (task)

```text
1. Scope:
   - Artifact(s): bpe/references/model-profiles.md (new)
   - Desired end state: Canonical schema documentation for `.claude/bpe.local.md` profile files. YAML frontmatter format with active_profile toggle, per-profile skills+agents override maps, BPE_PROFILE env var precedence, per-project shadow layer.

2. Tooling:
   - Skills: plugin-dev:plugin-settings
   - MCPs: none
   - External: none

3. Do the work:
   - Create bpe/references/model-profiles.md with the schema from spec.md Goal 11:
     ```yaml
     ---
     active_profile: personal
     profiles:
       personal:
         skills:
           <skill-name>: <model-id-or-alias>
         agents:
           <agent-name>: <model-id-or-alias>
       work:
         skills:
           <skill-name>: <model-id-or-alias>
         agents:
           <agent-name>: <model-id-or-alias>
     ---
     ```
   - Document lookup precedence: (1) BPE_PROFILE env var overrides file's active_profile, (2) per-project .claude/bpe.local.md at repo root overrides user-global ~/.claude/bpe.local.md, (3) profile override map, (4) skill/agent frontmatter default. Fall through to next level if key absent.
   - Document the "Unset skills or subagents fall back to their frontmatter model: field" behavior.
   - Give a concrete example matching spec.md Goal 11's YAML example (personal with claude-opus-4-7 pins, work with opus alias).

4. Verify:
   - Run `ls bpe/references/model-profiles.md` → file exists.
   - Run `grep "active_profile" bpe/references/model-profiles.md` → shows field.
   - Run `grep "BPE_PROFILE" bpe/references/model-profiles.md` → shows env var doc.
   - Manually validate the schema example parses as YAML (paste into a YAML validator).

5. Document:
   - This file IS the doc. Cross-reference from Goal 11 in spec.md.
```

### Step K2: Create `bpe/hooks/profile-check.md` UserPromptSubmit warning hook (task)

```text
1. Scope:
   - Artifact(s): bpe/hooks/profile-check.md (new), bpe/.claude-plugin/plugin.json
   - Desired end state: UserPromptSubmit hook fires when user types a `/bpe:<name>` invocation. Reads .claude/bpe.local.md and (if applicable) BPE_PROFILE env var, resolves the desired model for the skill, checks against the current session model. If mismatch, injects a warning ("current session on X, recommended for this skill: Y. Run /model Y first.").

2. Tooling:
   - Skills: plugin-dev:hook-development, plugin-dev:plugin-settings
   - MCPs: none
   - External: none

3. Do the work:
   - Create bpe/hooks/ directory.
   - Create bpe/hooks/profile-check.md as a prompt-based hook (per plugin-dev:hook-development guidance). Body: read the incoming user prompt from $CLAUDE_USER_PROMPT (or the appropriate env var), check if it starts with `/bpe:`, extract the skill name. Read .claude/bpe.local.md (repo-local first, then ~/.claude/bpe.local.md). Resolve the desired model per Component K1's precedence. If current session model (from $CLAUDE_MODEL, if exposed) differs from resolved model, inject a warning line into the prompt: "Note: skill <name> profile expects model <X>; current session is <Y>. Consider /model <X> before proceeding."
   - Add the hook to bpe/.claude-plugin/plugin.json under the appropriate hooks section (per plugin-dev:hook-development conventions).

4. Verify:
   - Run `ls bpe/hooks/profile-check.md` → file exists.
   - Run `grep "profile-check" bpe/.claude-plugin/plugin.json` → registered.
   - End-to-end: with .claude/bpe.local.md setting brainstorm to claude-opus-4-7 and session on claude-sonnet-4-6, type /bpe:brainstorm; confirm the warning appears in the transcript.
   - Absent .claude/bpe.local.md: hook fires no warning; skills use frontmatter defaults.

5. Document:
   - Hook file body documents its behavior. Cross-reference from bpe/references/model-profiles.md.
```

### Step K3: Ship example profile file and update README (task)

```text
1. Scope:
   - Artifact(s): .claude/bpe.local.md.example (new at repo root), bpe/README.md
   - Desired end state: Example .claude/bpe.local.md file at repo root that users can copy to their own ~/.claude/ or project-local .claude/. README explains the profile system with a getting-started section.

2. Tooling:
   - Skills: plugin-dev:plugin-settings
   - MCPs: none
   - External: none

3. Do the work:
   - Create .claude/bpe.local.md.example at repo root with a commented example matching spec.md Goal 11's YAML sample. Include comments explaining each field.
   - Update bpe/README.md with a "Per-user model profiles" section: point at bpe/references/model-profiles.md as canonical, show a quick usage example (copy .example to `~/.claude/bpe.local.md`, edit active_profile, override per-skill), mention the BPE_PROFILE env var toggle for shell-scoped switching.

4. Verify:
   - Run `ls .claude/bpe.local.md.example` → file exists.
   - Run `grep "Per-user model profiles" bpe/README.md` → shows section.
   - Manually validate the example YAML parses.

5. Document:
   - README section IS the user-facing doc.
```

## Component L: Version bump to 0.6.0

**Validator consults:** none

### Step L1: Bump `bpe/.claude-plugin/plugin.json` version to 0.6.0 (task)

**NOTE**: Lands after all Component A-K work has converged and been validated. Not to be run early.

```text
1. Scope:
   - Artifact(s): bpe/.claude-plugin/plugin.json
   - Desired end state: `"version": "0.6.0"` in the manifest.

2. Tooling:
   - Skills: plugin-dev:plugin-structure
   - MCPs: none
   - External: none

3. Do the work:
   - Read bpe/.claude-plugin/plugin.json.
   - Change `"version": "0.5.0"` to `"version": "0.6.0"`.
   - Ensure no other field changes accidentally.

4. Verify:
   - Run `grep '"version"' bpe/.claude-plugin/plugin.json` → shows 0.6.0.
   - Run `python3 -c "import json; json.load(open('bpe/.claude-plugin/plugin.json'))"` → parses without error.

5. Document:
   - No additional docs.
```

## Implementation Guidelines

- **Task shape only.** Every step's sub-steps are Scope / Tooling / Do / Verify / Document. No RED/GREEN/REFACTOR. No test scenarios. Verification is concrete: file exists, grep succeeds, YAML parses, slash command resolves, hook fires.
- **Skills as bootstrap.** Component A must land first. Every subsequent component edits files under `bpe/skills/<name>/SKILL.md` that exist because of A.
- **Model tier assignments deferred to J.** Components A through I set up structure; J wires the `model:` fields in a single sweep once all skills and agents exist.
- **K depends on J.** The profile-check hook (K2) references frontmatter `model:` fields as the fallback default; those need to exist first.
- **No `--no-verify` bypasses.** Each step's Verify sub-step is a hard gate. If verification fails, mark the step as `Failure:` per BPE convention and stop for user resolution.
- **Meta-prompting discipline.** The numbered sub-steps in each step ARE prompts the executor follows literally, not descriptive summaries. If a sub-step reads ambiguous, the plan is wrong; regenerate that step with `/bpe:plan --regen` (once Component G lands) or edit plan.md by hand.

## Success Metrics

Track convergence against spec.md's Success criteria (11 items). This plan produces the 24 commits that satisfy them.

Per-component convergence:

| Component | Steps | Success signal |
|---|---|---|
| A | 2 | All 13 `/bpe:<name>` commands still work after migration. |
| B | 3 | plan.md can mix Feature and Task steps; executor honors both. |
| C | 2 | `/bpe:plan` dispatches cheap-research; `--no-discover` skips it. |
| D | 1 | `/bpe:retrofit` produces spec.md on a spec-less repo. |
| E | 2 | Brainstorm and retrofit both open with the blindspot pass. |
| F | 3 | Deviations logged mid-implement; absorbed at finalize. |
| G | 3 | `/bpe:plan --archive` migrates plan+todo to `.ai-sessions/<slug>/`. |
| H | 1 | `/bpe:goal` runs on a spec.md-declared verification command. |
| I | 2 | Validator emits Vale findings on a prose section. |
| J | 1 | All frontmatter `model:` fields set per Goal 11 tables. |
| K | 3 | Profile file overrides skill model at invocation time; warning fires on mismatch. |
| L | 1 | plugin.json version bumped to 0.6.0. |

Final gate: all 12 rows check off, `git log` shows 24 commits on `fable` branch, tree is clean, `.ai-sessions/<slug>/accomplishment.md` documents what got done, plugin.json is at 0.6.0.
