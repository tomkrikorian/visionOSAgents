# visionOS Widgets (WidgetKit) — Reference

## What’s different about widgets on Apple Vision Pro

Widgets on visionOS are spatial objects. People place them in a room and pin
them to surfaces (horizontal or vertical). This drives a different set of
constraints than a flat 2D widget surface:

- **Distance variability:** A widget may be viewed from inches away or across a room.
- **Surface integration:** Vertical surfaces can present widgets **recessed** or **elevated**.
- **Material/texture:** Widgets can have a glass-like coating or a more poster-like paper texture.
- **Extension boundary:** Widget views render from timeline entries and shared
  data. They are not live windows into the running app process.

## Key decisions (fast)

1. **Does it support recessed placement?**
   - If the widget only makes sense embedded in a wall or window-like surface, consider `.supportedMountingStyles([.recessed])` only. If it breaks when mounted on a wall, prefer elevated-only or redesign the layout.
2. **How does it adapt to distance?**
   - Use `@Environment(\.levelOfDetail)` and implement `.default` + `.simplified` layouts.
3. **Does it need “poster” treatment?**
   - Consider `.widgetTexture(.paper)` (visionOS app widgets).
4. **Where does the data come from?**
   - Prefer timeline entries for snapshot data.
   - Use an App Group or background URL session when the widget extension must
     read data produced outside the timeline provider.
   - Use WidgetKit reload APIs or WidgetKit push notifications when fresh app
     or server data should request a new timeline.
5. **Is the widget interactive?**
   - Use `Button` or `Toggle` only for a bounded `AppIntent` action.
   - Use `Link` or `widgetURL(_:)` when the intended behavior is opening a
     scene in the host app.

## Minimal checklist (before you debug anything else)

- Confirm the widget **builds** and is included in the correct extension target.
- Confirm your widget declares the **families** you expect.
- For extra-large widgets on Vision Pro, use `.systemExtraLargePortrait`.
- Confirm you’ve tested both **mounting styles** (if supported).
- Confirm you’ve implemented a `.simplified` layout (or intentionally opted out).
- Confirm the widget renders correctly in `.fullColor`, `.accented`, and
  distance-driven simplified states when those modes apply.
- Confirm host-app mutations either update shared state then call
  `WidgetCenter.shared.reloadTimelines(ofKind:)`, or are represented by future
  timeline entries.

## Primary sources (Apple)

- Updating your widgets for visionOS: https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- WidgetKit updates (Vision Pro widgets): https://developer.apple.com/documentation/updates/widgetkit
- `LevelOfDetail`: https://developer.apple.com/documentation/widgetkit/levelofdetail
