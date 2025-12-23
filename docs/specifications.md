# Project Specifications

## Overview
This repository provides a curated set of AI agent guidance and skill definitions for visionOS and spatial computing development. It is designed to work with Cursor and OpenAI Codex, focusing on Swift, SwiftUI, RealityKit, and visionOS platform APIs.

## Goals
- Provide clear agent instructions via `AGENTS.MD` for consistent, platform-aligned assistance.
- Package reusable skill definitions for common visionOS workflows.
- Keep guidance aligned with Apple Human Interface Guidelines and visionOS best practices.

## Target Platforms and Tech Stack
- OS: visionOS 26.0+
- Language: Swift 6.2+ (strict concurrency)
- UI: SwiftUI (primary), UIKit only when explicitly required
- 3D/AR: RealityKit and ARKit

## Repository Structure
- `AGENTS.MD`: Primary agent instructions and workflow guidance.
- `skills/`: Skill definitions used by agents.
- `scripts/`: Utility scripts (for example, installing skills into a user environment).
- `docs/`: Project documentation.

## Skills Included
- arkit-visionos-developer
- coding-standards-enforcer
- ralph-driven-development
- realitykit-visionos-developer
- shareplay-developer
- spatial-swiftui-developer
- shadergraph-editor

## Usage
- Browse `skills/` to inspect or extend individual skill definitions.
- Run `./scripts/install-user-skills.sh` to install skills into `$CODEX_HOME/skills`.
