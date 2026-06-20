# Cloth Simulation


## Overview

A real-time cloth simulation system built from dedicated components: a
`ClothSimulationComponent` that owns solver and environment settings, one or
more `ClothBodyComponent` entities carrying simulated meshes, and
`ClothColliderComponent` entities the cloth collides against. Force volumes,
query volumes, and grab support round out the system. New in visionOS 27.
Also available on iOS, macOS, and macCatalyst 27; unavailable on tvOS.

## When to Use

- Simulating flags, curtains, capes, clothing, or banners
- Inflatable shapes via the inflation constraint
- Wind- or force-driven soft surfaces
- Letting users grab and pull cloth interactively
- Querying which cloth bodies enter a region of space

## How to Use

### Basic Setup

```swift
import RealityKit

// Solver + environment on a simulation entity
var simulation = ClothSimulationComponent(solver: .gaussSeidel(iterationCount: 4))
simulation.gravity = [0, -9.8, 0]
simulation.wind = [0.5, 0, 0]
simulationEntity.components.set(simulation)

// A cloth patch body
let mesh = try ClothMeshResource.patch(size: [1, 1])
var body = ClothBodyComponent(mesh: mesh)
body.mass = 0.2
clothEntity.components.set(body)

// A collider the cloth drapes over
let collider = ClothColliderComponent(shape: .sphere(ClothSphereShape(radius: 0.3)))
colliderEntity.components.set(collider)
```

### Cloth Meshes and Draping

`ClothMeshResource` provides generators and conversions (all `throws`):
`patch(size:targetEdgeLength:)`, `box(size:targetEdgeLength:)`,
`sphere(radius:targetEdgeLength:)`, `capsule(height:radius:targetEdgeLength:)`,
`cylinder(height:radius:withCaps:targetEdgeLength:)`,
`init(positions:triangleIndices:)`, and `init(from: MeshResource)`.
`MeshResource(from: ClothMeshResource)` converts back for rendering.
`ClothPoseResource(positions:)` supplies a pre-draped start pose via
`ClothBodyComponent(mesh:meshDraping:)`.

### Pinning, Forces, and Inflation

```swift
// Pin vertices near the top edge kinematically
let pinned = mesh.vertices(in: .box(ClothBoxShape(size: [1.1, 0.1, 1.1])),
                           center: [0, 0.5, 0])
body.motionTypes.set(vertexIndices: pinned, value: .kinematic)

// Inflate a watertight mesh toward a target volume
body.inflationConstraint = .init(targetVolume: 0.5, stiffness: 1.0)
```

`ClothForceVolumeComponent(shape:)` applies `constantForce`, `windForce`,
`noiseFrequency`, `noiseAmplitude`, and `falloffStart` inside a
`ClothVolumeShape` (`.plane`, `.sphere`, `.box`, `.roundedBox`, `.capsule`).
`ClothQueryVolumeComponent(shape:)` reports bodies intersecting the volume and
exposes `queryEntities`.

### Grabbing

```swift
var grab = ClothGrabComponent(mode: .ray)   // or .volume(shape:)
grab.isGrabbing = true                      // toggle from your gesture handling
grabEntity.components.set(grab)
```

`falloff` (`.enabled` / `.disabled`) softens the grab influence.

## Key Properties

### ClothSimulationComponent

- `gravity`, `wind: SIMD3<Float>` - environment forces
- `solver` - `.gaussSeidel(iterationCount:)` or `.jacobi(iterationCount:)`
- `dampingFactor: Float`, `timeStep: Float`
- `speedLimit` - `.unlimited` / `.automatic`
- `maximumStepsPerUpdate` - `.automatic` / `.fixed(steps:)`
- `meshCollidersUpdateInterval: Int` - how often mesh colliders refresh
- `targetClock: CMClockOrTimebase` - drive the simulation clock
- `materials`, `frictionOverrides` - named `ClothBodyMaterial` /
  `ClothColliderMaterial` lookup plus per-pair friction overrides

### ClothBodyComponent

- `mesh`, `initialMeshDraping`, `visualMesh: LowLevelMesh?`, `visualMeshWeights`
- `mass: Float`, `materialNames: [String]`
- `motionTypes` - per-vertex `.dynamic` / `.kinematic`
- `externalForces`, `collisionFilters` - per-vertex data
- `colliderBinding`, `targetShapes`, `inflationConstraint`
- `static resetDeformation(entity:)` - reset a body to its rest state

### ClothColliderComponent

- `shape: ClothColliderShape` - `.plane`, `.sphere`, `.box`, `.roundedBox`,
  `.capsule`, `.mesh`; shape structs: `ClothPlaneShape(normal:bias:)`,
  `ClothSphereShape(radius:)`, `ClothBoxShape(size:)`,
  `ClothRoundedBoxShape(size:edgeRadius:)`, `ClothCapsuleShape(height:radius:)`,
  `ClothMeshShape(mesh:bias:)`
- `isCollisionResponseEnabled`, `collisionFilter`, `materialNames`

## Events

Subscribe via `scene.subscribe(to:)` like other RealityKit events:

- `ClothSimulationEvents.Start` / `.BeforeUpdate` / `.AfterUpdate` -
  `simulationEntity`, `deltaTime`, `updateCount`
- `ClothBodyEvents.NewSimulationPositions` - `bodyEntity`, `updateCount`
- `ClothColliderEvents.NewBodyCollisions` - `colliderEntity` plus per-body
  `Collision` records
- `ClothQueryVolumeEvents.NewBodyIntersections` - `queryVolumeEntity`

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- Resource initializers (`ClothMeshResource`, `ClothPoseResource`) are
  `@MainActor` and `throws`.
- `inflationConstraint` needs a watertight mesh; check
  `ClothMeshResource.isWatertight` and `volume`.
- Lower `targetEdgeLength` raises vertex count and solver cost; tune iteration
  count and `maximumStepsPerUpdate` on device.

## Related Components

- `PhysicsBodyComponent` - rigid-body physics; cloth uses its own solver
- `ParticleEmitterComponent` - visual-only particle effects
- `MeshDeformerComponent` - non-simulated GPU mesh deformation
