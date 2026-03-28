---
name: vault-routing
description: "This skill should be used when the user asks about their Obsidian vault, note routing, or vault organization. Relevant when the user says 'add this to my vault', 'where does this go in Obsidian', 'process my voice transcript', 'create a note for this person', 'route this to the right folder', 'log this meeting note', or 'file this in Arcadia'. Covers vault structure, folder routing rules, cross-linking conventions, and writing voice for Mason's Arcadia vault."
---

# Vault Routing

Route information to the correct location in Mason's Arcadia Obsidian vault. The vault root is the current working directory when commands are invoked.

## Vault Structure

- **Journal/{year}/current/{MM-DD-YYYY}.md** — Daily notes, the primary entry point
- **Active/** — Currently active projects, work, relationships
  - `Active/Work/Temporal/Customers/` — Customer company tracking files
  - `Active/Community/PyTexas/` — PyTexas community work
- **Archive/** — Completed/abandoned projects (Community, Personal, Work subdirs)
- **Reference/** — Lookup material, people, places, resources
  - `Reference/People/Co-Workers/Temporal/` — Temporal colleagues
  - `Reference/People/Community/Python/` and `Community/PyTexas/` — Community contacts
  - `Reference/People/Customers/Temporal/` — Customer contact persons
  - `Reference/People/Friends/` — Friends
  - `Reference/People/Family/` — Family members
- **Inbox/** — Temporary capture for new items (triage to correct folder, add links, then remove from Inbox)
- **_Templates/** — Obsidian templates for consistent note creation

## Routing Rules

### People
- Temporal co-workers → `Reference/People/Co-Workers/Temporal/`
- Community/Python people → `Reference/People/Community/Python/` or `Community/PyTexas/`
- Customer contacts → `Reference/People/Customers/Temporal/`
- Friends → `Reference/People/Friends/`
- If unclear → `Reference/People/`

### Customer Work
- Customer companies → `Active/Work/Temporal/Customers/`
- Customer contacts → `Reference/People/Customers/Temporal/`
- Always create bidirectional links between company and contact files

### Ideas & Captures
- New ideas → `Inbox/` with enough context to be useful later
- These should be intentional captures, not empty shells

## File Naming Conventions

- **People files:** `Firstname Lastname.md` (e.g., `Jane Smith.md`)
- **Customer company files:** `Company Name.md` (e.g., `Acme Corp.md`)
- **Daily notes:** `MM-DD-YYYY.md` (e.g., `03-27-2026.md`)
- **Idea captures:** Descriptive title in Inbox (e.g., `Blog Post - Temporal Patterns.md`)

## Cross-Linking

- Always check if a file exists before creating a `[[cross-link]]`
- If no file exists but it's the kind of thing Mason tracks, create the link anyway
- Use existing file names exactly as they appear in the vault

## Writing Voice

When writing journal entries or notes in Mason's voice, consult **`references/writing-voice.md`** for tone, language patterns, and structure guidance.

## Todoist Integration

For Todoist CLI commands, project structure, and label conventions, consult **`references/todoist-setup.md`**.

## Dependencies

This skill works alongside:
- **todoist-cli** (marketplace skill) — for `todo` CLI usage patterns and flags
- **obsidian:obsidian-cli** (marketplace skill) — for Obsidian CLI operations
- **obsidian:obsidian-markdown** (marketplace skill) — for wikilink and frontmatter syntax
