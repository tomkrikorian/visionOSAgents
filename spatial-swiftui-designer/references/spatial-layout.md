# SwiftUI Spatial Layout

## WWDC 2025: Meet SwiftUI spatial layout

Session link: https://developer.apple.com/videos/play/wwdc2025/273/

### 3-02 Robot image frame

```swift
Image("RobotHead")
  .border(.red)
```

### 3-05 Color frame

```swift
Color.blue
  .border(.red)
```

### 3-15 Layout composed frame

```swift
VStack {
  Image("RobotHead")
    .border(.red)
  Image("RobotHead")
    .border(.red)
}
.border(.yellow)
```

### 4-00 Model3D frame

```swift
Model3D(named: "Robot")
  .debugBorder3D(.red)
```

### 4-25 Zero depth views

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

### 4-41 RealityView depth

```swift
RealityView { content in
  // Setup RealityView content
}
.debugBorder3D(.red)
```

### 4-56 GeometryReader3D depth

```swift
GeometryReader3D { proxy in
  // GeometryReader3D content
}
.debugBorder3D(.red)
```

### 5-01 Model3D scaledToFit3D

```swift
Model3D(url: robotURL) { resolved in
  resolved.resizable()
} placeholder: {
  ProgressView()
}
.scaledToFit3D()
.debugBorder3D(.red)
```

### 6-15 ZStack depth

```swift
ZStack {
  Model3D(named: "LargeRobot")
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

### 6-33 ZStack with RealityView

```swift
ZStack {
  RealityView { ... }
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

### 6-57 Layouts are 3D

```swift
HStack {
  Model3D(named: "LargeRobot")
    .debugBorder3D(.red)
  Model3D(named: "BabyBot")
    .debugBorder3D(.red)
}
.debugBorder3D(.yellow)
```

### 7-50 ResizableRobotView

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

### 8-11 Robot profile layout

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

### 8-38 Vertical alignment

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

### 8-52 Depth alignment

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

### 9-45 Favorite robots row

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

### 10-27 Custom depth alignment ID

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

### 10-51 Customizing depth alignment guides

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

### 12-00 Rotation3DEffect

```swift
Model3D(named: "ToyRocket")
  .rotation3DEffect(.degrees(45), axis: .z)
```

### 12-10 Rotation3DLayout

```swift
HStackLayout().depthAlignment(.front) {
  RocketDetailsCard()
  Model3D(named: "ToyRocket")
    .rotation3DLayout(.degrees(isRotated ? 45 : 0), axis: .z)
}
```

### 14-42 Pet radial layout

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

### 14-56 Rotated robot carousel

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

### 17-00 Spatial container

```swift
SpatialContainer(alignment: .topTrailingBack) {
  LargeBox()
  MediumBox()
  SmallBox()
}
```

### 17-35 Spatial overlay

```swift
LargeBox()
  .spatialOverlay(alignment: .bottomLeadingFront) {
    SmallBox()
  }
```

### 17-47 Selection ring spatial overlay

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

### 18-32 DebugBorder3D

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
