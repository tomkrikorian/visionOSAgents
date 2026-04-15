# Refactor Playbook

Use this file when the app already exists and the structure is the problem.

## Sequence

1. Identify the current root owner and list the concerns it mixes.
2. Freeze the scene boundary first.
3. Move state to the correct owner before splitting views further.
4. Extract immersive lifecycle and RealityKit mutation into named owners.
5. Split files by responsibility, not by arbitrary line count.
6. Re-run build and launch after each meaningful extraction slice.

## Goal

Keep behavior stable while making ownership and scene boundaries explicit.
