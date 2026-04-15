# Session Basics

Use this file when setting up `ARKitSession` or shared provider lifecycle.

## Rules

- Keep one long-lived `ARKitSession` per experience.
- Build the provider list explicitly instead of overloading a shared session.
- Request the required authorizations before `run(_:)`.
- Stop the session and cancel observation tasks on teardown.
- Follow the presentation requirements documented for the specific provider.

## Example

```swift
import ARKit

@MainActor
final class ARKitManager {
    private let session = ARKitSession()
    private let planeProvider = PlaneDetectionProvider(alignments: [.horizontal, .vertical])

    func start() async {
        let results = await session.requestAuthorization(for: PlaneDetectionProvider.requiredAuthorizations)
        let allowed = results.values.allSatisfy { $0 == .allowed }
        guard allowed else { return }

        do {
            try await session.run([planeProvider])
        } catch {
            print("ARKitSession run error: \(error)")
        }
    }

    func stop() {
        session.stop()
    }
}
```
