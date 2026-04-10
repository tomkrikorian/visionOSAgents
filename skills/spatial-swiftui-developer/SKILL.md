---
name: spatial-swiftui-developer
description: Design and implement visionOS 26 SwiftUI scenes that integrate RealityKit content. Use when building spatial UI with RealityView, Model3D, attachments, volumetric windows, ImmersiveSpace, or spatial gestures, or when choosing SwiftUI vs RealityKit APIs for 3D presentation.
---

# Spatial SwiftUI Developer

## Quick Start

1. If the task is really about surface choice, scene ownership, or file
   structure, switch to `spatial-app-architecture` first.
2. Pick the rendering track: `Model3D` for simple asset display, `RealityView`
   for custom entity graphs and attachments.
3. Load the matching reference only after you know the track you are on:
   - `windowing-immersion.md` for scene structure and transitions
   - `realityview.md` for RealityView, attachments, and update flow
   - `model3d.md` for model loading and simple presentation
   - `interaction.md` for gestures and manipulation
   - `spatial-layout.md` for layout, sizing, and debug helpers
4. Implement async loading and keep RealityKit mutations inside `RealityView`
   closures or explicit systems.
5. Route build, launch, simulator, and test problems to the plugin's
   `build-run-debug` workflow skill instead of expanding this skill with
   execution steps.

## Tracks

### Scene Shell

Use this track when the surface model is already chosen and you need to map it
to SwiftUI APIs.

- Start with `WindowGroup` unless the UI needs volume or immersion.
- Use `windowStyle(.volumetric)` for volume-style surfaces.
- Use `ImmersiveSpace` only when the experience needs an unbounded spatial scene.
- Use `defaultSize` as a hint for initial geometry, not a guarantee.

### RealityKit Bridge

Use this track when SwiftUI needs to host real 3D scene content.

- Use `RealityView` for scene loading, attachments, and state-driven entity updates.
- Use `Attachment` or `ViewAttachmentComponent` for SwiftUI UI placed in 3D.
- Keep entity mutation out of SwiftUI body computation.

### Interaction and Motion

Use this track when the scene needs direct manipulation or spatial gestures.

- Add `SpatialTapGesture` and entity-targeted input where needed.
- Prefer attachment-driven labels and controls for UI that must stay SwiftUI-native.
- Use `interaction.md` before adding custom gesture or manipulation logic.

### Data Visualization

Use this track when the scene is primarily charts or analytic surfaces.

- Load `charts-3d.md` only after confirming the chart belongs in spatial UI.
- Keep chart state separate from the spatial shell so it can be reused in 2D fallbacks.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When you need the general feature map, examples, and routing guidance for this skill. |
| [`model3d.md`](references/model3d.md) | When using `Model3D` for async model loading, assets, animation, or manipulation. |
| [`realityview.md`](references/realityview.md) | When setting up `RealityView`, attachments, or RealityKit integration patterns. |
| [`interaction.md`](references/interaction.md) | When implementing gestures or manipulation patterns for spatial input. |
| [`windowing-immersion.md`](references/windowing-immersion.md) | When managing windows, volumetric surfaces, or immersive space transitions. |
| [`spatial-layout.md`](references/spatial-layout.md) | When using SwiftUI spatial layout APIs, sizing, or debug tools. |
| [`charts-3d.md`](references/charts-3d.md) | When implementing `Chart3D` or other spatial data-visualization patterns. |

## Guardrails

- Keep RealityKit loads async; do not block the main actor with asset or entity loading.
- Mutate RealityKit content in `RealityView` make/update closures or in a system, not in SwiftUI body code.
- Use `Model3D` only when you need simple display and layout, not a custom ECS graph.
- Treat `ImmersiveSpace` as a separate scene with its own lifecycle and environment actions.
- Use `defaultSize` as an initial hint only; the system can clamp or restore geometry.
- Switch to the plugin's `build-run-debug` skill when the question is about launch, build, simulator, codesign, or debugging workflow.
- Use `spatial-app-architecture` when the question is about scene boundaries,
  ownership, or feature decomposition rather than API usage.

## Core Concepts

### Scene and Spatial Presentation

- Use `WindowGroup` with `windowStyle(.volumetric)` for volumes. Add `defaultSize` when you want a predictable initial size, but treat it as a hint rather than a hard guarantee.
- Use `ImmersiveSpace` for unbounded spatial scenes and `immersionStyle` selection.
- Use `openImmersiveSpace` and `dismissImmersiveSpace` for transitions.
- On visionOS 26, apply `defaultWorldScaling(_:)` with a `WorldScalingBehavior` when you want a volume or window to scale with viewing distance, and use `supportedVolumeViewpoints(_:)` + `onVolumeViewpointChange(updateStrategy:initial:_:)` to adjust layout when the viewer moves around a volume.
- Use `volumeBaseplateVisibility(_:)` to hide or show the system baseplate under a volume.

### RealityKit Embedding in SwiftUI

- Use `RealityView` for full RealityKit scenes and state-driven updates.
- Use `Attachment` and RealityView attachments to embed SwiftUI views in 3D.
- Use `ViewAttachmentEntity` and `ViewAttachmentComponent` for attachment entities.
- Use `breakthroughEffect(_:)` to apply the visionOS 26 breakthrough effect to RealityView attachments when the design calls for it.
- Use `visualEffect3D(_:)` to layer 3D visual effects on spatial content.

### 3D Model Presentation

- Use `Model3D` for async model loading with SwiftUI layout.
- Use `Model3DPhase` and `Model3DAsset` for loading phases and animation choices.

### Spatial Input

- Use `SpatialTapGesture` for spatial tap locations in 2D/3D coordinate spaces.

### Implementation Patterns

- Use `Model3D` when you only need display and layout; use `RealityView` for custom entity graphs and systems.
- Keep RealityKit mutations inside `RealityView` make/update closures.
- Prefer attachments for UI that should remain SwiftUI-driven but positioned in 3D.
- Treat `ImmersiveSpace` as a separate scene with its own lifecycle and environment actions.
- Prefer a custom `System` or `SceneEvents.Update` when behavior truly needs
  continuous per-frame updates.

### Pitfalls and Checks

- Do not block the main actor with synchronous model or entity loading.
- Do not update RealityKit entities inside SwiftUI body computation.
- Do not use volumetric window style with `Window` instead of `WindowGroup`.
- Do not treat `defaultSize` as a hard requirement or guaranteed final size; the system can clamp or restore window geometry.
- Use `.glassBackgroundEffect()` when you want the system glass treatment on visionOS, and use custom backgrounds deliberately when the design needs a different visual language.
