# Navigation Meshes and Behavior Trees


## Overview

Game-AI building blocks: `NavigationMeshResource` bakes a walkable navmesh
from scene geometry, `NavigationComponent` + `NavigationController` run async
pathfinding over it, and `BehaviorTreeResource` + `BehaviorTreeComponent` run
data-driven behavior trees that can trigger custom entity actions. New in
visionOS 27. Also on iOS, macOS, macCatalyst, and tvOS 27.

## When to Use

- NPC or agent movement across walkable surfaces
- Path queries with area costs (water, mud) and flag filtering
- Off-mesh links (jumps, ladders, teleporters)
- Authored AI logic with reusable, swappable behavior trees

## How to Use

### Build a Navigation Mesh

```swift
import RealityKit

let config = NavigationMeshResource.Configuration(
    cellSize: 0.05, cellHeight: 0.05,
    walkableSlopeAngle: 45,
    characterHeight: 1.8, walkableClimb: 0.3, characterRadius: 0.3)

let navMesh = try await NavigationMeshResource(
    mesh: levelMesh, configuration: config)
levelEntity.components.set(NavigationMeshComponent(navigationMeshes: [navMesh]))
```

Other inits: `(triangleIndices:vertices:offMeshConnections:configuration:)`,
`(meshDescriptor:offMeshConnections:configuration:)`, prebaked
`(named:in:)` bundle loading, and a raw-polygon init taking `areas`, `flags`,
and `HeightData`. `Configuration` also exposes `maximumEdgeLength`,
`maximumSimplificationError`, `minimumCellsPerRegion`,
`minimumCellsToMergeRegions`, `detailSampleDistance`,
`detailSampleMaximumError`, `maximumVerticesPerPolygon`, and `partitionMethod`
(`.watershed`, `.monotone`, `.layer`).

### Areas, Flags, Off-Mesh Connections

```swift
let water = NavigationMeshResource.Area(1)
navMesh.markAreaInBox(boundingBox: pondBounds, area: water)

let jump = NavigationMeshResource.OffMeshConnection(
    startPoint: [0, 0, 0], endPoint: [0, 0, 2], radius: 0.3)
// Pass off-mesh connections at bake time via offMeshConnections:.
```

Mark/remove helpers exist for cylinders, boxes, polygons, and off-mesh
connections, for both `Area` and `Flag`. `Layer` partitions multiple navmeshes;
`NavigationComponent(layer:)` selects one.

### Pathfind

```swift
var filter = NavigationComponent.Filter()
filter.areaCosts = [water: 10.0]
agent.components.set(NavigationComponent(layer: nil, filter: filter))

let controller = try NavigationController(entity: agent)
if let path = await controller.computePath(to: goalPosition) {
    for node in path {
        // node.position, node.category (.meshPoint / .offMeshConnection)
    }
}
```

Fire-and-forget alternative: `requestPath(to:)` / `requestPath(from:to:)`,
then poll `pathfindStatus` (`.none`, `.inProgress`, `.failed`, `.succeeded`)
and read `currentPath`. `stopPathfind()` cancels.

### Behavior Trees

```swift
let errors = BehaviorTreeResource.validate(definition: data)
guard errors.isEmpty else { return }
let tree = try BehaviorTreeResource(definition: data)
entity.components.set(BehaviorTreeComponent(
    behaviorTree: tree,
    availableBehaviorTrees: ["patrol": tree]))
```

`definition` is authored tree data; `parameterNames` lists tree parameters.
`availableBehaviorTrees` holds named trees to swap into `behaviorTree`.

Custom leaf actions conform to `BehaviorTreeAction` (an `EntityAction`).
Handle them with `BehaviorTreeActionHandler` (implement
`actionStartedWithResult` / `actionUpdatedWithResult` / etc., returning
`ActionResult` `.running`, `.success`, or `.failure`) or via the closure
subscription:

```swift
MyAction.subscribe(to: .updated) { event -> ActionResult in
    guard let entity = event.entity else { return .failure }
    // drive the entity, e.g. step along a NavigationController path
    return .running
}
```

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- Baking is expensive - prefer the `async` initializers or ship prebaked
  meshes loaded with `init(named:in:)`.
- `NavigationController(entity:)` throws if the entity is not set up for
  navigation; keep a `NavigationComponent` on the agent.
- `computePath` returns positions only; moving the entity along the path is
  your code (custom `System` or `CharacterControllerComponent`).

## Related Components

- `CharacterControllerComponent` - move agents along computed paths
- `SceneUnderstandingComponent` - real-world geometry as pathfinding input
- `AnimationGraphComponent` - drive locomotion states from behavior trees
- [`custom-systems.md`](../../realitykit-ecs-systems/references/custom-systems.md)
  - per-frame agent steering
