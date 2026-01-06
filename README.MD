# visionOS AGENTS & Skills

This repository provides an **AGENTS.MD** and **Skills definitions** designed to be used with **Cursor** and/or **OpenAI Codex**, with a **primary focus on visionOS and spatial computing development**.

It is intended for developers building applications for **Apple Vision Pro**, leveraging Swift, SwiftUI, RealityKit, and visionOS-specific APIs. The goal is to offer a structured, AI-friendly knowledge base that accelerates development while staying aligned with Apple’s platform conventions and best practices.

---

## Skills

All skill definitions live under `skills/`.

- `arkit-visionos-developer` - ARKit session setup, authorization, and data providers on visionOS.
- `coding-standards-enforcer` - Swift 6 concurrency and language standards enforcement.
- `realitykit-visionos-developer` - RealityKit components, systems, and ECS patterns for visionOS.
- `ralph-driven-development` - Ralph Driven Development (RDD) spec runner workflow and tooling.
- `shareplay-developer` - GroupActivities and SharePlay session lifecycle and sync patterns.
- `spatial-swiftui-developer` - SwiftUI + RealityKit spatial UI patterns for visionOS.
- `shadergraph-editor` - Manual .usda ShaderGraph and material editing for RealityKit.

## Install Skills to User Folder

Use the script below to copy all repo skills into your user skills directory (`$CODEX_HOME/skills`, defaults to `~/.codex/skills`):

```bash
./scripts/install-user-skills.sh
```

---

## Credits

This AGENTS.MD and SKILLS were inspired by the work of:
- [Ivan Campos](https://github.com/ivancampos)  
- [Paul Hudson](https://github.com/twostraws)
- [Pedro Piñera Buendía](https://github.com/pepicrft)
- [Thomas Ricouard](https://github.com/Dimillian/)

---

## Documentation
If you want to know more about AGENTS & SKILLS, look at the official documentation.

### AGENTS.MD
https://agents.md/

### SKILLS.MD
https://agentskills.io/
