# CameraFrameProvider

## Context

CameraFrameProvider provides camera frame streams for selected video formats. It exposes `cameraFrameUpdates(for:)`, which yields CameraFrame values you can process for computer vision or custom rendering pipelines.

## Best Practices

- Check `CameraFrameProvider.isSupported` before creating the provider.
- Choose a CameraVideoFormat that matches your latency and quality needs.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Offload heavy frame processing to a background task or actor.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class CameraFrameStreamer {
    private let session = ARKitSession()
    private let provider = CameraFrameProvider()

    func start(format: CameraVideoFormat) async {
        guard CameraFrameProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("CameraFrameProvider failed: \(error)")
            return
        }

        Task {
            for await frame in provider.cameraFrameUpdates(for: format) {
                handleFrame(frame)
            }
        }
    }

    private func handleFrame(_ frame: CameraFrame) {}
}
```
