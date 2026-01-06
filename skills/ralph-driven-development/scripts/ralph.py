#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path


def resolve_repo_path(path: str, repo_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else (repo_root / candidate)


def get_spec_list(specs_dir: Path) -> list[str]:
    if not specs_dir.exists():
        raise FileNotFoundError(f"Specs directory not found: {specs_dir}")
    specs: list[str] = []
    for path in sorted(specs_dir.glob("*.md")):
        if path.name in {"README.md", "done.md"}:
            continue
        if re.match(r"^\d{4}-.*\.md$", path.name):
            specs.append(str(path.as_posix()))
    if not specs:
        raise ValueError(f"No specs found in {specs_dir}")
    return specs


def build_prompt(spec_path: str, phrase: str) -> str:
    return (
        f"Implement spec: {spec_path}\n\n"
        "Requirements:\n"
        "- Read and follow the spec.\n"
        "- Work in this repo.\n"
        "- Commit when complete with a clear message.\n"
        "- Write useful learnings for future runs to AGENTS.md.\n"
        f"- After committing, print only the magic phrase: {phrase}\n"
        "- Do not print the magic phrase before the commit.\n"
    )


def load_done(done_path: Path) -> set[str]:
    if not done_path.exists():
        done_path.parent.mkdir(parents=True, exist_ok=True)
        done_path.write_text("", encoding="utf-8")
        return set()
    done: set[str] = set()
    for line in done_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*-\s+(.+)$", line)
        if match:
            done.add(match.group(1).strip())
    return done


def append_done(done_path: Path, spec: str) -> None:
    with done_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {spec}\n")


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run specs sequentially with Codex.")
    parser.add_argument("--magic-phrase", default="SPEC_COMPLETE")
    parser.add_argument("--codex-exe", default="codex")
    parser.add_argument(
        "--codex-args",
        default="exec --dangerously-bypass-approvals-and-sandbox",
        help="Space-separated codex args, e.g. 'exec --full-auto -m gpt-5.2-codex'",
    )
    parser.add_argument("--specs-dir", default="docs/tasks")
    parser.add_argument("--max-attempts-per-spec", type=int, default=5)
    parser.add_argument("--log-path", default="docs/logs/agent-run.log")
    parser.add_argument("--done-path", default="docs/done.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    os.chdir(repo_root)

    specs_dir = resolve_repo_path(args.specs_dir, repo_root)
    log_path = resolve_repo_path(args.log_path, repo_root)
    done_path = resolve_repo_path(args.done_path, repo_root)

    specs = get_spec_list(specs_dir)
    done_set = load_done(done_path)

    codex_args = args.codex_args.split()
    if not shutil_which(args.codex_exe):
        raise FileNotFoundError(f"Codex executable not found on PATH: {args.codex_exe}")

    completed_count = 0
    skipped_count = 0
    failed_count = 0
    total_specs = len(specs)

    for spec in specs:
        if spec in done_set:
            skipped_count += 1
            print(f"[skip] already done: {spec}")
            continue

        attempt = 1
        done = False

        while not done:
            if attempt > args.max_attempts_per_spec:
                failed_count += 1
                raise RuntimeError(f"Max attempts exceeded for spec: {spec}")

            prompt = build_prompt(spec, args.magic_phrase)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            append_log(log_path, f"=== {timestamp} | {spec} | attempt {attempt} ===\n")

            if args.dry_run:
                print(f"[dry-run] {spec} (attempt {attempt})")
                break

            progress_index = completed_count + skipped_count + 1
            print(f"[start] Spec {progress_index} of {total_specs} | attempt {attempt} :: {spec}")

            try:
                exit_code, output_text = run_codex(args.codex_exe, codex_args, prompt)
            except Exception:
                output_text = "[exception] codex invocation failed\n" + traceback.format_exc()
                append_log(log_path, output_text + ("\n" if not output_text.endswith("\n") else ""))
                print(f"[error] exception during codex run for {spec}")
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
                if reset_seconds is None:
                    wait_seconds = 60 * 60
                    print(f"[wait] usage limit reached; sleeping {wait_seconds} seconds before retry")
                    time.sleep(wait_seconds)
                    attempt += 1
                    continue
                wait_seconds = reset_seconds + 30
                print(f"[wait] usage limit reached; sleeping {wait_seconds} seconds before retry")
                time.sleep(wait_seconds)
                attempt += 1
                continue

            if exit_code != 0:
                print(f"[error] codex exit code {exit_code} for {spec}")
                attempt += 1
                continue

            if args.magic_phrase in output_text:
                done = True
                completed_count += 1
                append_done(done_path, spec)
                print(f"[done] {spec}")
                continue

            print(f"[retry] magic phrase not found for {spec}")
            attempt += 1

    print("=== Summary ===")
    print(f"Completed: {completed_count}")
    print(f"Skipped:   {skipped_count}")
    print(f"Failed:    {failed_count}")
    return 0


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


if __name__ == "__main__":
    raise SystemExit(main())
