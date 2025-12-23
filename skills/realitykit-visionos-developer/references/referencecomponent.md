# ReferenceComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/referencecomponent)

## Overview

A component that references an external entity asset for lazy loading. This component allows you to defer loading of entity assets until they are needed, improving initial load times and memory usage. Entities can reference other entities in external files that are loaded on demand.

## When to Use

- Implementing lazy loading of entity assets
- Referencing entities in external files
- Reducing initial load times by deferring asset loading
- Managing memory usage by loading assets on demand
- Creating references to entities in other Reality files
- Building large scenes with many assets

## How to Use

### Basic Setup

```swift
import RealityKit

// Create reference component
let reference = ReferenceComponent()
entity.components.set(reference)
```

**Note:** This component's API may vary by RealityKit version. For lazy loading, you can also use `Entity(named:in:)` to load entities on demand from Reality files or USDZ assets.

### Alternative: Lazy Loading Pattern

```swift
// Load entity on demand
func loadEntityWhenNeeded() async {
    let entity = try await Entity(named: "ExternalEntity", in: bundle)
    // Use entity...
}
```

## Key Properties

- Properties may include reference path, asset location, or loading configuration
- Consult official documentation for specific API details for your RealityKit version

## Important Notes

- Allows deferring entity asset loading until needed
- May not be fully documented in all RealityKit versions
- Alternative approach: use `Entity(named:in:)` for on-demand loading
- Available on visionOS, iOS, and other Apple platforms
- Check official documentation for your target SDK version

## Best Practices

- Use for large scenes where not all assets are needed immediately
- Load referenced entities asynchronously to avoid blocking
- Handle loading errors appropriately
- Consider memory usage when loading many referenced entities
- Test lazy loading behavior on target devices
- Use `Entity(named:in:)` as an alternative if component is not available

## Related Components

- `ModelComponent` - Referenced entities may contain models
- `AnchoringComponent` - Referenced entities may be anchored
