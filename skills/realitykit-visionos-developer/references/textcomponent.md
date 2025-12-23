# TextComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/textcomponent)

## Overview

A component that renders 3D text directly on entities in RealityKit scenes. This component allows you to display text in 3D space without using SwiftUI views, making it suitable for in-world labels, signs, or text that needs to be part of the 3D scene geometry.

## When to Use

- Displaying text labels in 3D space
- Creating in-world signs or information displays
- Adding text that needs to be part of scene geometry
- Rendering text that should be affected by 3D transformations
- Creating text that doesn't need SwiftUI interactivity
- Displaying text in immersive spaces

## How to Use

### Basic Setup

```swift
import RealityKit

// Create text mesh
let textMesh = MeshResource.generateText(
    "Hello, World!",
    extrusionDepth: 0.1,
    font: .systemFont(ofSize: 0.1),
    containerFrame: .zero,
    alignment: .center,
    lineBreakMode: .byWordWrapping
)

// Create material for text
let material = SimpleMaterial(color: .white, isMetallic: false)

// Create model component with text mesh
let model = ModelComponent(mesh: textMesh, materials: [material])
entity.components.set(model)
```

### Alternative: Using TextComponent (if available)

```swift
// Note: TextComponent API may vary by RealityKit version
// Check official documentation for your target SDK version
let textComponent = TextComponent(
    text: "Hello, World!",
    extrusionDepth: 0.1
)
entity.components.set(textComponent)
```

## Key Properties

- Properties may include text content, font, size, extrusion depth, alignment, etc.
- Consult official documentation for specific API details for your RealityKit version

## Important Notes

- Text rendering in RealityKit is typically done via `MeshResource.generateText()`
- TextComponent may not be available in all RealityKit versions
- Text is rendered as 3D geometry, not as 2D overlays
- Consider using `ViewAttachmentComponent` for interactive text with SwiftUI
- Available on visionOS, iOS, and other Apple platforms

## Best Practices

- Use `MeshResource.generateText()` for reliable text rendering
- Consider text size and readability in 3D space
- Use appropriate materials for text visibility
- For interactive text, consider `ViewAttachmentComponent` instead
- Test text readability at various distances
- Use appropriate font sizes for 3D space (typically larger than 2D)

## Related Components

- `ModelComponent` - Text is typically rendered using ModelComponent with text mesh
- `ViewAttachmentComponent` - Alternative for interactive text with SwiftUI
- `BillboardComponent` - For text that should always face the viewer
