#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"

print_usage() {
  cat <<'EOF'
Usage: pull-update-skills.sh [options] [skill-name ...]

Copies skills from a user skills directory back into this repo's ./skills.

Options:
  -t, --target <codex|agents|xcode>  Select source home (default: codex).
      --home <path>                 Override source home (reads from <home>/skills).
      --skills-dir <path>           Override source skills dir directly.
      --path <path>                 Alias for --skills-dir.
  -h, --help                        Show this help.

Environment variables:
  CODEX_HOME       Home for target=codex (default: ~/.codex)
  AGENTS_HOME      Home for target=agents (default: ~/.agents)
  XCODE_CODEX_HOME Home for target=xcode  (default: ~/Library/Developer/Xcode/CodingAssistant/codex)

Examples:
  ./scripts/pull-update-skills.sh
  ./scripts/pull-update-skills.sh --target xcode
  ./scripts/pull-update-skills.sh --target agents arkit-visionos-developer spatial-swiftui-developer
  ./scripts/pull-update-skills.sh --skills-dir /path/to/skills shadergraph-editor
EOF
}

expand_tilde() {
  local path="$1"
  if [[ "$path" == "~" ]]; then
    printf '%s\n' "$HOME"
    return 0
  fi
  if [[ "$path" == "~/"* ]]; then
    printf '%s\n' "${HOME}${path:1}"
    return 0
  fi
  printf '%s\n' "$path"
}

resolve_home_dir() {
  local target="$1"

  case "$target" in
    codex) printf '%s\n' "${CODEX_HOME:-$HOME/.codex}" ;;
    agents) printf '%s\n' "${AGENTS_HOME:-$HOME/.agents}" ;;
    xcode) printf '%s\n' "${XCODE_CODEX_HOME:-$HOME/Library/Developer/Xcode/CodingAssistant/codex}" ;;
    *)
      echo "Unknown target: $target" >&2
      return 1
      ;;
  esac
}

target="codex"
home_override=""
skills_dir_override=""
skill_names=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        print_usage >&2
        exit 2
      fi
      target="$2"
      shift 2
      ;;
    --home)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        print_usage >&2
        exit 2
      fi
      home_override="$2"
      shift 2
      ;;
    --skills-dir|--path)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        print_usage >&2
        exit 2
      fi
      skills_dir_override="$2"
      shift 2
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        skill_names+=("$1")
        shift
      done
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      print_usage >&2
      exit 2
      ;;
    *)
      skill_names+=("$1")
      shift
      ;;
  esac
done

user_skills_dir=""

if [[ -n "$skills_dir_override" ]]; then
  user_skills_dir="$(expand_tilde "$skills_dir_override")"
elif [[ -n "$home_override" ]]; then
  user_skills_dir="$(expand_tilde "$home_override")/skills"
else
  user_skills_dir="$(resolve_home_dir "$target")/skills"
fi

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

if [[ ${#skill_names[@]} -gt 0 ]]; then
  for skill_name in "${skill_names[@]}"; do
    skill_dirs+=("$skills_root/$skill_name")
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
