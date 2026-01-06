# Presentation and UI Components

Examples assume `import RealityKit` and an `Entity` named `entity`. SwiftUI is used where noted.

## ViewAttachmentComponent
Goal: Embeds a SwiftUI view into 3D space.

```swift
import SwiftUI

struct LabelView: View {
    var body: some View {
        Text("Hello")
    }
}

let attachment = ViewAttachmentComponent(rootView: LabelView())
entity.components.set(attachment)
```

## PresentationComponent
Goal: Presents SwiftUI modals or system UI from an entity.

```swift
entity.components.set(PresentationComponent())
```

## TextComponent
Goal: Renders 3D text on an entity.

```swift
let text = TextComponent(<#TextConfiguration#>)
entity.components.set(text)
```

## ImagePresentationComponent
Goal: Displays an image in 3D space.

```swift
let image = ImagePresentationComponent(<#ImageResource#>)
entity.components.set(image)
```

## VideoPlayerComponent
Goal: Plays video on an entity surface.

```swift
import AVFoundation

let player = AVPlayer(url: <#URL#>)
let video = VideoPlayerComponent(player: player)
entity.components.set(video)
```
