# BarcodeDetectionProvider

## Context

BarcodeDetectionProvider supplies real-time position updates for barcodes detected in a person's surroundings. It publishes BarcodeAnchor updates and requires the barcode detection entitlement to deliver data.

## Best Practices

- Ensure the barcode detection entitlement is present; without it the provider delivers no data.
- Limit the symbologies to the ones your experience needs to reduce false positives.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Use `anchorUpdates` to add, update, and remove barcode-driven content.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class BarcodeTrackingModel {
    private let session = ARKitSession()
    private var provider: BarcodeDetectionProvider?

    func startTracking(symbologies: [BarcodeAnchor.Symbology]) async {
        guard BarcodeDetectionProvider.isSupported else { return }
        let provider = BarcodeDetectionProvider(symbologies: symbologies)
        self.provider = provider

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Barcode detection failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleBarcodeAnchor(update.anchor)
                case .removed:
                    removeBarcodeAnchor(update.anchor.id)
                }
            }
        }
    }

    private func handleBarcodeAnchor(_ anchor: BarcodeAnchor) {}

    private func removeBarcodeAnchor(_ id: BarcodeAnchor.ID) {}
}
```
