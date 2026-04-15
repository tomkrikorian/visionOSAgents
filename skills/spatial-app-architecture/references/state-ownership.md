# State Ownership

Use this file when deciding what owns state and lifecycle responsibilities.

## Ownership Map

| Scope | Owns |
| --- | --- |
| App | top-level scene declarations, app-wide dependency injection, persistent preferences |
| Scene | navigation, presentation state, scene-local selection, immersive entry and exit coordination |
| Feature model or coordinator | async work, service coordination, long-lived feature state |
| Reality controller or system | entity graph mutation, component updates, simulation behavior |
| View | ephemeral local UI state and intent dispatch |

## State Placement Defaults

- `@State`: local control state and small scene-owned observable models
- `@Binding`: parent-owned state passed into a child
- `@SceneStorage`: scene-local restoration when it genuinely fits
- `@AppStorage`: app-wide preference or toggle
- `@Environment(Type.self)`: shared service, coordinator, or app context when
  that matches the project convention

Do not keep immersive lifecycle ownership or long-lived entity ownership in
transient leaf views.
