# CameraRegionProvider

## Context

CameraRegionProvider captures camera streams from defined regions in space using CameraRegionAnchor. It requires an enterprise license and the associated entitlement to deliver data.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Confirm enterprise licensing and the required entitlement before using the provider.
- Define region sizes in meters that match your capture needs and avoid oversized regions.
- Use `anchorUpdates(forID:)` to observe the region updates you care about.
- Remove anchors when you no longer need a region to keep processing lightweight.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit
import simd

@MainActor
final class CameraRegionModel {
    private let session = ARKitSession()
    private let provider = CameraRegionProvider()

    func start() async {
        guard CameraRegionProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: CameraRegionProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("CameraRegionProvider failed: \(error)")
        }
    }

    func addRegion(width: Float, height: Float) async {
        let anchor = CameraRegionAnchor(
            originFromAnchorTransform: matrix_identity_float4x4,
            width: width,
            height: height,
            cameraEnhancement: .stabilization
        )
        do {
            try await provider.addAnchor(anchor)
        } catch {
            print("Failed to add camera region: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates(forID: anchor.id) {
                handleRegionAnchor(update.anchor)
            }
        }
    }

    private func handleRegionAnchor(_ anchor: CameraRegionAnchor) {}
}
```
