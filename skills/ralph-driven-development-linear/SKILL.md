---
name: ralph-driven-development-linear
description: "Ralph Driven Development workflow that pulls Linear project issues via the Linear MCP and runs them sequentially with Codex. Use when automating task execution from a Linear project and when you need a runner that advances issues and asks for the next task automatically."
---

# Ralph Driven Development (Linear)

## Purpose

Run a Ralph-style loop that pulls Linear issues via MCP and processes them sequentially.

## Quick start

1. Ensure `codex` is on PATH.
2. Provide a Linear project name or ID in the prompt or look for it in `AGENTS.MD`.
3. If Auth fails, ask the user to run this line: codex mcp login linear
4. Run the script:

```bash
uv run python scripts/ralph-linear.py --project "project name"
```

## AGENTS.MD project format

Under `## PROJECT`, add a line with the name or ID of the project:

- `Linear Project: Example Project`
- `Linear Project: 00000000-0000-0000-0000-000000000000`

Use the first non-empty line in the `## PROJECT` section when `--project` is omitted.

## Runner contract

When `ralph-linear.py` invokes Codex, require it to:

- Use Linear MCP to list issues in the project (by name or ID from the prompt).
- Consider only issues in Backlog/Todo/Unstarted/In Progress.
- Select the highest-priority issue (Urgent > High > Normal > Low > None); break ties by earliest createdAt.
- Move the issue to In Progress if it is not already.
- Implement the work in this repo and commit.
- Move the issue to Done.
- Do not start another issue in the same run.
- Print only the magic phrase when finished.
- Print only the no-tasks phrase if no issues remain.

## Defaults

- Magic phrase: `TASK_COMPLETE`
- No tasks phrase: `NO_TASKS_AVAILABLE`
- Log path: `docs/logs/linear.log`

## Tips

- Pass `--max-tasks` to cap the number of issues per run.
- Use `--dry-run` to validate project resolution without running Codex.
