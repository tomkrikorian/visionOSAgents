# System and Component Creation

**Reference:** [System Documentation](https://developer.apple.com/documentation/realitykit/system) | [Component Documentation](https://developer.apple.com/documentation/realitykit/component)

## Overview

This guide covers creating custom Systems and Components in RealityKit's Entity Component System (ECS). Systems define continuous behavior that affects multiple entities every scene update, while Components store per-entity data and state. Together, they form the foundation of RealityKit's ECS architecture.

## When to Use

### Systems
- Implementing continuous, per-frame behavior
- Processing multiple entities with shared logic
- Creating game mechanics that update over time
- Optimizing performance by batching entity updates
- Implementing physics, animation, or AI behaviors

### Components
- Storing per-entity state and data
- Creating custom properties for entities
- Defining entity behavior through composition
- Enabling systems to query and process entities
- Persisting entity state across scene saves

## How to Use

### Creating Custom Components

Components store per-entity data and must conform to the `Component` protocol. For serialization support, also conform to `Codable`:

```swift
import RealityKit

// Simple component with Codable for serialization
struct HealthComponent: Component, Codable {
    var currentHealth: Float
    var maxHealth: Float
    
    init(currentHealth: Float, maxHealth: Float) {
        self.currentHealth = currentHealth
        self.maxHealth = maxHealth
    }
}

// Component with default values
struct SpinComponent: Component, Codable {
    var speed: Float = 1.0
    var axis: SIMD3<Float> = [0, 1, 0]
}

// Register custom component before use
HealthComponent.registerComponent()
```

### Attaching Components to Entities

```swift
let entity = Entity()

// Set a component
entity.components.set(HealthComponent(currentHealth: 100, maxHealth: 100))

// Access a component
if let health = entity.components[HealthComponent.self] {
    print("Health: \(health.currentHealth)")
}

// Remove a component
entity.components.remove(HealthComponent.self)
```

### Real-World Example: Rotation Component and System

This example from the Hello World sample shows a complete component and system implementation for rotating entities:

```swift
import RealityKit

/// Rotation information for an entity.
struct RotationComponent: Component {
    var speed: Float
    var axis: SIMD3<Float>

    init(speed: Float = 1.0, axis: SIMD3<Float> = [0, 1, 0]) {
        self.speed = speed
        self.axis = axis
    }
}

/// A system that rotates entities with a rotation component.
struct RotationSystem: System {
    static let query = EntityQuery(where: .has(RotationComponent.self))

    init(scene: RealityKit.Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard let component: RotationComponent = entity.components[RotationComponent.self] else { continue }
            entity.setOrientation(
                .init(angle: component.speed * Float(context.deltaTime), axis: component.axis),
                relativeTo: entity
            )
        }
    }
}

// Register in app initialization
RotationComponent.registerComponent()
RotationSystem.registerSystem()
```

### Real-World Example: Trace Component and System

This example shows a more complex component that stores mesh data and a system that dynamically updates geometry:

```swift
import RealityKit

/// Trace information for an entity.
struct TraceComponent: Component {
    var accumulatedTime: TimeInterval = 0
    var mesh: TraceMesh
    var isPaused: Bool = false
    weak var anchor: Entity?
    var model: ModelEntity?

    init(anchor: Entity, width: Float) {
        self.anchor = anchor
        self.mesh = TraceMesh(width: width)
    }
}

/// A system that draws a trace behind moving entities.
struct TraceSystem: System {
    static let query = EntityQuery(where: .has(TraceComponent.self))

    init(scene: Scene) { }

    func update(context: SceneUpdateContext) {
        for satellite in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            var trace: TraceComponent = satellite.components[TraceComponent.self]!
            defer { satellite.components[TraceComponent.self] = trace }

            guard let anchor = trace.anchor else { return }

            trace.accumulatedTime += context.deltaTime
            if trace.isPaused || trace.accumulatedTime <= 0.025 { return }
            trace.accumulatedTime = 0

            // Store the satellite's current position
            trace.mesh.addPosition(of: satellite, relativeTo: anchor)

            // Update or create the trace mesh
            let contents = trace.mesh.meshContents
            if let model = trace.model {
                try? model.model?.mesh.replace(with: contents)
            } else {
                let model = try? ModelEntity.makeTraceModel(with: contents)
                model?.name = "\(anchor.name)-trace"
                trace.model = model
                anchor.addChild(model!)
            }
        }
    }
}

// Register in app initialization
TraceComponent.registerComponent()
TraceSystem.registerSystem()
```

### Basic System Implementation

```swift
import RealityKit

// Define a component for state
struct SpinComponent: Component, Codable {
    var speed: Float
}

// Create a system that processes entities with SpinComponent
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

// Register the system
SpinSystem.registerSystem()
```

### System with Dependencies

```swift
struct DamageSystem: System {
    static let query = EntityQuery(where: .has(DamageComponent.self))
    
    static var dependencies: [SystemDependency] {
        [.after(PhysicsSystem.self)]
    }
    
    init(scene: Scene) {}
    
    func update(context: SceneUpdateContext) {
        // Process damage after physics simulation
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            // Apply damage logic
        }
    }
}
```

### System with Multiple Component Requirements

```swift
struct HealthSystem: System {
    static let query = EntityQuery(
        where: .has(HealthComponent.self) && .has(PhysicsBodyComponent.self)
    )
    
    init(scene: Scene) {}
    
    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard let health = entity.components[HealthComponent.self] else { continue }
            if health.currentHealth <= 0 {
                // Handle entity death
            }
        }
    }
}
```

### Real-World Example: System with ARKit Integration

This example from the Head Tracking sample shows how to create a system that uses ARKit to follow the device's position:

```swift
import RealityKit
import ARKit

/// A component to mark entities that should follow the device
public struct FollowComponent: Component, Codable {}

/// A system that moves entities to the device's transform each frame
public struct FollowSystem: System {
    static let query = EntityQuery(where: .has(FollowComponent.self))
    private let arkitSession = ARKitSession()
    private let worldTrackingProvider = WorldTrackingProvider()
    
    public init(scene: RealityKit.Scene) {
        runSession()
    }
    
    func runSession() {
        Task {
            do {
                try await arkitSession.run([worldTrackingProvider])
            } catch {
                print("Error: \(error). Head-position mode will still work.")
            }
        }
    }
    
    public func update(context: SceneUpdateContext) {
        // Check whether the world-tracking provider is running
        guard worldTrackingProvider.state == .running else { return }
        
        // Query the device anchor at the current time
        guard let deviceAnchor = worldTrackingProvider.queryDeviceAnchor(
            atTimestamp: CACurrentMediaTime()
        ) else { return }
        
        // Find the transform of the device
        let deviceTransform = Transform(matrix: deviceAnchor.originFromAnchorTransform)
    
        // Iterate through each entity in the scene containing FollowComponent
        let entities = context.entities(matching: Self.query, updatingSystemWhen: .rendering)
        
        for entity in entities {
            // Move the entity to the device's transform with smooth animation
            entity.move(
                to: deviceTransform,
                relativeTo: entity.parent,
                duration: 1.2,
                timingFunction: .easeInOut
            )
        }
    }
}

// Register in app initialization
FollowComponent.registerComponent()
FollowSystem.registerSystem()
```

## Key Concepts

### Entity Queries

Use `EntityQuery` with `QueryPredicate` to find entities that match specific criteria:

```swift
// Entities with a specific component
static let query = EntityQuery(where: .has(MyComponent.self))

// Entities with multiple components
static let query = EntityQuery(
    where: .has(ComponentA.self) && .has(ComponentB.self)
)

// Entities without a component
static let query = EntityQuery(where: .has(ComponentA.self) && !.has(ComponentB.self))
```

### Update Timing

Use `updatingSystemWhen` to control when the system updates:

- `.rendering` - Updates during rendering phase
- `.physics` - Updates during physics phase

### System Dependencies

Define update order using `SystemDependency`:

```swift
static var dependencies: [SystemDependency] {
    [
        .after(PhysicsSystem.self),
        .before(RenderingSystem.self)
    ]
}
```

## Important Notes

- Systems form a directed acyclic graph (DAG) - no circular dependencies
- Properties of a system are never serialized - store data in components
- Each system instance runs once per simulation step
- Systems without dependencies are updated in registration order
- Conflicting dependencies are ignored with a warning

## Best Practices

- Store per-entity state in components, not in the system
- Use `EntityQuery` to efficiently find relevant entities
- Define dependencies to ensure correct update order
- Profile system performance on device
- Keep system logic focused on a single responsibility
- Use `updatingSystemWhen` appropriately for your use case

## Registration

### Registering Components

Always register custom components before use:

```swift
// Register a component
MyComponent.registerComponent()
```

This ensures the component can be properly serialized and deserialized when saving/loading scenes.

### Registering Systems

Always register your system before use:

```swift
MySystem.registerSystem()
```

This is typically done in your app's initialization code or scene setup. Systems are registered globally and will be available to all scenes.

## Related APIs

### Component APIs
- `Component.registerComponent()` - Register a custom component
- `Component` - Protocol for all components
- `Codable` - Protocol for serializable components
- `Entity.components.set(_:)` - Attach a component to an entity
- `Entity.components[ComponentType.self]` - Access a component from an entity

### System APIs
- `System.registerSystem()` - Register a system with RealityKit
- `SystemDependency` - Control update order
- `EntityQuery` - Query entities from the scene
- `SceneUpdateContext` - Context for system updates
- `QueryPredicate` - Define query criteria
