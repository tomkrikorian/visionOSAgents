# Custom Components

Use this file when an entity needs new stored state.

```swift
import RealityKit

struct SpinComponent: Component, Codable {
    var speed: Float = 1.0
    var axis: SIMD3<Float> = [0, 1, 0]
}

SpinComponent.registerComponent()
```

## Rules

- Prefer composition over inheritance.
- Conform to `Codable` when serialization matters.
- Register custom components before attaching them to entities.
- Keep the component focused on data, not behavior.
