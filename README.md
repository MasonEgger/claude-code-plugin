# Mason's Claude Code Plugins

A multi-plugin repository for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) containing three plugins that cover software development workflows, technical writing, and personal productivity.

## Plugins

### BPE (Brainstorm-Plan-Execute)

A structured development workflow built around test-driven development with session tracking and lessons learned.

| Command | Purpose |
|---|---|
| `/bpe:brainstorm` | Iterative Q&A to develop a project specification (`spec.md`) |
| `/bpe:plan` | Transform spec into a TDD implementation roadmap (`plan.md` + `todo.md`) |
| `/bpe:execute-plan` | Implement the next unchecked step using strict TDD |
| `/bpe:gh-issue` | Fetch a GitHub issue and route to brainstorm or plan based on detail level |
| `/bpe:commit-msg` | Generate a commit message explaining what was changed |
| `/bpe:session-summary` | Generate a session recap and capture lessons learned |
| `/bpe:lessons` | View, search, and manage accumulated lessons |

**Skills:** `session-management` — format specs and workflow for `.ai-sessions/` tracking

The BPE loop: Brainstorm a spec through dialogue, Plan it into right-sized TDD steps, Execute one step at a time, then Review and Record lessons for next session.

### Writing

A technical writing toolkit for authoring tutorials in a modified DigitalOcean style with Mason Egger's voice.

| Component | Purpose |
|---|---|
| **Skill:** `tutorial-writing` | Style guide, code sandwich approach, voice matching, and step-by-step workflow |
| **Agent:** `copy-editor` | Vale-based style checking and copy editing for written content |
| **Script:** `wordcount` | Track tutorial word counts excluding code blocks |

**References included:** style guide, author voice patterns, Temporal-specific rules, code sandwich methodology, wordcount usage, and detailed workflow.

### Productivity

Personal productivity commands for Obsidian vault management, Todoist integration, and journaling.

| Command | Purpose |
|---|---|
| `/productivity:eod` | End-of-day brain dump — syncs Todoist, processes voice transcript, routes info across the vault |
| `/productivity:todoist-sync` | Pull completed and pending Todoist tasks into the daily journal |
| `/productivity:transcript-2-journal` | Convert a voice transcript into an Obsidian journal entry |
| `/productivity:discover-pain-points` | Evaluate sales discovery calls with a structured pain-level framework |

**Skills:** `vault-routing` — Obsidian vault structure, folder routing rules, cross-linking conventions, and file naming standards

**Dependencies:** This plugin works best alongside the `todoist-cli`, `obsidian:obsidian-cli`, and `obsidian:obsidian-markdown` marketplace skills.

## Installation

### Add the marketplace

Register this repository as a Claude Code marketplace:

```
/plugin marketplace add MasonEgger/claude-code-plugin
```

### Install individual plugins

Once the marketplace is registered, install whichever plugins you need:

```
/plugin install bpe@mason-claude-plugins
/plugin install writing@mason-claude-plugins
/plugin install productivity@mason-claude-plugins
```

### Browse available plugins

You can also use the interactive plugin manager to discover and install:

```
/plugin
```

Navigate to the **Discover** tab to see all available plugins from registered marketplaces.

### Update plugins

To pull the latest changes from this repository:

```
/plugin marketplace update mason-claude-plugins
```

## Repository Structure

```
claude-code-plugin/
├── marketplace.json              # Plugin registry for Claude Code
├── bpe/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/                 # 7 slash commands
│   └── skills/
│       └── session-management/   # Session tracking skill + references
├── writing/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   │   └── copy-editor.md       # Vale-based copy editing agent
│   └── skills/
│       └── tutorial-writing/     # Tutorial skill + 6 references + wordcount script
└── productivity/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── commands/                  # 4 slash commands
    └── skills/
        └── vault-routing/        # Vault routing skill + 2 references
```

## Prerequisites

These plugins assume certain tools are available depending on which you install:

- **BPE:** `gh` CLI (for `/bpe:gh-issue`)
- **Writing:** [Vale](https://vale.sh/) with bphogan style rules (for the copy-editor agent), [uv](https://docs.astral.sh/uv/) (for the wordcount script)
- **Productivity:** [Todoist CLI](https://github.com/sachaos/todoist) aliased as `todo`, an Obsidian vault

## License

MIT
