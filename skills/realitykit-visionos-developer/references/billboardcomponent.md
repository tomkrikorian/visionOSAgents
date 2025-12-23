# BillboardComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/billboardcomponent)

## Overview

Keeps the entity oriented toward the viewer. A billboard always faces the camera, which is useful for 2D sprites, text labels, UI elements, or any content that should always be visible from the front regardless of viewing angle.

## When to Use

- 2D sprites in 3D space
- Text labels that should always face the viewer
- UI elements in 3D scenes
- Creating "always visible" content
- HUD elements and overlays

## How to Use

### Basic Setup

```swift
import RealityKit

// Enable billboard behavior
entity.components.set(BillboardComponent())
```

### With Model

```swift
// Create a billboard entity with a model
let entity = ModelEntity(
    mesh: .generatePlane(width: 0.5, depth: 0.5),
    materials: [material]
)
entity.components.set(BillboardComponent())
```

## Key Properties

- [Billboard orientation is automatically managed]

## Important Notes

- Entity automatically rotates to face the viewer
- Useful for 2D content in 3D space
- Maintains consistent appearance from all angles
- Works well with flat geometry (planes, quads)

## Best Practices

- Use for 2D sprites and text labels
- Combine with flat geometry (planes)
- Use appropriate textures for billboard content
- Consider performance when using many billboards
- Test from various viewing angles

## Related Components

- `ModelComponent` - The visual component that faces the viewer
- `TextComponent` - Often used with billboards for readable text
