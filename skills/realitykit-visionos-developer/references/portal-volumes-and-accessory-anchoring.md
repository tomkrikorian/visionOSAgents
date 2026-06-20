# Portal Volumes and Accessory Anchoring


## Overview

Two additions new in visionOS 27. Portals gain volumetric clipping/crossing
(`PortalComponent.Volume`) and a `PortalFactory` that assembles a complete,
correctly wired portal setup in one call. `AnchoringComponent` gains accessory
anchoring types for spatial controllers and stylus (`.leftController`,
`.rightController`, `.eitherController`, `.stylus`). Portal additions are also
on macOS/iOS/tvOS 27; accessory types are visionOS-only.

## When to Use

- Portals whose content should clip/cross within a 3D box, not just a plane
- Quickly standing up a portal + world pair without manual wiring
- Softening the lighting transition at a portal boundary
- Anchoring content to a tracked spatial controller or stylus

## How to Use

### Volumetric Portals

```swift
import RealityKit

let volume = PortalComponent.Volume(extents: [1, 1, 1])  // position: .zero
var portal = PortalComponent(
    target: worldEntity,
    clippingMode: .volume(volume),
    crossingMode: .volume(volume))
portal.lightingBlendDistance = 0.2
portalEntity.components.set(portal)
```

`Volume(position:extents:)` is local to the portal entity. `.volume` joins
the existing `.plane(Plane)` and `.disabled` cases of `ClippingMode` and
`CrossingMode`. New in 27 as well: `Plane(position:normal:radius:)` and
`lightingBlendDistance: Float` (blend distance between the worlds' lighting
at the boundary).

### PortalFactory

```swift
let setup = PortalFactory.createPortal(
    style: .plane(width: 1.0, height: 1.5),   // radius: corner radius
    enableClipping: true,
    enableCrossing: false)

// setup.rootEntity  - add this to your scene
// setup.worldEntity - put portal-world content under this (has WorldComponent)
// setup.portalEntity - the portal surface itself
content.add(setup.rootEntity)
setup.worldEntity.addChild(skyboxEntity)
```

Use `createPortal(world:portalEntity:style:enableClipping:enableCrossing:)`
to reuse an existing world entity or supply your own portal entity.
`Style` currently offers `.plane(width:height:radius:)` (radius default 0).

### Accessory Anchoring (visionOS only)

```swift
let source = AnchoringComponent.AccessoryAnchoringSource(
    type: .rightController, location: nil)
guard let location = source.locationName(named: "aim") else { return }
entity.components.set(AnchoringComponent(
    .accessory(from: source, location: location)))
```

`AccessoryType` values: `.leftController`, `.rightController`,
`.eitherController`, `.stylus`; or construct with
`AccessoryType(identifier:chirality:)`. Inspect `source.accessoryLocations`
for the available `AccessoryLocation`s (`.origin` always exists). The
controller/stylus `AccessoryType` shorthands are new in visionOS 27.

## Key Properties

- `PortalComponent.Volume` - `position`, `extents` (both `SIMD3<Float>`)
- `PortalComponent.lightingBlendDistance: Float`
- `PortalFactory.PortalSetup` - `rootEntity`, `portalEntity`, `worldEntity`
- `AccessoryAnchoringSource.AccessoryType` - `identifier: String`,
  `chirality` (Codable in 27)

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- Volumetric crossing means entities transition between worlds across the
  box boundary; test `PortalCrossingComponent` content against the volume.
- The factory output already contains `WorldComponent` and portal wiring; do
  not add a second `PortalComponent` to its entities.
- Accessory anchoring tracks accessories the system pairs (spatial
  controllers, stylus); there is no macOS/iOS fallback - gate with
  `#available(visionOS 27, *)` and platform checks.

## Related Components

- `PortalComponent` - base portal reference (planes, options, hover/crossing)
- `PortalCrossingComponent` - per-entity crossing participation
- `WorldComponent` - declares the separate world rendered through the portal
- `AnchoringComponent` - all other anchoring targets (planes, hands, images)
- `SpatialTrackingSession` - tracking authorization on visionOS
