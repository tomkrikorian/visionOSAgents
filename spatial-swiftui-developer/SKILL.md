---
name: spatial-swiftui-developer
description: Design and implement visionOS SwiftUI scenes that integrate RealityKit content. Use when building spatial UI with RealityView, Model3D, attachments, volumetric windows, ImmersiveSpace, or spatial gestures, or when choosing SwiftUI vs RealityKit APIs for 3D presentation.
---

# Spatial SwiftUI Designer (visionOS)

## Overview

Use this skill to design SwiftUI-based spatial interfaces that embed RealityKit content on visionOS and to choose the right SwiftUI entry points for 3D presentation.

## Quick start workflow

1. Identify the presentation surface: `WindowGroup`, volumetric window, or `ImmersiveSpace`.
2. Choose a 3D API: `Model3D` for simple models, `RealityView` for full RealityKit scenes.
3. Load RealityKit content asynchronously and add entities in the `RealityView` make closure.
4. Use RealityView attachments to place SwiftUI UI in 3D space when needed.
5. Add spatial interaction with `SpatialTapGesture` or entity-targeted gestures.
6. Update RealityKit content in the `RealityView` update closure, not in SwiftUI body.
7. Validate scale using `defaultSize` for volumes and `immersionStyle` for immersive spaces.

## Core concepts

### Scene and spatial presentation

- Use `WindowGroup` with `windowStyle(.volumetric)` and `defaultSize` for volumes.
- Use `ImmersiveSpace` for unbounded spatial scenes and `immersionStyle` selection.
- Use `openImmersiveSpace` and `dismissImmersiveSpace` for transitions.

### RealityKit embedding in SwiftUI

- Use `RealityView` for full RealityKit scenes and per-frame updates.
- Use `Attachment` and RealityView attachments to embed SwiftUI views in 3D.
- Use `ViewAttachmentEntity` and `ViewAttachmentComponent` for attachment entities.

### 3D model presentation

- Use `Model3D` for async model loading with SwiftUI layout.
- Use `Model3DPhase` and `Model3DAsset` for loading phases and animation choices.

### Spatial input

- Use `SpatialTapGesture` for spatial tap locations in 2D/3D coordinate spaces.

## Implementation patterns

- Use `Model3D` when you only need display and layout; use `RealityView` for custom entity graphs and systems.
- Keep RealityKit mutations inside `RealityView` make/update closures.
- Prefer attachments for UI that should remain SwiftUI-driven but positioned in 3D.
- Treat `ImmersiveSpace` as a separate scene with its own lifecycle and environment actions.

## Pitfalls and checks

- Do not block the main actor with synchronous model or entity loading.
- Do not update RealityKit entities inside SwiftUI body computation.
- Do not use volumetric window style with `Window` instead of `WindowGroup`.
- Do not omit `defaultSize` for volumes; physical scale will be inconsistent.

## References

- [references/REFERENCE.md](references/REFERENCE.md) - index of feature-focused code patterns.
- [references/model3d.md](references/model3d.md) - Model3D loading, assets, animation, and manipulable.
- [references/realityview.md](references/realityview.md) - RealityView setup, attachments, and RealityKit patterns.
- [references/interaction.md](references/interaction.md) - Gestures and manipulation patterns for spatial input.
- [references/windowing-immersion.md](references/windowing-immersion.md) - Window management and immersive space patterns.
- [references/spatial-layout.md](references/spatial-layout.md) - SwiftUI spatial layout APIs and debug tools.
- [references/charts-3d.md](references/charts-3d.md) - Chart3D and surface plot patterns.
