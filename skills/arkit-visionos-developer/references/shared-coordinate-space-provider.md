# SharedCoordinateSpaceProvider

## Context

SharedCoordinateSpaceProvider establishes a shared coordinate space among multiple participants. It provides event updates and lets you push coordinate space data for synchronization.

## Best Practices

- Check `SharedCoordinateSpaceProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Listen to `eventUpdates` to react to session state changes.
- Push coordinate space data only when it changes to reduce bandwidth.
- Run in Full Space and keep the session and provider alive for the feature lifetime.

## Code Examples

```swift
import ARKit

@MainActor
final class SharedSpaceModel {
    private let session = ARKitSession()
    private let provider = SharedCoordinateSpaceProvider()

    func start() async {
        guard SharedCoordinateSpaceProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: provider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Shared coordinate space failed: \(error)")
            return
        }

        Task {
            for await event in provider.eventUpdates {
                handleEvent(event)
            }
        }
    }

    func publishNextCoordinateSpace() {
        if let data = provider.nextCoordinateSpaceData {
            provider.push(data: data)
        }
    }

    private func handleEvent(_ event: SharedCoordinateSpaceProvider.Event) {}
}
```
