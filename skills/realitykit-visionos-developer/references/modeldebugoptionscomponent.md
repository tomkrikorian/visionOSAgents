# ModelDebugOptionsComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/modeldebugoptionscomponent)

## Overview

Enables debug rendering options for model visualization. This component provides debugging tools to help visualize and diagnose rendering issues, such as wireframe rendering, bounding boxes, and other diagnostic information.

## When to Use

- Debugging rendering issues
- Visualizing model geometry
- Inspecting bounding boxes
- Diagnosing material or lighting problems
- Development and testing phases

## How to Use

### Basic Setup

```swift
import RealityKit

// Enable debug options
entity.components.set(ModelDebugOptionsComponent())
```

### With Specific Options

```swift
// Debug options are typically configured through the component
var debugOptions = ModelDebugOptionsComponent()
// Configure specific debug visualization options
entity.components.set(debugOptions)
```

## Key Properties

- [Debug visualization options configured by the component]

## Important Notes

- Primarily used during development and debugging
- May impact performance when enabled
- Should typically be disabled in production builds
- Helps visualize geometry, materials, and rendering state

## Best Practices

- Use only during development and debugging
- Disable in production for performance
- Use to diagnose rendering and material issues
- Combine with other debugging tools

## Related Components

- `ModelComponent` - The component being debugged
- `ModelSortGroupComponent` - For debugging draw order issues
