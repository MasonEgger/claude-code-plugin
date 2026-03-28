# Todoist Setup

## CLI Access
- Binary: `/opt/homebrew/bin/td`
- Alias: `todo` (because `td` is aliased to `tmux detach`)
- Auth: browser-based OAuth via `todo auth login`

## Projects
Known projects (run `todo project list` for current state):
- Temporal — primary work
- PyTexas — community involvement
- Personal — personal tasks
- Inbox — quick capture
- Continuing Education — learning
- Side Work — side projects

## Labels
Mason uses time-estimate labels, not Eisenhower quadrants:
- `5min`, `15min`, `30min`, `1hr`, `2hr`, `half-day`, `full-day`
- `AI` — AI-related tasks
- `reclaim`, `reclaim_personal` — Reclaim.ai managed tasks

## Key CLI Commands
```
todo completed --since YYYY-MM-DD --until YYYY-MM-DD --json --full --all
todo task list --due today --json --full --all
todo project list --json --all
todo label list --json --all
todo task list --filter "QUERY" --json --full
todo add "task text #Project @label"
```

## JSON Output
- Use `--json` for structured output, `--full` for all fields
- Results are in a `results` array
- Key fields: `content`, `projectId`, `labels`, `completedAt`, `due`, `priority`
