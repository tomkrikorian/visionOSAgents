# ObjectTrackingProvider

## Context

ObjectTrackingProvider tracks reference objects in a person's surroundings and emits ObjectAnchor updates. Use it for physical object recognition and anchoring virtual content to real-world objects.

## Best Practices

- Build reference objects with accurate size and orientation to improve tracking stability.
- Check `ObjectTrackingProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Use the tracking configuration to balance performance and fidelity for your use case.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class ObjectTrackingModel {
    private let session = ARKitSession()
    private var provider: ObjectTrackingProvider?

    func start(
        referenceObjects: [ReferenceObject],
        configuration: ObjectTrackingProvider.TrackingConfiguration? = nil
    ) async {
        guard ObjectTrackingProvider.isSupported else { return }
        let provider = ObjectTrackingProvider(
            referenceObjects: referenceObjects,
            trackingConfiguration: configuration
        )
        self.provider = provider

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Object tracking failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleObjectAnchor(update.anchor)
                case .removed:
                    removeObjectAnchor(update.anchor.id)
                }
            }
        }
    }

    private func handleObjectAnchor(_ anchor: ObjectAnchor) {}

    private func removeObjectAnchor(_ id: ObjectAnchor.ID) {}
}
```
