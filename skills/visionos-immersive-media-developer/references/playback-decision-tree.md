# Immersive media on visionOS — Reference

## Decision tree: what are you trying to build?

### A) “Video on a surface” (most common)

Use a RealityKit entity with `VideoPlayerComponent` attached to render video as a “screen” in a window/volume. This is typically the best default because it plays nicely with shared space and multitasking.

Use this path when the product needs custom RealityKit layout, colocated
objects, gestures, or synchronized scene content around the video.

### B) Portal playback (immersive media rendered in a portal)

If you want immersive media, but still framed as an object in the user’s space, use immersive media with `desiredImmersiveViewingMode = .portal`. Portal rendering keeps the experience grounded and often more comfortable.

### C) Progressive immersive playback (crown-controlled)

Use `.progressive` when you want a user-controlled ramp from partial to full coverage (not used for Spatial Video content types).

### D) Full immersive playback

Use `.full` when you want complete immersion. Plan for:

- obvious exit affordances
- comfort considerations
- scene transitions (entering/exiting an immersive space)

## Architecture Rules

- Use AVKit `AVExperienceController` when the system player experience is
  acceptable and the app mainly needs to transition between system-managed
  video experiences.
- Use RealityKit `VideoPlayerComponent` when video is part of a custom scene
  graph or needs colocated RealityKit content.
- Do not mix AVKit experience-controller transitions with
  `AVPlayerViewController` presentation APIs after accessing
  `experienceController`.
- Treat `desiredImmersiveViewingMode` as a requested target. Confirm the
  actual mode with `immersiveViewingMode` or `VideoPlayerEvents` before
  rearranging UI or scene state.

## Primary sources (Apple)

- RealityKit `VideoPlayerComponent`: https://developer.apple.com/documentation/realitykit/videoplayercomponent
- `VideoPlayerEvents`: https://developer.apple.com/documentation/realitykit/videoplayerevents
- ImmersiveMediaSupport: https://developer.apple.com/documentation/immersivemediasupport
