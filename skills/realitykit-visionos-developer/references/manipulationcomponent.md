# ManipulationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/manipulationcomponent)

## Overview

A component that adds fluid and immersive interactive behaviors and effects. `ManipulationComponent` enables rich interaction on entities in 3D space, including gesture-based movement and audio feedback. When applied to an entity, the system enables intuitive manipulation using hands or input devices like a trackpad.

## When to Use

- Creating draggable, rotatable, and scalable entities
- Implementing spatial interactions with built-in gestures
- Adding audio feedback to interactions
- Creating objects that respond to hand gestures
- Building intuitive manipulation experiences

## How to Use

### Basic Manipulation

```swift
import RealityKit

// Enable manipulation on an entity
entity.components.set(ManipulationComponent())
```

### Configure Entity for Manipulation

```swift
// Apply default configuration
ManipulationComponent.configureEntity(
    entity,
    hoverEffect: .default,
    allowedInputTypes: [.direct, .indirect],
    collisionShapes: [.generateBox(size: [0.1, 0.1, 0.1])]
)
```

### Custom Audio Configuration

```swift
var manipulation = ManipulationComponent()
manipulation.audioConfiguration = .none // Disable system audio
entity.components.set(manipulation)

// Listen to events and play custom audio
scene.subscribe(to: ManipulationEvents.DidUpdateTransform.self) { event in
    // Play custom audio
}
```

### Custom Dynamics

```swift
var manipulation = ManipulationComponent()
manipulation.dynamics = ManipulationComponent.Dynamics(
    // Customize interaction behavior
)
entity.components.set(manipulation)
```

## Interaction Features

- **Gestures**: Single-hand or trackpad gestures for translation, rotation, and scaling
- **Two-hand gestures**: Intuitive scaling and rotation
- **Handoff**: Seamless transfer between hands
- **Audio Feedback**: System plays audio cues at key interaction moments
- **Component Events**: Publishes events for interaction lifecycle

## Interaction Lifecycle Events

1. `WillBegin` - Interaction is about to start
2. `DidHandOff` - Object transferred between hands
3. `DidUpdateTransform` - Transform updated during interaction
4. `WillRelease` - Interaction is about to end
5. `WillEnd` - Interaction has ended

## Key Properties

- `audioConfiguration: ManipulationComponent.AudioConfiguration` - Audio configuration during interaction
- `dynamics: ManipulationComponent.Dynamics` - Settings for interaction behavior
- `releaseBehavior: ManipulationComponent.ReleaseBehavior` - Behavior when released

## Important Notes

- The system modifies the entity's transform directly
- If you need custom transforms, apply them to a subentity
- Listen to component events for custom behaviors and feedback
- Combine with `InputTargetComponent` and `CollisionComponent` for proper setup

## Best Practices

- Use `configureEntity` for quick setup with sensible defaults
- Listen to manipulation events for custom visual or audio feedback
- Use subentities for custom transform logic
- Combine with `HoverEffectComponent` for visual feedback
- Set `audioConfiguration` to `.none` if using custom audio

## Related Components

- `InputTargetComponent` - Required for input handling
- `CollisionComponent` - Required for hit testing
- `HoverEffectComponent` - Visual feedback on hover
- `GestureComponent` - For custom gesture handling
