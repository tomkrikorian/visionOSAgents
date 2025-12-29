# ARKit visionOS Code Patterns

## Notes
- Run ARKit only in a Full Space (ImmersiveSpace).
- Keep strong references to the session and providers for the lifetime of the feature.

## Session setup with explicit authorization

```swift
import ARKit
import SwiftUI

@MainActor
final class ARKitManager {
    private let session = ARKitSession()
    private let planeProvider = PlaneDetectionProvider(alignments: [.horizontal, .vertical])

    func start() async {
        let results = await session.requestAuthorization(for: planeProvider.requiredAuthorizations)
        let allowed = results.values.allSatisfy { $0 == .allowed }
        guard allowed else {
            return
        }

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

## Listen for session events

```swift
Task {
    for await event in session.events {
        switch event {
        case .authorizationChanged:
            break
        case .dataProviderStateChanged:
            break
        @unknown default:
            break
        }
    }
}
```

## Consume anchor updates

```swift
Task {
    for await update in planeProvider.anchorUpdates {
        switch update.event {
        case .added:
            addPlaneAnchor(update.anchor)
        case .updated:
            updatePlaneAnchor(update.anchor)
        case .removed:
            removePlaneAnchor(update.anchor)
        }
    }
}
```

## Map anchors to RealityKit entities

```swift
import RealityKit

final class AnchorStore {
    private var entitiesByAnchorID: [UUID: Entity] = [:]

    func upsertEntity(for anchorID: UUID) -> Entity {
        if let entity = entitiesByAnchorID[anchorID] {
            return entity
        }

        let entity = Entity()
        entitiesByAnchorID[anchorID] = entity
        return entity
    }

    func removeEntity(for anchorID: UUID) {
        entitiesByAnchorID[anchorID] = nil
    }
}
```
