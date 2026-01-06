# User Interaction Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## InputTargetComponent
Goal: Enables the entity to receive input events.

```swift
entity.components.set(InputTargetComponent())
```

## ManipulationComponent
Goal: Provides built-in translation, rotation, and scale interactions.

```swift
entity.components.set(ManipulationComponent())
```

## GestureComponent
Goal: Attaches custom gesture handling to an entity.

```swift
entity.components.set(GestureComponent())
```

## HoverEffectComponent
Goal: Adds focus and hover feedback when the user looks at an entity.

```swift
entity.components.set(HoverEffectComponent())
```

## AccessibilityComponent
Goal: Supplies accessibility metadata for assistive technologies.

```swift
entity.components.set(AccessibilityComponent())
```

## BillboardComponent
Goal: Keeps the entity oriented toward the viewer.

```swift
entity.components.set(BillboardComponent())
```
