# StereoPropertiesProvider

## Context

StereoPropertiesProvider supplies the latest viewpoint properties for stereo rendering. Use it to inform custom rendering or compositing pipelines.

## Best Practices

- Check `StereoPropertiesProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Read `latestViewpointProperties` as needed and avoid heavy processing on the main actor.
- Combine stereo properties with your rendering loop instead of polling excessively.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class StereoPropertiesModel {
    private let session = ARKitSession()
    private let provider = StereoPropertiesProvider()

    func start() async {
        guard StereoPropertiesProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
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
