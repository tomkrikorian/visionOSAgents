# Model3D Patterns

## Notes
- Use Model3D for SwiftUI-driven model presentation and layout.
- Load assets asynchronously and handle loading phases explicitly.

## Model3D with phases

```swift
import RealityKit
import SwiftUI

struct Model3DExample: View {
    let url = URL(string: "https://example.com/robot.usdz")!

    var body: some View {
        Model3D(url: url) { phase in
            if let model = phase.model {
                model
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            } else if phase.error != nil {
                Color.red
            } else {
                ProgressView()
            }
        }
        .frame(width: 300, height: 300)
    }
}
```

## WWDC 2025: Better together: SwiftUI and RealityKit (Model3D)

Session link: https://developer.apple.com/videos/play/wwdc2025/274/

### 1-42 Model3D

```swift
struct ContentView: View {
  var body: some View {
    Model3D(named: "sparky")
  }
}
```

### 1-52 Model3D with name sign

```swift
struct ContentView: View {
  var body: some View {
    HStack {
      NameSign()
      Model3D(named: "sparky")
    }
  }
}
```

### 3-18 Model3DAsset load

```swift
struct RobotView: View {
  @State private var asset: Model3DAsset?
  var body: some View {
    if asset == nil {
      ProgressView().task { asset = try? await Model3DAsset(named: "sparky") }
    }
  }
}
```

### 3-34 Model3DAsset with animation picker

```swift
struct RobotView: View {
  @State private var asset: Model3DAsset?
  var body: some View {
    if asset == nil {
      ProgressView().task { asset = try? await Model3DAsset(named: "sparky") }
    } else if let asset {
      VStack {
        Model3D(asset: asset)
        AnimationPicker(asset: asset)
      }
    }
  }
}
```

### 4-03 Model3DAsset with animation controls

```swift
struct RobotView: View {
  @State private var asset: Model3DAsset?
  var body: some View {
    if asset == nil {
      ProgressView().task { asset = try? await Model3DAsset(named: "sparky") }
    } else if let asset {
      VStack {
        Model3D(asset: asset)
        AnimationPicker(asset: asset)
        if let animationController = asset.animationPlaybackController {
          RobotAnimationControls(playbackController: animationController)
        }
      }
    }
  }
}
```

### 4-32 Animation playback controls

```swift
struct RobotAnimationControls: View {
  @Bindable var controller: AnimationPlaybackController

  var body: some View {
    HStack {
      Button(controller.isPlaying ? "Pause" : "Play") {
        if controller.isPlaying { controller.pause() }
        else { controller.resume() }
      }

      Slider(
        value: $controller.time,
        in: 0...controller.duration
      ).id(controller)
    }
  }
}
```

### 5-41 ConfigurationCatalog Model3D

```swift
struct ConfigCatalogExample: View {
  @State private var configCatalog: Entity.ConfigurationCatalog?
  @State private var configurations = [String: String]()
  @State private var showConfig = false
  var body: some View {
    if let configCatalog {
      Model3D(from: configCatalog, configurations: configurations)
        .popover(isPresented: $showConfig, arrowEdge: .leading) {
          ConfigPicker(
            name: "outfits",
            configCatalog: configCatalog,
            chosenConfig: $configurations["outfits"])
        }
    } else {
      ProgressView()
        .task {
          await loadConfigurationCatalog()
        }
    }
  }
}
```

### 12-30 manipulable

```swift
struct RobotView: View {
  let url: URL
  var body: some View {
    HStack {
      NameSign()
      Model3D(url: url)
        .manipulable()
    }
  }
}
```

### 12-33 manipulable operations

```swift
struct RobotView: View {
  let url: URL
  var body: some View {
    HStack {
      NameSign()
      Model3D(url: url)
        .manipulable(
          operations: [.translation,
                       .primaryRotation,
                       .secondaryRotation]
       )
    }
  }
}
```

### 12-41 manipulable inertia

```swift
struct RobotView: View {
  let url: URL
  var body: some View {
    HStack {
      NameSign()
      Model3D(url: url)
        .manipulable(inertia: .high)
    }
  }
}
```
