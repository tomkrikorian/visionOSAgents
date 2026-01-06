---
name: ralph-driven-development-linear
description: "Ralph Driven Development workflow that pulls Linear project issues via the Linear MCP and runs them sequentially with Codex. Use when automating task execution from a Linear project and when you need a runner that advances issues and asks for the next task automatically."
---

# Ralph Driven Development (Linear)

## Purpose

Run `ralph-linear.py` to execute Linear issues sequentially with Codex.

## Prereqs

- `codex` is on PATH.
- Linear MCP is authenticated: `codex mcp login linear`
- Provide a project via `--project` or `AGENTS.MD`.

## Run

```bash
python scripts/ralph-linear.py --project "Project Name"
```

## Flags

- `--project` Linear project name or ID. If omitted, reads `Linear Project:` under `## PROJECT` in `AGENTS.MD`.
- `--agents-path` Path to `AGENTS.MD`. Default: `AGENTS.MD`.
- `--codex-exe` Codex executable name or path. Default: `codex`.
- `--codex-args` Space-separated Codex args string. Default: `exec --dangerously-bypass-approvals-and-sandbox`.
- `--codex-timeout` Seconds before killing a Codex run; `0` = unlimited. Default: `0`.
- `--max-tasks` Max issues to process; `0` = unlimited. Default: `0`.
- `--max-attempts-per-task` Retries per issue. Default: `5`.
- `--log-path` Log file path (repo-relative or absolute). Default: `docs/logs/linear.log`.
- `--dry-run` Resolve project and exit without running Codex.

## Examples

```bash
python scripts/ralph-linear.py --project "VisionOS Agents" --max-tasks 3
```

```bash
python scripts/ralph-linear.py \
  --project "VisionOS Agents" \
  --codex-args 'exec --full-auto -m gpt-5.2-codex'
```
