# ComputeGraph (GPU Particles and Simulation)


## Overview

`ComputeGraph` is a GPU compute-node-graph framework: you assemble a graph of
compute nodes (built-in expression/math nodes or kernels from your own Metal
libraries), compile it into pipelines, and run it as a simulation of "elements"
(particles). A RealityKit bridge binds graph outputs to `ModelComponent`s and
materials so results render in a scene. This is the new GPU particle and
simulation engine; `ParticleEmitterComponent` is unchanged and remains the
simple CPU-configured option. New in visionOS 27. Also on iOS, macOS,
macCatalyst, and tvOS 27.

Importing both `RealityKit` and `ComputeGraph` activates the cross-import
overlay that provides the ECS types (`ComputeGraphComponent` and friends).

## When to Use

- Large-scale GPU particle systems beyond `ParticleEmitterComponent`
- Custom per-element simulation logic written as Metal compute kernels
- Authored compute-graph effect files loaded at runtime
- Reading simulation output buffers back for gameplay logic

## How to Use

### Load an Authored Graph into a Scene

```swift
import RealityKit
import ComputeGraph

let resource = try await ComputeGraphResource(
    contentsOf: url, bundle: nil)
var component = ComputeGraphComponent(resource: resource)
component.state = .playing
entity.components.set(component)
```

### Control Playback and Spawn Elements

```swift
component.play()                 // also: pause(), step(), fastForward()
component.spawn(element: ElementSpawnParameters(
    position: [0, 1, 0],
    velocity: [0, 0.5, 0],
    lifetime: 2.0))
component.setUniformValue(Float(0.5), named: "intensity")
component.setTexture(myTexture, at: 0)
```

`ElementSpawnParameters(position:velocity:size:color:lifetime:)` defaults:
`velocity: .zero`, `size: [0.01, 0.01]`, `color: [1, 1, 1, 1]`,
`lifetime: 1.0`.

### Build a Graph Programmatically

```swift
var graph = ComputeNodeGraph()
let library = ComputeNodeGraph.Library.shared
// Or bring your own kernels:
// let library = ComputeNodeGraph.Library(from: mtlLibrary,
//                                        bundleIdentifier: "com.example.fx")
if let def = library.definition(named: "myKernel", in: nil) {
    let id = try graph.addNode(ComputeNodeGraph.Node(definition: def))
    _ = id
}
let pipelines = try await ComputeNodeGraph.Pipelines(graph)

var deps = ComputeGraphResource.Dependencies()
deps.outputModels = [:]      // [NodeID: ModelComponent]
deps.outputMaterials = [:]   // [NodeID: any Material]
let resource = try ComputeGraphResource(
    graph: graph, pipelines: pipelines, dependencies: deps)
```

Edges connect `Port.Address(node:index:)` pairs via
`graph.addEdge(_:)` / `canAddEdge(_:)` / `removeEdge(_:)`, or set everything at
once with `replaceAll(nodes:edges:)`. Node inputs are set with
`node.setInput(_:_:)`. `Pipelines(descriptor:)` compiles from a
`PipelinesDescriptor(assembly:)` when you need `options` (`debugDraw`) or extra
libraries (`addLibrary(_:bundle:)`).

### Drive a Simulation Manually (No ECS)

```swift
let simulation = ComputeGraphSimulation(pipelines: pipelines,
                                        commandQueue: queue)
simulation.spawn(elements: [ElementSpawnParameters(position: .zero)],
                 in: nil, using: encoder)
simulation.advance(.init(deltaTime: 1 / 90,
                         commandBuffer: commandBuffer,
                         computeEncoder: encoder))
```

`AdvanceParams` also takes `localToWorld`, `worldToLocal`, `viewPosition`, and
`viewDirection`. Other controls: `fastForward()`,
`fastForward(stepCount:stepDeltaTime:)`, `reset(encoder:)`,
`setUniform(_:named:)`, `setBuffer`/`setTexture`, `setUserResources(_:)`,
`setOutputEnabled(_:enabled:)`, `resetRandomSeeds(using:)`, `simulationRate`.

## Key Types

- `ComputeNodeGraph` - nodes, edges, ports; `Library` of `NodeDefinition`s
- `ComputeNodeGraph.Pipelines` - compiled pipelines (async or sync init)
- `ComputeGraphSimulation` - low-level advance/spawn/uniform API
- `ComputeGraphResource` - loadable asset; `Dependencies` binds output
  `ModelComponent`s, materials, textures, and `BufferInfo` buffers by node/port
- `ComputeGraphComponent` - ECS component: `resource`, `pipelines`, `state`
  (`.playing`/`.paused`/`.stepping`), `models`, `materials`, `randomSeed`,
  play/pause/step/fastForward, spawn, uniform/texture/buffer setters
- `ComputeGraphRuntimeComponent` - transient; exposes the live `simulation`
  and `readOutput(_:)` / `readOutputs(_:)` for output `MTLBuffer`s
- `ComputeGraphOutputComponent` - transient marker on output entities
  (`outputID`)
- `ComputeGraphSharedUniforms` - per-entity uniform injection via
  `setUniform(_:)` / `setUniformTransform(_:)`
- `ComputeGraphViewpointComponent` - override `viewPosition`/`viewDirection`
- Enums: `Topology` (`.point`, `.triangle`, `.quad`, `.octagon`, `.strip`,
  `.instances`), `Sorting`, `ElementGrouping`, `CoordinateSpace`,
  `StandardLibraryFunction` (large math node vocabulary)

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- `ComputeGraphResource(graph:pipelines:dependencies:)` is `@MainActor` and
  `throws`; prefer the async `Pipelines` initializers off the main actor.
- Custom kernels come from your own `MTLLibrary` registered through
  `ComputeNodeGraph.Library`; `Library.shared` holds the built-in nodes.
- Authored graph files imply tooling support; loading via
  `ComputeGraphResource(contentsOf:bundle:)` is the stable path.

## Related Components

- `ParticleEmitterComponent` - simpler, CPU-configured particles
- `ModelComponent` - bound as graph output for rendering
- `TransientComponent` - the runtime/output components are transient
