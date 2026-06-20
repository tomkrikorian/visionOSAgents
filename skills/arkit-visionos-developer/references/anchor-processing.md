# Anchor Processing

Use this file when provider updates need to drive app or scene state.

## Rules

- Consume `anchorUpdates` and reconcile added, updated, and removed anchors.
- Normalize anchor IDs in your own state model.
- Treat ARKit streams as authoritative and keep rendering logic separate.
- Avoid mixing entity mutation directly into provider observation code when a
  model layer can own that state more clearly.

## Example

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

## Coordinate Spaces (visionOS 27)

New in visionOS 27: every anchor type — plus `HandSkeleton.Joint` —
conforms to `ARKitCoordinateSpaceProviding`. Call
`coordinateSpace(correction:)` to get an `ARKitCoordinateSpace` and convert
poses through the Spatial framework's coordinate-space system instead of
multiplying `originFromAnchorTransform` matrices by hand. Corrections are
`.none` and `.rendered`. Beta API: names may change before release.

```swift
// New in visionOS 27.
let space = anchor.coordinateSpace(correction: .none)
```
