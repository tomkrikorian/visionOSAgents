# ViewAttachmentComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/viewattachmentcomponent)

## Overview

A component containing additional information about a view attachment entity. Use it when you need to create or manage a SwiftUI-backed attachment entity directly in RealityKit, alongside the `RealityView` attachment builder APIs.

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

- `id: AnyHashable` - The identifier used for this view attachment
- `bounds: BoundingBox` - The bounding box of the view attachment, expressed in meters

## Important Notes

- View attachments are transient components - they don't serialize to files
- The view hierarchy is managed by RealityKit and updates automatically
- View attachments are positioned relative to their entity's transform
- `RealityView` attachment builders and `ViewAttachmentComponent` are complementary APIs; choose based on whether the SwiftUI view is declared by `RealityView` or attached directly to an entity

## Best Practices

- Keep view attachments lightweight - complex SwiftUI views can impact performance
- Use view attachments for UI elements that need to stay attached to entities
- Prefer the `RealityView` attachments builder for declarative SwiftUI-defined attachments, and use `ViewAttachmentComponent` when direct entity ownership is more natural
- Use materials and blur effects for better visual integration with 3D content
- Position view attachments carefully to avoid occlusion issues

## Related Components

- `PresentationComponent` - For modal presentations from entities
- `TextComponent` - For 3D text rendering (alternative to SwiftUI text)
