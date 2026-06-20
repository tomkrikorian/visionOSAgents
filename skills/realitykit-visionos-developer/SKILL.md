---
name: realitykit-visionos-developer
description: Route RealityKit work on visionOS 27 and handle core entity/component basics, RealityView scene setup, asset loading, input targets, SwiftUI attachments, anchoring, portals, synchronization, and USDStage bridge usage. Use for general RealityKit triage, choosing documented components, loading Reality Composer Pro, USD, USDZ, or .reality content, and deciding whether to hand off to realitykit-rendering-materials, realitykit-animation-physics, realitykit-audio-spatial, realitykit-ecs-systems, spatial-preview-developer, usdkit-runtime-developer, usd-editor, shadergraph-editor, ARKit, SwiftUI, or build-debug skills.
---

# RealityKit visionOS Developer

## Quick Start

1. Classify the request as core scene setup, rendering/materials,
   animation/physics, audio, custom ECS, USD authoring, Spatial Preview,
   SwiftUI UI, ARKit provider work, or build/debug plumbing.
2. Stay in this skill for RealityView setup, entity loading, component
   selection, input, attachments, anchoring, portals, synchronization, and
   the local `USDStageComponent` bridge.
3. Switch to the focused RealityKit skill when the task is primarily visual,
   animated, physical, audio, or custom ECS behavior.
4. Load only the narrow reference files needed for the task.
5. Keep all scene mutation inside documented RealityKit entry points:
   `RealityView` content/update closures, event handlers, or registered
   systems.

## RealityKit Routing

| Task | Use |
|---|---|
| General RealityKit triage, component choice, entity loading, input, attachments, anchoring, portals, sync, local USDStage bridge | This skill |
| Mesh display, materials, cameras, lights, shadows, post-processing, Gaussian splats, decals, LOD, occlusion, lightmaps, probes | `realitykit-rendering-materials` |
| Animation clips, character controllers, skeletal poses, IK, body tracking, retargeting, navigation, behavior trees, collision, physics, joints, forces, particles, cloth | `realitykit-animation-physics` |
| Spatial audio, ambient or channel audio, audio libraries, mix groups, reverb, acoustic simulation | `realitykit-audio-spatial` |
| Custom components, systems, ECS queries, registration, update ordering, per-frame multi-entity behavior | `realitykit-ecs-systems` |
| Mac app streaming documents or live USD stages to Vision Pro via Spatial Preview | `spatial-preview-developer` |
| Swift USDKit stage/layer/prim APIs | `usdkit-runtime-developer` |
| Authored USD edits or command-line USD inspection | `usd-editor` |
| ShaderGraph or RealityKit material graph editing in USDA | `shadergraph-editor` |
| ARKitSession providers, permissions, and direct anchor stream reconciliation | `arkit-visionos-developer` |
| SwiftUI layout, ornaments, windows, immersive spaces, or targeted gesture ergonomics | `spatial-swiftui-developer` |
| Building, launching, simulator/device logs, or runtime debugging | `build-run-debug` |

## Load References When

| Reference | When to Use |
|---|---|
| [`references/component-selection.md`](references/component-selection.md) | Choose between documented RealityKit components, SwiftUI targeted gestures, `SpatialTrackingSession`, ARKit, focused RealityKit skills, and custom ECS work. |
| [`references/component-index.md`](references/component-index.md) | Find the component category and the owning skill/reference to open next. |
| [`references/entity-loading-and-stored-entities.md`](references/entity-loading-and-stored-entities.md) | Load named stored entities, explicit file URLs, package-bundled assets, USD/USDZ, `.reality`, or Reality Composer Pro output. |
| [`references/inputtargetcomponent.md`](references/inputtargetcomponent.md) | Make entities eligible for hit testing and input. Pair with collision details from `realitykit-animation-physics` when needed. |
| [`references/manipulationcomponent.md`](references/manipulationcomponent.md) | Use built-in direct manipulation before writing a custom transform stack. |
| [`references/gesturecomponent.md`](references/gesturecomponent.md) | Attach a SwiftUI gesture directly to a RealityKit entity. |
| [`references/hovereffectcomponent.md`](references/hovereffectcomponent.md) and [`references/accessibilitycomponent.md`](references/accessibilitycomponent.md) | Add hover affordances or accessibility metadata to interactive entities. |
| [`references/viewattachmentcomponent.md`](references/viewattachmentcomponent.md) | Embed SwiftUI-backed views in the entity graph. |
| [`references/presentationcomponent.md`](references/presentationcomponent.md), [`references/textcomponent.md`](references/textcomponent.md), [`references/imagepresentationcomponent.md`](references/imagepresentationcomponent.md), [`references/videoplayercomponent.md`](references/videoplayercomponent.md) | Present text, images, video, or presentation-style content in RealityKit. |
| [`references/anchoringcomponent.md`](references/anchoringcomponent.md), [`references/arkitanchorcomponent.md`](references/arkitanchorcomponent.md), [`references/spatialtrackingsession.md`](references/spatialtrackingsession.md) | Anchor content to spatial targets or decide whether RealityKit-managed tracking is enough. |
| [`references/sceneunderstandingcomponent.md`](references/sceneunderstandingcomponent.md), [`references/dockingregioncomponent.md`](references/dockingregioncomponent.md), [`references/referencecomponent.md`](references/referencecomponent.md), [`references/attachedtransformcomponent.md`](references/attachedtransformcomponent.md) | Work with spatial references, docking, scene understanding, or transform attachments. |
| [`references/portalcomponent.md`](references/portalcomponent.md), [`references/portalcrossingcomponent.md`](references/portalcrossingcomponent.md), [`references/worldcomponent.md`](references/worldcomponent.md), [`references/environmentblendingcomponent.md`](references/environmentblendingcomponent.md), [`references/portal-volumes-and-accessory-anchoring.md`](references/portal-volumes-and-accessory-anchoring.md) | Compose portals, worlds, environment blending, and new visionOS 27 portal/accessory anchoring behavior. |
| [`references/synchronizationcomponent.md`](references/synchronizationcomponent.md), [`references/transientcomponent.md`](references/transientcomponent.md) | Synchronize or mark entity state for multi-user/session behavior. |
| [`references/usdstagecomponent.md`](references/usdstagecomponent.md) | Render a live USDKit stage inside RealityKit or export entity hierarchies to USD. For Swift USDKit stage authoring, switch to `usdkit-runtime-developer`; for Spatial Preview streaming, switch to `spatial-preview-developer`. |

## Guardrails

- Use `RealityView`; `ARView` is not available on visionOS.
- Load assets asynchronously and avoid blocking the main actor.
- Keep SwiftUI body code declarative; mutate RealityKit content through
  `RealityView`, events, or systems.
- Prefer documented components before custom ECS.
- Register custom components and systems once during app startup before scenes
  or assets that depend on them load.
- Prefer `ManipulationComponent.configureEntity(...)` when built-in direct
  manipulation fits the need.
- Use `SpatialPreview` only from macOS 27 sender apps; Vision Pro uses the
  built-in system viewer and has no visionOS `SpatialPreview` module.

## Output Expectations

Provide:

- the RealityKit task category
- which focused skill or references were used
- the component, attachment, entity-loading, or system path chosen
- the main constraint or pitfall
- routing back to SwiftUI, ARKit, USD, Spatial Preview, or build-debug if needed
