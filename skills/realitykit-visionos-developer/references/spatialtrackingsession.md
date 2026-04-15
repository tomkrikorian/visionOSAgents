# SpatialTrackingSession

## Overview

`SpatialTrackingSession` is the RealityKit-side complement to `ARKitSession`.
It lets entities receive anchor-derived transforms (plane, hand, image, world)
without the app running its own `ARKitSession`. RealityKit drives the tracking
session internally and publishes results through `AnchoringComponent`.

Use `SpatialTrackingSession` when the scene only needs AnchoringComponent-based
placement and does not need direct access to ARKit provider streams
(`anchorUpdates`, `HandTrackingProvider`, etc.).

## When to Use

- The entity graph uses `AnchoringComponent` and you want RealityKit to manage
  the underlying tracking automatically.
- You do not need raw anchor data, hand skeleton joints, or other
  provider-specific streams.
- You want a simpler setup than creating and running an `ARKitSession` with
  explicit providers.

## When NOT to Use

- You need direct access to `anchorUpdates` from a specific provider (world
  tracking, hand tracking, plane detection, etc.) — use `ARKitSession` via the
  `arkit-visionos-developer` skill instead.
- You need to request authorization for specific capabilities (hand tracking,
  world sensing) — `SpatialTrackingSession` does not expose the authorization
  flow; use `ARKitSession.requestAuthorization(for:)`.

## Configuration

```swift
import RealityKit

let session = SpatialTrackingSession()
let configuration = SpatialTrackingSession.Configuration(
    tracking: [.plane, .hand, .image, .world]
)
try await session.run(configuration)
```

The `tracking` parameter specifies which anchor types RealityKit should track.
Once the session is running, any `AnchoringComponent` targeting those anchor
types will receive updates automatically.

## Key Types

- `SpatialTrackingSession` — manages the tracking lifecycle.
- `SpatialTrackingSession.Configuration` — specifies which anchor types to
  track.
- `SpatialTrackingSession.UnavailableReason` — returned when a requested
  tracking capability is not available (e.g., missing entitlements, simulator
  limitations).

## Relationship to ARKitSession

| | SpatialTrackingSession | ARKitSession |
|---|---|---|
| Anchor placement via `AnchoringComponent` | Yes (automatic) | Yes (manual bridge via `ARKitAnchorComponent`) |
| Raw anchor streams (`anchorUpdates`) | No | Yes |
| Provider-specific data (hand joints, meshes) | No | Yes |
| Authorization flow | Implicit | Explicit (`requestAuthorization(for:)`) |
| Setup complexity | Lower | Higher |

## References

- `/documentation/RealityKit/SpatialTrackingSession`
- `/documentation/RealityKit/SpatialTrackingSession/Configuration-swift.struct`
