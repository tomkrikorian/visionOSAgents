# Interactive Widgets

Use this file when the widget needs controls instead of being purely
display-only.

visionOS widgets can host `Button` and `Toggle` controls backed by `AppIntent`.
Keep the interaction small and direct the user into the host app for richer
flows.

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
