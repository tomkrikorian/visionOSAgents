# OpacityComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/opacitycomponent)

## Overview

A component that controls the opacity of an entity and its descendants. An opacity component multiplies its `opacity` property with all visual components the entity and its descendants own. Visual components include `ModelComponent` and `ParticleEmitterComponent`. If a descendant also has its own opacity component, the system combines the two opacities by multiplying their values.

## When to Use

- Creating fade-in/fade-out effects
- Making entities semi-transparent
- Implementing visibility transitions
- Creating glass-like or translucent materials
- Building UI elements with transparency

## How to Use

### Basic Opacity

```swift
import RealityKit

// Load a model
let robot = try await Entity(named: "vintage_robot")

// Create an opacity component with 50% opacity
let opacityComponent = OpacityComponent(opacity: 0.5)
robot.components.set(opacityComponent)
```

### Variable Opacity

```swift
// Create and configure opacity
var opacity = OpacityComponent()
opacity.opacity = 0.75
entity.components.set(opacity)
```

### Hierarchical Opacity

```swift
// Parent entity with opacity
let parent = Entity()
parent.components.set(OpacityComponent(opacity: 0.5))

// Child entity (inherits parent's opacity)
let child = Entity()
parent.addChild(child)
// Child will have effective opacity of 0.5 * child's own opacity (if any)
```

## Key Properties

- `opacity: Float` - The floating-point value (0.0 to 1.0) the renderer applies to an entity and its descendants

## Important Notes

- Opacity values range from 0.0 (fully transparent) to 1.0 (fully opaque)
- Opacity multiplies hierarchically - child opacity is multiplied by parent opacity
- Applies to all visual components (ModelComponent, ParticleEmitterComponent)
- Works with materials that support transparency

## Best Practices

- Use opacity for smooth fade transitions
- Combine with animation for fade-in/fade-out effects
- Be aware of hierarchical opacity multiplication
- Use appropriate opacity values for your visual design
- Consider performance when animating opacity on many entities

## Related Components

- `ModelComponent` - Visual component affected by opacity
- `ParticleEmitterComponent` - Also affected by opacity
- `ModelSortGroupComponent` - For controlling draw order with transparency
