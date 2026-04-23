# Session Basics

Use this file when setting up `ARKitSession` or shared provider lifecycle.

## Rules

- Keep one long-lived `ARKitSession` per experience.
- Build the provider list explicitly instead of overloading a shared session.
- Gather each provider type's `requiredAuthorizations`, de-duplicate the
  combined list, and request authorization before `run(_:)`.
- Treat any non-`.allowed` authorization per capability; do not start a
  provider whose required authorization is unavailable.
- Observe `session.events` for authorization changes and provider state
  changes while the session is running.
- Stop the session and cancel observation/update tasks on teardown.
- If `run(_:)` throws, ARKit stops the associated providers. Recreate provider
  instances before retrying, especially after a `.stopped` provider state.
- Follow the presentation requirements documented for the specific provider.

## Example

```swift
import ARKit

@MainActor
final class ARKitManager {
    private let session = ARKitSession()
    private var eventTask: Task<Void, Never>?
    private var worldProvider = WorldTrackingProvider()
    private var planeProvider = PlaneDetectionProvider(alignments: [.horizontal, .vertical])

    func start() async {
        let requiredAuthorizations = Array(Set(
            WorldTrackingProvider.requiredAuthorizations +
            PlaneDetectionProvider.requiredAuthorizations
        ))

        let results = await session.requestAuthorization(for: requiredAuthorizations)
        guard requiredAuthorizations.allSatisfy({ results[$0] == .allowed }) else {
            return
        }

        eventTask = Task { [session] in
            for await event in session.events {
                switch event {
                case .authorizationChanged(let type, let status):
                    print("ARKit authorization changed: \(type) \(status)")
                case .dataProviderStateChanged(_, .stopped, let error):
                    print("ARKit provider stopped: \(String(describing: error))")
                default:
                    break
                }
            }
        }

        do {
            try await session.run([worldProvider, planeProvider])
        } catch {
            // Rebuild provider instances before retrying this run.
            print("ARKitSession run error: \(error)")
        }
    }

    func stop() {
        eventTask?.cancel()
        eventTask = nil
        session.stop()
    }
}
```
