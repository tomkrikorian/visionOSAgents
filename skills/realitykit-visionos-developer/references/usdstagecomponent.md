# USDStageComponent (USDKit Bridge)


## Overview

The `USDKit` + `RealityKit` cross-import overlay renders a live USD stage
inside a RealityKit scene. `USDStageComponent` attaches a `USDStage` to an
`Entity` and keeps it rendered as the stage changes; `USDPlayer` is the
lower-level pull API that emits per-frame diffs (meshes, materials, textures,
deformations) built on `LowLevelMesh`/`LowLevelTexture` payloads. Entity USD
export gains `WriteOptions` and multi-scene `write`. New in visionOS 27.
Also on iOS, macOS, macCatalyst, and tvOS 27.

For the USD stage/layer/prim API itself (opening, authoring, composition),
see the USDKit runtime skill:
[`usdkit-framework.md`](../../usdkit-runtime-developer/references/usdkit-framework.md).

## When to Use

- Displaying a USD file that is being edited live (USD editor, DCC bridge)
- Scrubbing USD time-sampled animation via `timeCode`
- Custom streaming/rendering of USD content through low-level resources
- Exporting entity hierarchies to USD with size/speed tradeoffs

## How to Use

### Attach a Stage to an Entity

```swift
import RealityKit
import USDKit   // cross-import auto-loads the bridge

let stage = try USDStage.open(fileURL)
let entity = Entity()
entity.components.set(await USDStageComponent(stage))
// Scrub animation:
entity.components[USDStageComponent.self]?.timeCode = 24.0
```

`init(_ stage:timeCode:allowsHitTesting:)` defaults: `timeCode: .default`,
`allowsHitTesting: true`. The component re-renders automatically
(`rendersAutomatically`); `stage` is readable from the component.

### One-Shot Render and Completion

```swift
let result = await USDStageComponent.render(stage, to: entity)
if result.status == .failed {
    // result.errors: [USDRenderError]
}
// Or wait on an entity that already has the component:
let done = await USDStageComponent.waitForRenderComplete(on: entity)
```

`Notification.Name.USDStageKitRenderComplete` is posted when a render
finishes.

### Frame-Diff Streaming with USDPlayer

```swift
let player = USDPlayer(stage: stage)   // or init(stage:gpuFamily:)
if var frame = player.update(timeCode: 0.0) {
    for id in frame.meshAdditions {
        if let mesh = frame.takeMeshAddition(id: id) {
            // mesh.descriptor: LowLevelMesh.Descriptor
            // mesh.parts, mesh.indexData, mesh.vertexData
            // mesh.instanceTransforms, mesh.assignedMaterials
            // mesh.meshType: .static or .deformable(DeformationID)
        }
    }
    // Same pattern for materialAdditions/materialUpdates (MaterialData),
    // textureAdditions (TextureData), deformationAdditions (DeformationData).
}
```

`FrameUpdate` lists additions/updates/removals per `MeshID`, `MaterialID`,
and `DeformationID`, additions/removals per `TextureID` (textures are not
updated in place), plus `errors`. Consuming accessors
(`takeMeshAddition(id:)`, `takeMeshUpdate(id:)`, ...) hand payloads over once.
`TextureData` carries a `LowLevelTexture.Descriptor`, level `layout`, and raw
`data`. `DeformationData` carries `SkinningData` (joint transforms, bind
poses, influences), `BlendShapeData` (weights, position offsets), and
`RenormalizationData` (adjacency), each with an `Update` variant.
`importCustomIBLTexture(data:)` converts IBL image data to `TextureData`.

### Entity USD Export Options

```swift
// Single entity, smaller textures:
try await entity.write(to: outputURL,
                       options: [.preferSmallTextureFiles(quality: .medium)])

// Multiple scenes into one USD:
try await Entity.write([sceneA, sceneB], to: outputURL,
                       options: .preferFastExport)
```

`WriteOptions`: `.preferFastExport`, `.preferSmallTextureFiles(quality:
.standard/.medium/.low)`. Conflicting combinations throw
`Entity.WriteError.conflictingOptions(String)`.

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- `USDStage` is not `Sendable`; keep a stage and its component/player work on
  one actor (component inits are `@MainActor`).
- `MaterialData.shaderGraph` references the `ShaderGraph` module surfaced
  through the RealityKit umbrella; treat full programmatic material decoding
  as advanced territory.
- `USDStageComponent` is the simple path; reach for `USDPlayer` only when you
  need custom resource management (own `LowLevelMesh` pools, custom
  streaming).
- The plain `entity.write(to:)` (no options) predates the visionOS 27
  additions; only the `WriteOptions` overloads are new.

## Related Components

- `entity-loading-and-stored-entities.md` - loading USDZ the standard way
- `ModelComponent` - rendered output for self-managed `USDPlayer` content
- usd-editor skill - authoring stages, layers, prims with USDKit
