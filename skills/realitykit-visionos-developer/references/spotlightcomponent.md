# SpotLightComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/spotlightcomponent)

## Overview

A component that adds a cone-shaped spotlight that emits light in a focused beam. Spotlights are useful for flashlights, headlights, stage lighting, or any focused light source. The light has an inner and outer angle that creates a soft falloff (penumbra) between the bright center and the edges.

## When to Use

- Creating flashlight or headlight effects
- Implementing stage lighting or focused beam effects
- Adding dramatic spotlighting to specific areas
- Creating searchlight or spotlight effects
- Implementing focused lighting that follows an entity

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a spotlight
var spotlight = SpotLightComponent()
spotlight.color = .white
spotlight.intensity = 2000
spotlight.innerAngleInDegrees = 30  // Bright center cone
spotlight.outerAngleInDegrees = 45  // Soft falloff edge
spotlight.attenuationRadius = 10.0  // Light reaches 10 meters
entity.components.set(spotlight)
```

### Flashlight Effect

```swift
// Create a flashlight attached to camera/head
var flashlight = SpotLightComponent()
flashlight.color = .white
flashlight.intensity = 1500
flashlight.innerAngleInDegrees = 20  // Narrow beam
flashlight.outerAngleInDegrees = 35  // Soft edges
flashlight.attenuationRadius = 15.0
flashlightEntity.components.set(flashlight)

// Point the light forward
flashlightEntity.orientation = simd_quatf(angle: 0, axis: [0, 1, 0])
```

### With Shadows

```swift
// Create spotlight with shadow support
var spotlight = SpotLightComponent()
spotlight.color = .white
spotlight.intensity = 2000
spotlight.innerAngleInDegrees = 30
spotlight.outerAngleInDegrees = 45

// Configure shadows
var shadow = SpotLightComponent.Shadow()
shadow.maximumDistance = 20.0
shadow.depthBias = 0.01
spotlight.shadow = shadow

entity.components.set(spotlight)
```

### Stage Lighting

```swift
// Create warm stage lighting
var stageLight = SpotLightComponent()
stageLight.color = .init(red: 1.0, green: 0.9, blue: 0.8)  // Warm white
stageLight.intensity = 3000
stageLight.innerAngleInDegrees = 15  // Tight focus
stageLight.outerAngleInDegrees = 25  // Sharp falloff
stageLight.attenuationRadius = 8.0
entity.components.set(stageLight)
```

## Key Properties

- `color: Color` - The color of the light (default: white)
- `intensity: Float` - The brightness of the light in lumens
- `innerAngleInDegrees: Float` - The angle of the bright center cone
- `outerAngleInDegrees: Float` - The angle of the soft falloff edge
- `attenuationRadius: Float` - The distance in meters at which light intensity reaches zero
- `shadow: Shadow?` - Shadow configuration with `maximumDistance` and `depthBias`

### Shadow Properties

- `maximumDistance: Float` - Maximum distance for shadow casting
- `depthBias: Float` - Depth bias to prevent shadow acne

## Important Notes

- Spotlights emit light in a cone shape from the entity's position
- Both position and orientation matter - the light points along the entity's negative Z-axis
- The inner angle defines the bright center, outer angle defines the soft edge
- Supports shadows when configured (depth-map shadows)
- Light intensity falls off with distance based on attenuation radius
- Available on iOS, macOS, and visionOS (with limitations on visionOS)
- In visionOS, Image-Based Lighting (IBL) is more consistently supported
- WWDC 2024 introduced improved dynamic lights & shadows support for visionOS

## Best Practices

- Set inner and outer angles to create natural-looking penumbra
- Use appropriate attenuation radius to limit light reach and improve performance
- Configure shadows when needed for realism, but be aware of performance cost
- Position and orient the spotlight entity to point the light where needed
- Use intensity values that match real-world light sources
- Consider Image-Based Lighting for visionOS experiences
- Test on target platforms - support varies by platform
- Avoid using too many spotlights - they can impact performance
- Combine with `DynamicLightShadowComponent` on entities that should cast shadows

## Related Components

- `PointLightComponent` - For omnidirectional point lights
- `DirectionalLightComponent` - For sun-like directional lighting
- `ImageBasedLightComponent` - For environment lighting (preferred on visionOS)
- `DynamicLightShadowComponent` - For per-entity shadow control
- `GroundingShadowComponent` - For grounding shadows
