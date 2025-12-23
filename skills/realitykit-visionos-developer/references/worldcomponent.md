# WorldComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/worldcomponent)

## Overview

A component that marks an entity root as a separate rendering "world" which is only visible through portals. Entities under this world are hidden unless viewed via a `PortalComponent` targeting this world. It enables separating scene hierarchy and visibility, allowing you to create isolated spaces that are only visible through portal openings.

## When to Use

- Creating separate renderable worlds for portal rendering
- Implementing portal effects where different scenes are visible through openings
- Creating isolated environments within a larger scene
- Building nested scenes or separate spaces
- Organizing scene hierarchy for portal-based rendering
- Creating "pocket dimensions" or separate virtual spaces

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a world entity
let worldEntity = Entity()
worldEntity.components.set(WorldComponent())

// Add content to the world
let spaceScene = try await Entity(named: "SpaceScene")
worldEntity.addChild(spaceScene)

// Create portal that targets this world
let portal = PortalComponent(target: worldEntity, ...)
portalEntity.components.set(portal)
```

### Multiple Portals to Same World

```swift
// Only one WorldComponent per target is needed
let worldEntity = Entity()
worldEntity.components.set(WorldComponent())
// Add content...

// Multiple portals can point to the same world
let portal1 = PortalComponent(target: worldEntity, ...)
let portal2 = PortalComponent(target: worldEntity, ...)
```

### Separate Worlds

```swift
// Create multiple separate worlds
let spaceWorld = Entity()
spaceWorld.components.set(WorldComponent())
// Add space content...

let oceanWorld = Entity()
oceanWorld.components.set(WorldComponent())
// Add ocean content...

// Create portals to each world
let spacePortal = PortalComponent(target: spaceWorld, ...)
let oceanPortal = PortalComponent(target: oceanWorld, ...)
```

## Key Properties

- No configurable properties - the component itself designates the entity as a world root

## Important Notes

- Entities under a world with `WorldComponent` are hidden unless viewed through a portal
- Only one `WorldComponent` per target entity is needed
- Multiple portals can point to the same world
- Worlds behave as isolated spaces within the scene hierarchy
- Available on visionOS, iOS, and other Apple platforms
- Works in conjunction with `PortalComponent` for visibility

## Best Practices

- Use descriptive names for world entities (e.g., "SpaceWorld", "OceanWorld")
- Organize world content hierarchically under the world entity
- Only one `WorldComponent` per world - reuse the same world for multiple portals
- Test portal visibility to ensure worlds render correctly
- Consider performance when using multiple worlds
- Combine with appropriate portal configuration for desired effects

## Related Components

- `PortalComponent` - Required to view world content (points to world entity)
- `PortalCrossingComponent` - For controlling behavior when entities cross into worlds
- `EnvironmentLightingConfigurationComponent` - For lighting configuration in worlds
