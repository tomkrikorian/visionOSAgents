# Observation And SwiftUI Data Flow

Use this file when the issue is state ownership, view models, or Observation.

## Official API Model

- Use the Observation `@Observable` macro for new observable reference models.
  The official `Observable` protocol marks an observable type, but protocol
  conformance alone does not synthesize observation behavior; the macro does.
- Use `@ObservationIgnored` for accessible properties that should not be tracked,
  such as caches, delegates, formatters, loggers, or service handles.
- Use SwiftUI `@State` as the source of truth for state owned by a view, scene,
  or app. For a view-owned observable reference model, store the model in
  `@State private var model = Model()`.
- Use SwiftUI `@Bindable` when a child view or local scope needs bindings to
  mutable properties of an observable model, including models read from typed
  environment values.
- Use `@Binding` for parent-owned value state passed to a child. Do not use it
  as a substitute for passing an observable model when the model itself owns the
  behavior.

## Isolation Rules

- `@Observable` does not imply `@MainActor`.
- Add Swift `@MainActor` when the model owns UI-bound mutable state or exposes
  methods that SwiftUI views call to mutate UI state.
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

- `@State`: local value state or view-owned observable reference model lifetime.
- `@Binding`: parent-owned value state passed into a child.
- Plain stored property: read-only access to an observable model passed from a
  parent.
- `@Bindable`: child view or local scope needs editable bindings into an
  `@Observable` model.
- `@Environment(Type.self)`: shared services or app-scoped context following
  project conventions.
- Local `@Bindable var model = model`: a typed environment observable needs
  binding projection inside `body`.
- `@SceneStorage`: scene restoration only when scene-local persistence is
  actually required.
- `@AppStorage`: app-wide preferences.

## Default Pattern

```swift
@Observable
@MainActor
final class EditorModel {
    var selectedID: UUID?
    var title = ""

    @ObservationIgnored
    private let formatter = DateFormatter()
}

struct EditorView: View {
    @State private var model = EditorModel()

    var body: some View {
        EditorContent(model: model)
    }
}

struct EditorContent: View {
    @Bindable var model: EditorModel

    var body: some View {
        TextField("Title", text: $model.title)
    }
}
```

Remove `@MainActor` from the model only when it does not own UI-bound mutable
state and its isolation is handled elsewhere.

## Typed Environment Pattern

```swift
@Observable
@MainActor
final class PreferencesModel {
    var displayName = ""
}

struct PreferencesView: View {
    @Environment(PreferencesModel.self) private var preferences

    var body: some View {
        @Bindable var preferences = preferences
        TextField("Name", text: $preferences.displayName)
    }
}
```

Use the local `@Bindable` variable only in the scope that needs `$` bindings.
Read-only views can use the environment value or passed model directly.

## Review Questions

- Does the model own UI behavior or only domain behavior?
- Is the state scoped too high or too low?
- Does the code mix observation, networking, and scene lifecycle in one type?
- Does the observable model use plain stored properties unless a property is
  deliberately marked `@ObservationIgnored`?
- Does the owning view store a view-owned observable model in `@State` rather
  than a legacy object wrapper?
- Does a child view use `@Bindable` only when it needs `$model.property`
  bindings?
- Is `@MainActor` applied because the model is UI-bound, not because every
  observable type was blanket-isolated?
- Is `Sendable` used only for values that safely cross actor or task
  boundaries?

## Official Apple API Anchors

- Observation: `Observable`, `@Observable`, `@ObservationIgnored`
- SwiftUI: `State`, `Bindable`, `Binding`, `Environment`
- Swift concurrency: `MainActor`, `MainActor.run`, `Sendable`, `@Sendable`
