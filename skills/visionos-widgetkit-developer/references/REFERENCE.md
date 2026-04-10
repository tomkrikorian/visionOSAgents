# visionOS Widgets (WidgetKit) — Reference

## What’s different about widgets on Apple Vision Pro

Widgets on visionOS are spatial objects. People place them in a room and pin
them to surfaces (horizontal or vertical). This drives a different set of
constraints than a flat 2D widget surface:

- **Distance variability:** A widget may be viewed from inches away or across a room.
- **Surface integration:** Vertical surfaces can present widgets **recessed** or **elevated**.
- **Material/texture:** Widgets can have a glass-like coating or a more poster-like paper texture.

## Key decisions (fast)

1. **Does it support recessed placement?**
   - If the widget only makes sense embedded in a wall or window-like surface, consider `.supportedMountingStyles([.recessed])` only. If it breaks when mounted on a wall, prefer elevated-only or redesign the layout.
2. **How does it adapt to distance?**
   - Use `@Environment(\.levelOfDetail)` and implement `.default` + `.simplified` layouts.
3. **Does it need “poster” treatment?**
   - Consider `.widgetTexture(.paper)` (visionOS app widgets).

## Minimal checklist (before you debug anything else)

- Confirm the widget **builds** and is included in the correct extension target.
- Confirm your widget declares the **families** you expect.
- For extra-large widgets on Vision Pro, use `.systemExtraLargePortrait`.
- Confirm you’ve tested both **mounting styles** (if supported).
- Confirm you’ve implemented a `.simplified` layout (or intentionally opted out).

## Primary sources (Apple)

- Updating your widgets for visionOS: https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- WidgetKit updates (Vision Pro widgets): https://developer.apple.com/documentation/updates/widgetkit
- `LevelOfDetail`: https://developer.apple.com/documentation/widgetkit/levelofdetail
