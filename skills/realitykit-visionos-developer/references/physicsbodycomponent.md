# PhysicsBodyComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/physicsbodycomponent)

## Overview

A component that defines an entity's behavior in physics body simulations. Only entities with a `PhysicsBodyComponent` and a `CollisionComponent` can participate in a scene's physics simulation. If you need to move an entity that participates in the physics system, it also needs a `PhysicsMotionComponent`.

## When to Use

- Creating entities that respond to physics forces
- Implementing gravity, collisions, and physical interactions
- Building dynamic objects that fall, bounce, or move
- Creating static objects that other entities can collide with
- Simulating realistic physical behavior

## How to Use

### Basic Physics Body

```swift
import RealityKit

// Create a dynamic physics body
var body = PhysicsBodyComponent()
body.mode = .dynamic
entity.components.set(body)

// Also requires CollisionComponent
let shapes: [ShapeResource] = [.generateBox(size: [0.1, 0.1, 0.1])]
entity.components.set(CollisionComponent(shapes: shapes))
```

### Static Physics Body

```swift
// Create a static body (doesn't move but can be collided with)
var body = PhysicsBodyComponent()
body.mode = .static
entity.components.set(body)
```

### Physics Body with Mass

```swift
// Create with specific mass
let shapes: [ShapeResource] = [.generateSphere(radius: 0.1)]
let body = PhysicsBodyComponent(
    shapes: shapes,
    mass: 1.0,
    material: nil,
    mode: .dynamic
)
entity.components.set(body)
```

### Physics Body with Material

```swift
// Create with physics material (friction, restitution)
let material = PhysicsMaterialResource(friction: 0.5, restitution: 0.8)
let body = PhysicsBodyComponent(
    shapes: shapes,
    density: 1.0,
    material: material,
    mode: .dynamic
)
entity.components.set(body)
```

### Locking Movement

```swift
var body = PhysicsBodyComponent()
body.mode = .dynamic
body.isTranslationLocked = (false, true, false) // Lock Y axis
body.isRotationLocked = (true, false, true) // Lock X and Z rotation
entity.components.set(body)
```

## Key Properties

- `mode: PhysicsBodyMode` - Behavioral mode (.dynamic, .static, .kinematic)
- `massProperties: PhysicsMassProperties` - Mass, inertia, and center of mass
- `material: PhysicsMaterialResource?` - Friction and restitution properties
- `isAffectedByGravity: Bool` - Whether gravity acts on the body
- `linearDamping: Float` - Controls how fast translation motion approaches zero
- `angularDamping: Float` - Controls how fast rotational motion approaches zero
- `isTranslationLocked: (Bool, Bool, Bool)` - Locks position along axes
- `isRotationLocked: (Bool, Bool, Bool)` - Locks rotation around axes
- `isContinuousCollisionDetectionEnabled: Bool` - For fast-moving objects

## Important Notes

- Model entities have a physics body component by default
- Requires `CollisionComponent` to participate in physics simulation
- Non-uniform scaling is only supported for box, convex mesh, and triangle mesh collision shapes
- If using non-uniform scale, avoid adding children with rotations below the scaled entity
- Use `PhysicsMotionComponent` to control velocity of physics bodies

## Physics Body Modes

- `.dynamic` - Fully participates in physics, responds to forces and collisions
- `.static` - Doesn't move but can be collided with (ground, walls)
- `.kinematic` - Moved by code but can push dynamic bodies

## Best Practices

- Use static bodies for immovable objects (ground, walls)
- Use dynamic bodies for objects that should respond to physics
- Set appropriate mass values for realistic behavior
- Use physics materials to control friction and bounciness
- Lock axes when you want to restrict movement (2D games, sliding doors)
- Enable continuous collision detection for fast-moving objects
- Keep collision shapes simple and aligned with mesh scale

## Related Components

- `CollisionComponent` - Required for physics participation
- `PhysicsMotionComponent` - For controlling velocity
- `PhysicsSimulationComponent` - For configuring simulation parameters
- `ForceEffectComponent` - For applying force fields
