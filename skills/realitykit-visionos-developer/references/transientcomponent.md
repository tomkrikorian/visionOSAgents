# TransientComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/transientcomponent)

## Overview

A component that marks an entity as "transient"—temporary, non-persistent content that shouldn't remain anchored or synchronized across sessions. It signals the system to treat the entity differently regarding anchoring, persistence, or synchronization. Entities with this component are not expected to survive across anchor state changes or session interruptions.

## When to Use

- Marking temporary visual effects (particles, sparks, etc.)
- Creating ghost previews or temporary indicators
- Spawning temporary objects that shouldn't persist
- Creating non-synchronized local-only entities
- Marking entities that shouldn't be saved or restored
- Creating temporary UI or feedback elements

## How to Use

### Basic Setup

```swift
import RealityKit

// Mark entity as transient
let transientComponent = TransientComponent()
entity.components.set(transientComponent)
```

### Temporary Visual Effect

```swift
// Create temporary particle effect
let particleEffect = Entity()
particleEffect.components.set(ParticleEmitterComponent(...))
particleEffect.components.set(TransientComponent())  // Mark as transient
scene.addChild(particleEffect)

// Effect will be cleaned up automatically
```

### Non-Synchronized Entity

```swift
// Create local-only entity that shouldn't sync
let localIndicator = Entity()
localIndicator.components.set(ModelComponent(...))
localIndicator.components.set(TransientComponent())  // Won't sync across network
```

## Key Properties

- No configurable properties - the component itself marks the entity as transient

## Important Notes

- Entities with `TransientComponent` are not persisted across sessions
- Transient entities are not synchronized in multiplayer scenarios
- Transient entities don't survive anchor state changes
- Use for temporary content that should be cleaned up automatically
- Available on visionOS, iOS, and other Apple platforms
- Opposite of persistent entities that should be saved/restored

## Best Practices

- Use for temporary visual effects and feedback
- Mark local-only entities that shouldn't sync
- Use for preview or ghost entities
- Don't use for important content that needs to persist
- Combine with temporary effects (particles, animations)
- Let the system handle cleanup of transient entities

## Related Components

- `SynchronizationComponent` - Opposite - marks entities that should sync
- `ParticleEmitterComponent` - Often marked as transient for temporary effects
- `AnchoringComponent` - Transient entities typically don't need anchoring
