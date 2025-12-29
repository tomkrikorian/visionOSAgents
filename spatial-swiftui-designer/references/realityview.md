# RealityView Patterns

## Notes
- Use RealityView for full RealityKit scene control and per-frame updates.
- Load entities asynchronously and mutate them in the make/update closures.

## RealityView basics

```swift
import RealityKit
import SwiftUI

struct RealityViewExample: View {
    var body: some View {
        RealityView { content in
            do {
                let entity = try await Entity(named: "Scene")
                content.add(entity)
            } catch {
                print("Failed to load entity: \(error)")
            }
        } update: { content in
            // Update entities based on SwiftUI state.
        }
    }
}
```

## RealityView with SwiftUI attachments

```swift
import RealityKit
import SwiftUI

struct AttachmentExample: View {
    var body: some View {
        RealityView { content, attachments in
            if let panel = attachments.entity(for: "panel") {
                content.add(panel)
            }
        } update: { content, attachments in
            if let panel = attachments.entity(for: "panel") {
                panel.position = [0, 1, -1]
            }
        } attachments: {
            Attachment(id: "panel") {
                VStack {
                    Text("Status")
                    Button("Reset", action: {})
                }
                .padding()
            }
        }
    }
}
```

## WWDC 2025: Better together: SwiftUI and RealityKit (RealityView)

Session link: https://developer.apple.com/videos/play/wwdc2025/274/

### 6-51 Switch to RealityView

```swift
struct RobotView: View {
  let url: URL = Bundle.main.url(forResource: "sparky", withExtension: "reality")!

  var body: some View {
    HStack {
      NameSign()
      RealityView { content in
        if let sparky = try? await Entity(contentsOf: url) {
          content.add(sparky)
        }
      }
    }
  }
}
```

### 7-25 RealityView fixed size layout

```swift
struct RobotView: View {
  let url: URL = Bundle.main.url(forResource: "sparky", withExtension: "reality")!

  var body: some View {
    HStack {
      NameSign()
      RealityView { content in
        if let sparky = try? await Entity(contentsOf: url) {
          content.add(sparky)
        }
      }
      .realityViewLayoutBehavior(.fixedSize)
    }
  }
}
```

### 8-48 RealityView animation

```swift
struct RobotView: View {
  let url: URL = Bundle.main.url(forResource: "sparky", withExtension: "reality")!

  var body: some View {
    HStack {
      NameSign()
      RealityView { content in
        if let sparky = try? await Entity(contentsOf: url) {
          content.add(sparky)
          sparky.playAnimation(getAnimation())
        }
      }
      .realityViewLayoutBehavior(.fixedSize)
    }
  }
}
```

### 10-34 Particle emitters

```swift
func setupSparks(robotHead: Entity) {
  let leftSparks = Entity()
  let rightSparks = Entity()

  robotHead.addChild(leftSparks)
  robotHead.addChild(rightSparks)

  rightSparks.components.set(sparksComponent())
  leftSparks.components.set(sparksComponent())

  leftSparks.transform.rotation = simd_quatf(Rotation3D(
    angle: .degrees(180),
    axis: .y))

  leftSparks.transform.translation = leftEarOffset()
  rightSparks.transform.translation = rightEarOffset()
}

// Create and configure the ParticleEmitterComponent
func sparksComponent() -> ParticleEmitterComponent { ... }
```

### 16-19 Attachment builder

```swift
struct RealityViewAttachments: View {
  var body: some View {
    RealityView { content, attachments in
      let bolts = await loadAndSetupBolts()
      if let nameSign = attachments.entity(
        for: "name-sign"
      ) {
        content.add(nameSign)
        place(nameSign, above: bolts)
      }
      content.add(bolts)
    } attachments: {
      Attachment(id: "name-sign") {
        NameSign("Bolts")
      }
    }
    .realityViewLayoutBehavior(.centered)
  }
}
```

### 16-37 ViewAttachmentComponent attachments

```swift
struct AttachmentComponentAttachments: View {
  var body: some View {
    RealityView { content in
      let bolts = await loadAndSetupBolts()
      let attachment = ViewAttachmentComponent(
          rootView: NameSign("Bolts"))
      let nameSign = Entity(components: attachment)
      place(nameSign, above: bolts)
      content.add(bolts)
      content.add(nameSign)
    }
    .realityViewLayoutBehavior(.centered)
  }
}
```
