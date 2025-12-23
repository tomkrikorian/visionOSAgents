# PerspectiveCameraComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/perspectivecameracomponent)

## Overview

A component that defines a perspective projection camera for RealityKit scenes. Perspective cameras simulate realistic depth and perspective, where objects farther away appear smaller (foreshortening). This is the standard camera type for immersive 3D scenes and provides a realistic view similar to how human eyes perceive depth.

## When to Use

- Creating immersive 3D scenes with realistic depth and perspective
- Simulating realistic camera behavior in non-AR contexts
- Modifying camera projection parameters in AR sessions (when possible)
- Rendering scenes where depth perception is important
- Creating preview or simulation views that behave like real-world cameras

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a perspective camera with default settings
let camera = PerspectiveCameraComponent()
entity.components.set(camera)
```

### Custom Field of View

```swift
// Create camera with custom field of view (wider angle)
let camera = PerspectiveCameraComponent(
    near: 0.01,
    far: .infinity,
    fieldOfViewInDegrees: 90.0  // Wide angle
)
entity.components.set(camera)
```

### Limited Depth Range

```swift
// Create camera with limited depth range
let camera = PerspectiveCameraComponent(
    near: 0.1,      // Objects closer than 0.1m are clipped
    far: 100.0,    // Objects beyond 100m are clipped
    fieldOfViewInDegrees: 60.0
)
entity.components.set(camera)
```

### Camera Entity Setup

```swift
// Create a camera entity
let cameraEntity = Entity()
cameraEntity.position = [0, 1.6, 0]  // Eye height
cameraEntity.orientation = simd_quatf(angle: 0, axis: [0, 1, 0])

let camera = PerspectiveCameraComponent(
    near: 0.01,
    far: .infinity,
    fieldOfViewInDegrees: 60.0
)
cameraEntity.components.set(camera)

scene.addChild(cameraEntity)
```

## Key Properties

- `near: Float` - Minimum visible depth in meters (must be > 0 and < far)
- `far: Float` - Maximum visible depth in meters (must be > near, default: infinity)
- `fieldOfViewInDegrees: Float` - Vertical field of view in degrees (default: 60°)

## Important Notes

- Horizontal FOV is computed automatically based on aspect ratio
- In AR sessions, the system typically supplies the camera automatically
- In non-AR contexts, you can add your own perspective camera
- Objects closer than `near` or farther than `far` are clipped (not visible)
- Field of view affects how "zoomed in" or "zoomed out" the view appears
- Available on iOS 13.0+, iPadOS 13.0+, macOS 10.15+, Mac Catalyst 13.0+, visionOS 1.0+
- On visionOS, the system camera is typically used - custom cameras may have limited use

## Best Practices

- Use default field of view (60°) for natural-looking scenes
- Set appropriate near and far planes to optimize rendering performance
- Avoid extremely small near values or extremely large far values
- Consider aspect ratio when setting field of view
- In AR/visionOS, prefer using the system camera when possible
- Use for immersive 3D scenes where realistic depth perception is important
- Test camera settings on target devices for optimal viewing experience

## Related Components

- `OrthographicCameraComponent` - For 2D-like views without perspective distortion
- `ProjectiveTransformCameraComponent` - For custom projection transforms (if available)
