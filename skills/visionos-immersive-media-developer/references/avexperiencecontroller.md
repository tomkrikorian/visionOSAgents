# AVExperienceController

Use this file when the system AVKit player experience fits the product.

## Rules

- Use `AVExperienceController` with `AVPlayerViewController` on visionOS 26+ to
  move between window, inline, expanded, and immersive experiences.
- Once attached, do not continue to drive presentation with
  `AVPlayerViewController` presentation APIs. Route experience changes through
  the experience controller.
- Configure the supported experiences up front, including any automatic
  transition to immersive playback.
- Call `transition(to:)` for explicit moves and handle a reversed transition
  result as a real state, not a cosmetic failure.
- When transitioning to `.immersive` while the player view controller is not in
  the view hierarchy, provide placement through the controller configuration or
  the transition can reverse.

## Ownership

- Keep the `AVPlayerViewController`, `AVPlayer`, and accessed
  `AVExperienceController` alive for the full playback flow.
- Put experience changes on the main actor and keep surrounding SwiftUI state in
  sync with transition results.
