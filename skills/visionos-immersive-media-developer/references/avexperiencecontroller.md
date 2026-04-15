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
