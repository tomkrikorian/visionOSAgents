# Custom Components

Use this file when an entity needs custom per-entity state.

```swift
import RealityKit

struct SpinComponent: Component, Codable {
    var speed: Float = 1.0
    var axis: SIMD3<Float> = [0, 1, 0]
}

// Register once during app startup before any scene or asset uses this type.
SpinComponent.registerComponent()
```

## Runtime Pattern

```swift
entity.components.set(SpinComponent(speed: 0.6))

if var spin = entity.components[SpinComponent.self] {
    spin.speed = 1.2
    entity.components.set(spin)
}
```

## Rules

- Prefer composition over inheritance.
- Conform to `Codable` for components that load from Reality Composer Pro,
  USD, saved scenes, or synchronized state.
- Register every custom component type once before attaching it to entities or
  loading content that may decode it. Built-in RealityKit components do not
  need manual registration.
- Keep the component focused on data, not behavior.
- Store continuous behavior in a `System`; store per-entity state in the
  component.
- Treat component mutation as read-copy-write. Fetch the value, modify the
  local copy, then set it back on the entity.
- Keep reference-type or process-local state out of serializable components.
  Use `TransientComponent` for local-only entities that should not persist or
  sync.
