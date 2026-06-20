# RealityKit Component Selection

Use this file before choosing a RealityKit component, switching to a focused
RealityKit skill, or inventing a new ECS type. Prefer documented components
when they match the behavior.

## Core Interaction

- [`InputTargetComponent`](inputtargetcomponent.md): make an entity eligible
  for input and hit testing.
- [`CollisionComponent`](../../realitykit-animation-physics/references/collisioncomponent.md):
  provide shapes for hit testing and physics contacts.
- [`HoverEffectComponent`](hovereffectcomponent.md): add system hover
  affordances.
- [`ManipulationComponent`](manipulationcomponent.md): use built-in direct
  manipulation before writing a custom transform stack.
- SwiftUI targeted gestures: use documented targeted gestures, such as
  `TapGesture().targetedToEntity(...)`, for entity-specific tap handling.
- [`GestureComponent`](gesturecomponent.md): attach a UI gesture to the entity
  as RealityKit component state when that ownership model is more natural than
  a SwiftUI view modifier.

## Presentation and UI

- [`ViewAttachmentComponent`](viewattachmentcomponent.md): attach SwiftUI-backed
  views as RealityKit entities when direct entity ownership is natural.
- `RealityView` attachments builder: prefer this for declarative SwiftUI-owned
  attachments inside a `RealityView`.
- [`TextComponent`](textcomponent.md): render text inside the entity graph.
- [`ImagePresentationComponent`](imagepresentationcomponent.md): present image
  content in RealityKit.
- [`VideoPlayerComponent`](videoplayercomponent.md): present AVPlayer-backed
  video in RealityKit.

## Scene Content and Rendering

- [`ModelComponent`](../../realitykit-rendering-materials/references/modelcomponent.md):
  render meshes and materials.
- [`OpacityComponent`](../../realitykit-rendering-materials/references/opacitycomponent.md):
  control entity opacity.
- [`ImageBasedLightComponent`](../../realitykit-rendering-materials/references/imagebasedlightcomponent.md)
  and
  [`ImageBasedLightReceiverComponent`](../../realitykit-rendering-materials/references/imagebasedlightreceivercomponent.md):
  configure image-based lighting.
- [`GroundingShadowComponent`](../../realitykit-rendering-materials/references/groundingshadowcomponent.md):
  use system grounding shadows where appropriate.
- `realitykit-rendering-materials`: use this skill for cameras, lights,
  shadows, materials, post-processing, splats, decals, lightmaps, probes,
  LOD, occlusion, or render-cost controls.

## Audio

- `AudioFileResource` with audio components: load and play spatial or channel
  audio.
- `realitykit-audio-spatial`: use this skill for spatial audio, ambient audio,
  channel audio, audio libraries, mix groups, reverb, grouped playback, or
  acoustic simulation.

## Tracking and Anchoring

- [`SpatialTrackingSession`](spatialtrackingsession.md): use when
  RealityKit-managed anchoring is enough.
- `ARKitSession`: use `arkit-visionos-developer` when the app needs provider
  streams, explicit authorization, or direct anchor-update reconciliation.
- [`AnchoringComponent`](anchoringcomponent.md) and
  [`ARKitAnchorComponent`](arkitanchorcomponent.md): use for RealityKit-owned
  anchor component state.

## Animation and Physics

- `realitykit-animation-physics`: use this skill for animation clips,
  character controllers, skeletal poses, IK, body tracking, blendshapes,
  animation graphs, retargeting, root motion, navigation, behavior trees,
  collision, physics bodies, joints, forces, particles, compute simulations,
  and cloth.

## New in visionOS 27

All entries below are new in visionOS 27; beta API names and shapes may change
before release.

- Rendering: use `realitykit-rendering-materials` for
  [`GaussianSplatComponent`](../../realitykit-rendering-materials/references/gaussiansplatcomponent.md),
  [`ToneMappingComponent`](../../realitykit-rendering-materials/references/tonemappingcomponent.md),
  [`BloomComponent`](../../realitykit-rendering-materials/references/bloomcomponent.md),
  [`PhysicallyBasedDecalComponent`](../../realitykit-rendering-materials/references/physicallybaseddecalcomponent.md),
  [`ClippingComponent`](../../realitykit-rendering-materials/references/clippingcomponent.md),
  [`LevelOfDetailComponent`](../../realitykit-rendering-materials/references/levelofdetailcomponent.md),
  [`OcclusionCullingComponent`](../../realitykit-rendering-materials/references/occlusioncullingcomponent.md),
  [`render layers and shadows`](../../realitykit-rendering-materials/references/render-layers-and-shadows.md),
  and [`lightmaps and probes`](../../realitykit-rendering-materials/references/lightmaps-and-probes.md).
- Animation and physics: use `realitykit-animation-physics` for
  [`cloth simulation`](../../realitykit-animation-physics/references/cloth-simulation.md),
  [`ComputeGraph` particles](../../realitykit-animation-physics/references/compute-graph-particles.md),
  [`animation graphs and retargeting`](../../realitykit-animation-physics/references/animation-graphs-and-retargeting.md),
  and
  [`navigation and behavior trees`](../../realitykit-animation-physics/references/navigation-and-behavior-trees.md).
- Audio: use `realitykit-audio-spatial` for
  [`audio groups and acoustics`](../../realitykit-audio-spatial/references/audio-groups-and-acoustics.md).
- Local USD rendering: use
  [`USDStageComponent`](usdstagecomponent.md). For Swift USDKit authoring, use
  `usdkit-runtime-developer`; for authored USD edits or command-line
  inspection, use `usd-editor`; for Mac-to-Vision-Pro streaming, use
  `spatial-preview-developer`.
- Portals and accessory anchoring: use
  [`portal-volumes-and-accessory-anchoring.md`](portal-volumes-and-accessory-anchoring.md).

## Custom ECS Boundary

Create a custom `Component` or `System` only when documented components do not
represent the needed state or behavior. Use `realitykit-ecs-systems` for
custom components, systems, registration, ECS queries, and per-frame behavior:

- [`custom-components.md`](../../realitykit-ecs-systems/references/custom-components.md)
- [`custom-systems.md`](../../realitykit-ecs-systems/references/custom-systems.md)
- [`systemandcomponentcreation.md`](../../realitykit-ecs-systems/references/systemandcomponentcreation.md)
