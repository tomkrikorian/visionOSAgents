# LevelOfDetailComponent


## Overview

A component that switches between detail levels of content based on a selection strategy. Each level is an array of entities (`DetailLevel = [Entity]`); RealityKit shows exactly one level at a time, chosen by camera distance, projected screen area, or a per-axis resolution metric. Use it to render cheap proxies far away and full-detail meshes up close.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Reducing triangle and material cost for distant objects
- Large scenes with many instances where only nearby ones need full detail
- Swapping imposter/proxy versions of complex assets automatically
- Keeping frame rate stable as users move through big environments

## How to Use

### Camera-Distance Levels (Helper)

```swift
import RealityKit

// Levels ordered nearest-first; maxDistance is where each level ends.
LevelOfDetailComponent.addByCameraDistance(
    to: entity,
    levels: [
        (entities: [highDetail], maxDistance: 2.0),
        (entities: [mediumDetail], maxDistance: 8.0),
        (entities: [lowDetail], maxDistance: 30.0),
    ]
)
```

### Screen-Area Levels (Helper)

```swift
// minArea is the smallest projected screen area where the level still shows.
LevelOfDetailComponent.addByScreenArea(
    to: entity,
    levels: [
        (entities: [highDetail], minArea: 0.25),
        (entities: [lowDetail], minArea: 0.01),
    ]
)
```

### Explicit Component with a Strategy

```swift
var lod = LevelOfDetailComponent(
    levels: [[highDetail], [mediumDetail], [lowDetail]],
    switchingAt: .cameraDistance([2.0, 8.0, 30.0])
)
entity.components.set(lod)
```

### Resolution-Metric Strategy

```swift
// Per-axis switching resolutions against the content's bounding box.
let resolutions = LevelOfDetailComponent.SelectionStrategy
    .ResolutionMetric.DirectionalSwitchingResolutions(
        positiveX: 256, negativeX: 256,
        positiveY: 256, negativeY: 256,
        positiveZ: 256, negativeZ: 256
    )
LevelOfDetailComponent.addByResolutionMetric(
    to: entity,
    levels: [(entities: [highDetail], switchingResolutions: resolutions)],
    boundingBox: contentBounds
)
```

### Force a Level

```swift
var lod = entity.components[LevelOfDetailComponent.self]!
lod.levelSelection = .fixed(0)   // Pin to the first level
// lod.levelSelection = .automatic  // Resume strategy-driven switching
entity.components.set(lod)
```

## Key Properties

- `levels: [DetailLevel]` - One entity array per detail level
- `strategy: SelectionStrategy` - `.cameraDistance([Float])`,
  `.screenArea([Float])`, or
  `.resolutionMetric(switchingResolutions:boundingBox:)`
- `levelSelection: LevelSelection` - `.automatic` or `.fixed(Int)`

Static helpers:
- `addByCameraDistance(to:levels:)` - `(entities:maxDistance:)` tuples
- `addByScreenArea(to:levels:)` - `(entities:minArea:)` tuples
- `addByResolutionMetric(to:levels:boundingBox:)` -
  `(entities:switchingResolutions:)` tuples plus a shared bounding box

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, tvOS 27,
  and macCatalyst 27.
- Threshold arrays correspond positionally to `levels`; keep counts aligned.
- A `DetailLevel` can contain multiple entities, so a level can be a group of
  parts, not just one mesh.
- `DirectionalSwitchingResolutions` lets switching differ per viewing axis,
  useful for flat or elongated content.
- `.fixed` is the debugging tool: pin each level to verify its content before
  trusting automatic switching.

## Best Practices

- Author meaningfully cheaper levels - LOD only pays off if lower levels cut
  triangles, materials, or texture bindings.
- Order levels highest-detail first and verify thresholds on device, where
  perceived sizes differ from the simulator.
- Prefer the static helpers; they bundle level/threshold pairing in one call.
- Avoid switching distances right at typical user standing distance, or
  content will pop as users sway.

## Related Components

- `ModelComponent` - For the meshes inside each detail level
- `OcclusionCullingComponent` - For skipping hidden geometry entirely
- `AdaptiveResolutionComponent` - For texture-resolution-driven adaptation
