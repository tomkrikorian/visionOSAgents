# SkeletalPosesComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/skeletalposescomponent)

## Overview

A component that provides direct access to a skeleton's joints in a `ModelEntity`, allowing you to manipulate joint transforms (rotation, translation, scale) manually or query them. Entities with a skinned mesh imported from USD files usually already have this component attached. It's useful for skeletal pose animation, modifying poses at runtime, or procedural animation.

## When to Use

- Manipulating joint transforms manually for procedural animation
- Creating custom skeletal poses at runtime
- Attaching entities to skeleton joints
- Querying joint transforms for animation or physics
- Implementing procedural character animation
- Rotating joints to follow targets (e.g., head following an object)

## How to Use

### Accessing Joint Transforms

```swift
import RealityKit

// Access skeletal poses component
if let poses = entity.components[SkeletalPosesComponent.self],
   let jointTransforms = poses.poses.default?.jointTransforms {
    
    // Access specific joint transform
    let neckJointIndex = 5  // Example joint index
    if neckJointIndex < jointTransforms.count {
        var transform = jointTransforms[neckJointIndex]
        // Modify transform (rotation, translation, scale)
        transform.rotation = newRotation
        jointTransforms[neckJointIndex] = transform
    }
}
```

### Rotating Joint to Follow Target

```swift
// Rotate neck joint to follow a target (e.g., butterfly)
func updateNeckRotation(to target: Entity) {
    guard let poses = entity.components[SkeletalPosesComponent.self],
          let jointTransforms = poses.poses.default?.jointTransforms else { return }
    
    let neckIndex = findJointIndex(named: "neck")
    guard neckIndex < jointTransforms.count else { return }
    
    // Calculate rotation to look at target
    let direction = normalize(target.position - entity.position)
    let rotation = simd_quatf(from: [0, 0, -1], to: direction)
    
    // Update joint transform
    var transform = jointTransforms[neckIndex]
    transform.rotation = rotation
    jointTransforms[neckIndex] = transform
}
```

### Attaching Entity to Joint

```swift
// Attach an entity to a skeleton joint
func attachToJoint(_ entity: Entity, jointName: String, on skeleton: Entity) {
    guard let poses = skeleton.components[SkeletalPosesComponent.self],
          let jointTransforms = poses.poses.default?.jointTransforms else { return }
    
    let jointIndex = findJointIndex(named: jointName)
    guard jointIndex < jointTransforms.count else { return }
    
    // Get joint transform in world space
    let jointTransform = jointTransforms[jointIndex]
    
    // Attach entity to joint
    entity.transform = jointTransform
    skeleton.addChild(entity)
}
```

## Key Properties

- `poses: SkeletalPoses` - Collection of skeletal poses
- `poses.default` - The default pose
- `poses.default?.jointTransforms` - Array of joint transforms (rotation, translation, scale)
- Each joint transform is in local space relative to its parent joint

## Important Notes

- Automatically attached to entities with skinned meshes from USD files
- Joint transforms are in local space (relative to parent joint)
- You can modify joint transforms at runtime for procedural animation
- Changes to joint transforms affect the mesh deformation immediately
- Available on iOS, macOS, and visionOS
- Works with skeletal animation and `AnimationLibraryComponent`

## Best Practices

- Access joint transforms through the component's poses structure
- Modify joint transforms in local space for correct hierarchy behavior
- Update joint transforms each frame for smooth procedural animation
- Use joint names or indices to find specific joints
- Combine with `IKComponent` for inverse kinematics
- Test joint modifications to ensure natural-looking movement
- Consider performance when modifying many joints per frame

## Related Components

- `AnimationLibraryComponent` - For storing and playing skeletal animations
- `IKComponent` - For inverse kinematics (often used together)
- `ModelComponent` - The mesh component that uses the skeleton
- `BlendShapeWeightsComponent` - For blend shape animation (different from skeletal)
