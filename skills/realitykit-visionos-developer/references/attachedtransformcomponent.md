# AttachedTransformComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/attachedtransformcomponent)

## Overview

A component that attaches an entity's transform to another entity for hierarchical positioning. This allows you to create transform relationships between entities where one entity's position, rotation, and scale are relative to another entity, enabling complex hierarchical transformations.

## When to Use

- Creating hierarchical transform relationships between entities
- Attaching entity transforms to other entities
- Implementing relative positioning systems
- Creating parent-child transform relationships
- Building complex entity hierarchies with transform dependencies

## How to Use

### Basic Setup

```swift
import RealityKit

// Attach entity transform to another entity
let attachedTransform = AttachedTransformComponent()
entity.components.set(attachedTransform)
```

**Note:** This component's API may vary by RealityKit version. An alternative approach is to use entity hierarchy with `entity.addChild()` where child entities automatically have transforms relative to their parent.

### Alternative: Entity Hierarchy

```swift
// Use entity hierarchy for relative transforms
let parent = Entity()
let child = Entity()
parent.addChild(child)  // Child transform is relative to parent

// Position child relative to parent
child.position = [1, 0, 0]  // Relative to parent
```

## Key Properties

- Properties may include target entity reference, transform offset, or attachment configuration
- Consult official documentation for specific API details

## Important Notes

- May not be fully documented in all RealityKit versions
- Alternative: use entity hierarchy (`addChild`) for relative transforms
- Child entities automatically have transforms relative to their parent
- Available on visionOS, iOS, and other Apple platforms
- Check official documentation for your target SDK version

## Best Practices

- Consider using entity hierarchy for relative transforms
- Use `entity.addChild()` to create parent-child relationships
- Child entity transforms are automatically relative to parent
- Test transform behavior on target platforms
- Use appropriate transform relationships for your use case

## Related Components

- Entity hierarchy - Use `addChild()` for relative transforms
- `Transform` - Built-in transform component on all entities
