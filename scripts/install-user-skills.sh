#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"

print_usage() {
  cat <<'EOF'
Usage: install-user-skills.sh [options] [skill-name ...]

Copies all skills from this repo's ./skills into a user skills directory.

Options:
  -t, --target <codex|agents|xcode>  Select destination home (default: codex).
      --home <path>                 Override destination home (installs to <home>/skills).
      --skills-dir <path>           Override destination skills dir directly.
      --path <path>                 Alias for --skills-dir.
  -h, --help                        Show this help.

Environment variables:
  CODEX_HOME       Home for target=codex (default: ~/.codex)
  AGENTS_HOME      Home for target=agents (default: ~/.agents)
  XCODE_CODEX_HOME Home for target=xcode  (default: ~/Library/Developer/Xcode/CodingAssistant/codex)

Examples:
  ./scripts/install-user-skills.sh
  ./scripts/install-user-skills.sh --target agents
  ./scripts/install-user-skills.sh --target xcode
  ./scripts/install-user-skills.sh --skills-dir /path/to/skills
  ./scripts/install-user-skills.sh shareplay-developer shadergraph-editor
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

if [[ ${#skill_names[@]} -gt 0 ]]; then
  for skill_name in "${skill_names[@]}"; do
    skill_dir="$skills_root/$skill_name"

    if [[ ! -d "$skill_dir" ]]; then
      echo "Skipping $skill_name (missing in $skills_root)"
      continue
    fi

    if [[ -f "$skill_dir/SKILL.md" ]]; then
      skill_files+=("$skill_dir/SKILL.md")
    elif [[ -f "$skill_dir/SKILL.MD" ]]; then
      skill_files+=("$skill_dir/SKILL.MD")
    else
      echo "Skipping $skill_name (missing SKILL.md)"
      continue
    fi
  done
else
  while IFS= read -r skill_file; do
    skill_files+=("$skill_file")
  done < <(find "$skills_root" -maxdepth 2 -type f \( -name "SKILL.md" -o -name "SKILL.MD" \))
fi

if [[ ${#skill_files[@]} -eq 0 ]]; then
  if [[ ${#skill_names[@]} -gt 0 ]]; then
    echo "No matching skills found in $skills_root."
  else
    echo "No skills found in $repo_root."
  fi
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
