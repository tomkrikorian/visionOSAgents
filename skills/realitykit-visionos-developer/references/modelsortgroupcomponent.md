# ModelSortGroupComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/modelsortgroupcomponent)

## Overview

Controls draw order for models to reduce depth fighting. Depth fighting (z-fighting) occurs when two surfaces are at nearly the same depth, causing flickering as they compete to be rendered. This component helps resolve these issues by controlling the rendering order of entities.

## When to Use

- Resolving depth fighting (z-fighting) issues
- Controlling render order for transparency
- Ensuring correct layering of overlapping geometry
- Fixing visual artifacts from overlapping surfaces
- Managing draw order in complex scenes

## How to Use

### Basic Setup

```swift
import RealityKit

// Enable model sort group
entity.components.set(ModelSortGroupComponent())
```

### With Sort Group

```swift
// Create with specific sort group
var sortGroup = ModelSortGroupComponent()
// Configure sort group settings
entity.components.set(sortGroup)
```

## Key Properties

- [Sort group configuration managed by the component]

## Important Notes

- Helps resolve z-fighting between overlapping surfaces
- Controls rendering order for better visual consistency
- Particularly useful with transparent or semi-transparent materials
- Works in conjunction with the rendering pipeline

## Best Practices

- Use when experiencing depth fighting issues
- Apply to entities with overlapping geometry
- Combine with proper material settings
- Test on target devices to verify fixes
- Use appropriate sort groups for your scene organization

## Related Components

- `ModelComponent` - The component whose draw order is controlled
- `OpacityComponent` - Often used together for transparent objects
