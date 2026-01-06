---
name: ralph-driven-development-linear
description: "Ralph Driven Development workflow that pulls Linear project issues via the Linear MCP and runs them sequentially with Codex. Use when automating task execution from a Linear project and when you need a runner that advances issues and asks for the next task automatically."
---

# Ralph Driven Development (Linear)

## Purpose

Run a Ralph-style loop that pulls Linear issues via MCP and processes them sequentially.

## Quick start

1. Ensure `codex` is on PATH.
2. Provide a Linear project name or ID via `--project` or `AGENTS.MD`.
3. Run the runner:

```bash
uv run python scripts/ralph-linear.py --project "project name"
```

## AGENTS.MD project format

Under `## PROJECT`, add one of the following lines:

- `Linear Project: Example Project`
- `Linear Project ID: 00000000-0000-0000-0000-000000000000`
- `Example Project`

Use the first non-empty line in the `## PROJECT` section when `--project` is omitted.

## Runner contract

When `ralph-linear.py` invokes Codex, require it to:

- Use Linear MCP to list issues in the project (by name or ID from the prompt).
- Select the next uncompleted issue (Todo/Backlog/Unstarted).
- Move the issue to In Progress.
- Implement the work in this repo and commit.
- Move the issue to Done.
- Print only the magic phrase when finished.
- Print only the no-tasks phrase if no issues remain.

## Defaults

- Magic phrase: `TASK_COMPLETE`
- No tasks phrase: `NO_TASKS_AVAILABLE`
- Log path: `docs/logs/linear.log`

## Tips

- Pass `--max-tasks` to cap the number of issues per run.
- Use `--dry-run` to validate project resolution without running Codex.
