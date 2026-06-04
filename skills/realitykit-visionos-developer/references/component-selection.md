# RealityKit Component Selection

Use this file before choosing a RealityKit component or inventing a new ECS
type. Prefer documented components when they match the behavior.

## Interaction

- `InputTargetComponent`: make an entity eligible for input and hit testing.
- `CollisionComponent`: provide shapes for hit testing and physics contacts.
- `HoverEffectComponent`: add system hover affordances.
- `ManipulationComponent`: use built-in direct manipulation before writing a
  custom transform stack.
- SwiftUI targeted gestures: use documented targeted gestures, such as
  `TapGesture().targetedToEntity(...)`, for entity-specific tap handling.
- `GestureComponent`: attach a UI gesture to the entity as RealityKit
  component state when that ownership model is more natural than a SwiftUI view
  modifier.

## Presentation and UI

- `ViewAttachmentComponent`: attach SwiftUI-backed views as RealityKit
  entities when direct entity ownership is natural.
- `RealityView` attachments builder: prefer this for declarative SwiftUI-owned
  attachments inside a `RealityView`.
- `TextComponent`: render text inside the entity graph.
- `ImagePresentationComponent`: present image content in RealityKit.
- `VideoPlayerComponent`: present AVPlayer-backed video in RealityKit.

## Scene Content

- `ModelComponent`: render meshes and materials.
- `OpacityComponent`: control entity opacity.
- `ImageBasedLightComponent` and `ImageBasedLightReceiverComponent`: configure
  image-based lighting.
- `GroundingShadowComponent`: use system grounding shadows where appropriate.
- `AudioFileResource` with audio components: load and play spatial or channel
  audio.

## Tracking

- `SpatialTrackingSession`: use when RealityKit-managed anchoring is enough.
- `ARKitSession`: use when the app needs provider streams, explicit
  authorization, or direct anchor-update reconciliation.

## Custom ECS Boundary

Create a custom `Component` or `System` only when documented components do not
represent the needed state or behavior. Register custom components and systems
once during app startup before assets or scenes that depend on them load.

## Reference Routing

Open the component-specific reference for details:

- [`inputtargetcomponent.md`](inputtargetcomponent.md)
- [`collisioncomponent.md`](collisioncomponent.md)
- [`hovereffectcomponent.md`](hovereffectcomponent.md)
- [`manipulationcomponent.md`](manipulationcomponent.md)
- [`gesturecomponent.md`](gesturecomponent.md)
- [`viewattachmentcomponent.md`](viewattachmentcomponent.md)
- [`videoplayercomponent.md`](videoplayercomponent.md)
- [`spatialtrackingsession.md`](spatialtrackingsession.md)
