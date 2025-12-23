# AnchoringComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/anchoringcomponent)

## Overview

A component that anchors virtual content to a real world target. This component is essential for getting AR features into RealityKit. Use `AnchoringComponent` to anchor virtual content to a real world target by attaching the component to any `Entity` in your RealityKit scene.

## When to Use

- Anchoring content to detected planes (floors, tables, walls)
- Attaching entities to tracked images or objects
- Anchoring to hand tracking locations
- Creating AR experiences that track real-world objects
- Building spatial experiences that respond to the environment

## How to Use

### Anchor to Hand

```swift
import RealityKit

// Anchor to left hand's wrist
let target = AnchoringComponent.Target.hand(.left, location: .wrist)
let anchoringComponent = AnchoringComponent(target, trackingMode: .predicted)
let entity = Entity()
entity.components.set(anchoringComponent)
```

### Anchor to Plane

```swift
// Anchor to horizontal plane (table, floor)
let target = AnchoringComponent.Target.plane(.horizontal, classification: .any, minimumBounds: [0.1, 0.1])
let anchoringComponent = AnchoringComponent(target)
entity.components.set(anchoringComponent)
```

### Anchor to Image

```swift
// Anchor to tracked image
let imageResource = try await TextureResource.load(named: "ReferenceImage")
let target = AnchoringComponent.Target.image(
    group: "ImageGroup",
    name: "ImageName",
    physicalWidth: 0.2
)
let anchoringComponent = AnchoringComponent(target)
entity.components.set(anchoringComponent)
```

### Anchor to World Origin

```swift
// Anchor to world origin
let target = AnchoringComponent.Target.world(transform: nil)
let anchoringComponent = AnchoringComponent(target)
entity.components.set(anchoringComponent)
```

### Real-World Example: Anchor to Head

This example from the Head Tracking sample shows how to anchor content to the wearer's head position:

```swift
import RealityKit

func startHeadPositionMode(content: RealityViewContent) {
    // Create an anchor for the head and set the tracking mode to `.once`
    // This stops tracking after the initial anchor is established
    let headAnchor = AnchorEntity(.head)
    headAnchor.anchoring.trackingMode = .once
    headAnchor.name = "headAnchor"
    
    // Add the AnchorEntity to the scene
    headAnchorRoot.addChild(headAnchor)
    
    // Add entities as subentities of a root
    headPositionedEntitiesRoot.addChild(feeder)
    headPositionedEntitiesRoot.addChild(hummingbird)
    
    // Position entities relative to the head anchor
    hummingbird.setPosition([0, 0, -0.15], relativeTo: headPositionedEntitiesRoot)
    
    // Add the positioned entities to the anchor, in front of the wearer
    headAnchor.addChild(headPositionedEntitiesRoot)
    headPositionedEntitiesRoot.setPosition([0, 0, -0.6], relativeTo: headAnchor)
}
```

**Important Notes about Head Anchoring:**
- Only works in immersive spaces
- No authorization required
- The transform property returns identity - you can't access the actual head transform
- Use `.once` tracking mode to stop tracking after initial anchor
- Content anchored to head moves with the wearer's head position

### Tracking Modes

```swift
// Use predicted tracking for smoother updates
let anchoringComponent = AnchoringComponent(
    target,
    trackingMode: .predicted
)

// Use precise tracking for accuracy
let anchoringComponent = AnchoringComponent(
    target,
    trackingMode: .precise
)
```

### Physics Simulation Space

```swift
// Specify physics simulation space
let anchoringComponent = AnchoringComponent(
    target,
    trackingMode: .predicted,
    physicsSimulation: .entity
)
```

## Key Properties

- `target: AnchoringComponent.Target` - The real world anchor target
- `trackingMode: AnchoringComponent.TrackingMode` - How the entity tracks its target
- `physicsSimulation: AnchoringComponent.PhysicsSimulation` - Physics simulation space

## Anchor Targets

- `.world(transform: simd_float4x4?)` - World origin or custom transform
- `.plane(.horizontal/.vertical, classification, minimumBounds)` - Detected planes
- `.image(group:name:physicalWidth:)` - Tracked images
- `.object(group:name:)` - Tracked 3D objects
- `.hand(.left/.right, location:)` - Hand tracking locations
- `.face(anchor:)` - Face tracking
- `.head` - Center of wearer's head (immersive spaces only, no authorization required)

## Important Notes

- The entity with `AnchoringComponent` is inactive when created
- RealityKit anchors and activates the entity when it finds a matching anchor
- Use `AnchoredStateChanged` events to monitor anchor status
- RealityKit unanchors the entity if the target disappears
- Check anchor status using scene events

## Best Practices

- Use `.predicted` tracking mode for smoother updates
- Use `.precise` tracking mode when accuracy is critical
- Monitor `AnchoredStateChanged` events to handle anchor lifecycle
- Provide fallback behavior when anchors are lost
- Use appropriate minimum bounds for plane anchors
- Combine with `ARKitAnchorComponent` to access underlying ARKit anchor

## Related Components

- `ARKitAnchorComponent` - Access the backing ARKit anchor
- `SceneUnderstandingComponent` - Access scene understanding data
- `CollisionComponent` - For interactive anchored entities
