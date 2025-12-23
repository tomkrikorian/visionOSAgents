# PortalComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/portalcomponent)

## Overview

A component that creates a "window" or portal through which only entities assigned to a particular `WorldComponent` are visible. Portals render a separate "world" that can be seen through mesh geometry, enabling effects like looking into another dimension, room, or scene through an opening.

## When to Use

- Creating windows or openings that reveal a different scene
- Implementing "portal" effects where one scene is visible through a surface
- Creating separate renderable worlds within a scene
- Implementing scene transitions or teleportation effects
- Creating nested scenes or separate environments
- Building immersive experiences with multiple visible spaces

## How to Use

### Basic Portal Setup

```swift
import RealityKit

// Create a world entity with WorldComponent
let worldEntity = Entity()
worldEntity.components.set(WorldComponent())
// Add content to worldEntity (models, lighting, etc.)

// Create portal entity with portal material
let portalEntity = ModelEntity(
    mesh: .generatePlane(width: 2, height: 2),
    materials: [PortalMaterial()]
)

// Create portal component pointing to the world
let portal = PortalComponent(
    target: worldEntity,
    clippingMode: .plane(.positiveZ),
    crossingMode: .plane(.positiveZ)
)
portalEntity.components.set(portal)

// Add both to scene
parentEntity.addChild(worldEntity)
parentEntity.addChild(portalEntity)
```

### Portal Without Crossing

```swift
// Portal that masks content (no crossing)
let portal = PortalComponent(
    target: worldEntity,
    clippingMode: .plane(.positiveZ),
    crossingMode: nil  // No crossing allowed
)
portalEntity.components.set(portal)
```

### Portal with Crossing

```swift
// Portal that allows entities to cross boundaries
let portal = PortalComponent(
    target: worldEntity,
    clippingMode: .plane(.positiveZ),
    crossingMode: .plane(.positiveZ)  // Entities can cross
)
portalEntity.components.set(portal)
```

## Key Properties

- `target: Entity` - The root entity of the world visible inside the portal (must have `WorldComponent`)
- `clippingMode: PortalComponent.ClippingMode` - Defines how content is clipped (e.g., `.plane(.positiveZ)`)
- `crossingMode: PortalComponent.CrossingMode?` - Allows entities to cross portal boundaries (optional)

### Clipping Modes

- `.plane(direction)` - Clips content using a plane (e.g., `.positiveZ`, `.negativeZ`)

### Crossing Modes

- `.plane(direction)` - Enables entity crossing through a plane boundary
- `nil` - No crossing allowed (entities are masked)

## Important Notes

- The target entity must have `WorldComponent` set
- Clipping plane must align with portal geometry for correct behavior
- Without crossing enabled, entities are simply masked (visible only when entirely in front of portal)
- With crossing enabled, objects can transition across the portal surface
- Portal geometry should use `PortalMaterial` for proper rendering
- Available on visionOS, iOS, and other Apple platforms
- Portal crossing features are newer (introduced in WWDC 2024)

## Best Practices

- Align clipping and crossing planes carefully with portal geometry
- Use `PortalMaterial` on portal mesh for proper rendering
- Test portal behavior with various entity positions and movements
- Consider lighting transitions when entities cross portals
- Use `EnvironmentLightingConfigurationComponent` to modulate lighting across portals
- Only one `WorldComponent` per target is needed (multiple portals can point to same world)
- Test on target platforms - portal features may vary by OS version

## Related Components

- `WorldComponent` - Required on the target entity
- `PortalCrossingComponent` - For controlling behavior when entities cross portals
- `EnvironmentLightingConfigurationComponent` - For lighting transitions across portals
- `PortalMaterial` - Material for portal geometry
