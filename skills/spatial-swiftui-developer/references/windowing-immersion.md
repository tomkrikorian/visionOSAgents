# Windowing and Immersive Spaces

## Context

WindowGroup is a scene that presents a group of identically structured windows. ImmersiveSpace presents content in an unbounded space on visionOS, and RemoteImmersiveSpace presents an unbounded space on a remote device.

## Best Practices

- Use explicit `id` values for WindowGroup and ImmersiveSpace so you can open them programmatically.
- Keep windows and volumes in WindowGroup scenes and immersive content in ImmersiveSpace scenes.
- Set `windowStyle(.volumetric)` and `defaultSize` for volumes to ensure consistent physical scale.
- Open and dismiss immersive spaces using the environment actions; only one immersive space can be open at a time.
- Use RemoteImmersiveSpace for macOS apps that present compositor content on visionOS hardware.

## Code Examples

### ImmersiveSpace open and dismiss

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

### Volumetric WindowGroup

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



#### Disabling restoration

```swift
WindowGroup("Tools", id: "tools") {
  ToolsView()
}
.restorationBehavior(.disabled)
```

#### Disabling restoration in UIKit

```swift
windowScene.destructionConditions = [
  .systemDisconnection
]
```

#### Specifying launch window

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

#### Suppressed launch behavior

```swift
WindowGroup("Tools", id: "tools") {
  ToolsView()
}
.restorationBehavior(.disabled)
.defaultLaunchBehavior(.suppressed)
```

#### Unique window

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

#### Surface snapping

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

#### Clipping margins

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

#### World recenter

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

#### Progressive immersion style

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

#### Mixed immersion style

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

#### Remote immersive space

```swift
RemoteImmersiveSpace(id: "preview-space") {
  CompositorLayer(configuration: config) { /* ... */ }
}

WindowGroup("Main Stage", id: "main") {
  StageView()
}
```

#### CompositorLayer is CompositorContent

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

#### Scene bridging

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
