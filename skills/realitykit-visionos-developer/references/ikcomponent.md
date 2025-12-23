# IKComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/ikcomponent)

## Overview

A component that enables inverse kinematics (IK) for procedural animation on entities with skeletons. IK allows natural joint movement where you specify a target position (e.g., a hand reaching toward an object), and the system automatically adjusts intermediate joints (elbow, shoulder, spine) to achieve the target while respecting constraints.

## When to Use

- Implementing procedural character animation (reaching, pointing, looking)
- Creating natural joint movement that follows targets
- Animating characters to interact with objects dynamically
- Implementing head/eye tracking that follows targets
- Creating procedural animation that blends with keyframe animation
- Building interactive characters that respond to user input

## How to Use

### Basic IK Setup

```swift
import RealityKit

// Create IK rig resource
let ikRig = IKRig(
    skeleton: skeletonResource,
    solverSettings: IKSolverSettings(
        maxIterations: 30,
        globalFkWeight: 0.5  // Blend between FK and IK
    )
)

let ikResource = IKResource(rig: ikRig)
let ikComponent = IKComponent(resource: ikResource)
entity.components.set(ikComponent)
```

### Creating IK Constraints

```swift
// Create point constraint for hand reaching
let handConstraint = IKConstraint.point(
    target: targetEntity.position,
    jointName: "hand"
)

// Create parent constraint to limit joint movement
let elbowConstraint = IKConstraint.parent(
    jointName: "elbow",
    limits: .range(min: -0.5, max: 0.5)
)

// Add constraints to IK component
var ik = entity.components[IKComponent.self]
ik?.constraints = [handConstraint, elbowConstraint]
entity.components[IKComponent.self] = ik
```

### Updating IK Targets

```swift
// Update IK target each frame
func updateIKTarget(to position: SIMD3<Float>) {
    guard var ik = entity.components[IKComponent.self] else { return }
    
    // Update point constraint target
    if let pointConstraint = ik.constraints.first(where: { $0.jointName == "hand" }) as? IKPointConstraint {
        pointConstraint.target = position
    }
    
    entity.components[IKComponent.self] = ik
}
```

### Head Following Target

```swift
// Make character head follow a target (e.g., butterfly)
func setupHeadTracking(target: Entity) {
    let ikRig = IKRig(skeleton: characterSkeleton)
    let ikResource = IKResource(rig: ikRig)
    var ik = IKComponent(resource: ikResource)
    
    // Create constraint for head joint
    let headConstraint = IKConstraint.point(
        target: target.position,
        jointName: "head"
    )
    ik.constraints = [headConstraint]
    
    characterEntity.components.set(ik)
    
    // Update target each frame
    Task {
        while true {
            if var ik = characterEntity.components[IKComponent.self] {
                // Update target position
                ik.constraints[0].target = target.position
                characterEntity.components[IKComponent.self] = ik
            }
            try? await Task.sleep(for: .milliseconds(16))  // ~60fps
        }
    }
}
```

## Key Properties

- `resource: IKResource` - The IK resource containing the rig and solver settings
- `constraints: [IKConstraint]` - Array of IK constraints (point, parent, etc.)

### IKRig Properties

- `skeleton: SkeletonResource` - The skeleton to apply IK to
- `solverSettings: IKSolverSettings` - Solver configuration

### IKSolverSettings

- `maxIterations: Int` - Maximum solver iterations (e.g., 30)
- `globalFkWeight: Float` - How much forward kinematics (normal animation) has influence versus IK corrections (0.0 = full IK, 1.0 = full FK)

### IKConstraint Types

- `.point(target:position:jointName:)` - Point constraint for reaching toward a target
- `.parent(jointName:limits:)` - Parent constraint to limit joint movement

## Important Notes

- Requires a skeleton (skinned mesh) on the entity
- IK blends with forward kinematics (FK) based on `globalFkWeight`
- Constraints define targets and limits for joint movement
- IK is computed each frame based on current constraints
- Available on iOS, macOS, and visionOS (introduced in WWDC 2024)
- Works with `SkeletalPosesComponent` for joint manipulation
- Can be combined with `AnimationLibraryComponent` for blended animation

## Best Practices

- Set appropriate `maxIterations` for performance vs accuracy tradeoff
- Use `globalFkWeight` to blend IK with keyframe animation
- Update IK targets each frame for smooth following behavior
- Use constraints to limit joint movement for natural-looking results
- Test IK behavior with various target positions
- Consider performance when using IK on multiple characters
- Combine with `SkeletalPosesComponent` for additional joint control

## Related Components

- `SkeletalPosesComponent` - For accessing and modifying joint transforms
- `AnimationLibraryComponent` - For keyframe animations that blend with IK
- `ModelComponent` - The mesh component that uses the skeleton
- `CharacterControllerComponent` - For character movement (can use IK for upper body)
