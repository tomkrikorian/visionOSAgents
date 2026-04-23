# State Ownership

Use this file when deciding what owns state and lifecycle responsibilities.

## Ownership Map

| Scope | Owns | Should Not Own |
| --- | --- | --- |
| App | top-level scene declarations, app-wide dependency injection, persistent preferences, shared services | feature selection churn, entity mutation, transient panel state |
| Scene | navigation, presentation state, scene-local selection, window/volume geometry intent, immersive entry and exit coordination | service internals, RealityKit graph details, unrelated scene state |
| Immersive session | open/dismiss status, current immersion mode, scene handoff state, recovery after failed open/dismiss | app-wide preferences, leaf control state |
| Feature model or coordinator | async work, service coordination, long-lived feature state, asset catalog state | direct RealityKit component mutation from arbitrary SwiftUI bodies |
| Reality controller or system | entity graph mutation, component updates, simulation behavior, attachment placement rules | SwiftUI navigation, account/preferences, view formatting |
| View | ephemeral local UI state and intent dispatch | long-lived immersive lifecycle, global stores, service singletons |

## State Placement Defaults

- `@State`: local control state and small scene-owned observable models
- `@Binding`: parent-owned state passed into a child
- `@SceneStorage`: scene-local restoration when it genuinely fits
- `@AppStorage`: app-wide preference or toggle
- `@Environment(Type.self)`: shared service, coordinator, or app context when
  that matches the project convention
- `@Observable`: default model/coordinator shape for new SwiftUI and visionOS
  state unless an existing repo convention or explicit compatibility blocker
  requires a different pattern

## Boundary Rules

- Put `openImmersiveSpace`, `dismissImmersiveSpace`, `openWindow`, and
  `dismissWindow` calls behind scene-level intent methods when several controls
  can trigger them.
- Keep entity references and subscriptions in a named RealityKit owner, not in
  throwaway SwiftUI rows or buttons.
- Let views describe user intent. Let coordinators decide whether that intent
  changes navigation, opens a scene, loads assets, or mutates entities.
- Treat attachments as part of the RealityKit presentation boundary: SwiftUI
  owns their view content; the Reality owner owns their 3D placement.
- Make cross-surface state explicit. If a selection appears in a window and an
  immersive space, put it in a shared scene/app model instead of duplicating it.

Do not keep immersive lifecycle ownership or long-lived entity ownership in
transient leaf views.
