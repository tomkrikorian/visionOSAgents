# ClippingComponent


## Overview

A component that clips rendered geometry to a box volume, with optional feathered (soft) edges. Anything outside `bounds` is cut away; the feathered edge fades geometry near the box faces instead of producing a hard cut. Useful for table-top scenes, portals into volumes, and revealing cross-sections.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Constraining content to a volume so it never pokes outside its region
- Cross-section or cutaway views of models
- Soft-fading content at the boundary of a diorama or table-top scene
- Reveal effects driven by animating the clip bounds

## How to Use

### Basic Box Clipping

```swift
import RealityKit

let bounds = BoundingBox(min: [-0.5, 0, -0.5], max: [0.5, 1, 0.5])
var clipping = ClippingComponent(bounds: bounds)
entity.components.set(clipping)
```

### Feathered Edges

```swift
var clipping = ClippingComponent(bounds: bounds)
clipping.featheredEdge = .init(
    symmetricEdgeInset: [0.05, 0.05, 0.05],  // Fade zone per axis
    falloff: .cubic                          // .linear or .cubic
)
entity.components.set(clipping)
```

### Asymmetric Feather and Scope

```swift
var clipping = ClippingComponent(bounds: bounds)
var edge = ClippingComponent.FeatheredEdge()
edge.positiveEdgeInset = [0.1, 0.0, 0.1]  // Fade on +X / +Z faces
edge.negativeEdgeInset = [0.0, 0.0, 0.0]  // Hard cut on -X / -Y / -Z
edge.falloff = .linear
clipping.featheredEdge = edge

clipping.shouldClipChildren = true  // Clip descendants
clipping.shouldClipSelf = true      // Clip this entity's own model
entity.components.set(clipping)
```

## Key Properties

- `bounds: BoundingBox` - The clip volume in the entity's local space
- `featheredEdge: FeatheredEdge` - Soft-edge configuration; `.none` for hard
  clipping
- `shouldClipChildren: Bool` - Whether descendant entities are clipped
- `shouldClipSelf: Bool` - Whether the entity's own geometry is clipped

`ClippingComponent.FeatheredEdge`:
- `falloff: Falloff` - `.linear` or `.cubic` fade curve
- `positiveEdgeInset: SIMD3<Float>` - Fade depth inside the +X/+Y/+Z faces
- `negativeEdgeInset: SIMD3<Float>` - Fade depth inside the -X/-Y/-Z faces
- `init(symmetricEdgeInset:falloff:)` - Same inset on both faces per axis
- `static var none` - No feathering

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, tvOS 27,
  and macCatalyst 27.
- `ClippingPrimitiveComponent` also exists in the SDK but is already
  deprecated with "Use ClippingComponent instead". Its `Feather` type
  used fractional edge values (`fractionPerPositiveEdge` /
  `fractionPerNegativeEdge`); `ClippingComponent.FeatheredEdge` uses metric
  insets instead. Write new code against `ClippingComponent`.
- Edge insets are measured inward from the box faces; the feather zone lives
  inside `bounds`, not outside it.
- Clipping is visual - collision shapes, physics, and input targets are not
  clipped.

## Best Practices

- Animate `bounds` for reveal effects instead of swapping meshes.
- Use `.cubic` falloff for smooth, organic fades; `.linear` for technical
  cross-sections.
- Keep `shouldClipChildren = true` (and structure content under one clip root)
  rather than attaching separate clip components per child.
- Pair with collision/input adjustments when clipped-away geometry should also
  stop being interactive.

## Related Components

- `PortalComponent` - For rendering content through a portal surface
- `OpacityComponent` - For whole-hierarchy fading without a volume
- `WorldComponent` - For separate world content shown through portals
