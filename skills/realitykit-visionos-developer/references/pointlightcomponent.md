# PointLightComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/pointlightcomponent)

## Overview

A component that adds an omnidirectional point light source that emits light in all directions from a position. Point lights are useful for localized light sources like light bulbs, torches, or flares. The light intensity falls off with distance based on the attenuation radius.

## When to Use

- Creating localized light sources (light bulbs, torches, lamps)
- Adding point light effects like flares or sparks
- Implementing dynamic lighting that changes with entity position
- Creating realistic indoor lighting scenarios
- Adding accent lighting to specific areas of a scene

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a point light
var light = PointLightComponent()
light.color = .white
light.intensity = 1000  // Lumens
light.attenuationRadius = 5.0  // Light reaches 5 meters
entity.components.set(light)
```

### Colored Point Light

```swift
// Create a colored point light (e.g., warm orange)
var light = PointLightComponent()
light.color = .init(red: 1.0, green: 0.7, blue: 0.5)  // Warm orange
light.intensity = 800
light.attenuationRadius = 3.0
entity.components.set(light)
```

### Positioned Light Source

```swift
// Create a light bulb entity
let lightBulb = Entity()
lightBulb.position = [2, 3, 1]

var light = PointLightComponent()
light.color = .white
light.intensity = 1500
light.attenuationRadius = 10.0
lightBulb.components.set(light)

scene.addChild(lightBulb)
```

## Key Properties

- `color: Color` - The color of the light (default: white)
- `intensity: Float` - The brightness of the light in lumens
- `attenuationRadius: Float` - The distance in meters at which light intensity reaches zero

## Important Notes

- Point lights emit light in all directions from their position
- Light intensity falls off with distance based on attenuation radius
- Point lights do **not** cast shadows (as of current RealityKit versions)
- Position matters - the light emits from the entity's position
- Use attenuation radius to limit light reach and improve performance
- Available on iOS, macOS, and visionOS (with limitations on visionOS - see platform notes)
- In visionOS, Image-Based Lighting (IBL) is more consistently supported

## Best Practices

- Set appropriate attenuation radius to limit light reach and improve performance
- Use point lights for localized light sources, not scene-wide lighting
- Avoid using too many point lights - they can impact performance
- Use intensity values that match real-world light sources
- Consider using Image-Based Lighting for visionOS experiences
- Test lighting on target platforms - support varies by platform
- Combine with `DynamicLightShadowComponent` if shadows are needed (note: point lights don't cast shadows)

## Related Components

- `DirectionalLightComponent` - For sun-like directional lighting
- `SpotLightComponent` - For focused cone-shaped lighting
- `ImageBasedLightComponent` - For environment lighting (preferred on visionOS)
- `DynamicLightShadowComponent` - For shadow control (not applicable to point lights)
- `GroundingShadowComponent` - For grounding shadows
