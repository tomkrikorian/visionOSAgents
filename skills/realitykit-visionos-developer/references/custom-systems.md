# Custom Systems

Use this file when behavior spans many entities or updates continuously.

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
            entity.transform.rotation *= simd_quatf(
                angle: spin.speed * Float(context.deltaTime),
                axis: [0, 1, 0]
            )
        }
    }
}

SpinSystem.registerSystem()
```

## Rules

- Query only the entities the system actually needs.
- Keep continuous behavior in `update(context:)`.
- Use system dependencies when ordering matters.
- Prefer systems over ad hoc per-frame work in SwiftUI closures.
