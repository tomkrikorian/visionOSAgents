# Model3D Patterns

## Context

Model3D is a RealityKit view that asynchronously loads and displays a 3D model in SwiftUI. Model3DPhase represents the current loading state, and Model3DAsset is a container for the loaded asset when you need animation metadata or playback control.

## Best Practices

- Use the `content` closure to apply `ResolvedModel3D` modifiers like `resizable()` and `aspectRatio`, not on `Model3D` directly.
- Prefer phase-based initializers when you need explicit placeholder and error handling.
- Use `Model3DAsset` when you need animation selection or playback controls.
- Keep loading asynchronous and supply a lightweight placeholder during fetch.

## Code Examples

### Model3D with phases

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



#### Model3D

```swift
struct ContentView: View {
  var body: some View {
    Model3D(named: "sparky")
  }
}
```

#### Model3D with name sign

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

#### Model3DAsset load

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

#### Model3DAsset with animation picker

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

#### Model3DAsset with animation controls

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

#### Animation playback controls

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

#### ConfigurationCatalog Model3D

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

#### manipulable

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

#### manipulable operations

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

#### manipulable inertia

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
