# DockingRegionComponent


## Overview

A component that marks where the system docks video playback inside a custom immersive environment. When system video playback (AVKit) runs while your immersive space is open, the system can dock the player at the entity that carries this component instead of leaving it floating in front of the user. The entity's position and orientation define the docked screen placement; `width` sets the docked screen width in meters.

## When to Use

- Building a custom immersive environment with a dedicated video screen
- Docking system video playback at a fixed spot in the environment
- Cinema-style experiences where video belongs on a designed screen surface

## How to Use

### Basic Setup

```swift
import RealityKit

// Place an entity where the docked video screen should appear
let screenAnchor = Entity()
screenAnchor.position = [0, 2, -8]

var dockingRegion = DockingRegionComponent()
dockingRegion.width = 10  // meters
screenAnchor.components.set(dockingRegion)
```

### Sizing

```swift
// width is the only tunable; the system controls the rest of the
// docked player's size and appearance
var region = DockingRegionComponent()
region.width = 4
```

## Key Properties

- `width: Float` - Width of the docked video screen in meters
- `init()` - No-argument initializer; set `width` afterwards

## Important Notes

- visionOS only - unavailable on iOS, macOS, and tvOS
- Docks system video playback; it does not snap arbitrary entities into place - use `ManipulationComponent` or a custom system for object snapping
- Position and orient the owning entity to place the docked screen; the component exposes no placement properties beyond `width`
- Only one docking region should be active in an environment at a time

## Best Practices

- Place the region at a comfortable viewing distance and height
- Scale `width` to the environment; oversized screens force head movement
- Test with real video content inside the immersive space on device
- Pair with dimmed or designed surroundings so the docked video reads as a screen

## Related Components

- `VideoPlayerComponent` - Entity-based video playback you place yourself
- `WorldComponent` / `PortalComponent` - Building immersive environment content
- `AnchoringComponent` - Anchoring environment content
