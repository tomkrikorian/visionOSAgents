# AVKit visionOS Playback

Use this file when the system player experience fits the product better than a
RealityKit-authored video entity.

## API Choice

Use `AVPlayerViewController` and `AVExperienceController` when the app should
use Apple's system playback UI, supported experiences, and transitions. Use
RealityKit `VideoPlayerComponent` when video is part of an app-authored entity
graph or needs to be composed with custom RealityKit content.

## AVExperienceController Checklist

- Access the controller through `AVPlayerViewController.experienceController`.
- Configure supported experiences before presenting controls that can request
  them.
- Use `transition(to:)` for explicit experience changes.
- Handle reversed transitions with `AVExperienceController.TransitionContext`
  and its reversed reason; a reversal is real state, not a cosmetic failure.
- Use the delegate preparation hook when a transition needs placement or
  configuration.
- Keep the `AVPlayer`, `AVPlayerViewController`, and experience controller
  alive for the full playback flow.

## Experience Routing

- `.embedded`: use for playback embedded in app UI.
- `.expanded`: use when the system expanded playback experience is desired.
- `.multiview`: use for supported multiview playback experiences.
- Use immersive experiences only when the media type and product flow justify
  leaving the current presentation surface.

## State Reconciliation

- Keep SwiftUI state aligned with the transition result, not only the request.
- Do not mix `AVPlayerViewController` presentation APIs with
  `AVExperienceController` for the same transition path after the controller is
  adopted.
- If the player view controller is not currently in the hierarchy, provide the
  placement/configuration required by the AVKit transition.
