# DynamicLightShadowComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/dynamiclightshadowcomponent)

## Overview

A component that controls whether an entity casts shadows when lit by dynamic lights (spotlights or directional lights). By default, entities under dynamic spotlights or directional lights will cast shadows. Use this component to disable shadow casting for specific entities or to configure shadow behavior.

## When to Use

- Disabling shadow casting for specific entities to improve performance
- Controlling which entities cast shadows in scenes with dynamic lighting
- Optimizing shadow rendering by selectively enabling shadows
- Creating special effects where some objects shouldn't cast shadows
- Fine-tuning shadow behavior in complex scenes

## How to Use

### Disable Shadow Casting

```swift
import RealityKit

// Disable shadow casting for an entity
let shadowComponent = DynamicLightShadowComponent(castsShadow: false)
entity.components.set(shadowComponent)
```

### Enable Shadow Casting (Explicit)

```swift
// Explicitly enable shadow casting (default behavior)
let shadowComponent = DynamicLightShadowComponent(castsShadow: true)
entity.components.set(shadowComponent)
```

### Selective Shadow Control

```swift
// Some entities cast shadows, others don't
let importantEntity = Entity()
importantEntity.components.set(DynamicLightShadowComponent(castsShadow: true))

let backgroundEntity = Entity()
backgroundEntity.components.set(DynamicLightShadowComponent(castsShadow: false))
```

## Key Properties

- `castsShadow: Bool` - Whether the entity casts shadows when lit by dynamic lights (default: true)

## Important Notes

- Only works with dynamic lights: `SpotLightComponent` and `DirectionalLightComponent`
- `PointLightComponent` does **not** cast shadows, so this component has no effect with point lights
- By default, entities cast shadows when lit by spotlights or directional lights
- Set `castsShadow: false` to disable shadow casting for specific entities
- Introduced in WWDC 2024 as part of RealityKit's dynamic lights & shadows APIs
- Available on visionOS, iOS, and other Apple platforms (check minimum OS requirements)
- Shadows can be performance-intensive - use selectively to optimize rendering

## Best Practices

- Disable shadow casting for background or distant entities to improve performance
- Keep shadow casting enabled for important foreground objects
- Use this component to fine-tune shadow behavior in complex scenes
- Test shadow performance on target devices
- Combine with appropriate light shadow configuration (`maximumDistance`, `depthBias`)
- Consider the visual impact when disabling shadows - some scenes may look unrealistic
- Use in conjunction with `SpotLightComponent` or `DirectionalLightComponent` shadow settings

## Related Components

- `SpotLightComponent` - Spotlights can cast shadows (configure via `shadow` property)
- `DirectionalLightComponent` - Directional lights can cast shadows (configure via `shadow` property)
- `PointLightComponent` - Point lights do not cast shadows (this component has no effect)
- `GroundingShadowComponent` - For grounding shadows (different from dynamic light shadows)
- `ImageBasedLightComponent` - For environment lighting (doesn't use this component)
