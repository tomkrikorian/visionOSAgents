#!/usr/bin/env python3
"""Sync the shared visionOS skill set between the agents and plugin repos."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


IGNORED_NAMES = {".DS_Store", "__pycache__", ".gitkeep"}
MANIFEST_PATH = Path("sync/shared-skills.json")
LOCK_PATH = Path("sync/shared-skills.lock.json")


class SyncError(Exception):
    """Raised when sync state or arguments are invalid."""


@dataclass(frozen=True)
class RepoState:
    root: Path
    skills_root: Path
    manifest_path: Path
    lock_path: Path
    shared_skills: list[str]
    lock_data: dict | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync shared visionOS skills between visionOSAgents and the Codex plugin repo.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Report shared-skill drift.")
    configure_repo_args(status_parser)
    status_parser.add_argument(
        "--skill",
        dest="skills",
        action="append",
        default=[],
        help="Restrict the command to one shared skill. Repeat for multiple skills.",
    )

    sync_parser = subparsers.add_parser("sync", help="Copy shared skills in one direction.")
    configure_repo_args(sync_parser)
    sync_parser.add_argument(
        "--from",
        dest="source_repo",
        required=True,
        choices=("agents", "plugin"),
        help="Which repo supplies the shared skill content.",
    )
    sync_parser.add_argument(
        "--to",
        dest="destination_repo",
        required=True,
        choices=("agents", "plugin"),
        help="Which repo receives the shared skill content.",
    )
    sync_parser.add_argument(
        "--skill",
        dest="skills",
        action="append",
        default=[],
        help="Restrict the sync to one shared skill. Repeat for multiple skills.",
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned sync work without changing either repo.",
    )

    return parser.parse_args()


def configure_repo_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--agents-repo",
        required=True,
        help="Path to the visionOSAgents repository root.",
    )
    parser.add_argument(
        "--plugin-repo",
        required=True,
        help="Path to the visionos-plugin-codex repository root.",
    )


def main() -> int:
    args = parse_args()
    try:
        repos = load_repos(args.agents_repo, args.plugin_repo)
        selected_skills = choose_skills(repos, args.skills)

        if args.command == "status":
            print_status(repos, selected_skills)
            return 0

        run_sync(
            repos,
            selected_skills,
            source_key=args.source_repo,
            destination_key=args.destination_repo,
            dry_run=args.dry_run,
        )
        return 0
    except SyncError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


def load_repos(agents_repo: str, plugin_repo: str) -> dict[str, RepoState]:
    agents_root = Path(agents_repo).resolve()
    plugin_root = Path(plugin_repo).resolve()

    return {
        "agents": build_repo_state(agents_root, "agents"),
        "plugin": build_repo_state(plugin_root, "plugin"),
    }


def build_repo_state(root: Path, repo_kind: str) -> RepoState:
    if not root.is_dir():
        raise SyncError(f"{repo_kind} repo does not exist: {root}")

    manifest_path = root / MANIFEST_PATH
    if not manifest_path.is_file():
        raise SyncError(f"missing shared skill manifest: {manifest_path}")

    manifest_data = load_json(manifest_path)
    shared_skills = validate_manifest(manifest_data, manifest_path)
    lock_path = root / LOCK_PATH
    lock_data = load_json(lock_path) if lock_path.is_file() else None

    if repo_kind == "agents":
        skills_root = root / "skills"
    else:
        skills_root = detect_plugin_skills_root(root)

    if not skills_root.is_dir():
        raise SyncError(f"missing skills directory for {repo_kind} repo: {skills_root}")

    return RepoState(
        root=root,
        skills_root=skills_root,
        manifest_path=manifest_path,
        lock_path=lock_path,
        shared_skills=shared_skills,
        lock_data=lock_data,
    )


def detect_plugin_skills_root(root: Path) -> Path:
    marketplace_path = root / ".agents/plugins/marketplace.json"
    if not marketplace_path.is_file():
        raise SyncError(f"missing plugin marketplace file: {marketplace_path}")

    marketplace = load_json(marketplace_path)
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise SyncError(f"marketplace file does not define any plugins: {marketplace_path}")

    for plugin in plugins:
        source = plugin.get("source", {})
        if source.get("source") != "local":
            continue
        plugin_path = source.get("path")
        if not isinstance(plugin_path, str) or not plugin_path:
            continue
        candidate = (root / plugin_path).resolve()
        skills_root = candidate / "skills"
        if skills_root.is_dir():
            return skills_root

    raise SyncError(f"could not locate plugin skills directory from {marketplace_path}")


def choose_skills(repos: dict[str, RepoState], requested_skills: list[str]) -> list[str]:
    agents_skills = repos["agents"].shared_skills
    plugin_skills = repos["plugin"].shared_skills

    if agents_skills != plugin_skills:
        raise SyncError(
            "shared skill manifests differ between repos; align sync/shared-skills.json first"
        )

    shared_skills = agents_skills
    if not requested_skills:
        return shared_skills

    invalid = sorted(set(requested_skills) - set(shared_skills))
    if invalid:
        raise SyncError(f"unknown shared skills: {', '.join(invalid)}")

    ordered = [skill for skill in shared_skills if skill in requested_skills]
    return ordered


def validate_manifest(data: dict, manifest_path: Path) -> list[str]:
    version = data.get("version")
    if version != 1:
        raise SyncError(f"unsupported manifest version in {manifest_path}: {version!r}")

    shared_skills = data.get("sharedSkills")
    if not isinstance(shared_skills, list) or not shared_skills:
        raise SyncError(f"sharedSkills must be a non-empty array in {manifest_path}")

    if any(not isinstance(skill, str) or not skill for skill in shared_skills):
        raise SyncError(f"sharedSkills must contain non-empty strings in {manifest_path}")

    if len(shared_skills) != len(set(shared_skills)):
        raise SyncError(f"sharedSkills contains duplicates in {manifest_path}")

    return shared_skills


def print_status(repos: dict[str, RepoState], skills: list[str]) -> None:
    lock_data = load_common_lock(repos)

    if lock_data is None:
        print("status: uninitialized")
        for skill in skills:
            agents_digest = skill_digest_or_missing(repos["agents"], skill)
            plugin_digest = skill_digest_or_missing(repos["plugin"], skill)
            print(
                f"{skill}: agents={agents_digest} plugin={plugin_digest} lock=<missing>"
            )
        return

    lock_digests = extract_lock_digests(lock_data)
    print("status: initialized")

    for skill in skills:
        agents_digest = skill_digest_or_missing(repos["agents"], skill)
        plugin_digest = skill_digest_or_missing(repos["plugin"], skill)
        lock_digest = lock_digests.get(skill)
        state = classify_skill_state(agents_digest, plugin_digest, lock_digest)
        print(
            f"{skill}: {state} agents={agents_digest} plugin={plugin_digest} lock={lock_digest}"
        )


def run_sync(
    repos: dict[str, RepoState],
    skills: list[str],
    source_key: str,
    destination_key: str,
    dry_run: bool,
) -> None:
    if source_key == destination_key:
        raise SyncError("--from and --to must target different repos")

    lock_data = load_common_lock(repos)
    source_repo = repos[source_key]
    destination_repo = repos[destination_key]

    actions: list[tuple[str, str]] = []
    next_digests: dict[str, str] = {}
    conflicts: list[str] = []

    if lock_data is None:
        for skill in skills:
            source_digest = skill_digest_or_missing(source_repo, skill)
            if source_digest == "<missing>":
                raise SyncError(f"source skill is missing from {source_key} repo: {skill}")
            actions.append((skill, "baseline-copy"))
            next_digests[skill] = source_digest
    else:
        lock_digests = extract_lock_digests(lock_data)
        for skill in skills:
            source_digest = skill_digest_or_missing(source_repo, skill)
            destination_digest = skill_digest_or_missing(destination_repo, skill)
            lock_digest = lock_digests.get(skill)

            if source_digest == "<missing>":
                raise SyncError(f"source skill is missing from {source_key} repo: {skill}")

            state = classify_skill_state(
                agents_digest=skill_digest_or_missing(repos["agents"], skill),
                plugin_digest=skill_digest_or_missing(repos["plugin"], skill),
                lock_digest=lock_digest,
            )

            if state == "conflict":
                conflicts.append(skill)
                continue
            if state == "lock-missing":
                if destination_digest == source_digest:
                    actions.append((skill, "lock-repair"))
                else:
                    actions.append((skill, "baseline-copy"))
                next_digests[skill] = source_digest
                continue
            if state == "clean":
                next_digests[skill] = source_digest
                continue
            if state == "both-changed-same":
                actions.append((skill, "lock-update"))
                next_digests[skill] = source_digest
                continue

            if state == f"{source_key}-changed":
                actions.append((skill, "copy"))
                next_digests[skill] = source_digest
                continue

            if state == f"{destination_key}-changed":
                raise SyncError(
                    f"{skill} only changed in the destination repo; use --from {destination_key} --to {source_key}"
                )

            raise SyncError(f"unexpected state for {skill}: {state}")

    if conflicts:
        raise SyncError(
            "conflicting changes detected in both repos: " + ", ".join(sorted(conflicts))
        )

    if not actions and lock_data is not None:
        print("No shared skill content needed copying.")
        return

    if actions:
        for skill, action in actions:
            if action == "copy" or action == "baseline-copy":
                print(f"{action}: {source_key} -> {destination_key} {skill}")
            else:
                print(f"{action}: {skill}")
    else:
        print("No shared skill files changed; refreshing the lock file only.")

    if dry_run:
        print("Dry run only; no files were changed.")
        return

    for skill, action in actions:
        if action in {"copy", "baseline-copy"}:
            copy_skill(source_repo, destination_repo, skill)

    final_digests = compute_final_digests(repos, skills, source_key, destination_key, next_digests)
    write_shared_lock(repos, final_digests, source_key, destination_key, skills)


def compute_final_digests(
    repos: dict[str, RepoState],
    selected_skills: list[str],
    source_key: str,
    destination_key: str,
    next_digests: dict[str, str],
) -> dict[str, str]:
    lock_data = load_common_lock(repos)
    final_digests = {}

    if lock_data is not None:
        final_digests.update(extract_lock_digests(lock_data))

    final_digests.update(next_digests)

    for skill in selected_skills:
        source_digest = skill_digest_or_missing(repos[source_key], skill)
        destination_digest = skill_digest_or_missing(repos[destination_key], skill)
        if source_digest == "<missing>" or destination_digest == "<missing>":
            raise SyncError(f"shared skill is missing after sync: {skill}")
        if source_digest != destination_digest:
            raise SyncError(f"sync produced mismatched digests for {skill}")
        final_digests[skill] = source_digest

    return final_digests


def load_common_lock(repos: dict[str, RepoState]) -> dict | None:
    agents_lock = repos["agents"].lock_data
    plugin_lock = repos["plugin"].lock_data

    if agents_lock is None and plugin_lock is None:
        return None
    if agents_lock is None or plugin_lock is None:
        raise SyncError("one repo is missing sync/shared-skills.lock.json")
    if agents_lock != plugin_lock:
        raise SyncError("shared skill lock files differ between repos")
    if agents_lock.get("version") != 1:
        raise SyncError("unsupported lock file version")
    return agents_lock


def extract_lock_digests(lock_data: dict) -> dict[str, str]:
    lock_skills = lock_data.get("skills")
    if not isinstance(lock_skills, dict):
        raise SyncError("lock file is missing the skills map")

    digests: dict[str, str] = {}
    for skill, entry in lock_skills.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("digest"), str):
            raise SyncError(f"lock entry for {skill!r} is invalid")
        digests[skill] = entry["digest"]
    return digests


def classify_skill_state(
    agents_digest: str,
    plugin_digest: str,
    lock_digest: str | None,
) -> str:
    if lock_digest is None:
        return "lock-missing"
    if agents_digest == lock_digest and plugin_digest == lock_digest:
        return "clean"
    if agents_digest != lock_digest and plugin_digest == lock_digest:
        return "agents-changed"
    if agents_digest == lock_digest and plugin_digest != lock_digest:
        return "plugin-changed"
    if agents_digest == plugin_digest:
        return "both-changed-same"
    return "conflict"


def write_shared_lock(
    repos: dict[str, RepoState],
    digests: dict[str, str],
    source_key: str,
    destination_key: str,
    selected_skills: list[str],
) -> None:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "version": 1,
        "lastSync": {
            "at": timestamp,
            "source": source_key,
            "destination": destination_key,
            "skills": list(selected_skills),
        },
        "skills": {
            skill: {"digest": digests[skill]}
            for skill in sorted(digests)
        },
    }

    for repo in repos.values():
        write_json(repo.lock_path, payload)


def copy_skill(source_repo: RepoState, destination_repo: RepoState, skill: str) -> None:
    source_dir = source_repo.skills_root / skill
    destination_dir = destination_repo.skills_root / skill

    if not source_dir.is_dir():
        raise SyncError(f"source skill directory does not exist: {source_dir}")

    if destination_dir.exists():
        shutil.rmtree(destination_dir)

    shutil.copytree(source_dir, destination_dir, ignore=ignore_entries)
    remove_ignored_entries(destination_dir)


def ignore_entries(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORED_NAMES}


def remove_ignored_entries(root: Path) -> None:
    for path in root.rglob("*"):
        if path.name not in IGNORED_NAMES:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def skill_digest_or_missing(repo: RepoState, skill: str) -> str:
    skill_dir = repo.skills_root / skill
    if not skill_dir.is_dir():
        return "<missing>"
    return digest_directory(skill_dir)


def digest_directory(root: Path) -> str:
    hasher = hashlib.sha256()

    for relative_path, file_path in iter_files(root):
        hasher.update(relative_path.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file_path.read_bytes())
        hasher.update(b"\0")

    return hasher.hexdigest()


def iter_files(root: Path) -> Iterable[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        relative = path.relative_to(root)
        if should_ignore(relative):
            continue
        files.append((relative.as_posix(), path))

    files.sort(key=lambda item: item[0])
    return files


def should_ignore(relative_path: Path) -> bool:
    return any(part in IGNORED_NAMES for part in relative_path.parts)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SyncError(f"invalid JSON in {path}: {error}") from error


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
