# visionOS AGENTS & Skills

This repository provides an **AGENTS.MD** and **Skills definitions** designed to be used with **Cursor** and/or **OpenAI Codex**, with a **primary focus on visionOS and spatial computing development**.

It is intended for developers building applications for **Apple Vision Pro**, leveraging Swift, SwiftUI, RealityKit, and visionOS-specific APIs. The goal is to offer a structured, AI-friendly knowledge base that accelerates development while staying aligned with Apple’s platform conventions and best practices.

---

## Skills

All skill definitions live under `skills/`. These skills are available on [skill.sh](https://skill.sh). Each section below includes the install command for that skill.

### visionOS Development

#### arkit-visionos-developer
ARKit session setup, authorization, and data providers on visionOS.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill arkit-visionos-developer
```

#### realitykit-visionos-developer
RealityKit components, systems, and ECS patterns for visionOS.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill realitykit-visionos-developer
```

#### spatial-swiftui-developer
SwiftUI + RealityKit spatial UI patterns for visionOS.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill spatial-swiftui-developer
```

#### shadergraph-editor
Manual .usda ShaderGraph and material editing for RealityKit.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill shadergraph-editor
```

#### shareplay-developer
GroupActivities and SharePlay session lifecycle and sync patterns.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill shareplay-developer
```

### Code Quality & Workflow

#### coding-standards-enforcer
Swift 6 concurrency and language standards enforcement.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill coding-standards-enforcer
```

#### ralph-driven-development
Ralph Driven Development (RDD) spec runner workflow and tooling.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill ralph-driven-development
```

#### ralph-driven-development-linear
RDD workflow that pulls Linear project issues via Linear MCP and runs them sequentially.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill ralph-driven-development-linear
```

### Skill Development

#### tkr-skill-writer
Guide for creating and structuring skills with consistent formatting, clear documentation, and proper reference organization.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill tkr-skill-writer
```

### USD & Assets

#### usd-editor
USD scene editing, composition, prims, and command-line tools.

```bash
npx skills add https://github.com/tomkrikorian/visionOSAgents --skill usd-editor
```

## Install skills without npx (when you have cloned this repo)

If you have cloned this repo and prefer not to use `npx skills add`, you can copy its skills into your user skills directory (`$CODEX_HOME/skills`, defaults to `~/.codex/skills`). From the repo root:

```bash
./scripts/install-user-skills.sh
```

## Pull updates back into the repo (when using a local clone)

If you cloned this repo, use the user-folder install above, and later modify skills in that folder, sync those changes back into your clone with:

```bash
./scripts/pull-update-skills.sh
```

You can also pass one or more skill names to update only those directories:

```bash
./scripts/pull-update-skills.sh arkit-visionos-developer spatial-swiftui-developer
```

---

## Credits

This AGENTS.MD and SKILLS were inspired by the work of:

- [Ivan Campos](https://github.com/ivancampos)  
- [Paul Hudson](https://github.com/twostraws)
- [Pedro Piñera Buendía](https://github.com/pepicrft)
- [Thomas Ricouard](https://github.com/Dimillian/)
- [Sharno](https://github.com/sharno)

---

## Documentation

If you want to know more about AGENTS & SKILLS, look at the official documentation.

### AGENTS.MD

[https://agents.md/](https://agents.md/)

### SKILLS.MD

[https://agentskills.io/](https://agentskills.io/)
