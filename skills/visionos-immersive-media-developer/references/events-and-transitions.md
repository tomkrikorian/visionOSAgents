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

## Primary sources (Apple)

- VideoPlayerEvents: https://developer.apple.com/documentation/realitykit/videoplayerevents

