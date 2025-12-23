# PhysicsSimulationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/physicssimulationcomponent)

## Overview

A component that defines how physics is simulated within an anchored entity. It attaches to anchors to indicate whether the entity participates in the physics simulation and configures collision options for physics behavior. This component is particularly relevant when defining anchors that behave physically in scenes.

## When to Use

- Configuring physics simulation behavior for anchored entities
- Defining collision options for physics simulation
- Controlling which entities participate in physics simulation
- Setting up physics simulation parameters for specific anchors
- Creating separate physics simulation spaces

## How to Use

### Basic Setup

```swift
import RealityKit

// Create physics simulation component
let simulation = PhysicsSimulationComponent()
entity.components.set(simulation)
```

### With Collision Options

```swift
// Configure collision options for physics simulation
var options = PhysicsSimulationComponent.CollisionOptions()
// Configure collision masks, groups, etc.

let simulation = PhysicsSimulationComponent(collisionOptions: options)
entity.components.set(simulation)
```

### On Anchored Entities

```swift
// Attach to an anchor entity to configure its physics simulation
let anchor = AnchorEntity(.plane(.horizontal, classification: .any, minimumBounds: [0.1, 0.1]))
let simulation = PhysicsSimulationComponent()
anchor.components.set(simulation)
```

## Key Properties

- `collisionOptions: CollisionOptions` - Options around collision behavior for physics simulation, including collision masks, groups, and how collisions are processed

### CollisionOptions

- Defines collision behavior specifics like collision masks and groups
- Controls how collisions are processed within the physics simulation

## Important Notes

- Attaches to anchors to indicate whether the entity participates in physics simulation
- Particularly relevant when defining anchors that behave physically in scenes
- Use `nearestSimulationEntity(for:)` to find the closest entity within the physics simulation context
- Works in conjunction with `AnchoringComponent` for anchored physics behavior
- Available on visionOS, iOS, and other Apple platforms

## Best Practices

- Attach to anchor entities when you need physics simulation for anchored content
- Configure collision options appropriately for your use case
- Use `nearestSimulationEntity(for:)` to query physics simulation entities
- Combine with `PhysicsBodyComponent` and `CollisionComponent` for complete physics setup
- Consider performance when configuring collision options for large scenes

## Related Components

- `AnchoringComponent` - Often used together for anchored physics behavior
- `PhysicsBodyComponent` - Entities in the simulation need physics bodies
- `CollisionComponent` - Required for collision detection in physics simulation
- `PhysicsMotionComponent` - For controlling motion in the simulation
