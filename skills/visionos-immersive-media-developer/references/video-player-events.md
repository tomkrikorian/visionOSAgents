# RealityKit VideoPlayer Events

Use this file when a RealityKit `VideoPlayerComponent` needs state-driven UI,
scene transitions, subtitles, comfort handling, or lifecycle cleanup.

## Core Rule

Treat `VideoPlayerComponent` mode changes as asynchronous state transitions.
Set the desired mode on the component, then reconcile app state from
`VideoPlayerEvents` and the component's actual state. Do not assume a requested
viewing or immersive mode was honored.

## Event Coverage

Subscribe before changing mode or presenting mode-dependent controls:

- `VideoPlayerEvents.ViewingModeDidChange`
- `VideoPlayerEvents.ImmersiveViewingModeWillTransition`
- `VideoPlayerEvents.ImmersiveViewingModeDidTransition`
- `VideoPlayerEvents.ImmersiveViewingModeDidChange`
- `VideoPlayerEvents.RenderingStatusDidChange`
- `VideoPlayerEvents.VideoSizeDidChange`
- `VideoPlayerEvents.SpatialVideoModeDidChange`
- `VideoPlayerEvents.VideoComfortMitigationDidOccur`

Use rendering status and video-size events to distinguish media readiness from
scene readiness. Use comfort mitigation events as visible playback state, not
as a transient warning to ignore.

## Subscription Lifecycle

- Retain each `EventSubscription`; dropping it cancels observation.
- Cancel subscriptions when the player entity is replaced or the scene tears
  down.
- Keep the `AVPlayer` and the RealityKit entity owner alive for the playback
  flow.
- On teardown, pause or replace the player and remove or disable the video
  entity deliberately.

## SwiftUI Reconciliation

- Update SwiftUI controls from observed RealityKit events.
- Hide or pin controls while immersive transitions are in flight.
- If a transition reverses, report the actual mode and restore the UI to match
  it.
- Do not advance a narrative or scene graph from guessed durations when a
  video-completion or mode-change event is the intended contract.
