# HandTrackingProvider

## Context

HandTrackingProvider supplies real-time data about a person's hands and joints via HandAnchor updates. Use it for custom gestures, hand-driven interactions, or visualizations.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Add `NSHandsTrackingUsageDescription` to Info.plist and request provider authorizations before running.
- Check `HandTrackingProvider.isSupported` and handle unsupported devices gracefully.
- Use `anchorUpdates` for continuous updates and `latestAnchors` for instant access.
- Treat hand data as transient and avoid persisting it.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class HandTrackingModel {
    private let session = ARKitSession()
    private let provider = HandTrackingProvider()

    func start() async {
        guard HandTrackingProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: HandTrackingProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Hand tracking failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                handleHandAnchor(update.anchor)
            }
        }
    }

    private func handleHandAnchor(_ anchor: HandAnchor) {}
}
```
