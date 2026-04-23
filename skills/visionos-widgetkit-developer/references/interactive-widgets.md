# Interactive Widgets

Use this file when the widget needs controls instead of being purely
display-only.

visionOS widgets can host `Button` and `Toggle` controls backed by `AppIntent`.
Keep the interaction small and direct the user into the host app for richer
flows.

Use `Button` or `Toggle` only when the interaction performs work from the
widget. If the desired result is opening the app, use `Link` or
`widgetURL(_:)` instead.

```swift
import AppIntents
import SwiftUI
import WidgetKit

struct ToggleFavoriteIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Favorite"
    @Parameter(title: "Item ID") var itemID: String

    func perform() async throws -> some IntentResult {
        return .result()
    }
}
```

## Implementation Rules

- Add the `AppIntent` to the widget extension target and to the app target when
  the same action should be reused in-app.
- Provide concrete parameter values from the widget view; widget interactions
  do not resolve missing parameters through a conversational flow.
- Keep `perform()` async, short, and safe to run in the widget extension
  process. If it changes shared data, write through the same App Group or
  service path that the timeline provider reads.
- Expect WidgetKit to ask for a fresh timeline after an interaction completes,
  but still return timeline entries that reflect the persisted source of truth.
- For toggles, remember the UI may update optimistically before `perform()`
  finishes; make failed writes visible in the next timeline entry rather than
  storing transient view state.

## Review Questions

- Does the action do real work, or should this be a deep link?
- Can the intent run without assuming the host app is already alive?
- Does the timeline provider read the same state that the intent mutates?
- Is the action still glanceable from across the room?

## Primary sources (Apple)

- Adding interactivity to widgets and Live Activities: https://developer.apple.com/documentation/widgetkit/adding-interactivity-to-widgets-and-live-activities
- Linking to specific app scenes from your widget or Live Activity: https://developer.apple.com/documentation/widgetkit/linking-to-specific-app-scenes-from-your-widget-or-live-activity
