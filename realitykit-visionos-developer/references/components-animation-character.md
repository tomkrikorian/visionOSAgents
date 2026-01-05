# Animation and Character Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## AnimationLibraryComponent
Goal: Stores multiple animations on an entity.

```swift
let library = AnimationLibraryComponent(animations: <#AnimationResources#>)
entity.components.set(library)
```

## CharacterControllerComponent
Goal: Adds character movement and physics behavior.

```swift
entity.components.set(CharacterControllerComponent())
```

## CharacterControllerStateComponent
Goal: Stores runtime state for a character controller.

```swift
entity.components.set(CharacterControllerStateComponent())
```

## SkeletalPosesComponent
Goal: Provides skeletal pose data for animation.

```swift
entity.components.set(SkeletalPosesComponent())
```

## IKComponent
Goal: Enables inverse kinematics for procedural animation.

```swift
entity.components.set(IKComponent())
```

## BodyTrackingComponent
Goal: Integrates body tracking data for an entity.

```swift
entity.components.set(BodyTrackingComponent())
```
