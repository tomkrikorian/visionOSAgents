# GeometricPinsComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/geometricpinscomponent)

## Overview

A component that defines geometric attachment points (pins) for entities. Pins define positions and orientations relative to an entity that can be used for connecting entities, creating joints, or attaching objects at specific locations. Pins are used with physics joints and other connection systems.

## When to Use

- Defining attachment points for physics joints
- Creating connection points between entities
- Specifying where entities should connect
- Setting up joint anchor points
- Creating geometric attachment systems
- Defining pin locations for entity connections

## How to Use

### Using Entity.pins API

```swift
import RealityKit

// Set a pin on an entity (from WWDC 2024 example)
let hookPin = spaceship.pins.set(named: "Hook", position: hookOffset)
let trailerPin = trailer.pins.set(named: "Trailer", position: .zero)

// Pins define position and orientation relative to the entity
// Later used with PhysicsJointsComponent
```

### With Physics Joints

```swift
// Create pins for joint connection
let pin0 = entity1.pins.set(named: "ConnectionPoint", position: [0, 0, 0])
let pin1 = entity2.pins.set(named: "ConnectionPoint", position: [0, 0, 0])

// Use pins in custom joint
var joint = PhysicsCustomJoint(pin0: pin0, pin1: pin1)
// Configure joint constraints...
```

### Pin with Orientation

```swift
// Set pin with position and orientation
let pin = entity.pins.set(
    named: "AttachmentPoint",
    position: [1, 0, 0],
    orientation: simd_quatf(angle: .pi / 2, axis: [0, 1, 0])
)
```

## Key Properties

- Pins are accessed via `Entity.pins` property
- `pins.set(named:position:)` - Creates or updates a pin
- Pins have position and orientation relative to the entity
- Each pin has a name for identification

## Important Notes

- Pins define positions and orientations relative to the entity
- Used with `PhysicsJointsComponent` for joint connections
- Introduced in WWDC 2024 ("Discover RealityKit APIs")
- Available on visionOS, iOS, and other Apple platforms
- API may be accessed via `Entity.pins` rather than a separate component
- Check official documentation for your target SDK version

## Best Practices

- Use descriptive names for pins (e.g., "Hook", "Trailer", "ConnectionPoint")
- Set pins at logical connection points on entities
- Use pins with physics joints for constrained connections
- Test pin positions to ensure correct attachment points
- Consider pin orientation for proper joint alignment
- Use pins consistently across related entities

## Related Components

- `PhysicsJointsComponent` - Uses pins for joint connections
- `PhysicsCustomJoint` - Connects entities via pins
- Entity hierarchy - Pins work with entity transforms
