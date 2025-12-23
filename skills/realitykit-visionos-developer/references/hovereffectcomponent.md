# HoverEffectComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/hovereffectcomponent)

## Overview

A component that applies a visual effect to a hierarchy of entities when a person looks at or selects an entity. On visionOS, you hover over an entity by looking at it or directly touching it. This component provides visual feedback to indicate that an entity is interactive or selected.

## When to Use

- Providing visual feedback on hover/look
- Indicating interactive entities
- Highlighting selectable objects
- Creating responsive UI feedback
- Enhancing user interaction cues

## How to Use

### Basic Setup

```swift
import RealityKit

// Entity needs InputTargetComponent and CollisionComponent
let boxSize = SIMD3<Float>(0.5, 0.1, 0.05)

let modelComponent = ModelComponent(
    mesh: MeshResource.generateBox(size: boxSize),
    materials: [SimpleMaterial(color: .black, roughness: 0.5, isMetallic: false)]
)
let collisionComponent = CollisionComponent(
    shapes: [ShapeResource.generateBox(size: boxSize)]
)
let inputTargetComponent = InputTargetComponent()
let hoverEffectComponent = HoverEffectComponent()

let entity = Entity()
entity.components.set([modelComponent, collisionComponent, inputTargetComponent, hoverEffectComponent])
```

### Custom Spotlight Effect

```swift
// Custom spotlight hover effect
let hoverComponent = HoverEffectComponent(.spotlight(
    HoverEffectComponent.SpotlightHoverEffectStyle(
        color: .green, strength: 2.0
    )
))
entity.components.set(hoverComponent)
```

### Highlight Effect

```swift
// Highlight hover effect
let hoverComponent = HoverEffectComponent(.highlight(
    HoverEffectComponent.HighlightHoverEffectStyle(
        color: .yellow, strength: 2.0
    )
))
entity.components.set(hoverComponent)
```

### Grouped Hover Effects

```swift
// Create a group ID for connected hover effects
let groupID = HoverEffectComponent.GroupID()

var hoverA = HoverEffectComponent(.highlight(
    HoverEffectComponent.HighlightHoverEffectStyle(
        color: .green, strength: 2.0
    )
))
hoverA.hoverEffect.groupID = groupID
entityA.components.set(hoverA)

var hoverB = HoverEffectComponent(.highlight(
    HoverEffectComponent.HighlightHoverEffectStyle(
        color: .green, strength: 2.0
    )
))
hoverB.hoverEffect.groupID = groupID
entityB.components.set(hoverB)
// Both entities will glow when either is hovered
```

## Key Properties

- `hoverEffect: HoverEffectComponent.HoverEffect` - The current hover effect configuration

## Important Notes

- **Requires** `InputTargetComponent` and `CollisionComponent` to work
- Applies to entire entity hierarchy
- Can be grouped to activate multiple entities together
- Supports spotlight, highlight, and shader-based effects
- On visionOS, hover is triggered by looking at or touching the entity

## Best Practices

- Always combine with `InputTargetComponent` and `CollisionComponent`
- Use appropriate colors and strengths for your design
- Group related entities for coordinated hover effects
- Test hover effects from various viewing angles
- Consider performance when using many hover effects

## Related Components

- `InputTargetComponent` - Required for hover detection
- `CollisionComponent` - Required for hit testing
- `ManipulationComponent` - Often used together for interactive entities
