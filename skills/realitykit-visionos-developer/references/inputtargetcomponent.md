# InputTargetComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/inputtargetcomponent)

## Overview

A component that gives an entity the ability to receive system input. This component should be added to an entity to inform the system that it should be treated as a target for input handling. It can be customized to require only specific forms of input like direct or indirect interactions.

## When to Use

- Making entities interactive (tappable, draggable, etc.)
- Handling user gestures and input events
- Creating UI elements in 3D space
- Implementing custom interaction behaviors

## How to Use

### Basic Input Setup

```swift
import RealityKit

// Enable the entity for input
entity.components.set(InputTargetComponent())
```

### Input with Collision

```swift
// Input requires a CollisionComponent for hit testing
entity.components.set(InputTargetComponent())

let shapes: [ShapeResource] = [.generateBox(size: [0.1, 0.1, 0.1])]
entity.components.set(CollisionComponent(shapes: shapes))
```

### Filtering Input Types

```swift
// Only allow direct input (touch/pointer)
let inputTypes: Set<InputTargetComponent.InputType> = [.direct]
entity.components.set(InputTargetComponent(allowedInputTypes: inputTypes))
```

### Input-Only (No Physics Collision)

```swift
// Enable input but disable physics collision
entity.components.set(InputTargetComponent())

var collision = CollisionComponent(shapes: [.generateSphere(radius: 0.1)])
collision.filter = CollisionFilter(group: [], mask: [])
entity.components.set(collision)
```

### Disabling Input on Descendants

```swift
// Disable input on a specific descendant
var inputComponent = InputTargetComponent()
inputComponent.isEnabled = false
childEntity.components.set(inputComponent)
```

## Key Properties

- `allowedInputTypes: Set<InputTargetComponent.InputType>` - The set of input types this component's entity can receive
- `isEnabled: Bool` - Whether the component's entity is enabled for input

## Important Notes

- `InputTargetComponent` behaves hierarchically - if added to a parent, descendants with `CollisionComponent`s will be used for input handling
- The hit testing shape is defined by the `CollisionComponent`
- `allowedInputTypes` propagates down the hierarchy, but can be overridden by descendants
- By default, the component handles all forms of input

## Best Practices

- Always combine with `CollisionComponent` for proper hit testing
- Use `allowedInputTypes` to restrict input to specific interaction methods
- Use `isEnabled` to temporarily disable input without removing the component
- Combine with `ManipulationComponent` for built-in drag/rotate/scale interactions
- Use `GestureComponent` for custom gesture handling

## Related Components

- `CollisionComponent` - Required for hit testing
- `ManipulationComponent` - Built-in spatial interactions
- `GestureComponent` - Custom gesture handling
- `HoverEffectComponent` - Visual feedback on hover
