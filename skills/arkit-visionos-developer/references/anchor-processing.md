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
