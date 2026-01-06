---
name: ralph-driven-development
description: "Guide and tooling for Ralph Driven Development (RDD), a spec runner that repeatedly invokes Codex (or other agents) over ordered specs until a magic phrase signals completion. Use when setting up or operating an RDD workflow with plan.md, specs/, done.md, agent-run.log, and a ralph.py runner, or when customizing the runner CLI and prompt contract."
---

# Ralph Driven Development (RDD)

## What is this?

Use `ralph` for Ralph Driven Development. Keep running an AI agent against prompts until it prints a magic phrase signaling completion.

Use it with `codex` by default, or swap to another agent by changing the runner CLI flags.

## Guide

Use a plan, a sequenced specs backlog, and a runner that executes each spec with Codex agents until completion.

## What You Have

- `docs/specifications.md`: the product plan and architecture overview.
- `docs/tasks/0001-...`: incremental work units.
- `scripts/ralph.py`: Python runner (execute directly from the skill folder).

## Quick Start (Python + uv)

```bash
uv run python scripts/ralph.py
```

## How It Works

1. Read `docs/tasks/` for spec files and sort by filename order.
2. Skip completed specs listed in `docs/done.md`.
3. Invoke Codex with a prompt that:
   - follows the spec,
   - commits on completion,
   - records useful learnings in `AGENTS.md`,
   - prints the magic phrase when done.
4. Move to the next spec only after the magic phrase appears.
5. Sleep on usage limit errors until reset, then retry.

## Progress Tracking

- Show live console output:
  - `[start]` when a spec begins,
  - `[done]` when a spec completes,
  - `[retry]` when no magic phrase is found,
  - `[skip]` when a spec is already in `docs/done.md`.
- Append full logs to `docs/logs/agent-run.log`.
- Append completed specs to `docs/done.md`.

## Resume After Interruptions

Rerun the script; it skips specs already listed in `docs/done.md`.

## Customize Defaults

### Python + uv

```bash
uv run python scripts/ralph.py \
  --magic-phrase SPEC_COMPLETE \
  --codex-exe codex \
  --codex-args "exec --dangerously-bypass-approvals-and-sandbox -m gpt-5.2-codex"
```

## Troubleshooting

- Handle usage limits by sleeping until reset time and retrying.
- Inspect `docs/logs/agent-run.log` for repeated failures.
- Ensure `codex` is on `PATH` if not found.

## Where to Start

Create the plan in `docs/specifications.md` and some `docs/tasks/...` files for incremental work, then run the runner. Start at the first spec not listed in `docs/done.md`.
