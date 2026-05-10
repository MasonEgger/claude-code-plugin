# Mason's Claude Code Plugins

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin repository. Two plugins are published here under the `mmegger-plugins` marketplace:

- **`bpe`** — Brainstorm-Plan-Execute development workflow with session tracking, HTML artifact review, and conversational handoffs.
- **`python`** — Python development standards, toolchain preferences, and coding conventions for modern Python projects.

## BPE (Brainstorm-Plan-Execute)

A structured development workflow built around test-driven development with session tracking and lessons learned.

| Command | Purpose |
|---|---|
| `/bpe:brainstorm` | Iterative Q&A to develop a project specification (`spec.md`) |
| `/bpe:plan` | Transform spec into a TDD implementation roadmap (`plan.md` + `todo.md`) |
| `/bpe:execute-plan` | Implement the next unchecked step using strict TDD |
| `/bpe:gh-issue` | Fetch a GitHub issue and route to brainstorm or plan based on detail level |
| `/bpe:commit-message` | Generate a commit message explaining what was changed |
| `/bpe:review` | Generate an HTML view of `spec.md` / `plan.md` / `todo.md` and serve it locally for visual review with annotations |
| `/bpe:apply-review` | Load saved review feedback and apply changes to the reviewed artifact |
| `/bpe:handoff` | Compact the current conversation into an ephemeral handoff document for a fresh agent |
| `/bpe:session-summary` | Generate a session recap and capture lessons learned |
| `/bpe:lessons` | View, search, and manage accumulated lessons |

The BPE loop: Brainstorm a spec through dialogue, Plan it into right-sized TDD steps, Execute one step at a time, then Review and Record lessons for next session. `/bpe:review` and `/bpe:apply-review` give you an interactive HTML pass over any of the BPE artifacts; `/bpe:handoff` lets you pause mid-flight and pass live conversational state to a fresh agent. Format specs and workflow rules for `.ai-sessions/` live in `bpe/references/session-management.md`, read directly by the relevant commands.

## Python Development Standards

A skill that triggers when working with Python projects (`.py` files, `pyproject.toml`, or any Python tooling configuration). Enforces type hints on all public interfaces, RST docstrings, absolute imports, modern Python idioms (PEP 604 union syntax, descriptive names), and a uv-based workflow. Loads reference docs on demand for toolchain configuration (uv, ruff, mypy, pytest, nox, just), PEP 723 inline-metadata CLI scripts, documentation patterns, and the red-green-refactor TDD cycle.

See [`python/README.md`](python/README.md) for the full skill contents.

## Installation

### Add the marketplace

Register this repository as a Claude Code marketplace:

```
/plugin marketplace add MasonEgger/claude-code-plugin
```

### Install plugins

Once the marketplace is registered, install whichever plugins you want:

```
/plugin install bpe@mmegger-plugins
/plugin install python@mmegger-plugins
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
/plugin marketplace update mmegger-plugins
```

## Repository Structure

- `.claude-plugin/marketplace.json` — plugin registry for Claude Code
- `bpe/.claude-plugin/plugin.json` — BPE plugin manifest
- `bpe/commands/` — slash commands
- `bpe/scripts/` — bundled helper scripts (e.g. `review-server.py` for `/bpe:review`)
- `bpe/references/` — plugin-bundled reference docs that commands read directly (e.g. `session-management.md`)
- `python/.claude-plugin/plugin.json` — Python plugin manifest
- `python/skills/python/` — the `python` skill (SKILL.md plus reference docs for toolchain, CLI scripts, documentation, and TDD workflow)

## Prerequisites

- **`/bpe:gh-issue`** — `gh` CLI installed and authenticated
- **`/bpe:review`** — Python 3 (uses stdlib only; no extra packages)

## License

MIT
