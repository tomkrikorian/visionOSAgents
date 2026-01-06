# Rendering and Appearance Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## ModelComponent
Goal: Defines the mesh and materials that render an entity.

```swift
let mesh = MeshResource.generateBox(size: 0.1)
let material = SimpleMaterial(color: .white, isMetallic: false)
entity.components.set(ModelComponent(mesh: mesh, materials: [material]))
```

## ModelSortGroupComponent
Goal: Controls draw order for models to reduce depth fighting.

```swift
entity.components.set(ModelSortGroupComponent())
```

## OpacityComponent
Goal: Applies a uniform opacity to the entity and its descendants.

```swift
var opacity = OpacityComponent()
opacity.opacity = 0.5
entity.components.set(opacity)
```

## AdaptiveResolutionComponent
Goal: Adjusts render resolution based on viewing distance.

```swift
entity.components.set(AdaptiveResolutionComponent())
```

## ModelDebugOptionsComponent
Goal: Enables debug rendering options for model visualization.

```swift
entity.components.set(ModelDebugOptionsComponent())
```

## MeshInstancesComponent
Goal: Renders many instances of a mesh efficiently.

```swift
let instances = MeshInstancesComponent(
    mesh: <#MeshResource#>,
    materials: <#Materials#>,
    instances: <#MeshInstanceCollection#>
)
entity.components.set(instances)
```

## BlendShapeWeightsComponent
Goal: Controls blend shape weights on a mesh for morph targets.

```swift
var weights = BlendShapeWeightsComponent()
weights.weights = <#BlendShapeWeights#>
entity.components.set(weights)
```
