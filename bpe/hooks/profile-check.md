# Profile-Check Hook

A `UserPromptSubmit` prompt-based hook that warns when a `/bpe:<name>` invocation's profile-resolved model differs from the current session model.
This file is the canonical hook body and behavior documentation.
The registered configuration lives in `hooks/profile-check.json` (referenced from `.claude-plugin/plugin.json` via its `hooks` field) and embeds the prompt below; the two must stay in sync.
Resolution semantics are defined in `references/model-profiles.md`, the canonical schema doc for `.claude/bpe.local.md` profile files.

## Behavior

1. On every prompt submission, the hook inspects the submitted prompt text.
2. Prompts that do not start with `/bpe:` (after optional leading whitespace) pass through untouched. The hook contributes nothing to the transcript.
3. For a `/bpe:<name>` invocation, the hook extracts the skill name and injects `additionalContext` instructing the session agent to:
   1. Skip silently when neither `.claude/bpe.local.md` at the repo root nor `~/.claude/bpe.local.md` exists. Frontmatter defaults apply and no warning fires. This is the fresh-install state.
   2. Resolve the active profile name once: `BPE_PROFILE` env var when set (checked via Bash), else `active_profile` in the per-project file, else in the user-global file.
   3. Look up `skills.<name>` under that profile in the per-project file, falling through to the user-global file (shadowing is key-level). No entry means the skill's frontmatter `model:` applies and no warning fires.
   4. Compare the resolved value to the current session model. A family alias (`opus`, `sonnet`, `haiku`) matches any session model of that family.
   5. Only on mismatch, emit the warning before proceeding:

      > Note: skill \<name\> profile expects model \<X\>; current session is \<Y\>. Consider /model \<X\> before proceeding.

   6. Continue with the skill either way. The hook warns; it never blocks.

## Why the Resolution Is Delegated

Prompt-based hooks receive the hook-input JSON (the submitted prompt arrives via `$USER_PROMPT` substitution) and nothing else.
They cannot read files, observe process environment variables, or see the session's model.
The session agent can do all three: it reads both `bpe.local.md` locations, checks `BPE_PROFILE` through Bash, and knows its own model.
So the hook handles detection and name extraction, and the injected context delegates the four-level precedence walk (see `references/model-profiles.md`, "Lookup Precedence") to the agent.
This keeps the full chain intact, including the `BPE_PROFILE` level that the hook process itself cannot observe.

## Canonical Prompt

The prompt registered in `hooks/profile-check.json`:

```text
You are screening a just-submitted user prompt for the BPE plugin's model-profile check. The submitted prompt text is:

$USER_PROMPT

A BPE invocation starts, after optional leading whitespace, with '/bpe:' followed by a skill name made of letters, digits, and hyphens (for example '/bpe:brainstorm').

If the prompt is NOT a BPE invocation, respond with exactly: {}

If the prompt IS a BPE invocation, extract the skill name (the characters between '/bpe:' and the first whitespace character, or the end of the prompt) and respond with exactly this JSON, substituting the extracted name for <name> everywhere it appears:

{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "Model-profile check for bpe skill '<name>'. Before executing the skill, resolve its profile model per the bpe plugin's references/model-profiles.md: (1) If neither .claude/bpe.local.md at the repo root nor ~/.claude/bpe.local.md exists, skip this check silently; frontmatter defaults apply. (2) Resolve the active profile name once: the BPE_PROFILE environment variable when set (check it with a Bash echo of BPE_PROFILE), else active_profile in the per-project file, else in the user-global file. (3) Look up skills.<name> under that profile in the per-project file, falling through to the user-global file (shadowing is key-level). If no entry exists, skip silently; the skill's frontmatter model applies. (4) Compare the resolved value to the current session model; a family alias (opus, sonnet, haiku) matches any session model of that family. (5) Only on mismatch, state before proceeding: Note: skill <name> profile expects model <X>; current session is <Y>. Consider /model <X> before proceeding. Then continue with the skill either way."}}
```

## Testing

Hooks load at session start; editing this hook or its JSON requires exiting and restarting Claude Code before the change takes effect.

End-to-end check (requires a reloaded interactive session):

1. Write a `.claude/bpe.local.md` at the repo root pinning `brainstorm` to a model that differs from the session's (for example `claude-opus-4-7` while the session runs a Sonnet model).
2. Type `/bpe:brainstorm` and confirm the warning line appears in the transcript before the skill runs.
3. Delete the settings file, restart, type `/bpe:brainstorm` again, and confirm no warning appears.

For a quick static check, run `claude plugin validate ./bpe` and confirm exit 0, and inspect loaded hooks in-session with `/hooks`.
