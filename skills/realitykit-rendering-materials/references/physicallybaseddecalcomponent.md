# PhysicallyBasedDecalComponent


## Overview

A component that projects a physically based decal onto surrounding geometry. The decal carries optional PBR slots (base color, normal, roughness, metallic, specular, emissive, opacity) that blend onto receiving surfaces inside the decal's bounds - bullet holes, scorch marks, posters, dirt, and damage without modifying the receiving meshes.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Projecting damage, dirt, graffiti, or signage onto existing meshes
- Layering surface detail that should follow receiver geometry
- Stamping dynamic marks (impacts, footprints) at runtime
- Avoiding mesh or texture edits for localized surface changes

## How to Use

### Basic Decal

```swift
import RealityKit

// Decal entity: position/orientation control the projection
var decal = PhysicallyBasedDecalComponent(
    baseColor: .init(texture: .init(decalTexture))
)
decal.bounds = [0.5, 0.5, 0.25]  // Projection volume size in meters
decalEntity.components.set(decal)
```

### Full PBR Slots

```swift
var decal = PhysicallyBasedDecalComponent()
decal.baseColor = .init(texture: .init(colorTexture))
decal.normal = .init(texture: .init(normalTexture))
decal.roughness = .init(texture: .init(roughnessTexture))
decal.opacity = .init(texture: .init(maskTexture))
decal.bounds = [1.0, 1.0, 0.5]
decalEntity.components.set(decal)
```

### Limit Receivers and Order Overlaps

```swift
var decal = PhysicallyBasedDecalComponent()
decal.baseColor = .init(texture: .init(posterTexture))
decal.receiverEntities = [wallEntity]  // Only the wall receives it
decal.sortOrder = 1                    // Drawn over sortOrder 0 decals
decalEntity.components.set(decal)
```

## Key Properties

- `baseColor: PhysicallyBasedMaterial.BaseColor?` - Albedo contribution
- `normal: PhysicallyBasedMaterial.Normal?` - Normal-map contribution
- `roughness: PhysicallyBasedMaterial.Roughness?` - Roughness contribution
- `metallic: PhysicallyBasedMaterial.Metallic?` - Metallic contribution
- `specular: PhysicallyBasedMaterial.Specular?` - Specular contribution
- `emissive: PhysicallyBasedMaterial.EmissiveColor?` - Emissive contribution
- `opacity: PhysicallyBasedMaterial.Opacity?` - Blend mask for the decal
- `receiverEntities: Set<Entity>` - Entities the decal projects onto
- `sortOrder: Int32` - Ordering between overlapping decals
- `layers: RenderLayer.Set` - Render layers the decal belongs to
- `bounds: SIMD3<Float>` - Size of the projection volume

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, tvOS 27,
  and macCatalyst 27.
- All material slots are optional and reuse the `PhysicallyBasedMaterial`
  slot types - unset slots leave the receiver's corresponding channel intact.
- The decal entity's transform places and orients the projection; `bounds`
  sizes the volume it projects through.
- An empty `receiverEntities` set follows the component default; set it
  explicitly to restrict projection to known receivers.
- `layers` integrates decals with the named render-layer system (see
  `render-layers-and-shadows.md`).

## Best Practices

- Provide an `opacity` mask so decal edges fade instead of showing the
  rectangular bounds.
- Keep `bounds` as tight as possible around the visible decal area.
- Use `sortOrder` deliberately when decals overlap; rely on it rather than
  transform tweaks to control layering.
- Restrict `receiverEntities` in busy scenes so decals do not bleed onto
  unintended geometry behind the receiver.

## Related Components

- `ModelComponent` - For the receiving meshes and their materials
- `RenderLayerComponent` - For layer-scoped rendering
- `ClippingComponent` - For box-bounded clipping rather than projection
