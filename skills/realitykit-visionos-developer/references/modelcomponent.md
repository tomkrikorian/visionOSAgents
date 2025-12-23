# ModelComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/modelcomponent)

## Overview

A component that contains a mesh and materials for the visual appearance of an entity. This component is foundational for all visual content in RealityKit. Use `ModelComponent` to render 3D models by attaching it to any `Entity` in your RealityKit scene.

## When to Use

- Rendering any 3D geometry in your scene
- Displaying loaded USDZ or Reality files
- Creating primitive shapes (boxes, spheres, cylinders, etc.)
- Applying materials to visual entities

## How to Use

### Basic Setup

```swift
import RealityKit

// Create a simple blue, metallic box
let mesh = MeshResource.generateBox(size: 1, cornerRadius: 0.05)
let material = SimpleMaterial(color: .blue, isMetallic: true)
let modelComponent = ModelComponent(mesh: mesh, materials: [material])

let entity = Entity()
entity.components.set(modelComponent)
```

### Loading from Assets

```swift
// Load a USDZ or Reality file
let entity = try await Entity(named: "MyModel")
// The entity will already have a ModelComponent if the asset contains geometry
```

### Multiple Materials

```swift
// For meshes with multiple submeshes, provide multiple materials
let mesh = MeshResource.generateBox(size: 1)
let material1 = SimpleMaterial(color: .red, isMetallic: false)
let material2 = SimpleMaterial(color: .blue, isMetallic: true)
let modelComponent = ModelComponent(mesh: mesh, materials: [material1, material2])
```

### Real-World Example: Creating a Starfield

This example from the Hello World sample shows how to create a large sphere with a texture for a starfield background:

```swift
import RealityKit

RealityView { content in
    // Create a material with a star field texture
    guard let resource = try? await TextureResource(named: "Starfield") else {
        fatalError("Unable to load starfield texture.")
    }
    var material = UnlitMaterial()
    material.color = .init(texture: .init(resource))

    // Attach the material to a large sphere
    let entity = Entity()
    entity.components.set(ModelComponent(
        mesh: .generateSphere(radius: 1000),
        materials: [material]
    ))

    // Ensure the texture image points inward at the viewer
    entity.scale *= .init(x: -1, y: 1, z: 1)

    content.add(entity)
}
```

### Real-World Example: Dynamic Mesh Updates

This example shows how to update a ModelComponent's mesh dynamically (from TraceSystem):

```swift
// Update an existing model's mesh
if let model = trace.model {
    try model.model?.mesh.replace(with: newMeshContents)
} else {
    // Create a new model entity with the mesh
    let model = try ModelEntity.makeTraceModel(with: meshContents)
    entity.components.set(ModelComponent(mesh: meshContents, materials: [material]))
}
```

## Key Properties

- `mesh: MeshResource` - The mesh that defines the model's shape
- `materials: [Material]` - The materials that define the model's visual appearance
- `boundsMargin: Float` - A margin applied to an entity's bounding box that determines object visibility

## Best Practices

- Always provide at least one material when creating a ModelComponent
- Use `boundsMargin` to improve culling performance for large scenes
- Combine with `CollisionComponent` and `InputTargetComponent` for interactive entities
- Load complex models asynchronously to avoid blocking the main actor

## Related Components

- `CollisionComponent` - For interactive entities
- `PhysicsBodyComponent` - For physics simulation
- `OpacityComponent` - For transparency effects
- `ModelSortGroupComponent` - For controlling draw order
