# CollisionComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/collisioncomponent)

## Overview

A component that gives an entity the ability to collide with other entities that also have collision components. This component holds the entity's data related to participating in the scene's physics simulation and is also used to calculate collision queries, raycasts, and convex shape casts.

## When to Use

- Making entities interactive (required for input handling)
- Physics simulation and collision detection
- Raycasting and hit testing
- Creating trigger volumes for game logic
- Defining collision boundaries for spatial interactions

## How to Use

### Basic Collision Setup

```swift
import RealityKit

// Create collision shapes
let shapes: [ShapeResource] = [.generateBox(size: [0.1, 0.1, 0.1])]
let collision = CollisionComponent(shapes: shapes)
entity.components.set(collision)
```

### Trigger Volume

```swift
// Create a trigger that detects overlaps but doesn't affect physics
var collision = CollisionComponent(shapes: [.generateSphere(radius: 0.5)])
collision.mode = .trigger
entity.components.set(collision)
```

### Collision Filtering

```swift
// Control which entities can collide with each other
let group = CollisionGroup(rawValue: 1)
let mask = CollisionGroup(rawValue: 2)
let filter = CollisionFilter(group: group, mask: mask)

let collision = CollisionComponent(
    shapes: [.generateBox(size: [1, 1, 1])],
    filter: filter
)
entity.components.set(collision)
```

### Input-Only Collision (No Physics)

```swift
// Enable input but disable physics collision
entity.components.set(InputTargetComponent())

var collision = CollisionComponent(shapes: [.generateSphere(radius: 0.1)])
collision.filter = CollisionFilter(group: [], mask: [])
entity.components.set(collision)
```

## Key Properties

- `shapes: [ShapeResource]` - Collection of shape resources representing the entity's collision boundaries
- `mode: CollisionComponent.Mode` - The collision mode (default, trigger, etc.)
- `filter: CollisionFilter` - Determines which other objects the entity collides with
- `isStatic: Bool` - Whether the collider is static
- `collisionOptions: CollisionComponent.CollisionOptions` - Options for how collisions are reported

## Important Notes

- If an entity has a `PhysicsBodyComponent`, the collision component's mode is ignored
- An entity can be a rigid body OR a trigger, but not both
- Non-uniform scaling is only supported for box, convex mesh, and triangle mesh collision shapes
- For non-uniform scales, avoid adding children with rotations below the scaled entity

## Best Practices

- Keep collision shapes simple and aligned with mesh scale
- Use collision filters to optimize performance by reducing unnecessary collision checks
- Use trigger mode for game logic events (doors, pickups, etc.)
- Combine with `InputTargetComponent` for interactive entities
- Use `PhysicsBodyComponent` for entities that need to participate in physics simulation

## Related Components

- `InputTargetComponent` - Required for input handling
- `PhysicsBodyComponent` - For physics simulation
- `PhysicsMotionComponent` - For controlling physics velocity
