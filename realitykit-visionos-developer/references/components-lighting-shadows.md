# Lighting and Shadows Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## PointLightComponent
Goal: Adds an omnidirectional point light source.

```swift
entity.components.set(PointLightComponent())
```

## DirectionalLightComponent
Goal: Adds a directional light source with parallel rays.

```swift
entity.components.set(DirectionalLightComponent())
```

## SpotLightComponent
Goal: Adds a cone-shaped spotlight.

```swift
entity.components.set(SpotLightComponent())
```

## ImageBasedLightComponent
Goal: Applies environment lighting from an HDR texture.

```swift
let light = ImageBasedLightComponent(texture: <#TextureResource#>)
entity.components.set(light)
```

## ImageBasedLightReceiverComponent
Goal: Enables an entity to receive image-based lighting.

```swift
entity.components.set(ImageBasedLightReceiverComponent())
```

## GroundingShadowComponent
Goal: Adds a grounding shadow to anchor content visually.

```swift
entity.components.set(GroundingShadowComponent())
```

## DynamicLightShadowComponent
Goal: Enables dynamic shadows from light sources.

```swift
entity.components.set(DynamicLightShadowComponent())
```

## EnvironmentLightingConfigurationComponent
Goal: Configures environment lighting behavior.

```swift
entity.components.set(EnvironmentLightingConfigurationComponent())
```

## VirtualEnvironmentProbeComponent
Goal: Provides reflection probes for virtual environments.

```swift
entity.components.set(VirtualEnvironmentProbeComponent())
```
