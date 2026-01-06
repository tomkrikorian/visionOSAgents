# Camera Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## PerspectiveCameraComponent
Goal: Configures a perspective camera for a scene.

```swift
entity.components.set(PerspectiveCameraComponent())
```

## OrthographicCameraComponent
Goal: Configures an orthographic camera for a scene.

```swift
entity.components.set(OrthographicCameraComponent())
```

## ProjectiveTransformCameraComponent
Goal: Provides a custom projection transform for a camera.

```swift
let camera = ProjectiveTransformCameraComponent(transform: <#float4x4#>)
entity.components.set(camera)
```
