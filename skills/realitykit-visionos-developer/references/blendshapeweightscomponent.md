# BlendShapeWeightsComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/blendshapeweightscomponent)

## Overview

Controls blend shape weights on a mesh for morph targets. Blend shapes (also called morph targets) allow you to deform a mesh by blending between different vertex positions. This component lets you control the weights of these blend shapes, enabling facial animation, character expressions, and other morphing effects.

## When to Use

- Facial animation and expressions
- Character morphing and deformation
- Creating animated expressions
- Blending between mesh states
- Procedural mesh deformation

## How to Use

### Basic Setup

```swift
import RealityKit

// Create blend shape weights component
var weights = BlendShapeWeightsComponent()
weights.weights = blendShapeWeights
entity.components.set(weights)
```

### Setting Specific Weights

```swift
// Create and configure blend shape weights
var weights = BlendShapeWeightsComponent()

// Set weights for specific blend shapes
weights.weights["smile"] = 0.8
weights.weights["frown"] = 0.2
weights.weights["blink"] = 1.0

entity.components.set(weights)
```

### Animating Blend Shapes

```swift
// Animate blend shape weights over time
var weights = BlendShapeWeightsComponent()
entity.components.set(weights)

// In your update loop or animation
weights.weights["smile"] = Float(sin(time) * 0.5 + 0.5)
entity.components.set(weights)
```

## Key Properties

- `weights: BlendShapeWeights` - Dictionary of blend shape names to weight values (0.0 to 1.0)

## Important Notes

- Blend shape weights typically range from 0.0 to 1.0
- Mesh must have blend shapes defined in the asset
- Multiple blend shapes can be active simultaneously
- Weights are interpolated to create smooth transitions

## Best Practices

- Use descriptive names for blend shapes
- Animate weights smoothly for natural-looking effects
- Combine multiple blend shapes for complex expressions
- Test blend shape limits on your target mesh
- Use appropriate weight ranges for your use case

## Related Components

- `ModelComponent` - The mesh component that uses blend shapes
- `AnimationLibraryComponent` - For storing blend shape animations
