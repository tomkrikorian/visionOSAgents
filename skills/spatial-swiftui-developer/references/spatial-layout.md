# SwiftUI Spatial Layout

## Context

SwiftUI spatial layout APIs let you measure, align, and compose views in three dimensions for visionOS. `GeometryReader3D` reads a view's available size and coordinate space including depth, and returns a flexible preferred size and depth to its parent. `ZStack` composes child depths the way `VStack` composes child heights, and in visionOS 26 can use `spacing` to separate adjacent children along the depth axis. `SpatialContainer` is a layout container that aligns overlapping content in 3D space and sizes itself to the maximum dimension of its children. `spatialOverlay(alignment:content:)` adds secondary views within a view's 3D bounds, stacking multiple overlays depthwise using a `SpatialContainer`. `rotation3DLayout` rotates a view while updating its layout frame to account for the rotation, which can change the view's layout size.

## Best Practices

- Use `GeometryReader3D` only when you need depth measurements; it participates in depth layout and can affect ZStack sizing.
- When layering SwiftUI UI in a `ZStack`, decide whether depth is semantic layout
  or a small visual lift. Use `ZStack(alignment:spacing:)`,
  `frame(depth:alignment:)`, and layout `depthAlignment(_:)` for semantic depth;
  use `offset(z:)` only for fine visual separation.
- Prefer `SpatialContainer` and `Alignment3D` or `DepthAlignment` guides over hard-coded offsets for composable 3D layout.
- Use `.front` depth alignment when text, controls, or labels need to remain
  readable in front of deeper 3D content. Use `.back` when models or panels
  should share a stable rear plane.
- Give fixed-format 3D UI stable depth proposals with
  `frame(depth:alignment:)`; do not let a `RealityView` or resizable `Model3D`
  unexpectedly consume all available depth in a `ZStack`.
- Keep decorative depth shallow. Apple recommends small amounts of depth even in
  windows, but large offsets can increase occlusion, clipping, and visual
  confusion.
- Do not use `zIndex(_:)` as a substitute for spatial depth. `zIndex(_:)`
  changes drawing order; `offset(z:)`, `frame(depth:alignment:)`, ZStack
  spacing, `SpatialContainer`, and `depthAlignment(_:)` express layout depth.
- Use `spatialOverlay` for adornments like labels or selection rings that should live within the same 3D bounds; keep overlays lightweight to avoid occlusion.
- Use `rotation3DLayout` when rotation should affect layout size; use `rotation3DEffect` for purely visual rotation.
- Keep debug helpers like `debugBorder3D` for development only.

## ZStack Depth Decision Guide

- Start with the layout question. If children are true layers in a 3D stack, use
  `ZStack(alignment:spacing:)` so SwiftUI composes the depth and can resize the
  parent correctly.
- If a child needs an explicit depth budget, wrap it in
  `frame(depth:alignment:)` before layering it. This is useful for panels,
  labels, selection affordances, and bounded 3D previews.
- If the whole row or column should align on a depth plane, use
  `HStackLayout().depthAlignment(...)` or `VStackLayout().depthAlignment(...)`
  instead of giving every child its own z offset.
- If an element only needs a hover-like lift or a shadow-card separation, apply
  `offset(z:)` to the element itself and keep the value small.
- If an overlay belongs to a model's bounds, prefer
  `spatialOverlay(alignment:content:)` over a sibling `ZStack` layer.
- If several overlapping elements must be aligned inside one 3D space, prefer
  `SpatialContainer` over nested `ZStack` offsets.
- Check clipping in windows and volumes. Content outside the proposed or fixed
  depth can be clipped by the system.

## Code Examples



#### Robot image frame

```swift
Image("RobotHead")
  .border(.red)
```

#### Color frame

```swift
Color.blue
  .border(.red)
```

#### Layout composed frame

```swift
VStack {
  Image("RobotHead")
    .border(.red)
  Image("RobotHead")
    .border(.red)
}
.border(.yellow)
```

#### Model3D frame

```swift
Model3D(named: "Robot")
  .debugBorder3D(.red)
```

#### Zero depth views

```swift
HStack {
  Image("RobotHead")
    .debugBorder3D(.red)
  Text("Hello! I'm a piece of text. I have 0 depth.")
    .debugBorder3D(.red)
  Color.blue
    .debugBorder3D(.red)
    .frame(width: 200, height: 200)
}
```

#### RealityView depth

```swift
RealityView { content in
  // Setup RealityView content
}
.debugBorder3D(.red)
```

#### GeometryReader3D depth

```swift
GeometryReader3D { proxy in
  // GeometryReader3D content
}
.debugBorder3D(.red)
```

#### Model3D scaledToFit3D

```swift
Model3D(url: robotURL) { resolved in
  resolved.resizable()
} placeholder: {
  ProgressView()
}
.scaledToFit3D()
.debugBorder3D(.red)
```

#### ZStack depth

```swift
ZStack(alignment: .center, spacing: 16) {
  Model3D(named: "LargeRobot")
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

#### Stable card and label depth

```swift
ZStack(alignment: .center, spacing: 8) {
  RoundedRectangle(cornerRadius: 12)
    .fill(.regularMaterial)
    .frame(width: 260, height: 160)
    .frame(depth: 12, alignment: .back)

  Text("Battery 82%")
    .font(.headline)
    .padding(16)
    .glassBackgroundEffect()
    .frame(depth: 4, alignment: .front)
    .offset(z: 6)
}
```

#### Front-aligned controls beside 3D content

```swift
HStackLayout().depthAlignment(.front) {
  Model3D(named: "Robot") { resolved in
    resolved.resizable()
  } placeholder: {
    ProgressView()
  }
  .scaledToFit3D()
  .frame(width: 220, height: 220)

  VStack(alignment: .leading) {
    Text("Robot")
      .font(.title2)
    Button("Inspect") {
      openInspector()
    }
  }
  .glassBackgroundEffect()
}
```

#### ZStack with RealityView

```swift
ZStack {
  RealityView { ... }
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

#### Layouts are 3D

```swift
HStack {
  Model3D(named: "LargeRobot")
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

#### ResizableRobotView

```swift
struct ResizableRobotView: View {
  let asset: Model3DAsset

  var body: some View {
    Model3D(asset: asset) { resolved in
      resolved
        .resizable()
    }
    .scaledToFit3D()
  }
}
```

#### Robot profile layout

```swift
struct RobotProfile: View {
  let robot: Robot

  var body: some View {
    VStack {
      ResizableRobotView(asset: robot.model3DAsset)
      RobotNameCard(robot: robot)
    }
    .frame(width: 300)
  }
}
```

#### Vertical alignment

```swift
HStack(alignment: .bottom) {
  Image("RobotHead")
    .border(.red)
  Color.blue
    .frame(width: 100, height: 100)
    .border(.red)
}
.border(.yellow)
```

#### Depth alignment

```swift
struct RobotProfile: View {
  let robot: Robot

  var body: some View {
    VStackLayout().depthAlignment(.front) {
      ResizableRobotView(asset: robot.model3DAsset)
      RobotNameCard(robot: robot)
    }
    .frame(width: 300)
  }
}
```

#### Favorite robots row

```swift
struct FavoriteRobotsRow: View {
  let robots: [Robot]

  var body: some View {
    HStack {
      RobotProfile(robot: robots[2])
      RobotProfile(robot: robots[0])
      RobotProfile(robot: robots[1])
    }
  }
}
```

#### Custom depth alignment ID

```swift
struct DepthPodiumAlignment: DepthAlignmentID {
  static func defaultValue(in context: ViewDimensions3D) -> CGFloat {
    context[.front]
  }
}

extension DepthAlignment {
  static let depthPodium = DepthAlignment(DepthPodiumAlignment.self)
}
```

#### Customizing depth alignment guides

```swift
struct FavoritesRow: View {
  let robots: [Robot]

  var body: some View {
    HStackLayout().depthAlignment(.depthPodium) {
      RobotProfile(robot: robots[2])
      RobotProfile(robot: robots[0])
        .alignmentGuide(.depthPodium) {
          $0[DepthAlignment.back]
        }
      RobotProfile(robot: robots[1])
        .alignmentGuide(.depthPodium) {
          $0[DepthAlignment.center]
        }
    }
  }
}
```

#### Rotation3DEffect

```swift
Model3D(named: "ToyRocket")
  .rotation3DEffect(.degrees(45), axis: .z)
```

#### Rotation3DLayout

```swift
HStackLayout().depthAlignment(.front) {
  RocketDetailsCard()
  Model3D(named: "ToyRocket")
    .rotation3DLayout(.degrees(isRotated ? 45 : 0), axis: .z)
}
```

#### Pet radial layout

```swift
struct PetRadialLayout: View {
  let pets: [Pet]

  var body: some View {
    MyRadialLayout {
      ForEach(pets) { pet in
        PetImage(pet: pet)
      }
    }
  }
}
```

#### Rotated robot carousel

```swift
struct RobotCarousel: View {
  let robots: [Robot]

  var body: some View {
    VStack {
      Spacer()
      MyRadialLayout {
        ForEach(robots) { robot in
          ResizableRobotView(asset: robot.model3DAsset)
            .rotation3DLayout(.degrees(-90), axis: .x)
        }
      }
      .rotation3DLayout(.degrees(90), axis: .x)
    }
  }
}
```

#### Spatial container

```swift
SpatialContainer(alignment: .topTrailingBack) {
  LargeBox()
  MediumBox()
  SmallBox()
}
```

#### Spatial overlay

```swift
LargeBox()
  .spatialOverlay(alignment: .bottomLeadingFront) {
    SmallBox()
  }
```

#### Selection ring spatial overlay

```swift
struct RobotCarouselItem: View {
  let robot: Robot
  let isSelected: Bool

  var body: some View {
    ResizableRobotView(asset: robot.model3DAsset)
      .spatialOverlay(alignment: .bottom) {
        if isSelected {
          ResizableSelectionRingModel()
        }
      }
  }
}
```

#### DebugBorder3D

```swift
extension View {
  func debugBorder3D(_ color: Color) -> some View {
    spatialOverlay {
      ZStack {
        Color.clear.border(color, width: 4)
        ZStack {
          Color.clear.border(color, width: 4)
          Spacer()
          Color.clear.border(color, width: 4)
        }
        .rotation3DLayout(.degrees(90), axis: .y)
        Color.clear.border(color, width: 4)
      }
    }
  }
}
```
