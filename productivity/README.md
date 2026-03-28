# Productivity Plugin

Personal productivity system for managing Mason's Obsidian vault, Todoist integration, journaling, and customer tracking.

## Commands

| Command | Purpose |
|---|---|
| `/productivity:eod` | End-of-day brain dump — voice transcript processing + Todoist sync + vault routing |
| `/productivity:todoist-sync` | Pull completed & pending Todoist tasks into today's journal |
| `/productivity:transcript-2-journal` | Convert voice transcript to journal entry (blog section only) |
| `/productivity:discover-pain-points` | Evaluate sales discovery calls for customer pain points |

## Skills

| Skill | Purpose |
|---|---|
| `vault-routing` | Obsidian vault structure, routing rules, writing voice, and Todoist setup |

## Dependencies

This plugin works alongside marketplace skills:
- **todoist-cli** — Todoist CLI usage patterns and commands
- **obsidian** — Obsidian CLI and markdown syntax

## Workflow

1. Throughout the day: use Todoist to track tasks
2. End of day: record a voice transcript of your day
3. Run `/productivity:eod` — syncs Todoist tasks, processes transcript, routes info across the vault
4. Or run `/productivity:todoist-sync` standalone for just the task sync

## Setup

1. Todoist CLI installed and aliased as `todo` (`/opt/homebrew/bin/td`)
2. Authenticated via `todo auth login`
3. Obsidian vault at the working directory with Journal/{year}/current/ structure
