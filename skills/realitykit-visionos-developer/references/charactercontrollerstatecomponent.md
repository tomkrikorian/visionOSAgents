# CharacterControllerStateComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/charactercontrollerstatecomponent)

## Overview

A component that tracks the runtime state of a character controller over time. It provides information about whether the character is grounded, walking up a slope, stepping, colliding, or in the air. This component is automatically updated by the character controller system and is used to respond to state changes for gameplay logic.

## When to Use

- Tracking whether a character is grounded or in the air
- Detecting when a character is walking up a slope
- Determining if a character is stepping over obstacles
- Responding to collision state changes
- Implementing gameplay logic based on character state (jumping, falling, etc.)
- Creating state-driven character behaviors

## How to Use

### Basic Setup

```swift
import RealityKit

// Create state component (automatically updated by system)
let state = CharacterControllerStateComponent()
entity.components.set(state)

// Use with CharacterControllerComponent
let controller = CharacterControllerComponent(
    radius: 0.3,
    height: 1.8,
    skinWidth: 0.01,
    slopeLimit: 0.7,
    stepLimit: 0.3,
    upVector: [0, 1, 0],
    collisionFilter: .default
)
entity.components.set(controller)
```

### Checking Character State

```swift
// Check if character is grounded
if let state = entity.components[CharacterControllerStateComponent.self] {
    if state.isGrounded {
        // Character is on ground - allow jumping
        if shouldJump {
            applyJumpForce()
        }
    } else {
        // Character is in air - apply gravity or air control
        applyAirControl()
    }
    
    // Check if walking up slope
    if state.isWalkingUpSlope {
        // Reduce movement speed or apply different animation
    }
    
    // Check if stepping
    if state.isStepping {
        // Character is stepping over obstacle
    }
}
```

### State-Driven Animation

```swift
// Switch animations based on state
func updateCharacterAnimation() {
    guard let state = entity.components[CharacterControllerStateComponent.self] else { return }
    
    if state.isGrounded {
        if state.velocity.magnitude > 0.1 {
            playAnimation("walk")
        } else {
            playAnimation("idle")
        }
    } else {
        playAnimation("jump")
    }
}
```

## Key Properties

- `isGrounded: Bool` - Whether the character is on the ground
- `isWalkingUpSlope: Bool` - Whether the character is walking up a slope
- `isStepping: Bool` - Whether the character is stepping over an obstacle
- `velocity: SIMD3<Float>` - Current velocity of the character
- `collision: Collision?` - Information about current collisions

## Important Notes

- Automatically updated by the character controller system
- State changes reflect the character's current condition
- Use this component to drive gameplay logic and animations
- State is updated each frame based on character controller movement
- Available on iOS, macOS, and visionOS
- Must be used with `CharacterControllerComponent`

## Best Practices

- Check state each frame to respond to changes
- Use `isGrounded` to control jumping and falling behavior
- Use `velocity` to drive animations based on movement speed
- Respond to `isWalkingUpSlope` to adjust movement or animations
- Use state information to trigger sound effects or visual effects
- Combine state checks for complex character behaviors
- Test state transitions on various terrain types

## Related Components

- `CharacterControllerComponent` - Required - provides the character controller behavior
- `CollisionComponent` - Required on scene geometry for collision detection
- `AnimationLibraryComponent` - For character animations based on state
