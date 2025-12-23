# PhysicsMotionComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/physicsmotioncomponent)

## Overview

A component that controls the linear and angular velocity of physics bodies. Use this component to set or modify the motion properties of entities that have a `PhysicsBodyComponent`. This allows you to programmatically control how physics bodies move and rotate.

## When to Use

- Setting initial velocity for physics bodies (throwing, launching, etc.)
- Controlling velocity of physics bodies programmatically
- Implementing player-controlled movement in physics simulations
- Creating moving platforms or kinematic objects
- Applying impulses or forces to physics bodies
- Implementing custom movement systems that work with physics

## How to Use

### Basic Setup

```swift
import RealityKit

// Create physics body first
let physics = PhysicsBodyComponent(
    massProperties: .default,
    material: nil,
    mode: .dynamic
)
entity.components.set(physics)

// Set motion with linear and angular velocity
let motion = PhysicsMotionComponent(
    linearVelocity: [1, 0, 0],  // Move along X axis at 1 m/s
    angularVelocity: [0, 1, 0]   // Rotate around Y axis at 1 rad/s
)
entity.components.set(motion)
```

### Throwing an Object

```swift
// Launch an entity with initial velocity
let throwVelocity = SIMD3<Float>(2.0, 5.0, 0.0)  // Forward and up
let motion = PhysicsMotionComponent(linearVelocity: throwVelocity)
entity.components.set(motion)
```

### Rotating Object

```swift
// Make an object spin
let spinVelocity = SIMD3<Float>(0, 2.0, 0)  // Rotate around Y axis
let motion = PhysicsMotionComponent(
    linearVelocity: .zero,
    angularVelocity: spinVelocity
)
entity.components.set(motion)
```

### Updating Motion Dynamically

```swift
// Update motion during gameplay
if var motion = entity.components[PhysicsMotionComponent.self] {
    motion.linearVelocity = newVelocity
    motion.angularVelocity = newAngularVelocity
    entity.components[PhysicsMotionComponent.self] = motion
}
```

## Key Properties

- `linearVelocity: SIMD3<Float>` - The velocity vector in meters per second for linear motion (X, Y, Z)
- `angularVelocity: SIMD3<Float>` - The rotational velocity in radians per second around each axis (X, Y, Z)

## Important Notes

- Requires a `PhysicsBodyComponent` with mode `.dynamic` or `.kinematic` to have any effect
- Static bodies (`.static` mode) don't respond to motion components
- Velocity values are integrated each physics simulation step
- Extremely large velocity values may cause instability or tunneling
- Motion is affected by damping (`linearDamping`, `angularDamping` on `PhysicsBodyComponent`)
- Gravity and other force effects also affect motion
- The component can be updated dynamically during runtime

## Best Practices

- Set appropriate velocity values - avoid extremely large values that cause instability
- Consider damping when motion doesn't behave as expected
- Use for initial velocity, then let physics simulation handle ongoing motion
- Update motion component dynamically for player-controlled movement
- Combine with `PhysicsBodyComponent` locking to restrict movement along certain axes
- Test velocity values on device for realistic behavior
- Use continuous collision detection for fast-moving objects

## Related Components

- `PhysicsBodyComponent` - Required for motion to have any effect
- `CollisionComponent` - Required for physics participation
- `PhysicsSimulationComponent` - For configuring simulation parameters
- `ForceEffectComponent` - For applying force fields that affect motion
