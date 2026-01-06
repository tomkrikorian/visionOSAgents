# ARKit visionOS Code Patterns

## Notes
- Run ARKit only in a Full Space (ImmersiveSpace).
- Keep strong references to the session and providers for the lifetime of the feature.

## Provider guides

- [accessory-tracking-provider.md](accessory-tracking-provider.md) - Track supported spatial accessories.
- [barcode-detection-provider.md](barcode-detection-provider.md) - Detect barcode anchors in the environment.
- [camera-frame-provider.md](camera-frame-provider.md) - Stream camera frames for CV or custom rendering.
- [camera-region-provider.md](camera-region-provider.md) - Capture a camera stream for a defined region.
- [environment-light-estimation-provider.md](environment-light-estimation-provider.md) - Match lighting with environment probes.
- [hand-tracking-provider.md](hand-tracking-provider.md) - Track hands and joint poses.
- [image-tracking-provider.md](image-tracking-provider.md) - Track reference images in the environment.
- [object-tracking-provider.md](object-tracking-provider.md) - Track reference objects in space.
- [plane-detection-provider.md](plane-detection-provider.md) - Detect horizontal and vertical planes.
- [room-tracking-provider.md](room-tracking-provider.md) - Track the current room and its surfaces.
- [scene-reconstruction-provider.md](scene-reconstruction-provider.md) - Reconstruct scene meshes.
- [shared-coordinate-space-provider.md](shared-coordinate-space-provider.md) - Share coordinate spaces across participants.
- [stereo-properties-provider.md](stereo-properties-provider.md) - Access stereo viewpoint properties.
- [world-tracking-provider.md](world-tracking-provider.md) - Track device pose and world anchors.

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
