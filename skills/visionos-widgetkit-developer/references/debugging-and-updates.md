# Debugging and updates (timelines, refresh, and “why isn’t my widget changing?”)

## Common “it doesn’t show up” causes

- Widget extension isn’t embedded in the correct app target/scheme.
- The widget declares the wrong families for your testing surface.
- Your view crashes at runtime (check extension logs).

## Common “it shows but never updates” causes

- Timeline policy doesn’t request refresh when you expect.
- Your widget data fetch fails silently (network, decoding, timeouts).
- You rely on app-side state without a reload strategy.

## Practical debugging checklist

1. **Start with Preview**: validate both `.default` and `.simplified` layouts.
2. **Force a reload in development**:
   - Use WidgetKit reload APIs from the host app in debug builds.
3. **Log timeline decisions**:
   - Ensure your provider returns entries at the cadence you expect.
4. **Test mounting styles**:
   - Confirm recessed doesn’t clip, invert contrast, or break layout.

## Notes about Vision Pro specifics

- Treat the `.simplified` layout as a strong design requirement for widgets that need to remain legible at distance.
- Recessed mounting can change perceived contrast and edges; verify your background strategy.

## Primary sources (Apple)

- Developing a WidgetKit strategy: https://developer.apple.com/documentation/widgetkit/developing-a-widgetkit-strategy
- Updating your widgets for visionOS: https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
