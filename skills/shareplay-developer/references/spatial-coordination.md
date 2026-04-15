# Spatial Coordination

Use this file when the SharePlay experience coordinates people in the same
immersive space.

## Rules

- Await `GroupSession.systemCoordinator`.
- Set `spatialTemplatePreference` and `supportsGroupImmersiveSpace` before
  `join()`.
- Use participant state APIs to track local and remote placement.
- `.immersiveEnvironmentBehavior(.coexist)` controls whether the system
  immersive environment remains visible; it is not the colocated-session API.

On visionOS 26, observe `SystemCoordinator.groupImmersionStyle` to keep local
UI aligned with the group's immersion style.
