# Events and transitions (VideoPlayerEvents)

## Why you should subscribe

Immersive viewing mode transitions are user-perceivable and can be jarring if your UI doesn’t match the moment (controls floating in the wrong place, unexpected scene dismissals, etc.). Use `VideoPlayerEvents` to:

- toggle UI during transitions
- react to mode changes reliably
- respond to rendering status changes

## Commonly useful events

- `ImmersiveViewingModeWillTransition` / `ImmersiveViewingModeDidTransition`
- `ImmersiveViewingModeDidChange`
- `VideoSizeDidChange`
- `RenderingStatusDidChange`
- `SpatialVideoModeDidChange`
- `VideoComfortMitigationDidOccur` (visionOS 26+)

## Transition Handling

- Subscribe before changing `desiredImmersiveViewingMode`.
- On "will transition", hide or pin controls that would be disorienting during
  the transition.
- On "did transition" or "did change", reconcile SwiftUI scene state with the
  actual `currentMode`; do not assume the requested mode was honored.
- Cancel event subscriptions on scene teardown and when replacing the player
  entity.
- Treat comfort mitigation events as user-visible playback state and avoid
  immediately re-requesting the mode that triggered mitigation.

## Primary sources (Apple)

- VideoPlayerEvents: https://developer.apple.com/documentation/realitykit/videoplayerevents
