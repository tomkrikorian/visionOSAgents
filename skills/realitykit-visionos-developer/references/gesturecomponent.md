# GestureComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/gesturecomponent)

## Overview

Attaches custom gesture handling to an entity. This component allows you to implement custom gesture recognition and handling beyond the built-in manipulation gestures provided by `ManipulationComponent`. Use this when you need specialized gesture behaviors or want to handle gestures in a custom way.

## When to Use

- Implementing custom gesture recognition
- Creating specialized interaction behaviors
- Handling gestures not supported by ManipulationComponent
- Building custom input handling
- Creating unique interaction patterns

## How to Use

### Basic Setup

```swift
import RealityKit

// Create gesture component with custom gesture handler
let gestureComponent = GestureComponent(gestureHandler)
entity.components.set(gestureComponent)
```

### With Input Target

```swift
// Entity needs InputTargetComponent for gesture handling
entity.components.set(InputTargetComponent())
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))

// Add custom gesture component
let gestureComponent = GestureComponent(customGestureHandler)
entity.components.set(gestureComponent)
```

## Key Properties

- [Gesture handler configuration managed by the component]

## Important Notes

- Requires `InputTargetComponent` and `CollisionComponent` for input detection
- Allows custom gesture implementation beyond built-in gestures
- Use when `ManipulationComponent` doesn't meet your needs
- Provides flexibility for specialized interaction patterns

## Best Practices

- Combine with `InputTargetComponent` and `CollisionComponent`
- Use for gestures not supported by `ManipulationComponent`
- Implement efficient gesture recognition
- Test gesture handling thoroughly
- Consider user experience when designing custom gestures

## Related Components

- `InputTargetComponent` - Required for input handling
- `CollisionComponent` - Required for hit testing
- `ManipulationComponent` - Alternative for built-in gestures
- `GestureComponent` - For custom gesture handling
