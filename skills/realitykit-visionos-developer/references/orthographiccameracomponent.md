# OrthographicCameraComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/orthographiccameracomponent)

## Overview

A component that defines an orthographic projection camera for RealityKit scenes. Orthographic cameras maintain object size regardless of depth - there's no perspective distortion or foreshortening. This is useful for technical plans, UI overlays, 2D-like modes, or stylized rendering where measurements need to remain true.

## When to Use

- Architectural visualization where measurements need to remain accurate
- Map views or diagrammatic representations in 3D scenes
- Engineering drawings or technical plans
- UI overlays where depth should not affect object size
- Stylized rendering that avoids perspective distortion
- Creating 2D-like views within 3D scenes

## How to Use

### Basic Setup

```swift
import RealityKit

// Create an orthographic camera with default settings
let camera = OrthographicCameraComponent()
entity.components.set(camera)
```

### Custom Scale

```swift
// Create camera with custom orthographic scale
let camera = OrthographicCameraComponent(
    near: 0.01,
    far: 100.0,
    orthographicScale: 10.0  // Controls view size
)
entity.components.set(camera)
```

### Technical Drawing View

```swift
// Create orthographic camera for technical drawings
let camera = OrthographicCameraComponent(
    near: 0.1,
    far: 1000.0,
    orthographicScale: 5.0  // Zoom level
)
cameraEntity.components.set(camera)

// Position camera to view from top
cameraEntity.position = [0, 10, 0]
cameraEntity.orientation = simd_quatf(angle: -.pi / 2, axis: [1, 0, 0])
```

## Key Properties

- `near: Float` - Minimum visible distance in meters (objects closer are clipped)
- `far: Float` - Maximum visible distance in meters (objects beyond are clipped)
- `orthographicScale: Float` - Scale that defines the size of the visible orthographic region (controls zoom)

## Important Notes

- Objects maintain size regardless of distance - no perspective distortion
- Orthographic scale controls how "zoomed in" or "zoomed out" the view is
- No field of view parameter - scale replaces FOV in orthographic projection
- Useful for technical or diagrammatic views where measurements must be accurate
- Available on iOS 13.0+, iPadOS 13.0+, macOS 10.15+, Mac Catalyst 13.0+, visionOS 1.0+
- On visionOS, the system camera is typically used - custom cameras may have limited use

## Best Practices

- Use for technical drawings, maps, or UI overlays where perspective isn't desired
- Set appropriate orthographic scale for the desired zoom level
- Configure near and far planes to optimize rendering
- Use when object size accuracy is more important than depth perception
- Consider using for HUD-like displays or 2D-like views in 3D scenes
- Test scale values to achieve the desired view size
- Combine with appropriate camera positioning for the desired view angle

## Related Components

- `PerspectiveCameraComponent` - For realistic depth and perspective (default for 3D scenes)
- `ProjectiveTransformCameraComponent` - For custom projection transforms (if available)
