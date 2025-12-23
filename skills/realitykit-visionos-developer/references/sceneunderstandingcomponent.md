# SceneUnderstandingComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/sceneunderstandingcomponent)

## Overview

A component that provides access to scene understanding data for an entity. Scene understanding allows RealityKit apps to obtain a mesh or representation of the real environment (walls, floors, obstacles) and make virtual entities interact with it through collision detection, physics, and occlusion. This enables virtual content to properly interact with the real world.

## When to Use

- Accessing scene understanding mesh data
- Implementing collision detection with real-world geometry
- Creating physics interactions with the environment
- Enabling occlusion of virtual content by real objects
- Accessing detected objects or room reconstruction data
- Building experiences that respond to the real environment

## How to Use

### Basic Setup

```swift
import RealityKit
import ARKit

// Configure SpatialTrackingSession with scene understanding
let configuration = SpatialTrackingSession.Configuration()
configuration.sceneUnderstanding = [.collision, .physics]

// Entities can access scene understanding data
let entity = Entity()
entity.components.set(SceneUnderstandingComponent())
```

### With Collision and Physics

```swift
// Enable scene understanding for collision and physics
let configuration = SpatialTrackingSession.Configuration()
configuration.sceneUnderstanding = [.collision, .physics]

// Entity can now collide with real-world geometry
let entity = Entity()
entity.components.set(PhysicsBodyComponent(...))
entity.components.set(SceneUnderstandingComponent())
```

### Environment Mesh Access

```swift
// Access scene understanding mesh
if let sceneUnderstanding = entity.components[SceneUnderstandingComponent.self] {
    // Access mesh data, detected objects, etc.
    // Use for collision, physics, or occlusion
}
```

## Key Properties

- Properties provide access to scene understanding mesh, detected objects, room reconstruction, etc.
- Consult official documentation for specific API details

## Important Notes

- Requires `SpatialTrackingSession.Configuration` with scene understanding flags
- Scene understanding flags include `.collision` and `.physics`
- Works with `EnvironmentBlendingComponent` for occlusion by real geometry
- Available on visionOS and other Apple platforms
- Introduced in WWDC 2025
- Provides mesh representation of the real environment

## Best Practices

- Configure scene understanding flags appropriately (`.collision`, `.physics`)
- Use scene understanding mesh for collision detection
- Combine with `EnvironmentBlendingComponent` for occlusion
- Test scene understanding on various environments
- Consider performance when using scene understanding
- Handle cases where scene understanding is not available
- Use for realistic interaction between virtual and real content

## Related Components

- `EnvironmentBlendingComponent` - For occlusion by real-world objects
- `CollisionComponent` - For collision detection with scene mesh
- `PhysicsBodyComponent` - For physics interaction with environment
- `AnchoringComponent` - For anchoring to detected planes
- `ARKitAnchorComponent` - For accessing ARKit anchor data
