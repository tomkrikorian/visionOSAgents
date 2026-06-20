# OcclusionCullingComponent


## Overview

A component that opts an entity into occlusion culling, so geometry fully hidden behind other opaque geometry is skipped instead of rendered. The component is a single switch (`isEnabled`); RealityKit performs the visibility determination.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Dense scenes where large occluders (walls, terrain, furniture) hide much of the content
- Interior environments with rooms the user cannot see into
- Reducing GPU cost when overdraw, not triangle count, is the bottleneck

## How to Use

### Enable Culling

```swift
import RealityKit

entity.components.set(OcclusionCullingComponent(isEnabled: true))
```

### Toggle at Runtime

```swift
var culling = entity.components[OcclusionCullingComponent.self]!
culling.isEnabled = false
entity.components.set(culling)
```

## Key Properties

- `isEnabled: Bool` - Whether occlusion culling applies to the entity

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, tvOS 27,
  and macCatalyst 27.
- Occlusion culling skips rendering work for hidden geometry; it does not
  disable the entity - systems, physics, and audio continue to run.
- Culling effectiveness depends on having solid occluders in front of the
  culled content; transparent or cut-out materials make poor occluders.
- The component carries no tuning parameters in the current interface; it is
  purely opt-in/opt-out per entity.

## Best Practices

- Apply to content that is frequently hidden (room interiors, geometry behind
  large props), not to content that is almost always visible.
- Profile before and after: in open scenes with little occlusion, the
  visibility tests add cost without saving draw work.
- Combine with `LevelOfDetailComponent` - LOD reduces the cost of visible
  content, occlusion culling removes the cost of hidden content.
- Disable temporarily (`isEnabled = false`) when debugging missing geometry to
  confirm whether culling is the cause.

## Related Components

- `LevelOfDetailComponent` - For distance/size-based detail switching
- `ModelComponent` - For the rendered geometry being culled
- `AdaptiveResolutionComponent` - For resolution-based content adaptation
