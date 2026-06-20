# Render Layers and Shadow Controls

Use this file for the visionOS 27 named render-layer system and the expanded
light/shadow controls: per-light layer masks, cascaded directional shadows,
spot-shadow quality and soft shadows, projective spotlight textures, and
surroundings lights that illuminate passthrough.

All API in this file is new in visionOS 27. Beta API: names and shapes may
change before release.

## Named Render Layers

`RenderLayer` is a named tag; `RenderLayer.Set` is a collection of them.
Entities declare membership with `RenderLayerComponent`; lights, shadows, and
decals carry layer masks that scope which content they affect.

```swift
import RealityKit

let heroLayer = RenderLayer("hero")

// Tag content with layers.
heroEntity.components.set(RenderLayerComponent(heroLayer))
// Or: RenderLayerComponent(layers: [heroLayer, RenderLayer.defaultLayer])

// Explicitly place content on the default layer.
backgroundEntity.components.set(RenderLayerComponent.defaultLayer)
```

- `RenderLayer.defaultLayer` - the implicit layer for untagged content
- `RenderLayer(_ name: StaticString)` / `RenderLayer(rawValue: String)?`
- `RenderLayer.Set` - `insert`, `remove`, `contains`, array-literal syntax
- `RenderLayerComponent(layers:)`, `RenderLayerComponent(_ layers...)`,
  `RenderLayerComponent(layer:)`

## Per-Light Layer Masks

`DirectionalLightComponent`, `SpotLightComponent`, and `PointLightComponent`
gained `layers: RenderLayer.Set` - the light only illuminates entities on
those layers. Directional and spot `Shadow` types gained an optional
`layers: RenderLayer.Set?` (and `init(layers:)`) to scope shadow casting
independently of illumination.

```swift
var spot = SpotLightComponent()
spot.layers = [heroLayer]                 // Light only the hero content
spot.shadow = .init(layers: [heroLayer])  // Shadows from hero content only
lightEntity.components.set(spot)
```

## Cascaded Directional Shadows

`DirectionalLightComponent.Shadow.Cascades` splits the shadow map into
cascades for stable quality across large distances.

```swift
var sun = DirectionalLightComponent()
var shadow = DirectionalLightComponent.Shadow()
shadow.cascades = .fixed(4, bias: 0.5)  // Or .automatic
sun.shadow = shadow
sunEntity.components.set(sun)
```

- `.fixed(_ count: Int, bias: Float = 0.0)` - explicit cascade count;
  `bias` shifts the split distribution
- `.automatic` - let RealityKit choose

## Spot Shadow Quality and Soft Shadows

`SpotLightComponent.Shadow` gained a quality mode and an area-light size for
soft penumbras.

```swift
var spot = SpotLightComponent()
var shadow = SpotLightComponent.Shadow()
shadow.quality = .high       // .low / .medium / .high
shadow.lightSize = 0.05      // Larger source -> softer shadow edges
spot.shadow = shadow
lightEntity.components.set(spot)
```

`lightSize` and `quality` are not available on tvOS; they cover visionOS 27,
iOS 27, macCatalyst 27, and macOS 27.

## Projective Spotlight Textures

`SpotLightComponent.ProjectiveTexture` is a separate component set on the
spotlight entity. It projects a texture (gobo/projector pattern) through the
spotlight cone.

```swift
lightEntity.components.set(SpotLightComponent())
lightEntity.components.set(
    SpotLightComponent.ProjectiveTexture(texture: goboTexture)
)
// Variants:
//   init(texture:scale:)                scale defaults to [1.0, 1.0]
//   init(texture:coordinateTransform:)  full TextureCoordinateTransform
```

- `texture: TextureResource`
- `coordinateTransform: TextureCoordinateTransform` (typealias of
  `MaterialParameterTypes.TextureCoordinateTransform`)
- Not available on tvOS.

## Surroundings Lights (Passthrough Illumination)

`SpotLightComponent.SurroundingsLight` and
`PointLightComponent.SurroundingsLight` are marker components that make the
light illuminate the real passthrough surroundings, not just virtual content.
visionOS 27 and macOS 27 only - unavailable on iOS, macCatalyst, and tvOS.

```swift
lightEntity.components.set(SpotLightComponent())
lightEntity.components.set(SpotLightComponent.SurroundingsLight())
```

Both are empty (`init()`) marker components; configure intensity, color, and
cone on the base light component.

## Pitfalls

- A light with a non-default `layers` set silently stops lighting untagged
  content; keep `RenderLayer.defaultLayer` in the set when mixing tagged and
  untagged entities.
- `Shadow.layers = nil` (default) follows the light; set it only to decouple
  shadow casting from illumination.
- More cascades and `.high` quality cost shadow-map memory and fill rate;
  tune on device.
- `PhysicallyBasedDecalComponent.layers` participates in the same layer
  system (see `physicallybaseddecalcomponent.md`).

## Related References

- `directionallightcomponent.md`, `spotlightcomponent.md`,
  `pointlightcomponent.md` - base light setup
- `dynamiclightshadowcomponent.md` - per-entity shadow opt-in/out
- `physicallybaseddecalcomponent.md` - layer-scoped decals
