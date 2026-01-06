---
name: realitykit-visionos-developer
description: Build, debug, and optimize RealityKit scenes for visionOS, including entity/component setup, rendering, animation, physics, audio, input, attachments, and custom systems. Use when implementing RealityKit features or troubleshooting ECS behavior on visionOS.
---

# RealityKit visionOS Developer

## Overview

Use this skill to implement RealityKit-based spatial experiences on visionOS, focusing on entity composition, component-driven behavior, and ECS systems that update every frame.

## Quick start workflow

1. Start with `RealityView` and its `RealityViewContent` to add entities and attach components.
2. Load assets asynchronously and build a clean entity hierarchy.
3. Add the components you need for rendering, interaction, physics, audio, and animation.
4. Prefer `ViewAttachmentComponent` when embedding SwiftUI into 3D; avoid the `RealityView` attachments closure.
5. Register custom components and systems (`Component.registerComponent()`, `System.registerSystem()`) so they decode and update correctly.
6. Use custom systems for continuous behavior and profile performance on device.

## Core concepts

### Entities and components

- Entities are lightweight containers; behavior comes from components.
- Prefer composition over inheritance and use custom `Component` + `Codable` when you need per-entity state.
- Register custom components once with `Component.registerComponent()` before use.
- Keep entity transforms and component updates on the main actor.

### RealityView and attachments

- Use `RealityView` to bridge SwiftUI and RealityKit.
- Load assets with `Entity(named:)` or `Entity(contentsOf:)` asynchronously and handle errors.
- Prefer `ViewAttachmentComponent` for SwiftUI overlays in 3D and avoid the `RealityView` attachments closure.

### Systems and queries

- Use a custom `System` for continuous, per-frame behavior.
- Query entities with `EntityQuery` + `QueryPredicate` and process them in `update(context:)`.
- Use `SystemDependency` to control update order when multiple systems interact.

### Interaction and physics

- Add `CollisionComponent` and `InputTargetComponent` for input-driven entities.
- Use `ManipulationComponent` for built-in spatial interactions and `GestureComponent` for custom gestures.
- Keep physics bodies and collision shapes aligned with your mesh scale.

### Rendering, lighting, and audio

- Use `ImageBasedLightComponent` and `GroundingShadowComponent` to anchor content visually.
- Use `EnvironmentBlendingComponent` for spatially aware compositing.
- Use `SpatialAudioComponent` and `ReverbComponent` for immersive soundscapes.

## Implementation patterns

### RealityView async load

```swift
RealityView { content in
    do {
        let entity = try await Entity(named: "Scene")
        content.add(entity)
    } catch {
        print("Failed to load entity: \(error)")
    }
}
```

### Interactive entity setup

```swift
let entity = ModelEntity(mesh: .generateBox(size: 0.1))
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))
entity.components.set(InputTargetComponent())
entity.components.set(ManipulationComponent())
```

### Custom system skeleton

```swift
import RealityKit

struct SpinComponent: Component, Codable {
    var speed: Float
}

struct SpinSystem: System {
    static let query = EntityQuery(where: .has(SpinComponent.self))

    init(scene: Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard let spin = entity.components[SpinComponent.self] else { continue }
            entity.transform.rotation *= simd_quatf(angle: spin.speed * Float(context.deltaTime), axis: [0, 1, 0])
        }
    }
}

SpinSystem.registerSystem()
```

## Pitfalls and checks

- Always load assets asynchronously; avoid blocking the main actor.
- Avoid `ARView` on visionOS; use `RealityView`.
- Add `CollisionComponent` + `InputTargetComponent` for draggable or tappable entities.
- Use a custom `System` for continuous behavior instead of the `RealityView` update closure.
- Mesh generation is limited to `box`, `sphere`, `plane`, `cylinder`, and `cone`.

## References

- [references/components.md](references/components.md) - RealityKit component catalog for visionOS.
- [references/systems.md](references/systems.md) - RealityKit systems API surface and ECS utilities.
