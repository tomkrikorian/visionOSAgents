# EnvironmentLightEstimationProvider

## Context

EnvironmentLightEstimationProvider supplies lighting information about the environment using EnvironmentProbeAnchor updates. Use it to match virtual lighting to real-world conditions.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Check `EnvironmentLightEstimationProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Use anchor updates to refresh RealityKit lighting or image-based lighting resources.
- Avoid heavy lighting recomputation on the main actor.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class LightEstimationModel {
    private let session = ARKitSession()
    private let provider = EnvironmentLightEstimationProvider()

    func start() async {
        guard EnvironmentLightEstimationProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: EnvironmentLightEstimationProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Light estimation failed: \(error)")
            return
        }

        Task {
            for await update in provider.anchorUpdates {
                updateLighting(from: update.anchor)
            }
        }
    }

    private func updateLighting(from anchor: EnvironmentProbeAnchor) {}
}
```
