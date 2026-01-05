# ImageTrackingProvider

## Context

ImageTrackingProvider tracks known 2D images in a person's surroundings and emits ImageAnchor updates. Use it to attach content to specific printed or displayed images.

## Best Practices

- Supply reference images with accurate physical sizes for stable tracking.
- Check `ImageTrackingProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Keep the reference image set focused to improve detection performance.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class ImageTrackingModel {
    private let session = ARKitSession()
    private var provider: ImageTrackingProvider?

    func start(referenceImages: [ReferenceImage]) async {
        guard ImageTrackingProvider.isSupported else { return }
        let provider = ImageTrackingProvider(referenceImages: referenceImages)
        self.provider = provider

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Image tracking failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleImageAnchor(update.anchor)
                case .removed:
                    removeImageAnchor(update.anchor.id)
                }
            }
        }
    }

    private func handleImageAnchor(_ anchor: ImageAnchor) {}

    private func removeImageAnchor(_ id: ImageAnchor.ID) {}
}
```
