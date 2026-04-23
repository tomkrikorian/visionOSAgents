# RealityView Patterns

## Context

RealityView is a RealityKit view that hosts 3D content in SwiftUI using make and update closures. RealityViewAttachments provides access to attachment entities created by the attachment builder, and ViewAttachmentComponent stores metadata for a SwiftUI view attachment entity.

## Best Practices

- Load RealityKit entities asynchronously in the make closure to avoid UI hangs.
- Keep state-driven mutations inside the update closure instead of SwiftUI body.
- Use `attachments.entity(for:)` to resolve SwiftUI attachments and position them in 3D.
- Use `ViewAttachmentComponent` when you need explicit attachment entities or bounds.
- Keep `make` for initial content creation and registration. Keep `update`
  idempotent: find existing entities and mutate them; do not repeatedly add
  duplicate children.
- Put long-lived entity references, subscriptions, and placement rules in a
  named Reality owner when more than one closure or view needs them.
- Use attachments for SwiftUI controls that belong inside the 3D scene; keep
  ordinary navigation and settings in windows unless the scene context matters.
- Prefer stable attachment IDs and central placement code so the SwiftUI view
  content can change without breaking 3D layout.

## Closure Ownership

| Location | Good Use | Avoid |
| --- | --- | --- |
| `make` | async entity loading, root graph creation, one-time component setup, adding attachments once | reading rapidly changing SwiftUI state as if it will update automatically |
| `update` | state-driven transforms, visibility, selected entity highlights, attachment repositioning | adding duplicate roots, starting async loads repeatedly |
| attachment builder | SwiftUI controls, labels, panels, small status surfaces | entity placement logic, long-running tasks, global state ownership |
| Reality owner/system | subscriptions, entity lookup cache, simulation, component mutation rules | SwiftUI navigation and window lifecycle |

If the code needs both SwiftUI controls and a custom RealityKit graph, route the
controls through attachments and keep the graph mutation in the Reality owner.

## Attachment Rules

- Resolve attachments with `attachments.entity(for:)` before positioning them.
- Add each attachment entity to the content graph once, then update transform,
  opacity, or enabled state as needed.
- Keep attachment SwiftUI content compact and scene-specific. A large inspector
  usually belongs in a window controlling the scene.
- Treat attachment placement as meters/entity-space work, not SwiftUI layout.
- Use `ViewAttachmentComponent` when dynamic entity creation is clearer than an
  attachment builder, especially for generated labels or per-entity adornments.

## Code Examples

### RealityView basics

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

### RealityView with SwiftUI attachments

```swift
import RealityKit
import SwiftUI

struct AttachmentExample: View {
    var body: some View {
        RealityView { content, attachments in
            if let panel = attachments.entity(for: "panel") {
                panel.position = [0, 1, -1]
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

### Reality owner handoff

```swift
@MainActor
final class StageRealityController {
    private var root: Entity?

    func install(in content: RealityViewContent) async {
        guard root == nil else { return }
        let scene = try? await Entity(named: "Stage")
        if let scene {
            root = scene
            content.add(scene)
        }
    }

    func apply(selection: String?) {
        guard let root, let selection else { return }
        root.findEntity(named: selection)?
            .components.set(OpacityComponent(opacity: 1))
    }

    func placePanel(_ panel: Entity) {
        panel.position = [0, 1.2, -0.8]
    }
}

struct StageView: View {
    @State private var controller = StageRealityController()
    let selection: String?

    var body: some View {
        RealityView { content, attachments in
            await controller.install(in: content)
            if let panel = attachments.entity(for: "status") {
                controller.placePanel(panel)
                content.add(panel)
            }
        } update: { _, attachments in
            controller.apply(selection: selection)
            if let panel = attachments.entity(for: "status") {
                controller.placePanel(panel)
            }
        } attachments: {
            Attachment(id: "status") {
                Text(selection ?? "No selection")
                    .padding()
            }
        }
    }
}
```



#### Switch to RealityView

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

#### RealityView fixed size layout

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

#### RealityView animation

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

#### Particle emitters

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

#### Attachment builder

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

#### ViewAttachmentComponent attachments

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
