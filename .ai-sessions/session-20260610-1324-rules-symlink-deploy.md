# Session Summary: Rules drift fix + symlink-based ansible deploy + lessons promote guard

**Date**: 2026-06-10
**Duration**: ~Multi-turn conversational session (spanning several wall-clock days per system date reminders)
**Conversation Turns**: ~20
**Estimated Cost**: ~$8–12 (heavy Opus session with multiple file reads, ansible runs, and web fetch)
**Model**: claude-opus-4-7

## Key Actions

- Compared the user's BPE plugin against Matt Van Horn's `/ce-plan` + `/ce-work` Compound Engineering workflow (fetched via r.jina.ai mirror). Produced an honest dimension-by-dimension breakdown, conceded several initial assessments after pushback (no `tldr` need — BPE has `/bpe:review`; subagents are structurally cleaner than multi-tab).
- Identified three real BPE gaps worth pursuing: lightweight entry lane (`/bpe:quick`), cross-project lessons-to-rules promotion pipeline, and provenance trail for the existing `promote` command.
- Audited `~/.claude/` vs `~/Code/MasonEgger/homedir/.claude/` and found drift in three places: `CLAUDE.md`, `rules/code-style.md` (+ 6 obsolete rule files only present in live), and `settings.json`. Each file's "newer wins" direction differed.
- Discovered an uncommitted June 2 refactor sitting in the homedir repo's working tree (consolidated CLAUDE.md, frontmatter-scoped code-style.md folding Error Handling + Testing in, six obsolete rule files deleted). The refactor was started but never committed or deployed.
- Synced live `settings.json` → homedir repo so the in-flight refactor would be complete before deploy.
- Rewrote `ansible/tasks/claude.yml` from `copy` to symlink-based deploy. Each tracked `.claude` entry (CLAUDE.md, rules/, settings.json, settings.local.json) becomes a symlink to the repo copy. Per-machine runtime state (history.jsonl, backups/, cache/, file-history/, credentials) stays local. Added a shell-based backup step that moves pre-existing real files/dirs to `~/.claude/.bak.<timestamp>/` before symlinking, since `ansible.builtin.file state=link force=true` refuses to replace a non-empty directory.
- Took a manual safety snapshot of `~/.claude/{CLAUDE.md,rules,settings.json,settings.local.json}` to `~/.claude.pre-symlink-snapshot.<timestamp>/` before running the playbook.
- Ran `ansible-playbook setup.yml --tags claude` for real. Backup task moved the old files aside; symlink task created four correct symlinks. Verified all four symlink targets resolve to the repo, content matches, obsolete rule files are gone, idempotency holds (second run made no changes).
- Edited `bpe/commands/lessons.md` to add two changes to the `promote` subcommand: (1) a `git -C ~/.claude/rules rev-parse --show-toplevel` pre-flight guard that refuses to write if the destination is not version-controlled, and (2) a provenance trail appended to `.ai-sessions/lessons-pruned.md` under a `## Promoted <date>` heading, closing the asymmetry where `prune` recorded dispositions but `promote` deleted silently.
- Bumped `bpe/.claude-plugin/plugin.json` from `0.4.5` to `0.4.6` matching the user's per-change versioning pattern.

## Prompt Inventory

| Prompt/Command | Action Taken | Outcome |
|---|---|---|
| "Read this twitter post and compare it to my bpe ... how does my bpe rate on a scale of 1/10?" | Fetched Van Horn post via r.jina.ai; read all BPE command/agent/reference files; produced dimension-by-dimension comparison with rating | Honest breakdown: 7.5/10 head-to-head, with stated rationale |
| "I think a bpe:quick or bpe:idea is a good place to start ... I don't get the value of multi-tab I have sub agents. ... Maybe a command for reading lessons and then seeing what should be promoted into rules?" | Engaged with each pushback; conceded tldr and multi-tab; expanded on lessons-to-rules promotion design with criteria, pruning, and rule-side gate suggestions | Reached design alignment |
| "criterion but c isn't a blocker its signal ... delete it from current lessons ... reference a rule ... homedir is the source of truth" | Read the actual current `/bpe:lessons` command; discovered `promote`/`prune` already largely existed; identified version-control gap (writes to non-repo `~/.claude/rules/`) | Surfaced asymmetry (prune records dispositions, promote doesn't) |
| "It will always be in the same location ~/Code/MasonEgger/homedir" | Verified path; ran full drift audit; found code-style.md drift was actually the repo being newer (consolidation refactor) — corrected earlier "local is newer" claim | Set up Option A (adopt repo refactor) |
| "Check this all again and make sure it's still relevant" | Re-ran audit; confirmed nothing had changed; restated open items | Confirmed status |
| "What cleanup do I need to do?" | Provided concrete bash commands for Option A vs Option B; surfaced that what looked like "drift" was a half-done June 2 refactor | User chose "whatever is newer" |
| "make the changes in homedir and run the ansible playbooks ... If the playbook can't do it, make it do it" | Explored ansible structure; rewrote claude.yml from copy to symlink; ran playbook with --tags claude; verified | Symlinks deployed, drift structurally prevented |
| "yes, do both lessons.md edits" | Added version-control guard to `promote`; added `## Promoted <date>` archive trail | Edits applied to `bpe/commands/lessons.md` |
| "bump to 0.4.6 and commit on a branch" | Bumped plugin.json version; invoked /bpe:session-summary (this file); next: /bpe:commit-message + branch + commit | In progress |

## Efficiency Insights

**What went well:**
- Pushback-driven refinement: user corrections on `tldr` and multi-tab forced me to engage with what BPE actually provides instead of grafting Van Horn's solutions on. Conceding cleanly rather than defending bad takes kept the conversation moving.
- Parallel audit commands (`diff`, `stat`, `find`, `git ls-tree`) bundled into single Bash calls — surfaced the full picture (CLAUDE.md drift + settings drift + unstaged refactor) in one round trip rather than three sequential reads.
- Belt-and-suspenders backup before running the ansible deploy. Both the playbook's automatic backup and the manual snapshot exist; either can serve as recovery if Claude Code starts misbehaving.
- Idempotency verification after the first playbook run was cheap and bought real confidence — second run made no changes, confirming the migration is one-shot and stable.

**What could improve:**
- Initial Van Horn comparison overstated multi-tab parallelism as something he had that BPE lacked. Subagents solve the same problem more structurally. Should have caught this in the first pass instead of needing the user's correction.
- Initial drift assessment claimed "local is newer" for `code-style.md` — wrong direction. The repo file's June 2 mtime should have been the first thing I checked, not the last. Stat both files at the start of any drift discussion.
- Recommended `git rev-parse` guard for both `promote` and `prune`, then reasoned my way to "just `promote` is load-bearing." Should have made that scope call at the design stage instead of revisiting.
- Did not preemptively check whether `~/.claude/` was a git repo until the user prompted with "where do rules live?" — the symlink/copy question is the foundational one for any "is the live state version-controlled?" claim.

**Course corrections:**
- Conceded `tldr` as redundant given `/bpe:review`. Withdrew.
- Conceded multi-tab as a workaround for not having subagents. Withdrew.
- Pivoted from "add new commands" to "fix the existing commands' destination" once the `/bpe:lessons promote` audit revealed it already implemented the design.
- Pivoted from "rules-only drift" to "all-of-.claude drift" once the audit found CLAUDE.md and settings.json had also diverged.

## Process Improvements

- For any "drift" question, run a `stat` on every pair of paths and a `diff -q` matrix up front, before discussing what should win. Cheap, comprehensive, prevents direction-of-drift mistakes.
- When changing an ansible deploy strategy from copy to symlink, dry-run with `--check --diff` is misleading because `ansible.builtin.shell` skips in check mode — any migration that involves shell-based pre-work (backup, mv) won't show its effect, and downstream tasks (like `state=link` on a still-populated directory) will appear to fail. Skip the dry-run, run for real, but take a manual snapshot first.
- `ansible.builtin.file state=link force=true` does NOT replace a non-empty directory with a symlink — it errors. Migrations from a real-dir layout to a symlinked layout need an explicit `shell` step to move the directory aside first.
- When auditing whether a global state (like `~/.claude/`) is "version-controlled", check ALL tracked entries together, not just the file with the obvious symptom. Direction-of-drift can differ per file: a refactor can be repo-newer in one file (CLAUDE.md) and live-newer in another (settings.json).
- Commands that write to global locations need a `git rev-parse --show-toplevel` guard against the destination. One bash line, clear refusal message, prevents silent writes to non-backed-up dirs that vanish on re-provision.

## Observations

- The user discovered a real ongoing failure mode that had been live for ~8 months: copy-based dotfiles deploy + edit-anywhere created silent divergence between `~/.claude/` and the repo. The deploy "worked" in the sense that ansible reported success, but nothing ever flowed back. Six rule files existed only in live; one rule file was newer in the repo than live; one settings file was newer in live than repo.
- The June 2 refactor in the homedir repo was a careful piece of design work (consolidate always-on rules into CLAUDE.md, scope conditional rules with frontmatter `paths:`) that the user started, working-tree-completed, then forgot about for 8 days. The refactor only resurfaced because we audited together.
- The ergonomics of the `/bpe:lessons` command turned out to be much closer to what the user wanted than my initial design suggested. Reading the actual command before designing a "new" feature would have saved a turn.
- The user's existing BPE step-executor invariants (SEQUENTIAL DISPATCHES, verify-against-reported-SHA, one-commit-per-dispatch) are well-thought-out and substantially safer than Van Horn's bypassPermissions + multi-tab approach for production work. Worth noting in any future comparison.

## Suggested Skills for Next Session

- `plugin-dev:command-development` — if the next session implements `/bpe:quick` (the lightweight one-shot plan command identified as a real BPE gap), it'll need the command structure and frontmatter guidance from this skill.
