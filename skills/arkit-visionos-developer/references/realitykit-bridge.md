# RealityKit Bridge

Use this file when ARKit state needs to become RealityKit content.

## Rules

- Map anchors to RealityKit entities only after the model layer has stable
  state.
- Use `ARKitAnchorComponent` when an entity needs backing anchor data.
- Hand off scene-composition detail to `realitykit-visionos-developer` once the
  tracking model is understood.

## Example

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
