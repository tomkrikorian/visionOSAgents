---
name: realitykit-visionos-developer
description: Build, debug, and optimize RealityKit scenes for visionOS 26, including entity/component setup, rendering, animation, physics, audio, input, attachments, and custom systems. Use when implementing RealityKit features or troubleshooting ECS behavior on visionOS.
---

# RealityKit visionOS Developer

## Quick Start

1. Decide whether the task is component selection, scene setup, animation,
   physics, audio, input, or ECS debugging.
2. Load only the component, category, or custom-system references that match
   the task instead of reading the whole catalog.
3. Use `RealityView` as the SwiftUI bridge and keep all content mutation inside
   documented RealityKit entry points.
4. Register custom components before use, then keep per-frame behavior in
   systems instead of ad hoc view logic.
5. Route app launch, simulator flow, or build-debug plumbing to
   `build-run-debug`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`references/component-index.md`](references/component-index.md) | When you need the RealityKit category map and guidance on which component reference to open next. |
| [`references/systemandcomponentcreation.md`](references/systemandcomponentcreation.md) | When you need a complete custom ECS registration, query, and update-order pattern. |
| [`references/modelcomponent.md`](references/modelcomponent.md) | When rendering meshes and materials. |
| [`references/inputtargetcomponent.md`](references/inputtargetcomponent.md) | When making entities interactive. |
| [`references/anchoringcomponent.md`](references/anchoringcomponent.md) | When anchoring content to planes, hands, images, or world targets. |
| [`references/spatialaudiocomponent.md`](references/spatialaudiocomponent.md) | When placing audio in 3D space. |
| [`references/collisioncomponent.md`](references/collisioncomponent.md) | When defining collision shapes or hit testing. |
| [`references/viewattachmentcomponent.md`](references/viewattachmentcomponent.md) | When embedding SwiftUI into 3D space. |
| [`references/synchronizationcomponent.md`](references/synchronizationcomponent.md) | When synchronizing entity state across a session. |
| [`references/custom-components.md`](references/custom-components.md) | When defining custom per-entity state. |
| [`references/custom-systems.md`](references/custom-systems.md) | When implementing custom systems or per-frame behavior. |

## Workflow

1. Classify the task by scene, component, or system responsibility.
2. Load the narrowest matching reference files.
3. Implement or inspect the smallest RealityKit slice that answers the
   question.
4. Keep mutation inside `RealityView`, event handlers, or systems.
5. Summarize the chosen component or system path and the next validation step.

## Guardrails

- Always load assets asynchronously; avoid blocking the main actor.
- On visionOS, `ARView` is not available. Use `RealityView`.
- Keep `RealityView` update logic and ECS mutation out of SwiftUI body code.
- Register custom components and systems once during app startup before scenes
  or assets that depend on them are loaded.
- Prefer `ManipulationComponent.configureEntity(...)` when built-in interaction
  fits the need.
- Prefer a custom `System` when behavior spans multiple entities or needs
  continuous updates.

## Output Expectations

Provide:
- the RealityKit task category
- which references were used
- the component, attachment, or system path chosen
- the main constraint or pitfall
- routing back to SwiftUI, architecture, or build-debug if needed
