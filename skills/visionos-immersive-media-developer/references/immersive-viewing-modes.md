# Immersive viewing modes (portal / progressive / full)

## The three modes

RealityKit exposes immersive viewing modes for immersive media types:

- **`.portal`**: immersive video rendered as a portal “window” that matches the containing entity transform.
- **`.progressive`**: partial-to-full coverage controlled by the Digital Crown (not available for Spatial Video).
- **`.full`**: full field-of-view immersive playback.

## Practical guidance

- Prefer **portal** by default for comfort and context.
- Use **progressive** when you want the user to “ease in” via crown control.
- Use **full** only when you have a strong reason and an obvious exit.

## Switching modes often requires scene changes

Mode switches can imply different scene presentation:

- Portal playback commonly lives in a **window scene** (shared space).
- Progressive/full commonly live in **immersive spaces**.

When transitioning between portal and progressive/full, coordinate:

1. Set `desiredImmersiveViewingMode`.
2. Wait for a mode-change event.
3. Dismiss/open the appropriate scene(s) in a user-friendly way.

## Primary sources (Apple)

- `VideoPlayerComponent.ImmersiveViewingMode`: https://developer.apple.com/documentation/realitykit/videoplayercomponent/immersiveviewingmode-swift.enum
- VideoPlayerComponent overview: https://developer.apple.com/documentation/realitykit/videoplayercomponent

