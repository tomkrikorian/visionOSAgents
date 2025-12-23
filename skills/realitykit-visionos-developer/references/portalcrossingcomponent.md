# PortalCrossingComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/portalcrossingcomponent)

## Overview

A component that controls behavior when entities cross portal boundaries. This component allows you to define custom logic or effects that trigger when entities move from one world to another through a portal, such as teleportation, scene switching, or state changes.

## When to Use

- Implementing teleportation effects when entities cross portals
- Triggering scene switches or state changes on portal crossing
- Applying transformations or effects to entities crossing boundaries
- Creating transition effects between worlds
- Implementing game logic based on portal crossings
- Handling entity state when moving between portal worlds

## How to Use

### Basic Setup

```swift
import RealityKit

// Add to entities that should respond to portal crossings
let crossingComponent = PortalCrossingComponent()
entity.components.set(crossingComponent)
```

### With Portal Component

```swift
// Portal with crossing enabled
let portal = PortalComponent(
    target: worldEntity,
    clippingMode: .plane(.positiveZ),
    crossingMode: .plane(.positiveZ)  // Enable crossing
)
portalEntity.components.set(portal)

// Entities with PortalCrossingComponent will trigger crossing behavior
let player = Entity()
player.components.set(PortalCrossingComponent())
```

## Key Properties

- Properties may include configuration for crossing behavior, callbacks, or state management
- Consult official documentation for specific API details

## Important Notes

- Works in conjunction with `PortalComponent` that has `crossingMode` enabled
- Entities need this component to participate in portal crossing behavior
- Crossing behavior is tied to the portal's plane definition
- Available on visionOS, iOS, and other Apple platforms
- Portal crossing features are newer (introduced in WWDC 2024)

## Best Practices

- Add component to entities that should respond to portal crossings
- Ensure portal has `crossingMode` enabled for crossing to work
- Handle state transitions appropriately when entities cross
- Test crossing behavior with various entity types and movements
- Consider performance when many entities cross portals
- Combine with appropriate portal configuration for desired effects

## Related Components

- `PortalComponent` - Required with `crossingMode` enabled
- `WorldComponent` - Defines the target world for the portal
- `EnvironmentLightingConfigurationComponent` - For lighting transitions
