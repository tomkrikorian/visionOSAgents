# visionOS Runtime Loading

Use this file when the question is how authored USD or USDZ content is loaded
in a visionOS app.

## Reality Composer Pro Packages

Reality Composer Pro projects usually ship as a Swift package such as
`RealityKitContent`. Load scenes by prim path and content bundle:

```swift
import RealityKit
import RealityKitContent

let scene = try await Entity(
    named: "Scene",
    in: realityKitContentBundle
)
```

## Raw USDZ Files

For standalone `.usdz` assets bundled with the app, use `Entity(contentsOf:)`
with a bundle URL.

## Runtime Pitfalls

- visionOS expects meters and Y-up for comfortable scale and orientation
- validate shipping assets with `usdchecker --arkit <path>`
- prefer runtime-supported texture formats such as PNG or JPEG when packaging
  USDZ content
