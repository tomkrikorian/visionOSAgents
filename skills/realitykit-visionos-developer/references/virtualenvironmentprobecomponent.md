# VirtualEnvironmentProbeComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/virtualenvironmentprobecomponent)

## Overview

A component that provides reflection probes for virtual environments. Environment probes capture environment lighting, texture, and color information from their surroundings and apply it to virtual content for accurate reflections and environment-based lighting. This enables realistic reflections on surfaces in virtual environments.

## When to Use

- Implementing accurate reflections in virtual environments
- Creating environment-based lighting for virtual scenes
- Applying realistic reflections to metallic or reflective surfaces
- Capturing environment information for material rendering
- Creating immersive virtual environments with proper lighting
- Implementing reflection probes for spatial experiences

## How to Use

### Basic Setup

```swift
import RealityKit

// Create environment probe component
let probe = VirtualEnvironmentProbeComponent()
entity.components.set(probe)
```

### Positioned Probe

```swift
// Place probe at specific location to capture environment
let probeEntity = Entity()
probeEntity.position = [0, 1, 0]  // Position in scene
probeEntity.components.set(VirtualEnvironmentProbeComponent())
scene.addChild(probeEntity)
```

## Key Properties

- Properties may include probe configuration, capture settings, or influence radius
- Consult official documentation for specific API details

## Important Notes

- Environment probes capture lighting and reflection information from their surroundings
- Probes affect how materials reflect the environment
- Position probes strategically to capture appropriate environment data
- Available on visionOS, iOS, and other Apple platforms
- Works with materials that support environment reflections

## Best Practices

- Position probes at locations where accurate reflections are needed
- Use multiple probes for large or complex environments
- Consider probe placement relative to reflective surfaces
- Test reflection quality on target devices
- Combine with appropriate materials that support environment reflections
- Use probes for virtual environments (not typically needed for mixed reality)

## Related Components

- `ImageBasedLightComponent` - For environment lighting (different approach)
- `ImageBasedLightReceiverComponent` - For entities that receive IBL lighting
- `ModelComponent` - Materials on models can use probe reflections
- `EnvironmentLightingConfigurationComponent` - For environment lighting configuration
