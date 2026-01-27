#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"
user_skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

normalize_skill_filename() {
  local dir="$1"
  local has_upper=0
  local has_lower=0

  if ls -1 "$dir" | grep -qx "SKILL.MD"; then
    has_upper=1
  fi

  if ls -1 "$dir" | grep -qx "SKILL.md"; then
    has_lower=1
  fi

  if [[ $has_upper -eq 1 && $has_lower -eq 0 ]]; then
    mv "$dir/SKILL.MD" "$dir/.skill_tmp.md"
    mv "$dir/.skill_tmp.md" "$dir/SKILL.md"
  fi
}

if [[ ! -d "$skills_root" ]]; then
  echo "Skills folder not found at $skills_root."
  exit 1
fi

if [[ ! -d "$user_skills_dir" ]]; then
  echo "User skills folder not found at $user_skills_dir."
  exit 1
fi

skill_dirs=()

if [[ $# -gt 0 ]]; then
  for skill_name in "$@"; do
    skill_dir="$skills_root/$skill_name"
    if [[ ! -d "$skill_dir" ]]; then
      echo "Skill not found in repo: $skill_name"
      exit 1
    fi
    skill_dirs+=("$skill_dir")
  done
else
  while IFS= read -r skill_file; do
    skill_dirs+=("$(dirname "$skill_file")")
  done < <(find "$skills_root" -maxdepth 2 -type f \( -name "SKILL.md" -o -name "SKILL.MD" \))
fi

if [[ ${#skill_dirs[@]} -eq 0 ]]; then
  echo "No skills found in $skills_root."
  exit 1
fi

for skill_dir in "${skill_dirs[@]}"; do
  skill_name="$(basename "$skill_dir")"
  src_dir="$user_skills_dir/$skill_name"
  dest_dir="$skills_root/$skill_name"

  if [[ ! -d "$src_dir" ]]; then
    echo "Skipping $skill_name (missing in $user_skills_dir)"
    continue
  fi

  echo "Updating $skill_name <- $src_dir"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$src_dir/" "$dest_dir/"
  else
    mkdir -p "$dest_dir"
    cp -R "$src_dir/." "$dest_dir/"
  fi

  normalize_skill_filename "$dest_dir"
done

echo "Done. Skills updated in $skills_root"
