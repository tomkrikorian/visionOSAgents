# Immersive media on visionOS — Reference

## Decision tree: what are you trying to build?

### A) “Video on a surface” (most common)

Use a RealityKit entity with `VideoPlayerComponent` attached to render video as a “screen” in a window/volume. This is typically the best default because it plays nicely with shared space and multitasking.

### B) Portal playback (immersive media rendered in a portal)

If you want immersive media, but still framed as an object in the user’s space, use immersive media with `desiredImmersiveViewingMode = .portal`. Portal rendering keeps the experience grounded and often more comfortable.

### C) Progressive immersive playback (crown-controlled)

Use `.progressive` when you want a user-controlled ramp from partial to full coverage (not used for Spatial Video content types).

### D) Full immersive playback

Use `.full` when you want complete immersion. Plan for:

- obvious exit affordances
- comfort considerations
- scene transitions (entering/exiting an immersive space)

## Primary sources (Apple)

- RealityKit `VideoPlayerComponent`: https://developer.apple.com/documentation/realitykit/videoplayercomponent
- `VideoPlayerEvents`: https://developer.apple.com/documentation/realitykit/videoplayerevents
- ImmersiveMediaSupport: https://developer.apple.com/documentation/immersivemediasupport

