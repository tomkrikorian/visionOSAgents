# WorldTrackingProvider

## Context

WorldTrackingProvider supplies device pose and world anchor updates in a person's surroundings. Use it for world-locked content, spatial anchors, and device pose queries.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Check `WorldTrackingProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Use `anchorUpdates` for world anchor changes and `queryDeviceAnchor(atTimestamp:)` for predicted device pose.
- Manage anchor lifecycle carefully and remove anchors when no longer needed.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class WorldTrackingModel {
    private let session = ARKitSession()
    private let provider = WorldTrackingProvider()

    func start() async {
        guard WorldTrackingProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: WorldTrackingProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("World tracking failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleWorldAnchor(update.anchor)
                case .removed:
                    removeWorldAnchor(update.anchor.id)
                }
            }
        }
    }

    func predictedDeviceAnchor(at timestamp: Double) -> DeviceAnchor? {
        provider.queryDeviceAnchor(atTimestamp: timestamp)
    }

    private func handleWorldAnchor(_ anchor: WorldAnchor) {}

    private func removeWorldAnchor(_ id: WorldAnchor.ID) {}
}
```
