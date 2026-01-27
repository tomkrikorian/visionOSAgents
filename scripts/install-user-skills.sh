#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"
user_skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$user_skills_dir"

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

skill_files=()
while IFS= read -r skill_file; do
  skill_files+=("$skill_file")
done < <(find "$skills_root" -maxdepth 2 -type f \( -name "SKILL.md" -o -name "SKILL.MD" \))

if [[ ${#skill_files[@]} -eq 0 ]]; then
  echo "No skills found in $repo_root."
  exit 1
fi

for skill_file in "${skill_files[@]}"; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  dest_dir="$user_skills_dir/$skill_name"

  echo "Installing $skill_name -> $dest_dir"

  if [[ -d "$dest_dir" ]]; then
    rm -rf "$dest_dir"
  fi

  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$skill_dir/" "$dest_dir/"
  else
    mkdir -p "$dest_dir"
    cp -R "$skill_dir/." "$dest_dir/"
  fi

  normalize_skill_filename "$dest_dir"
done

echo "Done. Skills installed in $user_skills_dir"
