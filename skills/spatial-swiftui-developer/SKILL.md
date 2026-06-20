---
name: spatial-swiftui-developer
description: Design and implement visionOS 27 SwiftUI scenes that integrate RealityKit content. Use when building spatial UI with RealityView, Model3D, attachments, volumetric windows, ImmersiveSpace, spatial gestures, windowing, spatial layout, or when choosing SwiftUI vs RealityKit APIs for 3D presentation.
---

# Spatial SwiftUI Developer

## Quick Start

1. If the task is really about surface choice, scene ownership, or file
   structure, switch to `spatial-app-architecture` first.
2. If the task is about `Chart3D`, `SurfacePlot`, 3D chart marks, or
   `Chart3DPose`, switch to `$swiftui-chart3d-developer`.
3. Pick the rendering track: `Model3D` for simple asset display, `RealityView`
   for custom entity graphs and attachments.
4. Load only the matching reference files.
5. Keep loading async and keep RealityKit mutations inside its intended entry
   points.
6. Route build, launch, simulator, and test problems to `build-run-debug`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`swiftui-spatial-overview.md`](references/swiftui-spatial-overview.md) | When you need the general feature map, examples, and routing guidance for this skill. |
| [`model3d.md`](references/model3d.md) | When using `Model3D` for async model loading, assets, animation, or manipulation. |
| [`realityview.md`](references/realityview.md) | When setting up `RealityView`, attachments, or RealityKit integration patterns. |
| [`interaction.md`](references/interaction.md) | When implementing gestures or manipulation patterns for spatial input. |
| [`buttons-and-controls.md`](references/buttons-and-controls.md) | When implementing visible SwiftUI buttons, links styled as buttons, toolbars, forms, or control surfaces. |
| [`swiftui-scene-lifecycle.md`](references/swiftui-scene-lifecycle.md) | When checking official `Window`, `WindowGroup`, `ImmersiveSpace`, open/dismiss, restoration, and launch contracts. |
| [`windowing-immersion.md`](references/windowing-immersion.md) | When managing windows, volumetric surfaces, or immersive space transitions. |
| [`spatial-layout.md`](references/spatial-layout.md) | When using SwiftUI spatial layout APIs, sizing, or debug tools. |

## Workflow

1. Confirm the architecture and scene ownership are already settled.
2. Choose the rendering surface: `Model3D`, `RealityView`, window, volume, or
   immersive scene.
3. Load only the matching reference files.
4. Implement the smallest viable scene and keep mutations in the right layer.
5. Summarize the chosen SwiftUI-to-RealityKit integration path.

## Guardrails

- Every visible button gets an explicit `.buttonBorderShape(...)` (`.capsule`
  for labeled actions, `.circle` for icon-only,
  `.roundedRectangle(radius:)` matching the background for card-like
  buttons - on visionOS this is also what shapes the button's hover
  highlight). Non-button hover surfaces pair `.hoverEffect()` with a matching
  `.contentShape(.hoverEffect, ...)`. Load
  [`buttons-and-controls.md`](references/buttons-and-controls.md) before
  writing any control code - this applies even when buttons are incidental to
  a larger task.
- Keep RealityKit loads async; do not block the main actor with asset or entity loading.
- Mutate RealityKit content in `RealityView` make or update closures or in a
  system, not in SwiftUI body code.
- Use `Model3D` only when you need simple display and layout, not a custom ECS graph.
- Treat `ImmersiveSpace` as a separate scene with its own lifecycle and environment actions.
- Use `defaultSize` as an initial hint only; the system can clamp or restore geometry.
- Use `$swiftui-chart3d-developer` for Chart3D and spatial data visualization.
- Switch to `build-run-debug` when the question is about launch, build,
  simulator, codesign, or debugging workflow.
- Use `spatial-app-architecture` when the question is about scene boundaries,
  ownership, or feature decomposition rather than API usage.
- visionOS 27 SwiftUI adds no new scene, volume, or immersion APIs; the
  guidance here is current for visionOS 27. New in 27: gesture `inputKinds:`
  filtering (see `interaction.md`) plus cross-platform toolbar and navigation
  refinements that also apply on visionOS.

## Output Expectations

Provide:
- the chosen rendering and scene path
- which references were used
- the API surface involved (`Model3D`, `RealityView`, windowing, interaction,
  or layout)
- the main implementation constraint or pitfall
- routing back to architecture, Chart3D, or build/debug if needed
