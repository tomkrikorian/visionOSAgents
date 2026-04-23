# Debugging and updates (timelines, refresh, and “why isn’t my widget changing?”)

## Common “it doesn’t show up” causes

- Widget extension isn’t embedded in the correct app target/scheme.
- The widget declares the wrong families for your testing surface.
- Your view crashes at runtime (check extension logs).
- The simulator or device is still showing a cached snapshot from the previous
  install.

## Common “it shows but never updates” causes

- Timeline policy doesn’t request refresh when you expect.
- Your widget data fetch fails silently (network, decoding, timeouts).
- You rely on app-side state without a reload strategy.
- The `kind` passed to `WidgetCenter.shared.reloadTimelines(ofKind:)` does not
  match the widget configuration kind exactly.
- The provider reads a different store than the App Intent or host app writes.

## Practical debugging checklist

1. **Start with Preview**: validate both `.default` and `.simplified` layouts.
2. **Force a reload in development**:
   - Use `WidgetCenter.shared.reloadTimelines(ofKind:)` for a specific widget
     kind, or `reloadAllTimelines()` when the whole extension should refresh.
3. **Log timeline decisions**:
   - Ensure your provider returns entries at the cadence you expect.
4. **Test mounting styles**:
   - Confirm recessed doesn’t clip, invert contrast, or break layout.
5. **Check the extension process**:
   - Read widget-extension logs, not just host-app logs.
   - Confirm App Group identifiers, entitlements, and shared container paths
     match between the app and widget extension.

## Notes about Vision Pro specifics

- Treat the `.simplified` layout as a strong design requirement for widgets that need to remain legible at distance.
- Recessed mounting can change perceived contrast and edges; verify your background strategy.
- WidgetKit chooses when to run the extension. Treat reload calls and push
  notifications as requests for new timelines, not as guaranteed immediate
  redraws.
- If timeline generation uses async work, keep the slow path bounded and return
  a reasonable fallback entry rather than timing out the extension.

## Primary sources (Apple)

- Developing a WidgetKit strategy: https://developer.apple.com/documentation/widgetkit/developing-a-widgetkit-strategy
- Updating your widgets for visionOS: https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- Keeping a widget up to date: https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date
- `WidgetCenter.reloadTimelines(ofKind:)`: https://developer.apple.com/documentation/widgetkit/widgetcenter/reloadtimelines(ofkind:)
