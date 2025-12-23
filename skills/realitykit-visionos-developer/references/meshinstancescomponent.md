# MeshInstancesComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/meshinstancescomponent)

## Overview

Renders many instances of a mesh efficiently. This component allows you to render multiple copies of the same mesh with different transforms, which is much more efficient than creating separate entities for each instance. Ideal for rendering crowds, forests, particle-like objects, or any scenario where you need many copies of the same geometry.

## When to Use

- Rendering many copies of the same mesh (trees, characters, objects)
- Creating particle-like effects with geometry
- Optimizing performance for repeated geometry
- Building crowds or large collections of objects
- Instancing geometry for performance

## How to Use

### Basic Setup

```swift
import RealityKit

// Create mesh instances component
let instances = MeshInstancesComponent(
    mesh: meshResource,
    materials: [material],
    instances: meshInstanceCollection
)
entity.components.set(instances)
```

### Creating Instance Collection

```swift
// Create a collection of instance transforms
var instanceCollection = MeshInstanceCollection()

// Add instances with different transforms
for i in 0..<100 {
    let transform = Transform(
        translation: [Float(i) * 0.5, 0, 0],
        rotation: .identity,
        scale: 1.0
    )
    instanceCollection.add(transform)
}

let instances = MeshInstancesComponent(
    mesh: meshResource,
    materials: [material],
    instances: instanceCollection
)
entity.components.set(instances)
```

## Key Properties

- `mesh: MeshResource` - The mesh to instance
- `materials: [Material]` - Materials to apply to instances
- `instances: MeshInstanceCollection` - Collection of instance transforms

## Important Notes

- Much more efficient than creating separate entities
- All instances share the same mesh and materials
- Each instance can have a different transform
- Ideal for static or infrequently updated instances

## Best Practices

- Use for rendering many copies of the same geometry
- Prefer over individual entities for performance
- Use appropriate instance counts for your target device
- Consider LOD (Level of Detail) for very large instance counts
- Update instance collections efficiently when needed

## Related Components

- `ModelComponent` - Alternative for single mesh rendering
- `MeshResource` - The mesh resource being instanced
