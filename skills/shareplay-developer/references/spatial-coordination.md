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

## Configuration Sequence

1. Await `session.systemCoordinator`; if it is `nil`, fall back to non-spatial
   SharePlay behavior or decline the immersive-spatial session.
2. Set `systemCoordinator.configuration.supportsGroupImmersiveSpace = true`
   before `session.join()` when spatial Personas should remain visible inside
   the immersive space.
3. Set `systemCoordinator.configuration.spatialTemplatePreference` before
   `session.join()` when the product requires a specific participant layout.
4. After joining, observe `localParticipantStates` before enabling controls
   that require the local participant to support shared spatial context.
5. Observe `remoteParticipantStates` when content must appear relative to a
   remote participant's seat or pose.

On visionOS 26, observe `SystemCoordinator.groupImmersionStyle` to keep local
UI aligned with the group's immersion style. Treat `nil` as "no participant is
currently showing the immersive space"; offer or perform dismissal without
interrupting unrelated local work.
