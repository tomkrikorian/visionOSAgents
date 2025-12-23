# PresentationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/presentationcomponent)

## Overview

A component that integrates SwiftUI content as modal presentations (popovers, sheets, etc.) into RealityKit entities. This helps bridge 2D SwiftUI view content into 3D spatial contexts, allowing entities to present SwiftUI modals or system UI in a spatially-aware manner.

## When to Use

- Presenting SwiftUI modals from 3D entities
- Showing popovers or sheets triggered by entity interactions
- Integrating SwiftUI UI into spatial experiences
- Creating interactive UI that appears from entities
- Presenting system UI from spatial interactions
- Building spatially-aware presentation flows

## How to Use

### Basic Setup

```swift
import RealityKit
import SwiftUI

// Create presentation component with popover
let presentation = PresentationComponent(
    configuration: .popover(arrowEdge: .bottom),
    content: {
        VStack {
            Text("Entity Info")
            Button("Close") { }
        }
        .padding()
    }
)
entity.components.set(presentation)
```

### With Popover

```swift
// Create popover presentation
let presentation = PresentationComponent(
    configuration: .popover(arrowEdge: .top),
    content: {
        MySwiftUIView()
    }
)
entity.components.set(presentation)

// Toggle presentation
if var presentation = entity.components[PresentationComponent.self] {
    presentation.isPresented = true
    entity.components[PresentationComponent.self] = presentation
}
```

### Sheet Presentation

```swift
// Create sheet presentation
let presentation = PresentationComponent(
    configuration: .sheet,
    content: {
        NavigationView {
            MyDetailView()
        }
    }
)
entity.components.set(presentation)
```

## Key Properties

- `configuration: PresentationComponent.Configuration` - Presentation configuration (popover, sheet, etc.)
- `content: () -> some View` - SwiftUI view content to present
- `isPresented: Bool` - Boolean to toggle the presentation on/off

### Configuration Types

- `.popover(arrowEdge:)` - Popover presentation with arrow edge
- `.sheet` - Sheet presentation
- Other presentation types as available

## Important Notes

- Introduced in recent RealityKit releases (WWDC 2025)
- Allows 3D entities to show SwiftUI content in spatially-aware presentation modes
- Works in spatial contexts and immersive spaces
- Available on visionOS and other Apple platforms
- Bridges SwiftUI UI into RealityKit spatial experiences

## Best Practices

- Use appropriate presentation configuration for your use case
- Toggle `isPresented` to show/hide presentations
- Design SwiftUI content to work well in spatial contexts
- Test presentation behavior in immersive spaces
- Consider spatial positioning when presenting from entities
- Use for modal UI that should appear from entity interactions

## Related Components

- `ViewAttachmentComponent` - For embedding SwiftUI views directly in 3D space
- `InputTargetComponent` - For making entities interactive to trigger presentations
- `ImagePresentationComponent` - For displaying images
- `VideoPlayerComponent` - For video playback
