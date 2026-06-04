# VideoPlayerComponent basics (RealityKit)

## What it is

`VideoPlayerComponent` is a RealityKit component that supports video playback with an `AVPlayer`. On visionOS, it also supports features that are important for a strong media experience:

- captions/subtitles support (via system playback controls)
- passthrough tinting (visionOS only)
- immersive viewing modes for immersive media

## Minimal setup

1. Create an entity to represent the display.
2. Create an `AVPlayer`.
3. Create `VideoPlayerComponent(avPlayer:)`.
4. Attach it to the entity.
5. Start the player.

## Useful configuration points

- `desiredViewingMode` — for example, request stereo playback when available.
- `isPassthroughTintingEnabled` — visually emphasize video content in mixed reality.
- `desiredImmersiveViewingMode` — choose portal/progressive/full for immersive media types.

## Lifecycle and State

- Keep the `AVPlayer` alive outside the temporary RealityKit content builder.
- Treat component configuration as scene state: mutate the component, assign it
  back to the entity, and keep the owning model aware of the intended mode.
- For immersive mode reconciliation and event subscription rules, load
  [`video-player-events.md`](video-player-events.md).
- Pause or replace the player deliberately on teardown; do not leave immersive
  playback running after the containing scene is dismissed.
