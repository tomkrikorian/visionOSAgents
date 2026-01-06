# AccessoryTrackingProvider

## Context

AccessoryTrackingProvider supplies real-time pose updates for accessories in the user's environment. It publishes AccessoryAnchor updates and can return the latest anchor state or a predicted pose for latency compensation.

## Best Practices

- Check `AccessoryTrackingProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` and handle denied states before running the session.
- Track only the accessories needed for the experience to reduce noise.
- Use `anchorUpdates` to add, update, and remove entities, and use `predictAnchor(for:at:)` when you need a future pose.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class AccessoryTrackingModel {
    private let session = ARKitSession()
    private var provider: AccessoryTrackingProvider?

    func startTracking(accessories: [Accessory]) async {
        guard AccessoryTrackingProvider.isSupported else { return }
        let provider = AccessoryTrackingProvider(accessories: accessories)
        self.provider = provider

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Accessory tracking failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleAccessoryAnchor(update.anchor)
                case .removed:
                    removeAccessoryAnchor(update.anchor.id)
                }
            }
        }
    }

    private func handleAccessoryAnchor(_ anchor: AccessoryAnchor) {}

    private func removeAccessoryAnchor(_ id: AccessoryAnchor.ID) {}
}
```
