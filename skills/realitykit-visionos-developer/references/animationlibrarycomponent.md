# AnimationLibraryComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/animationlibrarycomponent)

## Overview

A component that represents a collection of animations that an entity can play. You use an `AnimationLibraryComponent` to access an entity's animation resources. You can store animations with an entity by packaging them together into a `.reality` file using Reality Composer Pro or by building a custom tool.

## When to Use

- Storing multiple animations on a single entity
- Organizing character animations (idle, walk, run, etc.)
- Creating animation libraries for reuse
- Loading animations from USD files
- Managing animation playback for characters

## How to Use

### Loading from Reality File

```swift
import RealityKit

// Load entity with animation library
let robot = try await Entity(named: "robot")

// Access the animation library
let animationLibrary = robot.components[AnimationLibraryComponent.self]

// Play an animation by name
if let walkAnimation = animationLibrary?.animations["walk"] {
    robot.playAnimation(walkAnimation)
}
```

### Creating Animation Library Programmatically

```swift
// Create an empty animation library
var animationLibrary = AnimationLibraryComponent()

// Load entities containing animations
let entityIdleAnimation = try await Entity(named: "idle")
let entityWalkAnimation = try await Entity(named: "walk")

// Assign animations to the library by name
animationLibrary.animations["idle"] = entityIdleAnimation.availableAnimations.first
animationLibrary.animations["walk"] = entityWalkAnimation.availableAnimations.first

// Assign to entity
robot.components.set(animationLibrary)
```

### Using Dictionary Literal Syntax

```swift
let animationLibrary = AnimationLibraryComponent(
    animations: [
        "idle": idleAnimation,
        "walk": walkAnimation,
        "run": runAnimation
    ]
)
entity.components.set(animationLibrary)
```

### Playing Animations

```swift
// Play animation by name
if let animation = animationLibrary.animations["walk"] {
    let controller = entity.playAnimation(animation)
    // Control playback with controller
}

// Play default animation
if let defaultAnimation = animationLibrary.defaultAnimation {
    entity.playAnimation(defaultAnimation)
}
```

### Saving Entity with Animations

```swift
// After configuring animation library
robot.components.set(animationLibrary)

// Write entity with animations to file
robot.write(to: fileURL)
```

## Key Properties

- `animations: AnimationLibraryComponent.AnimationCollection` - Collection of animations keyed by name
- `defaultAnimation: AnimationResource?` - The default animation resource
- `defaultKey: String?` - The name of the default animation resource
- `unkeyedResources: [AnimationResource]` - Animations without queryable names

## Important Notes

- Animations are stored by name in a dictionary
- Use Reality Composer Pro to package animations with entities
- Animations can be loaded from USD files
- The library persists when saving entities to `.reality` files
- Access animations using dictionary-style subscripting

## Best Practices

- Use descriptive names for animations (e.g., "idle", "walk", "run")
- Set a default animation for automatic playback
- Load animations asynchronously to avoid blocking
- Store related animations together in one library
- Use `unkeyedResources` for animations that don't need names
- Combine with `CharacterControllerComponent` for character animation

## Related Components

- `CharacterControllerComponent` - For character movement and animation
- `SkeletalPosesComponent` - For skeletal animation data
- `AnimationPlaybackController` - For controlling animation playback
