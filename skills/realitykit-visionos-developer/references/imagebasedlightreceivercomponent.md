# ImageBasedLightReceiverComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/imagebasedlightreceivercomponent)

## Overview

A component that enables an entity to receive and respond to image-based lighting (IBL) in the scene. This component must be paired with `ImageBasedLightComponent` to create realistic lighting effects. Entities with this component will reflect and respond to the environment lighting provided by image-based light sources.

## When to Use

- Enabling entities to receive image-based lighting from skybox textures
- Creating realistic reflections on surfaces
- Making entities respond to environment lighting
- Implementing sunlight or directional lighting effects
- Creating materials that reflect the environment

## How to Use

### Real-World Example: Sunlight Setup

This example from the Hello World sample shows how to pair ImageBasedLightComponent with ImageBasedLightReceiverComponent:

```swift
import RealityKit

extension Entity {
    func setSunlight(intensity: Float?) {
        if let intensity {
            Task {
                guard let resource = try? await EnvironmentResource(named: "Sunlight") else { return }
                var iblComponent = ImageBasedLightComponent(
                    source: .single(resource),
                    intensityExponent: intensity
                )
                iblComponent.inheritsRotation = true

                // Set the light source
                components.set(iblComponent)
                
                // Enable this entity to receive the light
                components.set(ImageBasedLightReceiverComponent(imageBasedLight: self))
            }
        } else {
            components.remove(ImageBasedLightComponent.self)
            components.remove(ImageBasedLightReceiverComponent.self)
        }
    }
}
```

### Basic Setup

```swift
import RealityKit

// First, add the image-based light source
let iblComponent = ImageBasedLightComponent(
    source: .single(environmentResource),
    intensityExponent: 14.0
)
entity.components.set(iblComponent)

// Then, enable the entity to receive the light
entity.components.set(ImageBasedLightReceiverComponent(imageBasedLight: entity))
```

### With Specific Light Source

```swift
// Reference a specific entity that has ImageBasedLightComponent
let lightSourceEntity = // ... entity with ImageBasedLightComponent
entity.components.set(ImageBasedLightReceiverComponent(imageBasedLight: lightSourceEntity))
```

## Key Properties

- `imageBasedLight: Entity?` - The entity that provides the image-based lighting (typically the same entity or a parent)

## Important Notes

- Must be used together with `ImageBasedLightComponent` on the same or a referenced entity
- Entities without this component will not respond to image-based lighting
- Typically added to the same entity that has the `ImageBasedLightComponent`
- Required for realistic reflections and environment lighting effects
- Can reference a different entity if the light source is separate

## Best Practices

- Always pair with `ImageBasedLightComponent` for complete IBL setup
- Add to entities that should reflect the environment
- Use on the same entity as the light source for simple setups
- Reference a parent entity if the light source is in a hierarchy
- Remove both components together when disabling lighting

## Related Components

- `ImageBasedLightComponent` - Required companion component that provides the light source
- `DirectionalLightComponent` - Alternative for simpler directional lighting
- `PointLightComponent` - For point light sources
