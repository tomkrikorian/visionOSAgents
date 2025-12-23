# GroundingShadowComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/groundingshadowcomponent)

## Overview

A component that adds grounding shadows to an entity in RealityKit. Grounding shadows help communicate depth and spatial relationships between virtual objects and their physical environment, making it clear when an object is floating above or resting on a surface. This component is essential for creating realistic spatial experiences where virtual content needs to appear grounded in the real world.

## When to Use

- Adding shadows to virtual objects to show they're floating above or resting on surfaces
- Communicating depth and spatial relationships in mixed reality experiences
- Making virtual content appear more grounded and realistic in the physical environment
- Creating visual cues that help users understand object placement in space
- Improving spatial perception in visionOS immersive experiences

## How to Use

### Basic Setup

```swift
import RealityKit

// Simple grounding shadow
entity.components.set(GroundingShadowComponent())

// Or with explicit parameters
entity.components.set(GroundingShadowComponent(
    castsShadow: true,
    receivesShadow: true,
    fadeBehaviorNearPhysicalObjects: .fade
))
```

### Real-World Example

```swift
import RealityKit
import SwiftUI

RealityView { content in
    // Load an entity
    let vase = try? await Entity(named: "flower_tulip")
    
    // Add grounding shadow to make it appear grounded
    vase?.components.set(GroundingShadowComponent(castsShadow: true))
    
    content.add(vase)
}
```

### With Fade Behavior

```swift
// Shadow fades near physical objects
let shadowComponent = GroundingShadowComponent(
    castsShadow: true,
    receivesShadow: true,
    fadeBehaviorNearPhysicalObjects: .fade
)
entity.components.set(shadowComponent)
```

## Key Properties

- `castsShadow: Bool` - Whether the entity casts a grounding shadow onto surfaces below it
- `receivesShadow: Bool` - Whether the entity can receive grounding shadows from other objects
- `fadeBehaviorNearPhysicalObjects: GroundingShadowComponent.FadeBehavior` - Specifies how the shadow fades near real-world physical objects

## Initializer

```swift
init(
    castsShadow: Bool,
    receivesShadow: Bool,
    fadeBehaviorNearPhysicalObjects: GroundingShadowComponent.FadeBehavior
)
```

## Important Notes

- Primarily designed for visionOS, also available in iOS 18+ when using RealityView
- In `RealityView`, the system automatically provides an imaginary directional light straight downward - no need to manually add a light source or shadow catcher
- Behavior differs between `ARView` and `RealityView` - shadows may be more pronounced in `ARView`
- Grounding shadows help users understand spatial relationships between virtual and real objects
- The shadow automatically adapts to the surface below the entity

## Best Practices

- Add grounding shadows to floating or elevated virtual objects to improve spatial perception
- Use `castsShadow: true` for objects that should appear grounded
- Set `receivesShadow: true` for objects that should show shadows from other entities
- Use appropriate fade behavior to blend shadows naturally with physical objects
- Combine with proper lighting setup for best visual results
- Test shadow appearance in both immersive and shared spaces

## Related Components

- `DynamicLightShadowComponent` - For real-time dynamic shadows cast by light sources
- `PointLightComponent` - For point light sources that can cast shadows
- `DirectionalLightComponent` - For directional lighting that can cast shadows
- `ModelComponent` - Entities with models can cast and receive shadows
