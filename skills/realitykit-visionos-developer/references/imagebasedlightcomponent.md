# ImageBasedLightComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/imagebasedlightcomponent)

## Overview

A component that applies environment lighting from an HDR texture (skybox). Image-based lighting (IBL) provides realistic reflections and ambient lighting by using an environment map. This creates more natural-looking scenes with proper light reflection and ambient occlusion.

## When to Use

- Creating realistic sunlight or directional lighting effects
- Applying environment lighting from skybox textures
- Simulating outdoor lighting conditions
- Adding ambient lighting that matches the environment
- Creating lighting that rotates with an entity

## How to Use

### Real-World Example: Sunlight from Skybox

This example from the Hello World sample shows how to add sunlight using an image-based light:

```swift
import RealityKit

extension Entity {
    /// Adds an image-based light that emulates sunlight.
    /// Assumes the project contains a folder called `Sunlight.skybox`
    /// with an image of a white dot on a black background.
    func setSunlight(intensity: Float?) {
        if let intensity {
            Task {
                guard let resource = try? await EnvironmentResource(named: "Sunlight") else { return }
                var iblComponent = ImageBasedLightComponent(
                    source: .single(resource),
                    intensityExponent: intensity
                )

                // Ensure that the light rotates with its entity
                iblComponent.inheritsRotation = true

                components.set(iblComponent)
                components.set(ImageBasedLightReceiverComponent(imageBasedLight: self))
            }
        } else {
            components.remove(ImageBasedLightComponent.self)
            components.remove(ImageBasedLightReceiverComponent.self)
        }
    }
}

// Usage
earthEntity.setSunlight(intensity: 14.0)
```

### Basic Setup

```swift
import RealityKit

// Load environment resource
let environmentResource = try await EnvironmentResource(named: "Sunlight")

// Create image-based light component
var iblComponent = ImageBasedLightComponent(
    source: .single(environmentResource),
    intensityExponent: 14.0
)

// Make light rotate with entity
iblComponent.inheritsRotation = true

entity.components.set(iblComponent)
```

### With ImageBasedLightReceiverComponent

Entities that should receive image-based lighting need both components:

```swift
// Add the light source
var iblComponent = ImageBasedLightComponent(
    source: .single(environmentResource),
    intensityExponent: intensity
)
entity.components.set(iblComponent)

// Add receiver so the entity responds to the light
entity.components.set(ImageBasedLightReceiverComponent(imageBasedLight: entity))
```

## Key Properties

- `source: ImageBasedLightComponent.Source` - The environment resource(s) providing the lighting
- `intensityExponent: Float` - The brightness of the light (higher values = brighter)
- `inheritsRotation: Bool` - Whether the light rotates with the entity (default: false)

## Important Notes

- Requires an `EnvironmentResource` (skybox) containing an HDR image
- The position of bright spots in the skybox image determines light direction
- Use a small bright dot on a dark background for directional sunlight
- Must be paired with `ImageBasedLightReceiverComponent` on entities that should receive the light
- Set `inheritsRotation = true` if you want the light to rotate with the entity

## Best Practices

- Use skybox images with a small bright dot for directional sunlight
- Tune `intensityExponent` to match your scene's lighting needs
- Set `inheritsRotation = true` for lights attached to rotating entities (like planets)
- Remove the component when disabling lighting to improve performance
- Load environment resources asynchronously to avoid blocking the main actor

## Related Components

- `ImageBasedLightReceiverComponent` - Required on entities that should receive IBL lighting
- `DirectionalLightComponent` - Alternative for simpler directional lighting
- `PointLightComponent` - For point light sources
