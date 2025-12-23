# PhysicsJointsComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/physicsjointscomponent)

## Overview

A component that holds a collection of physics joints attached to the physics simulation. Joints connect two entities' physics bodies and apply constraints on how they can move or rotate relative to each other. This enables creating articulated structures, hinges, springs, and other constrained physics behaviors.

## When to Use

- Creating articulated structures (robots, vehicles, characters)
- Implementing hinges, doors, or rotating connections
- Building spring-based connections between physics bodies
- Creating constrained motion between entities
- Implementing physics-based mechanisms and contraptions
- Connecting physics bodies with custom motion constraints

## How to Use

### Basic Joint Setup

```swift
import RealityKit

// Define pins on each entity where the joint will connect
let hookPin = spaceship.pins.set(named: "Hook", position: hookOffset)
let trailerPin = trailer.pins.set(named: "Trailer", position: .zero)

// Create a custom joint with constraints
var joint = PhysicsCustomJoint(pin0: hookPin, pin1: trailerPin)

// Configure linear motion constraints (fixed = no movement)
joint.linearMotionAlongX = .fixed
joint.linearMotionAlongY = .fixed
joint.linearMotionAlongZ = .fixed

// Configure angular motion constraints (range = limited rotation)
joint.angularMotionAroundX = .range(-.pi * 0.05 ... .pi * 0.05)
joint.angularMotionAroundY = .range(-.pi * 0.2 ... .pi * 0.2)
joint.angularMotionAroundZ = .range(-.pi * 0.2 ... .pi * 0.2)

// Create joints component and add to entity
let jointsComponent = PhysicsJointsComponent(joints: [joint])
entity.components.set(jointsComponent)
```

### Hinge Joint Example

```swift
// Create a hinge that rotates around Y axis
var hinge = PhysicsCustomJoint(pin0: doorPin, pin1: framePin)

// Allow rotation only around Y axis
hinge.angularMotionAroundX = .fixed
hinge.angularMotionAroundY = .free  // Free rotation
hinge.angularMotionAroundZ = .fixed

// Lock all linear motion
hinge.linearMotionAlongX = .fixed
hinge.linearMotionAlongY = .fixed
hinge.linearMotionAlongZ = .fixed

let joints = PhysicsJointsComponent(joints: [hinge])
doorEntity.components.set(joints)
```

### Spring Joint Example

```swift
// Create a spring connection with limited range
var spring = PhysicsCustomJoint(pin0: object1Pin, pin1: object2Pin)

// Allow movement along one axis (spring direction)
spring.linearMotionAlongX = .free
spring.linearMotionAlongY = .fixed
spring.linearMotionAlongZ = .fixed

// Lock rotations
spring.angularMotionAroundX = .fixed
spring.angularMotionAroundY = .fixed
spring.angularMotionAroundZ = .fixed

let joints = PhysicsJointsComponent(joints: [spring])
entity.components.set(joints)
```

## Key Properties

- `joints: [PhysicsJoint]` - Array of physics joints connecting entities

### PhysicsCustomJoint Properties

- `pin0: GeometricPin` - First pin (anchoring point on first entity)
- `pin1: GeometricPin` - Second pin (anchoring point on second entity)
- `linearMotionAlongX/Y/Z: MotionConstraint` - Linear motion constraints along each axis
- `angularMotionAroundX/Y/Z: MotionConstraint` - Angular motion constraints around each axis

### Motion Constraint Types

- `.fixed` - No motion allowed
- `.free` - Motion is unrestricted
- `.range(ClosedRange<Float>)` - Motion limited to a specific range

## Important Notes

- Joints connect two entities via "pins" (points defined relative to each entity)
- Pins have positions and orientations relative to their parent entities
- Both entities must have `PhysicsBodyComponent` for joints to work
- Joints are active once added to the physics simulation
- Real-time motion and forces reflect the constraints
- Use `GeometricPinsComponent` or `Entity.pins.set()` to define pin locations

## Best Practices

- Define pins at logical connection points on entities
- Use descriptive pin names for easier debugging
- Start with fixed constraints and gradually allow motion as needed
- Test joint behavior thoroughly - constraints can be complex
- Use range constraints to limit motion to realistic values
- Consider performance when using many joints in a scene
- Combine with `PhysicsBodyComponent` locking for additional constraints

## Related Components

- `PhysicsBodyComponent` - Required on both entities for joints to work
- `GeometricPinsComponent` - For defining pin locations on entities
- `CollisionComponent` - Entities with joints typically need collision
- `PhysicsMotionComponent` - For applying motion to jointed entities
