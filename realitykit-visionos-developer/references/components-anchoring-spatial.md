# Anchoring and Spatial Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## AnchoringComponent
Goal: Anchors an entity to a world, plane, or image target.

```swift
let anchoring = AnchoringComponent(<#AnchorTarget#>)
entity.components.set(anchoring)
```

## ARKitAnchorComponent
Goal: Exposes the backing ARKit anchor for an entity.

```swift
if let arkit = entity.components[ARKitAnchorComponent.self] {
    _ = arkit
}
```

## SceneUnderstandingComponent
Goal: Accesses scene understanding data for an entity.

```swift
entity.components.set(SceneUnderstandingComponent())
```

## DockingRegionComponent
Goal: Defines regions where content can dock.

```swift
let docking = DockingRegionComponent(<#DockingRegion#>)
entity.components.set(docking)
```

## ReferenceComponent
Goal: References an external entity asset for lazy loading.

```swift
let reference = ReferenceComponent(<#Reference#>)
entity.components.set(reference)
```

## AttachedTransformComponent
Goal: Attaches an entity transform to another entity.

```swift
entity.components.set(AttachedTransformComponent())
```
