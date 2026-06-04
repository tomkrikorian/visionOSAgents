# GestureComponent

Use this file when attaching a SwiftUI gesture directly to a RealityKit entity
through Apple's `RealityKit.GestureComponent`.

## Overview

`GestureComponent` is a RealityKit `Component` that attaches a UI gesture to an
entity.

Use it when the interaction is entity-scoped and the built-in
`ManipulationComponent` behavior is not the right fit. For full drag, rotate,
scale, hover, and direct-manipulation behavior, try `ManipulationComponent`
first.

## Basic Setup

```swift
import RealityKit
import SwiftUI

let gesture = TapGesture().onEnded {
    // Update entity-owned or model-owned state.
}

entity.components.set(GestureComponent(gesture))
```

## Required Interaction Setup

Entity gestures still need a hittable target:

```swift
entity.components.set(InputTargetComponent())
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))
entity.components.set(GestureComponent(TapGesture().onEnded {
    // Handle the tap.
}))
```

## Decision Rules

- Use `GestureComponent` when the gesture should travel with the RealityKit
  entity as component state.
- For the broader choice between SwiftUI gestures, targeted gestures, and
  manipulation APIs, load
  [`interaction.md`](../../spatial-swiftui-developer/references/interaction.md)
  or [`component-selection.md`](component-selection.md).

## Guardrails

- Keep gesture side effects on the main actor when mutating UI or observable
  model state.
- Keep continuous or multi-entity behavior in a `System` instead of stuffing it
  into gesture closures.
- Do not confuse Apple's `RealityKit.GestureComponent` with app-defined wrapper
  types that may use the same name.
