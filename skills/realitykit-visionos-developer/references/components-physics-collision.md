# Physics and Collision Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## CollisionComponent
Goal: Defines collision shapes for an entity.

```swift
let shapes: [ShapeResource] = [.generateBox(size: [0.1, 0.1, 0.1])]
entity.components.set(CollisionComponent(shapes: shapes))
```

## PhysicsBodyComponent
Goal: Adds mass and physical behavior to an entity.

```swift
var body = PhysicsBodyComponent()
body.mode = .dynamic
entity.components.set(body)
```

## PhysicsMotionComponent
Goal: Controls linear and angular velocity.

```swift
var motion = PhysicsMotionComponent()
motion.linearVelocity = [0, 0, 0]
entity.components.set(motion)
```

## PhysicsSimulationComponent
Goal: Configures simulation parameters for physics.

```swift
entity.components.set(PhysicsSimulationComponent())
```

## ParticleEmitterComponent
Goal: Emits particle effects from an entity.

```swift
entity.components.set(ParticleEmitterComponent())
```

## ForceEffectComponent
Goal: Applies force fields to physics bodies.

```swift
entity.components.set(ForceEffectComponent())
```

## PhysicsJointsComponent
Goal: Creates joints between physics bodies.

```swift
let joints = PhysicsJointsComponent(joints: <#Joints#>)
entity.components.set(joints)
```

## GeometricPinsComponent
Goal: Defines geometric attachment points for entities.

```swift
entity.components.set(GeometricPinsComponent())
```
