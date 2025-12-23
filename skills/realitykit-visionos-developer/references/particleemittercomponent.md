# ParticleEmitterComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/particleemittercomponent)

## Overview

A component that generates particle systems—tiny visual elements like sparks, smoke, fire, rain, etc.—attached to entities in a scene. Particle emitters create visual effects by spawning many small particles that can have various properties like color, velocity, lifespan, and billboard behavior.

## When to Use

- Creating visual effects (sparks, smoke, fire, explosions)
- Implementing particle-based effects (rain, snow, debris)
- Adding atmospheric effects to scenes
- Creating dynamic visual feedback
- Implementing particle-based animations
- Adding visual polish to interactions

## How to Use

### Basic Setup

```swift
import RealityKit

// Create particle emitter
var emitter = ParticleEmitterComponent.ParticleEmitter()

// Configure particle properties
emitter.color = .constant(.single(.red))
emitter.lifeSpan = 2.0  // Particles live for 2 seconds
emitter.billboardMode = .viewPlaneAligned  // Face the camera

let component = ParticleEmitterComponent(emitter: emitter)
entity.components.set(component)
```

### Spark Effect

```swift
var sparkEmitter = ParticleEmitterComponent.ParticleEmitter()
sparkEmitter.color = .constant(.single(.yellow))
sparkEmitter.lifeSpan = 0.5
sparkEmitter.spawnSpreadFactor = 0.3
sparkEmitter.radialAmount = 5.0
sparkEmitter.burstCountVariation = 10

let component = ParticleEmitterComponent(emitter: sparkEmitter)
entity.components.set(component)
```

### Smoke Effect

```swift
var smokeEmitter = ParticleEmitterComponent.ParticleEmitter()
smokeEmitter.color = .constant(.single(.gray))
smokeEmitter.lifeSpan = 3.0
smokeEmitter.spawnSpreadFactor = 0.1
smokeEmitter.radialAmount = 2.0
smokeEmitter.billboardMode = .viewPlaneAligned

let component = ParticleEmitterComponent(emitter: smokeEmitter)
entity.components.set(component)
```

## Key Properties

### ParticleEmitter Properties

- `color: ParticleColor` - Particle color (e.g., `.constant(.single(.red))`)
- `lifeSpan: Float` - How long each particle lives before disappearing
- `billboardMode: BillboardMode` - How particles are oriented (e.g., `.viewPlaneAligned`)
- `spawnSpreadFactor: Float` - How much particles spread out spatially when spawned
- `radialAmount: Float` - How strongly particles spread radially from emission origin
- `burstCountVariation: Int` - Randomness in number of particles when emitter bursts fire
- `sortOrder: SortOrder` - Rendering order among particles and other scene elements

## Important Notes

- Particles are attached to an entity and inherit transforms
- Some versions may have offset issues from the parent entity
- Particle properties can be constants, curves, or enums depending on the effect
- Available on visionOS, iOS, and other Apple platforms
- Particle systems can impact performance - use judiciously

## Best Practices

- Configure particle properties to match your desired effect
- Use appropriate `lifeSpan` values for particle duration
- Set `billboardMode` for desired particle orientation
- Adjust `spawnSpreadFactor` and `radialAmount` for emission patterns
- Consider performance when using many particle emitters
- Test particle effects on target devices
- Use `sortOrder` to control rendering order if needed

## Related Components

- `ModelComponent` - Entities with particle emitters typically have models
- `PhysicsBodyComponent` - For particles that need physics interaction
- `TransientComponent` - For temporary particle effects
