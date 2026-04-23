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

// Register once during app startup, after custom component registration.
SpinSystem.registerSystem()
```

## Update Timing

- Use `.rendering` for visual or interaction state that should track rendered
  frames.
- Use `.physics` only for work that must align with RealityKit physics.
- `context.entities(matching:updatingSystemWhen:)` can increase the rate at
  which RealityKit calls `update(context:)`; if the condition is not met, it
  returns an empty result.

## Dependencies

```swift
static var dependencies: [SystemDependency] {
    [.after(SomeRegisteredSystem.self)]
}
```

Dependencies define ordering between system types. Systems without dependencies
run in registration order, and cycles or conflicting dependencies are ignored
with a runtime warning.

## Rules

- Query only the entities the system actually needs.
- Keep continuous behavior in `update(context:)`.
- Use system dependencies when ordering matters.
- Store serialized or synced state on components, not on the system instance.
- When modifying a component in a system, copy it into a local `var`, mutate it,
  then set it back on the entity.
- Register the system once before the first scene that depends on it is loaded.
- Prefer systems over ad hoc per-frame work in SwiftUI closures.
