# Interaction and Gestures

## Context

SpatialTapGesture is a SwiftUI gesture that recognizes taps and reports their location. ManipulationComponent adds immersive interaction behaviors to RealityKit entities, while GestureComponent lets you attach custom gesture recognition to entities.

## Best Practices

- Use SpatialTapGesture when you need tap locations in a specific coordinate space.
- Configure ManipulationComponent on entities that should be directly manipulated, and rely on its lifecycle events for feedback.
- Add GestureComponent when you need targeted entity gestures with custom logic.
- Keep gesture handling on the main actor and update RealityKit entities in RealityView closures.

## Code Examples

### SpatialTapGesture

```swift
import SwiftUI

struct SpatialTapExample: View {
    @State private var point: CGPoint = .zero

    var body: some View {
        Circle()
            .fill(point.x > 50 ? .blue : .red)
            .frame(width: 100, height: 100)
            .gesture(
                SpatialTapGesture()
                    .onEnded { value in
                        point = value.location
                    }
            )
    }
}
```



#### ManipulationComponent configure

```swift
RealityView { content in
  let sparky = await loadSparky()
  content.add(sparky)
  ManipulationComponent.configureEntity(sparky)
}
```

#### ManipulationComponent configure with options

```swift
RealityView { content in
  let sparky = await loadSparky()
  content.add(sparky)
  ManipulationComponent.configureEntity(
    sparky,
    hoverEffect: .spotlight(.init(color: .purple)),
    allowedInputTypes: .all,
    collisionShapes: myCollisionShapes()
  )
}
```

#### ManipulationEvents

```swift
public enum ManipulationEvents {

  /// When an interaction is about to begin on a ManipulationComponent's entity
  public struct WillBegin: Event { }

  /// When an entity's transform was updated during a ManipulationComponent
  public struct DidUpdateTransform: Event { }

  /// When an entity was released
  public struct WillRelease: Event { }

  /// When the object has reached its destination and will no longer be updated
  public struct WillEnd: Event { }

  /// When the object is directly handed off from one hand to another
  public struct DidHandOff: Event { }
}
```

#### Custom manipulation audio

```swift
RealityView { content in
  let sparky = await loadSparky()
  content.add(sparky)

  var manipulation = ManipulationComponent()
  manipulation.audioConfiguration = .none
  sparky.components.set(manipulation)

  didHandOff = content.subscribe(to: ManipulationEvents.DidHandOff.self) { event in
    sparky.playAudio(handoffSound)
  }
}
```

#### Targeted-to-entity gesture

```swift
struct AttachmentComponentAttachments: View {
  @State private var bolts = Entity()
  @State private var nameSign = Entity()

  var body: some View {
    RealityView { ... }
    .realityViewLayoutBehavior(.centered)
    .gesture(
      TapGesture()
        .targetedToEntity(bolts)
        .onEnded { value in
          nameSign.isEnabled.toggle()
        }
    )
  }
}
```

#### GestureComponent

```swift
struct AttachmentComponentAttachments: View {
  var body: some View {
    RealityView { content in
      let bolts = await loadAndSetupBolts()
      let attachment = ViewAttachmentComponent(
          rootView: NameSign("Bolts"))
      let nameSign = Entity(components: attachment)
      place(nameSign, above: bolts)
      bolts.components.set(GestureComponent(
        TapGesture().onEnded {
          nameSign.isEnabled.toggle()
        }
      ))
      content.add(bolts)
      content.add(nameSign)
    }
    .realityViewLayoutBehavior(.centered)
  }
}
```
