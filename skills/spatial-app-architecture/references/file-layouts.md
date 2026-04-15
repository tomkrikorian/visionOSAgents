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

If the repo already has a stronger convention, preserve it rather than forcing
a new global layout.
