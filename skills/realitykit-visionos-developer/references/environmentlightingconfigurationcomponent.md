# EnvironmentLightingConfigurationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/environmentlightingconfigurationcomponent)

## Overview

A component that configures environment lighting behavior, intensity, or blending modes for entities or scenes. It allows you to control how environment lighting is applied, including transitions when entities cross portals or move between different lighting environments.

## When to Use

- Configuring environment lighting behavior for scenes
- Modulating lighting intensity or blending modes
- Creating lighting transitions when entities cross portals
- Adjusting environment lighting based on scene context
- Controlling how environment lighting affects entities
- Implementing dynamic lighting configuration

## How to Use

### Basic Setup

```swift
import RealityKit

// Create environment lighting configuration
let config = EnvironmentLightingConfigurationComponent()
entity.components.set(config)
```

### With Portal Transitions

```swift
// Configure lighting for portal transitions
let config = EnvironmentLightingConfigurationComponent()
// Configure lighting behavior for portal crossing
entity.components.set(config)
```

## Key Properties

- Properties may include intensity, blending modes, or transition settings
- Consult official documentation for specific API details

## Important Notes

- Used to configure how environment lighting behaves in scenes
- Can be used to modulate lighting when entities cross portals
- Works with `ImageBasedLightComponent` and environment lighting
- Available on visionOS, iOS, and other Apple platforms
- Portal crossing features are newer (introduced in WWDC 2024)

## Best Practices

- Configure lighting appropriately for your scene's needs
- Use for smooth lighting transitions across portals
- Test lighting configuration on target devices
- Combine with `PortalComponent` for portal-based lighting
- Consider performance when configuring environment lighting
- Use appropriate intensity and blending settings

## Related Components

- `ImageBasedLightComponent` - For environment lighting sources
- `ImageBasedLightReceiverComponent` - For entities receiving environment lighting
- `PortalComponent` - For portals that may need lighting transitions
- `VirtualEnvironmentProbeComponent` - For reflection probes in environments
