# Observation And State Modeling

Use this file when the issue is state ownership, view models, or Observation.

## Observation Rules

- `@Observable` does not imply `@MainActor`.
- Add `@MainActor` when the model owns UI-bound mutable state.
- Leave a model unannotated, or isolate it more narrowly, when it coordinates
  background work or non-UI services.

## Observation Vs Combine

- Observation is the default for new SwiftUI and visionOS code:
  use `@Observable`, `@Bindable`, and plain stored properties.
- Do not introduce `ObservableObject`, `@StateObject`, or `@ObservedObject` in
  new code unless the user explicitly asks for a Combine-based path or there is
  a concrete compatibility blocker that prevents Observation.
- When touching an existing Combine-based architecture, preserve
  `ObservableObject`, `@StateObject`, and `@ObservedObject` only when that
  compatibility requirement is real and immediate. Otherwise, migrate toward
  Observation instead of adding more Combine-based observation surface area.
- Never pair an `@Observable` model with `@StateObject` or `@ObservedObject`.
  Those wrappers are for `ObservableObject` and should not appear in new
  Observation-based code.

## State Placement Defaults

- `@State`: small local state owned by a view.
- `@Binding`: parent-owned state passed into a child.
- `@State` with an `@Observable` model: view-owned reference model lifetime.
- `@Bindable`: child view needs editable bindings into an `@Observable` model.
- `@Environment(Type.self)`: shared services or app-scoped context following
  project conventions.
- `@SceneStorage`: scene restoration only when scene-local persistence is
  actually required.
- `@AppStorage`: app-wide preferences.

## Default Pattern

```swift
@Observable
@MainActor
final class InspectorModel {
    var selectedID: UUID?
}

struct InspectorView: View {
    @State private var model = InspectorModel()

    var body: some View {
        InspectorContent(model: model)
    }
}

struct InspectorContent: View {
    @Bindable var model: InspectorModel
}
```

Remove `@MainActor` from the model only when it does not own UI-bound mutable
state and its isolation is handled elsewhere.

## Review Questions

- Does the model own UI behavior or only domain behavior?
- Is the state scoped too high or too low?
- Does the code mix observation, networking, and scene lifecycle in one type?
- Is `ObservableObject` present for a real compatibility reason, or is it just
  legacy inertia that should be removed?
- Does an `@Observable` type accidentally use `@StateObject` or
  `@ObservedObject` at the view boundary?
- Would Observation remove boilerplate without changing behavior?
