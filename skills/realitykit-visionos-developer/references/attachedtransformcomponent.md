# AttachedTransformComponent


## Overview

A component that attaches an entity to a `GeometricPin` on another entity. The system keeps the attached entity's `source` pin (or its origin when `source` is `nil`) aligned to the `target` pin, so the entity follows the target as it moves - including pins bound to skeletal joints. Use it instead of re-parenting via `addChild()` when content must track a named point such as a joint or a socket on a mesh.

## When to Use

- Attaching props or accessories to a skeletal joint pin
- Keeping an entity glued to a named point on another entity
- Following a moving attachment point without re-parenting
- Pairing with pins created through `Entity.pins`

## How to Use

### Basic Setup

```swift
import RealityKit

// Define pins on both entities
let socket = machine.pins.set(named: "Socket", position: [0, 0.2, 0])
let plug = tool.pins.set(named: "Plug", position: .zero)

// tool's "Plug" pin tracks machine's "Socket" pin
tool.components.set(
    AttachedTransformComponent(source: plug, target: socket)
)
```

### Convenience API

```swift
// Entity.attach(_:to:) sets the component for you
tool.attach(plug, to: socket)

// Omit the source to attach the entity's origin to the target pin
tool.attach(to: socket)
```

### Skeletal Joint Pin

```swift
// Bind a pin to a skeleton joint, then attach an accessory to it
let jointPin = character.pins.set(
    named: "HeadPin",
    skeletalJointName: "head"
)
hat.attach(to: jointPin)
```

## Key Properties

- `target: GeometricPin` - The pin this entity attaches to
- `source: GeometricPin?` - The pin on this entity aligned to `target`; `nil` attaches the entity's origin
- `init(source:target:)` - `source` defaults to `nil`

## Important Notes

- The system drives the attached entity's transform; do not also parent it to the target or write its transform per frame
- For static relative placement, plain `addChild()` hierarchy is simpler
- `Entity.attach(_:to:)` is shorthand for setting this component

## Best Practices

- Name pins descriptively and look them up via `entity.pins["Name"]`
- Use skeletal joint pins for animated characters instead of polling joint transforms each frame
- Remove the component when the attachment should end
- Keep one transform owner: either this component or your own code, not both

## Related Components

- `GeometricPinsComponent` - Stores the pins referenced by `source` and `target`
- `IKComponent` / `SkeletalPosesComponent` - Drive the joints that pins can follow
- `PhysicsJointsComponent` - Pin-based physics joints instead of rigid following
