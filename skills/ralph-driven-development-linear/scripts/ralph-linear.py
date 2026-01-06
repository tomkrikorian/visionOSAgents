#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import time
import traceback
from pathlib import Path

DEFAULT_MAGIC_PHRASE = "TASK_COMPLETE"
DEFAULT_NO_TASKS_PHRASE = "NO_TASKS_AVAILABLE"


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.MD").exists() or (candidate / ".git").exists():
            return candidate
    return start


def resolve_repo_path(path: str, repo_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else (repo_root / candidate)


def extract_project_from_agents(agents_path: Path) -> str | None:
    if not agents_path.exists():
        return None
    text = agents_path.read_text(encoding="utf-8")
    in_section = False
    for line in text.splitlines():
        if re.match(r"^##\s*PROJECT\b", line):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+\S", line):
            break
        if not in_section:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("//"):
            continue
        if stripped.lower().startswith("todo"):
            continue
        stripped = re.sub(r"^[*-]\s*", "", stripped)
        if ":" in stripped:
            _, value = stripped.split(":", 1)
            stripped = value.strip()
        if stripped:
            return stripped
    return None


def build_prompt(project: str, magic_phrase: str, no_tasks_phrase: str) -> str:
    return (
        "Use Linear MCP to execute the next issue for this project:\n"
        f"{project}\n\n"
        "Requirements:\n"
        "- Use Linear MCP to list issues in the project by name or ID.\n"
        "- Select the next uncompleted issue (Todo/Backlog/Unstarted).\n"
        "- Move the issue to In Progress.\n"
        "- Implement the work in this repo and commit.\n"
        "- Move the issue to Done.\n"
        "- Write concise learnings to AGENTS.MD if relevant.\n"
        f"- If no issues remain, print only: {no_tasks_phrase}\n"
        f"- After committing, print only the magic phrase: {magic_phrase}\n"
        "- Do not print the magic phrase before the commit.\n"
    )


def append_log(log_path: Path, text: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def run_codex(codex_exe: str, codex_args: list[str], prompt: str) -> tuple[int, str]:
    process = subprocess.run(
        [codex_exe, *codex_args, "-"],
        input=prompt,
        text=True,
        capture_output=True,
        cwd=os.getcwd(),
    )
    output = (process.stdout or "") + (process.stderr or "")
    return process.returncode, output


def parse_reset_seconds(text: str) -> int | None:
    match = re.search(r'resets_in_seconds"\s*:\s*(\d+)', text)
    if match:
        return int(match.group(1))
    match = re.search(r'resets_at"\s*:\s*(\d+)', text)
    if match:
        reset_epoch = int(match.group(1))
        return max(0, reset_epoch - int(time.time()))
    for line in text.splitlines():
        line = line.strip()
        if not (line.startswith("{") and line.endswith("}")):
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            reset_seconds = payload.get("resets_in_seconds")
            if isinstance(reset_seconds, int):
                return reset_seconds
            reset_epoch = payload.get("resets_at")
            if isinstance(reset_epoch, int):
                return max(0, reset_epoch - int(time.time()))
    return None


def shutil_which(executable: str) -> str | None:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / executable
        if candidate.exists():
            return str(candidate)
        if os.name == "nt":
            for ext in (".exe", ".cmd", ".bat"):
                if candidate.with_suffix(ext).exists():
                    return str(candidate.with_suffix(ext))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Linear issues sequentially with Codex.")
    parser.add_argument("--project", help="Linear project name or ID")
    parser.add_argument("--agents-path", default="AGENTS.MD")
    parser.add_argument("--magic-phrase", default=DEFAULT_MAGIC_PHRASE)
    parser.add_argument("--no-tasks-phrase", default=DEFAULT_NO_TASKS_PHRASE)
    parser.add_argument("--codex-exe", default="codex")
    parser.add_argument(
        "--codex-args",
        default="exec --dangerously-bypass-approvals-and-sandbox",
        help="Space-separated codex args, e.g. 'exec --full-auto -m gpt-5.2-codex'",
    )
    parser.add_argument("--max-tasks", type=int, default=50)
    parser.add_argument("--max-attempts-per-task", type=int, default=5)
    parser.add_argument("--log-path", default="docs/logs/ralph-linear.log")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    os.chdir(repo_root)

    agents_path = resolve_repo_path(args.agents_path, repo_root)
    project = args.project or extract_project_from_agents(agents_path)
    if not project:
        raise ValueError("Provide --project or set a project under ## PROJECT in AGENTS.MD")

    log_path = resolve_repo_path(args.log_path, repo_root)

    codex_args = shlex.split(args.codex_args)
    if not shutil_which(args.codex_exe):
        raise FileNotFoundError(f"Codex executable not found on PATH: {args.codex_exe}")

    max_tasks = None if args.max_tasks <= 0 else args.max_tasks
    completed_count = 0
    failed_count = 0

    while max_tasks is None or completed_count < max_tasks:
        attempt = 1
        done = False

        while not done:
            if attempt > args.max_attempts_per_task:
                failed_count += 1
                raise RuntimeError("Max attempts exceeded for current task")

            prompt = build_prompt(project, args.magic_phrase, args.no_tasks_phrase)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            append_log(log_path, f"=== {timestamp} | task {completed_count + 1} | attempt {attempt} ===\n")

            if args.dry_run:
                print(f"[dry-run] {project} (attempt {attempt})")
                return 0

            print(f"[start] Task {completed_count + 1} | attempt {attempt} | project: {project}")

            try:
                exit_code, output_text = run_codex(args.codex_exe, codex_args, prompt)
            except Exception:
                output_text = "[exception] codex invocation failed\n" + traceback.format_exc()
                append_log(log_path, output_text + ("\n" if not output_text.endswith("\n") else ""))
                print("[error] exception during codex run")
                attempt += 1
                continue

            append_log(log_path, output_text + ("\n" if not output_text.endswith("\n") else ""))

            usage_limit = (
                "usage_limit_reached" in output_text
                or "Too Many Requests" in output_text
                or "You've hit your usage limit" in output_text
            )

            if usage_limit:
                reset_seconds = parse_reset_seconds(output_text)
                wait_seconds = (reset_seconds + 30) if reset_seconds is not None else 60 * 60
                print(f"[wait] usage limit reached; sleeping {wait_seconds} seconds before retry")
                time.sleep(wait_seconds)
                attempt += 1
                continue

            if exit_code != 0:
                print(f"[error] codex exit code {exit_code}")
                attempt += 1
                continue

            if args.no_tasks_phrase in output_text:
                print("[done] no tasks remaining")
                print("=== Summary ===")
                print(f"Completed: {completed_count}")
                print(f"Failed:    {failed_count}")
                return 0

            if args.magic_phrase in output_text:
                done = True
                completed_count += 1
                print("[done] task completed")
                continue

            print("[retry] magic phrase not found")
            attempt += 1

    print("=== Summary ===")
    print(f"Completed: {completed_count}")
    print(f"Failed:    {failed_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
