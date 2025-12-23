# ForceEffectComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/forceeffectcomponent)

## Overview

A component that allows you to attach one or more force effects to an entity. These effects continuously apply physics-based forces to physics bodies within a defined volume. Force effects can be built-in (like gravity wells, vortices, drag, or turbulence) or custom implementations that apply forces based on position, distance, or other parameters.

## When to Use

- Creating gravity wells or attraction/repulsion effects
- Implementing vortex effects that make bodies circulate around an axis
- Applying drag forces to slow down moving bodies
- Creating turbulence effects with random forces
- Implementing custom force fields (explosions, magnetic fields, etc.)
- Applying area-of-effect forces to multiple physics bodies

## How to Use

### Custom Force Effect Implementation

```swift
import RealityKit

// Define a custom force effect
struct Gravity: ForceEffectProtocol {
    var parameterTypes: PhysicsBodyParameterTypes { [.position, .distance] }
    var forceMode: ForceMode = .force

    func update(parameters: inout ForceEffectParameters) {
        guard let positions = parameters.positions,
              let distances = parameters.distances else { return }
        
        for i in 0..<parameters.physicsBodyCount {
            let pos = positions[i]
            let dist = distances[i]
            // Compute force vector toward center, magnitude depends on distance
            let forceVec = computeForce(distance: dist, position: pos)
            parameters.setForce(forceVec, index: i)
        }
    }
    
    func computeForce(distance: Float, position: SIMD3<Float>) -> SIMD3<Float> {
        // Force toward center, inverse square law
        let direction = -normalize(position)
        let magnitude = 9.8 / (distance * distance)
        return direction * magnitude
    }
}

// Create force effect with spatial falloff and mask
let gravityEffect = ForceEffect(
    effect: Gravity(),
    spatialFalloff: .sphere(radius: 8.0),
    mask: .asteroids  // Only affect entities matching bitmask
)

// Attach to entity
planetEntity.components.set(ForceEffectComponent(effects: [gravityEffect]))
```

### Built-in Force Effects

```swift
// Constant radial effect (pushes/pulls uniformly)
let radialEffect = ForceEffect(
    effect: ConstantRadialForce(direction: .outward, strength: 10.0),
    spatialFalloff: .sphere(radius: 5.0)
)

// Vortex effect (makes bodies circulate around axis)
let vortexEffect = ForceEffect(
    effect: VortexForce(axis: [0, 1, 0], strength: 5.0),
    spatialFalloff: .sphere(radius: 3.0)
)

// Drag effect (slows down moving bodies)
let dragEffect = ForceEffect(
    effect: DragForce(strength: 2.0),
    spatialFalloff: .sphere(radius: 10.0)
)

// Turbulence effect (random forces)
let turbulenceEffect = ForceEffect(
    effect: TurbulenceForce(strength: 1.0),
    spatialFalloff: .sphere(radius: 5.0)
)

entity.components.set(ForceEffectComponent(effects: [radialEffect, vortexEffect]))
```

### Multiple Force Effects

```swift
// Combine multiple force effects
let effects = [
    ForceEffect(effect: Gravity(), spatialFalloff: .sphere(radius: 8.0)),
    ForceEffect(effect: DragForce(strength: 1.0), spatialFalloff: .sphere(radius: 10.0))
]

entity.components.set(ForceEffectComponent(effects: effects))
```

## Key Properties

- `effects: [ForceEffect]` - Array of force effects to apply

### ForceEffect Properties

- `effect: ForceEffectProtocol` - The force effect implementation (built-in or custom)
- `spatialFalloff: SpatialForceFalloff` - The bounds/volume of influence (e.g., `.sphere(radius:)`)
- `mask: UInt32` - Bitmask to filter which physics bodies are affected

### ForceEffectProtocol Requirements

- `parameterTypes: PhysicsBodyParameterTypes` - Which physics body parameters are needed
- `forceMode: ForceMode` - How the computed vector should be interpreted (e.g., `.force`)
- `update(parameters:)` - The logic computing the effect per physics body

## Important Notes

- Force effects only work on entities with `PhysicsBodyComponent`
- Bodies must be `.dynamic` (not `.static`) to respond to force effects
- Effects are applied continuously each physics simulation step
- Spatial falloff defines the volume of influence - bodies outside are unaffected
- Use bitmasks to filter which entities are affected by the force
- Custom force effects can use position, distance, velocity, and other physics body parameters
- Available on visionOS, iOS, and other Apple platforms (introduced in WWDC 2024)

## Best Practices

- Use spatial falloff to limit the area of effect and improve performance
- Use bitmasks to selectively affect only relevant entities
- Start with built-in force effects before creating custom ones
- Test force magnitudes to avoid instability or unrealistic behavior
- Combine multiple force effects for complex behaviors (e.g., gravity + drag)
- Consider performance when applying forces to many physics bodies
- Use appropriate spatial falloff shapes (sphere, box, etc.) for your use case

## Related Components

- `PhysicsBodyComponent` - Required on entities that should respond to force effects
- `PhysicsMotionComponent` - Can be used to set initial velocity for orbiting objects
- `CollisionComponent` - Entities with force effects typically need collision
- `PhysicsSimulationComponent` - For configuring physics simulation parameters
