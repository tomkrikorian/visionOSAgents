# BodyTrackingComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/bodytrackingcomponent)

## Overview

A component that integrates ARKit body tracking data with RealityKit entities. It enables full-body tracking using ARKit's body tracking capabilities, allowing entities to reflect real-world body poses and movements. This component works with ARKit's body tracking configuration to provide skeleton and joint information.

## When to Use

- Creating virtual characters that mirror real-world body movements
- Implementing full-body tracking experiences
- Animating entities based on ARKit body pose data
- Creating avatars that follow user movements
- Building body-tracking-based interactions
- Implementing fitness or movement tracking applications

## How to Use

### Basic Setup with ARKit

```swift
import RealityKit
import ARKit

// Set up ARKit body tracking
let configuration = ARBodyTrackingConfiguration()
arView.session.run(configuration)

// Create entity with body tracking component
let avatar = Entity()
avatar.components.set(BodyTrackingComponent())
```

### Checking Body Tracking Support

```swift
// Check if body tracking is available
if ARBodyTrackingConfiguration.isSupported {
    // Body tracking is supported
    let configuration = ARBodyTrackingConfiguration()
    arView.session.run(configuration)
    
    // Add body tracking component to entity
    entity.components.set(BodyTrackingComponent())
} else {
    // Body tracking not available on this device
}
```

### Accessing Body Tracking Data

```swift
// Entities or systems that conform to HasBodyTracking can access body data
protocol HasBodyTracking {
    var bodyTracking: BodyTrackingComponent? { get }
}

// Access body tracking information
if let bodyTracking = entity.components[BodyTrackingComponent.self] {
    // Access body joints, skeleton, etc.
}
```

## Key Properties

- Properties depend on ARKit body tracking integration
- Provides access to body joints and skeleton information
- Reflects real-world body pose data from ARKit

## Important Notes

- Requires ARKit body tracking support (hardware and software)
- Works with `ARBodyTrackingConfiguration` in ARKit
- Available on supported devices (typically newer iPhones and iPads)
- Requires appropriate Info.plist permissions
- Body tracking data comes from ARKit, not RealityKit directly
- Check `ARBodyTrackingConfiguration.isSupported` before use
- Platform availability may vary - check documentation for your target OS version

## Best Practices

- Check for body tracking support before attempting to use it
- Request appropriate permissions in Info.plist
- Handle cases where body tracking is not available gracefully
- Test on devices that support body tracking
- Consider performance implications of body tracking
- Use body tracking data to drive character animations
- Combine with `SkeletalPosesComponent` for skeleton manipulation
- Update entity poses based on body tracking data each frame

## Related Components

- `SkeletalPosesComponent` - For accessing and modifying skeleton joints based on body tracking
- `AnimationLibraryComponent` - For blending body tracking with keyframe animations
- `AnchoringComponent` - For anchoring body-tracked content
- `ARKitAnchorComponent` - For accessing underlying ARKit anchor data
