# Observation And State Modeling

Use this file when the issue is state ownership, view models, or Observation.

## Observation Rules

- `@Observable` does not imply `@MainActor`.
- Add `@MainActor` when the model owns UI-bound mutable state.
- Leave a model unannotated, or isolate it more narrowly, when it coordinates
  background work or non-UI services.

## Observation Vs Combine

- Prefer Observation (`@Observable`, `@Bindable`, plain stored properties) in
  new SwiftUI code when supported by the deployment target.
- Keep `ObservableObject`, `@StateObject`, and `@ObservedObject` when an
  existing Combine-based architecture or compatibility requirement still needs
  them.

## State Placement Defaults

- `@State`: small local state owned by a view.
- `@Binding`: parent-owned state passed into a child.
- `@Environment(Type.self)`: shared services or app-scoped context following
  project conventions.
- `@SceneStorage`: scene restoration only when scene-local persistence is
  actually required.
- `@AppStorage`: app-wide preferences.

## Review Questions

- Does the model own UI behavior or only domain behavior?
- Is the state scoped too high or too low?
- Does the code mix observation, networking, and scene lifecycle in one type?
- Would Observation remove boilerplate without changing behavior?
