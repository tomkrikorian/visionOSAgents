# StereoPropertiesProvider

## Context

StereoPropertiesProvider supplies the latest viewpoint properties for stereo rendering. Use it to inform custom rendering or compositing pipelines.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Check `StereoPropertiesProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Read `latestViewpointProperties` as needed and avoid heavy processing on the main actor.
- Combine stereo properties with your rendering loop instead of polling excessively.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class StereoPropertiesModel {
    private let session = ARKitSession()
    private let provider = StereoPropertiesProvider()

    func start() async {
        guard StereoPropertiesProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: StereoPropertiesProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("StereoPropertiesProvider failed: \(error)")
            return
        }
    }

    func updateViewpoint() {
        guard let properties = provider.latestViewpointProperties else { return }
        applyViewpointProperties(properties)
    }

    private func applyViewpointProperties(_ properties: ViewpointProperties) {}
}
```
