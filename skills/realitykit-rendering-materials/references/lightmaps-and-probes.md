# Lightmaps and Diffuse Light Probes

Use this file for baked global illumination on visionOS 27: lightmap atlases
applied through `LightmapResource` / `LightmapComponent`, and tetrahedral
diffuse light probes applied through `DiffuseProbeResource` and the
light-probe group/receiver components.

All API in this file is new in visionOS 27. Beta API: names and shapes may
change before release.

## Lightmaps

`LightmapResource` wraps baked lighting stored in texture atlases.
`LightmapComponent` applies it to an entity hierarchy and maps each entity to
its slot in the resource.

### Bake Types

`LightmapResource.BakeType` declares what a baked atlas contains:

- `.ambientOcclusion` - baked AO
- `.indirectDiffuseIrradiance` - indirect diffuse irradiance
- `.indirectDiffuseSHL1Irradiance` - indirect irradiance as SH L1
- `.finalShadedColor` - fully baked shaded color

Each bake type has a matching descriptor (`AmbientOcclusionBakeDescriptor`,
`IndirectDiffuseIrradianceBakeDescriptor`,
`IndirectDiffuseIrradianceSHBakeDescriptor`,
`FinalShadedColorBakeDescriptor`), all constructed with
`init(sourceAtlasReference:)` and wrapped in the `BakeDescriptor` enum.

### Building the Resource

```swift
import RealityKit

// Where this part's lightmap lives inside the atlas.
var atlasRef = LightmapResource.AtlasReference()
atlasRef.atlasTextureIndex = 0
atlasRef.atlasTextureSlice = 0
atlasRef.uvOffset = [0.0, 0.0]
atlasRef.uvScale = [0.5, 0.5]

let part = try LightmapResource.MeshPartLightmapDescriptor(
    bakeDescriptor: .ambientOcclusion(.init(sourceAtlasReference: atlasRef))
)
let entityDesc = try LightmapResource.EntityLightmapDescriptor(
    perPartData: [part]
)
let lightmap = try LightmapResource(
    atlasTextures: [atlasTexture],   // [TextureResource]
    perEntityData: [entityDesc]
)
```

`LightmapResource` also has `init(perEntityData:)`, plus `entityCount` and
`bakeTypes` for inspection.

### Applying the Component

```swift
var component = LightmapComponent(resource: lightmap)
component.entityIndexInLightmapResource = [meshEntity: 0]
component.indirectIrradianceContributionScale = 1.0
rootEntity.components.set(component)
```

- `entityIndexInLightmapResource: [Entity: Int]` - which resource slot each
  entity uses
- `lightmap: LightmapResource` - swap baked data at runtime
- `indirectIrradianceContributionScale: Float` - scales the indirect
  contribution
- `FinalShadedColorBakeMaterial` - a `Material` (plain `init()`) for parts
  whose appearance is entirely the `.finalShadedColor` bake

### Bake Tooling Is macOS-Only

`LightmapComponent.SurfaceExtractor` (`init(lightmapRootEntity:)`,
`extractSurfacesForAtlasSlice(mode:atlasTextureIndex:textureSliceIndex:cameraOutput:cameraTransform:cameraFOVDegrees:onComplete:)`
with `ExtractionMode` `.baseColor` / `.finalShadedColor`) is available on
macOS 27 only and unavailable on visionOS. Bake on macOS, ship the atlas
textures with your app, and apply them on visionOS.

## Tetrahedral Diffuse Light Probes

`DiffuseProbeResource` stores a tetrahedral grid of diffuse light probes for
sampled indirect lighting on dynamic objects.

- The data initializer
  `init(positions:coefficients:tetrahedronIndices:)` is macOS 27 only -
  positions are probe locations, coefficients are per-probe SH data, and
  tetrahedron indices define the interpolation mesh. Build probe data on
  macOS (or ship pre-built resources with content); the visionOS interface
  exposes no constructor for raw probe data.

Two components wire probes into the scene:

```swift
// The entity that owns the probe grid.
probeGroupEntity.components.set(
    DiffuseLightProbeGroupComponent(resource: probeResource)
)

// Dynamic entities that should sample the grid.
characterEntity.components.set(
    DiffuseLightProbeReceiverComponent(probeGroup: probeGroupEntity)
)
```

- `DiffuseLightProbeGroupComponent.resource: DiffuseProbeResource`
- `DiffuseLightProbeReceiverComponent.probeGroup: Entity` - points at the
  entity holding the group component

## Choosing Between Them

- Lightmaps: static geometry with stable lighting; highest quality per texel.
- Diffuse probes: dynamic or movable objects that need to pick up baked
  indirect light as they move through the space.
- Both can coexist - lightmap the environment, probe-light the characters.

## Pitfalls

- Bake pipelines run on macOS; plan an asset pipeline that produces atlas
  textures and probe resources ahead of time for visionOS.
- Keep `entityIndexInLightmapResource` in sync when cloning or restructuring
  the hierarchy; indices refer to slots in the resource, not entity order.
- `uvOffset` / `uvScale` in `AtlasReference` must match the packer that
  produced the atlas or lightmaps will sample the wrong region.
- A receiver without a valid `probeGroup` entity (or a group without its
  component) gets no probe lighting; there is no fallback chain.

## Related References

- `imagebasedlightcomponent.md` / `imagebasedlightreceivercomponent.md` -
  image-based lighting
- `virtualenvironmentprobecomponent.md` - environment probes for reflections
- `render-layers-and-shadows.md` - dynamic light and shadow scoping
