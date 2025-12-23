# CharacterControllerComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/charactercontrollercomponent)

## Overview

A component that enables character movement and physics behavior for player-controlled characters in RealityKit. It handles movement, collision detection, ground detection, slope limits, and step limits. The character controller uses a capsule-shaped collider and provides collision information for responsive character movement.

## When to Use

- Implementing player-controlled character movement
- Creating characters that walk, run, or move in 3D space
- Handling character collision with the environment
- Implementing ground detection and slope/step limits
- Creating characters that respond to physics while maintaining control
- Building games or interactive experiences with character movement

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a character controller with capsule collider
let characterController = CharacterControllerComponent(
    radius: 0.3,        // Capsule radius
    height: 1.8,        // Capsule height
    skinWidth: 0.01,    // Buffer to avoid getting stuck
    slopeLimit: 0.7,    // Max slope angle (radians)
    stepLimit: 0.3,     // Max step height
    upVector: [0, 1, 0], // Up direction
    collisionFilter: .default
)
entity.components.set(characterController)
```

### Character Movement

```swift
// Move character and handle collisions
func moveCharacter(_ entity: Entity, direction: SIMD3<Float>, deltaTime: Float) {
    guard let controller = entity.components[CharacterControllerComponent.self] else { return }
    
    // Apply movement
    let movement = direction * deltaTime * speed
    let collision = controller.move(into: movement, relativeTo: entity.parent, deltaTime: deltaTime)
    
    // Handle collision response
    if collision.hitEntity != nil {
        // Character hit something - adjust movement
        // Use collision.hitPosition, hitNormal, etc.
    }
}
```

### With State Component

```swift
// Use CharacterControllerStateComponent to track state
let state = CharacterControllerStateComponent()
entity.components.set(state)

// Check if grounded
if state.isGrounded {
    // Allow jumping
} else {
    // Character is in air
}
```

## Key Properties

### Initializer Parameters

- `radius: Float` - The radius of the character's capsule collider
- `height: Float` - The height of the capsule collider
- `skinWidth: Float` - Buffer around the collider to avoid getting stuck on surfaces
- `slopeLimit: Float` - Maximum slope angle the character can walk up (in radians)
- `stepLimit: Float` - Maximum height the character can step up over
- `upVector: SIMD3<Float>` - Defines which direction is 'up' in your scene (typically [0, 1, 0])
- `collisionFilter: CollisionFilter` - Specifies which collision groups the character interacts with

### Collision Information

- `hitPosition: SIMD3<Float>` - World-space position where collision was detected
- `hitEntity: Entity?` - The entity that was hit
- `hitNormal: SIMD3<Float>` - Normal vector of the collision surface
- `moveDirection: SIMD3<Float>` - Direction of movement
- `moveDistance: Float` - Distance moved

## Important Notes

- Uses a capsule-shaped collider for character collision
- Requires `CollisionComponent` on scene geometry for collision detection
- Movement is handled by calling `move(into:relativeTo:deltaTime:)` method
- Collision information is returned from move operations
- Works with `CharacterControllerStateComponent` to track character state
- Available on iOS, macOS, and visionOS

## Best Practices

- Set appropriate radius and height to match your character model
- Use skinWidth to prevent characters from getting stuck on surfaces
- Configure slopeLimit based on your game's movement requirements
- Set stepLimit to allow characters to step over small obstacles
- Use collision filters to optimize performance
- Combine with `CharacterControllerStateComponent` for state tracking
- Handle collision responses appropriately for smooth movement
- Test movement on various terrain types

## Related Components

- `CharacterControllerStateComponent` - Tracks runtime state (grounded, colliding, etc.)
- `CollisionComponent` - Required on scene geometry for collision detection
- `PhysicsBodyComponent` - Not used with character controller (controller handles physics)
- `AnimationLibraryComponent` - For character animations (idle, walk, run)
