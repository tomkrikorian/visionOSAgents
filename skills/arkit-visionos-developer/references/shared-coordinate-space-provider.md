# SharedCoordinateSpaceProvider

## Context

SharedCoordinateSpaceProvider establishes a shared coordinate space among multiple participants. It provides event updates and lets you push coordinate space data for synchronization.


For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Best Practices

- Check `SharedCoordinateSpaceProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Listen to `eventUpdates` to react to session state changes.
- Push coordinate space data only when it changes to reduce bandwidth.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class SharedSpaceModel {
    private let session = ARKitSession()
    private let provider = SharedCoordinateSpaceProvider()

    func start() async {
        guard SharedCoordinateSpaceProvider.isSupported else { return }

        let results = await session.requestAuthorization(for: SharedCoordinateSpaceProvider.requiredAuthorizations)
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
