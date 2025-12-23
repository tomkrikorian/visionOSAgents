# ViewAttachmentComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/viewattachmentcomponent)

## Overview

A component containing additional information about a view attachment entity provided via the `Attachment` function. This component manages a SwiftUI view hierarchy embedded in 3D space, allowing you to place SwiftUI UI elements directly in your RealityKit scene.

## When to Use

- Embedding SwiftUI views in 3D space
- Creating 3D UI overlays and labels
- Displaying interactive SwiftUI controls in spatial experiences
- Adding text labels or information panels to entities
- Creating spatial UI elements that respond to SwiftUI state

## How to Use

### Basic View Attachment

```swift
import RealityKit
import SwiftUI

struct LabelView: View {
    var body: some View {
        Text("Hello, World!")
            .padding()
            .background(.ultraThinMaterial)
    }
}

let attachment = ViewAttachmentComponent(rootView: LabelView())
entity.components.set(attachment)
```

### View Attachment with RealityView

```swift
RealityView { content in
    let entity = Entity()
    
    let attachment = ViewAttachmentComponent(rootView: {
        VStack {
            Text("Entity Info")
            Button("Action") {
                // Handle action
            }
        }
        .padding()
    })
    
    entity.components.set(attachment)
    content.add(entity)
}
```

### Dynamic View Updates

```swift
struct DynamicLabelView: View {
    @State var count: Int = 0
    
    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
        .padding()
    }
}

let attachment = ViewAttachmentComponent(rootView: DynamicLabelView())
entity.components.set(attachment)
```

## Key Properties

- `id: UUID` - The identifier used for this view attachment
- `bounds: BoundingBox` - The bounding box of the view attachment, expressed in meters

## Important Notes

- View attachments are transient components - they don't serialize to files
- The view hierarchy is managed by RealityKit and updates automatically
- View attachments are positioned relative to their entity's transform
- Use this instead of the `RealityView` attachments closure for better performance

## Best Practices

- Keep view attachments lightweight - complex SwiftUI views can impact performance
- Use view attachments for UI elements that need to stay attached to entities
- Prefer `ViewAttachmentComponent` over the `RealityView` attachments closure
- Use materials and blur effects for better visual integration with 3D content
- Position view attachments carefully to avoid occlusion issues

## Related Components

- `PresentationComponent` - For modal presentations from entities
- `TextComponent` - For 3D text rendering (alternative to SwiftUI text)
