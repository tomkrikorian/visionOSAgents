# Windowing and Immersive Spaces

## Notes
- Use WindowGroup with explicit IDs and window styles for spatial presentation.
- Treat ImmersiveSpace as a separate scene with its own lifecycle.

## ImmersiveSpace open and dismiss

```swift
import SwiftUI

struct ImmersiveControls: View {
    @Environment(\.openImmersiveSpace) private var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) private var dismissImmersiveSpace

    var body: some View {
        HStack {
            Button("Open") {
                Task { await openImmersiveSpace(id: "space") }
            }
            Button("Close") {
                Task { await dismissImmersiveSpace() }
            }
        }
    }
}
```

## Volumetric WindowGroup

```swift
import SwiftUI

@main
struct VolumeApp: App {
    var body: some Scene {
        WindowGroup(id: "Volume") {
            ContentView()
        }
        .windowStyle(.volumetric)
        .defaultSize(width: 0.6, height: 0.6, depth: 0.6, in: .meters)
    }
}
```

## WWDC 2025: Set the scene with SwiftUI in visionOS

Session link: https://developer.apple.com/videos/play/wwdc2025/290/

### 4-10 Disabling restoration

```swift
WindowGroup("Tools", id: "tools") {
  ToolsView()
}
.restorationBehavior(.disabled)
```

### 4-36 Disabling restoration in UIKit

```swift
windowScene.destructionConditions = [
  .systemDisconnection
]
```

### 5-02 Specifying launch window

```swift
@AppStorage("isFirstLaunch") private var isFirstLaunch = true

var body: some Scene {
  WindowGroup("Stage Selection", id: "selection") {
    SelectionView()
  }

  WindowGroup("Welcome", id: "welcome") {
    WelcomeView()
      .onAppear {
        isFirstLaunch = false
      }
  }
  .defaultLaunchBehavior(isFirstLaunch ? .presented : .automatic)
}
```

### 6-39 Suppressed launch behavior

```swift
WindowGroup("Tools", id: "tools") {
  ToolsView()
}
.restorationBehavior(.disabled)
.defaultLaunchBehavior(.suppressed)
```

### 7-44 Unique window

```swift
@AppStorage("isFirstLaunch") private var isFirstLaunch = true

var body: some Scene {
  Window("Welcome", id: "welcome") {
    WelcomeView()
      .onAppear {
        isFirstLaunch = false
      }
  }
  .defaultLaunchBehavior(isFirstLaunch ? .presented : .automatic)

  WindowGroup("Main Stage", id: "main") {
    StageView()
  }
}
```

### 10-24 Surface snapping

```swift
@Environment(\.surfaceSnappingInfo) private var snappingInfo
@State private var hidePlatform = false

var body: some View {
  RealityView { /* ... */ }
    .onChange(of: snappingInfo) { _, newValue in
      if newValue.isSnapped &&
          SurfaceSnappingInfo.authorizationStatus == .authorized
      {
        switch newValue.classification {
        case .table:
          hidePlatform = true
        default:
          hidePlatform = false
        }
      }
    }
}
```

### 14-41 Clipping margins

```swift
@Environment(\.windowClippingMargins) private var windowMargins
@PhysicalMetric(from: .meters) private var pointsPerMeter = 1

var body: some View {
  RealityView { content in
    // ...
    waterfall = createWaterfallEntity()
    content.add(waterfall)
  } update: { content in
    waterfall.scale.y = Float(min(
      windowMargins.bottom / pointsPerMeter,
      maxWaterfallHeight))
    // ...
  }
  .preferredWindowClippingMargins(.bottom, maxWaterfallHeight * pointsPerMeter)
}
```

### 16-44 World recenter

```swift
var body: some View {
  RealityView { content in
    // ...
  }
  .onWorldRecenter {
    recomputePositions()
  }
}
```

### 17-58 Progressive immersion style

```swift
@State private var selectedStyle: ImmersionStyle = .progressive

var body: some Scene {
  ImmersiveSpace(id: "space") {
    ImmersiveView()
  }
  .immersionStyle(
    selection: $selectedStyle,
    in: .progressive(aspectRatio: .portrait))
}
```

### 18-37 Mixed immersion style

```swift
@State private var selectedStyle: ImmersionStyle = .progressive

var body: some Scene {
  ImmersiveSpace(id: "space") {
    ImmersiveView()
  }
  .immersionStyle(selection: $selectedStyle, in: .mixed)
  .immersiveEnvironmentBehavior(.coexist)
}
```

### 20-14 Remote immersive space

```swift
RemoteImmersiveSpace(id: "preview-space") {
  CompositorLayer(configuration: config) { /* ... */ }
}

WindowGroup("Main Stage", id: "main") {
  StageView()
}
```

### 20-48 CompositorLayer is CompositorContent

```swift
struct ImmersiveContent: CompositorContent {
  @Environment(\.scenePhase) private var scenePhase

  var body: some CompositorContent {
    CompositorLayer { renderer in
      // ...
    }
    .onImmersionChange { oldImmersion, newImmersion in
      // ...
    }
  }
}
```

### 23-00 Scene bridging

```swift
import UIKit
import SwiftUI

class MyHostingSceneDelegate: NSObject, UIHostingSceneDelegate {
  static var rootScene: some Scene {
    WindowGroup(id: "my-volume") {
      ContentView()
    }
    .windowStyle(.volumetric)
  }
}

func openMyVolumeScene() {
  guard let requestWithId = UISceneSessionActivationRequest(
    hostingDelegateClass: MyHostingSceneDelegate.self,
    id: "my-volume")
  else {
    return
  }

  UIApplication.shared.activateSceneSession(for: requestWithId)
}
```
