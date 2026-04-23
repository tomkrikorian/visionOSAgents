# File Layouts

Use this file when the app needs a proposed file or module shape.

## Layered Scene-First Shape

- `App/<AppName>App.swift`
- `Scenes/<Feature>Scene.swift`
- `Views/<Feature>RootView.swift`
- `Views/<Feature>DetailView.swift`
- `Models/*.swift`
- `Stores/*.swift`
- `Services/*.swift`
- `Support/*.swift`

Use this when the codebase is already layered or when multiple scenes share the
same services and models.

## Feature-Sliced Shape

- `App/<AppName>App.swift`
- `Scenes/MainWindowScene.swift`
- `Scenes/ImmersiveRootScene.swift`
- `Features/<Feature>/<Feature>View.swift`
- `Features/<Feature>/<Feature>Model.swift`
- `Reality/<Feature>RealityController.swift`

Use this when a spatial feature has strong ownership boundaries that deserve to
stay together.

## Mixed Surface Feature Shape

- `Scenes/<Feature>WindowScene.swift`
- `Scenes/<Feature>VolumeScene.swift`
- `Scenes/<Feature>ImmersiveScene.swift`
- `Features/<Feature>/<Feature>Coordinator.swift`
- `Features/<Feature>/<Feature>State.swift`
- `Features/<Feature>/<Feature>ControlsView.swift`
- `Features/<Feature>/<Feature>ImmersiveView.swift`
- `Features/<Feature>/<Feature>RealityController.swift`

Use this when one user workflow crosses a window, bounded volume, and
immersive space. Keep scene declarations separate from views so launch behavior,
restoration, IDs, and default sizes are easy to audit.

## Naming Defaults

- Name scene files after the surface they declare.
- Name coordinators after the workflow they coordinate, not after SwiftUI.
- Name RealityKit owners `RealityController`, `RealityScene`, or `System`
  according to the repo's existing convention.
- Keep attachments near the Reality owner when placement is core behavior; keep
  ordinary panels near SwiftUI views when they are just controls.

If the repo already has a stronger convention, preserve it rather than forcing
a new global layout.
