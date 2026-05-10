# BPE Plugin

Brainstorm-Plan-Execute development workflow with session tracking and lessons learned.

## Overview

This plugin packages the BPE loop - a structured workflow for building software with Claude Code using test-driven development. It also includes session management for tracking work history and accumulating lessons across sessions.

## Commands

| Command | Purpose |
|---|---|
| `/bpe:brainstorm` | Iterative Q&A to develop a project specification (`spec.md`) |
| `/bpe:plan` | Transform spec into implementation roadmap (`plan.md` + `todo.md`) |
| `/bpe:execute-plan` | Implement one step at a time following strict TDD |
| `/bpe:gh-issue` | Fetch a GitHub issue and route to brainstorm or plan |
| `/bpe:commit-message` | Generate a commit message explaining what was changed |
| `/bpe:session-summary` | Generate session recap and capture lessons learned |
| `/bpe:handoff` | Compact the current conversation into an ephemeral handoff document for a fresh agent |
| `/bpe:review` | Generate an HTML view of `spec.md` / `plan.md` / `todo.md` and serve it locally for visual review with annotations |
| `/bpe:apply-review` | Load saved review feedback and apply changes to the reviewed artifact |
| `/bpe:lessons` | View, search, and manage accumulated lessons |

## The BPE Loop

1. **Brainstorm** - Develop a thorough specification through iterative dialogue
2. **Plan** - Break the spec into right-sized, TDD-structured implementation steps
3. **Execute** - Implement steps one at a time, following the plan exactly
4. **Review & Record** - Summarize the session and capture lessons for next time

## Session Management

Session artifacts live in `.ai-sessions/` at the project root:

- **Session summaries** - Individual markdown files capturing what happened each session
- **lessons.md** - Accumulated cross-session learnings in a hybrid format (recent + categorized)

The execute-plan command automatically reads the most recent session summary for continuity. Format specs and workflow rules live in `references/session-management.md`, which the relevant commands read directly. There is intentionally no Skill registered for this — invocation is always via an explicit slash command.

## Installation

This plugin is deployed via the homedir Ansible playbook. It lives at `.claude/plugins/bpe/` in the homedir repository.

## Reference

- [How I Actually Use the Damn Thing](https://mason.dev/blog/how-i-actually-use-the-damn-thing/) - The BPE loop explained
- [What I Found Actually Works](https://mason.dev/blog/what-i-found-actually-works-with-ai/) - Prompts as code philosophy
- [Skills, Plugins, and MCP Oh My](https://mason.dev/blog/skills-plugins-and-mcp-oh-my/) - Claude Code customization approach
