# SynchronizationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/synchronizationcomponent)

## Overview

A component that enables or influences how entities are synchronized across devices or sessions in RealityKit. It's part of RealityKit's synchronization service that allows entities to automatically replicate state changes across participants in a shared session, enabling collaborative AR and multi-user experiences.

## When to Use

- Creating collaborative AR or multi-user experiences
- Synchronizing entity state across multiple devices
- Implementing shared spatial experiences
- Replicating entity transforms and components across network
- Building multiplayer or shared reality experiences
- Enabling state synchronization in networked sessions

## How to Use

### Basic Setup

```swift
import RealityKit

// Mark entity for synchronization
let syncComponent = SynchronizationComponent()
entity.components.set(syncComponent)
```

### With Collaboration Enabled

```swift
// Enable collaboration in AR session configuration
let configuration = ARWorldTrackingConfiguration()
configuration.isCollaborationEnabled = true
arView.session.run(configuration)

// Mark entities for synchronization
let sharedEntity = Entity()
sharedEntity.components.set(SynchronizationComponent())
scene.addChild(sharedEntity)
```

### Synchronized Entity Updates

```swift
// Entities with SynchronizationComponent automatically sync
// State changes are replicated across participants
let entity = Entity()
entity.components.set(SynchronizationComponent())

// Transform and component changes will sync automatically
entity.position = newPosition
entity.components.set(newComponent)
```

## Key Properties

- Properties may include synchronization configuration, ownership, or sync settings
- Consult official documentation for specific API details

## Important Notes

- Requires collaboration to be enabled in AR session configuration
- Works with RealityKit's `scene.synchronizationService`
- Entities with this component automatically replicate state changes
- State changes (transforms, components) are synchronized across participants
- Available on visionOS, iOS, and other Apple platforms
- Works with MultipeerConnectivity or other networking frameworks

## Best Practices

- Enable collaboration in AR session configuration
- Mark entities that should be shared with `SynchronizationComponent`
- Use `TransientComponent` for local-only entities that shouldn't sync
- Test synchronization behavior in multi-user scenarios
- Consider network performance when synchronizing many entities
- Handle synchronization errors and network disconnections gracefully
- Use appropriate sync frequency for your use case

## Related Components

- `TransientComponent` - Opposite - marks entities that shouldn't sync
- `AnchoringComponent` - Anchored entities may need synchronization
- `PhysicsBodyComponent` - Physics bodies can be synchronized

