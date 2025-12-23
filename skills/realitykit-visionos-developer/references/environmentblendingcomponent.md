# EnvironmentBlendingComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/environmentblendingcomponent)

## Overview

A component that enables realistic occlusion between virtual entities and static real-world objects in mixed reality experiences. It allows virtual content to be hidden (partially or fully) when static objects in the real world are between the camera and the virtual entity, creating more realistic blending between virtual and real environments.

## When to Use

- Creating mixed reality experiences where virtual content should be occluded by real objects
- Implementing realistic occlusion in immersive spaces
- Making virtual content appear behind real-world furniture, walls, or objects
- Creating seamless blending between virtual and real environments
- Implementing spatial occlusion for mixed reality applications

## How to Use

### Basic Setup

```swift
import RealityKit

// Enable occlusion by static surroundings
let blending = EnvironmentBlendingComponent(
    preferredBlendingMode: .occluded(by: .surroundings)
)
entity.components.set(blending)
```

### Default Blending Mode

```swift
// Default mode (no special occlusion)
let blending = EnvironmentBlendingComponent(
    preferredBlendingMode: .default
)
entity.components.set(blending)
```

### Occluded by Surroundings

```swift
// Entity will be occluded by static real-world objects
let blending = EnvironmentBlendingComponent(
    preferredBlendingMode: .occluded(by: .surroundings)
)
entity.components.set(blending)

// Example: Virtual object behind a real chair will be partially hidden
```

## Key Properties

- `preferredBlendingMode: EnvironmentBlendingComponent.BlendingMode` - The blending mode configuration

### Blending Modes

- `.default` - No special blending, behaves like normal virtual content
- `.occluded(by: .surroundings)` - Enables occlusion by static surroundings (furniture, walls, etc.)

## Important Notes

- Only works in **mixed space** or **immersive spaces** - not in volumes or windowed content
- Only **static** real-world objects can occlude entities (moving objects like people won't cause occlusion)
- Entities with this component are treated as part of the background environment
- Virtual content layering (virtual–virtual) still dominates - virtual objects draw in front of occluded content
- Introduced in WWDC 2025 cycle
- Available on visionOS and other Apple platforms (check minimum OS requirements)

## Best Practices

- Use for virtual content that should appear behind real-world objects
- Only use in mixed or immersive spaces (not in volumes)
- Understand that only static objects cause occlusion
- Test occlusion behavior with various real-world objects
- Consider visual hierarchy - virtual objects still draw in front
- Use appropriate blending mode for your use case
- Test on target devices to ensure proper occlusion behavior

## Related Components

- `AnchoringComponent` - For anchoring content to real-world targets
- `SceneUnderstandingComponent` - For accessing scene understanding data
- `ImageBasedLightComponent` - For environment lighting that matches real world
