---
name: realitykit-visionos-developer
description: Build, debug, and optimize RealityKit scenes for visionOS 26, including entity/component setup, rendering, animation, physics, audio, input, attachments, and custom systems. Use when implementing RealityKit features or troubleshooting ECS behavior on visionOS.
---

# RealityKit visionOS Developer

## Quick Start

1. Decide whether the task is component selection, scene setup, animation, physics, audio, input, or ECS debugging.
2. Load only the component or system references that match the task instead of reading the whole catalog.
3. Use `RealityView` as the SwiftUI bridge and keep all content mutation inside documented RealityKit entry points.
4. Register custom components before use, then keep per-frame behavior in systems instead of ad hoc view logic.
5. If the issue is app launch, simulator flow, or build/debug plumbing, switch to the plugin's `build-run-debug` workflow skill.

## Tracks

### Scene Assembly

Use this track when you are building or restructuring the entity graph.

- Prefer composition over inheritance.
- Use custom `Component` plus `Codable` when you need per-entity state.
- Register custom components once with `Component.registerComponent()`.
- Mutate entities from `RealityView` closures, event handlers, or systems.

### Loading and Attachments

Use this track when SwiftUI and RealityKit must coexist in the same scene.

- Use `RealityView` for the bridge.
- Load assets asynchronously with `Entity(named:)` or `Entity(contentsOf:)`.
- Use the `RealityView` attachments closure when the attachment belongs with the view.
- Use `ViewAttachmentComponent` when the attachment is better modeled as ECS state.

### Systems and Queries

Use this track when behavior must update continuously or across many entities.

- Use a custom `System` for per-frame behavior.
- Query entities with `EntityQuery` and `QueryPredicate`.
- Keep the update path in `update(context:)`.
- Use `SystemDependency` when system ordering matters.

### Component Selection

Use this track when you need the right API for the job and are not sure which component to pick.

- Load only the matching reference rows below.
- Prefer the smallest component that solves the problem.
- Keep the larger catalog in the tables, but do not treat it as a required read.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`ModelComponent`](references/modelcomponent.md) | When rendering 3D geometry with meshes and materials on entities. |
| [`InputTargetComponent`](references/inputtargetcomponent.md) | When making entities interactive or handling user input events. |
| [`AnchoringComponent`](references/anchoringcomponent.md) | When anchoring content to detected planes, hand locations, or world targets. |
| [`SpatialAudioComponent`](references/spatialaudiocomponent.md) | When playing positioned 3D audio. |
| [`CollisionComponent`](references/collisioncomponent.md) | When defining collision shapes for hit testing or physics interactions. |
| [`ViewAttachmentComponent`](references/viewattachmentcomponent.md) | When embedding SwiftUI views into 3D space. |
| [`SynchronizationComponent`](references/synchronizationcomponent.md) | When synchronizing state across networked sessions. |
| [`System and Component Creation`](references/systemandcomponentcreation.md) | When creating custom systems or custom per-entity state. |

## Guardrails

- Always load assets asynchronously; avoid blocking the main actor.
- On visionOS, `ARView` is not available — it inherits from `UIView`/`NSView`. Always use `RealityView`.
- Keep `RealityView` update logic and ECS mutation out of SwiftUI body code.
- Add `CollisionComponent` plus `InputTargetComponent` for draggable or tappable entities.
- Prefer a custom `System` when behavior spans multiple entities or needs continuous updates.
- Route launch, build, simulator, and codesign problems to the plugin's `build-run-debug` workflow skill instead of expanding this skill with execution steps.

## Information About the Skill

### Core Concepts

#### Entities and Components

- Entities are lightweight containers; behavior comes from components.
- Prefer composition over inheritance and use custom `Component` + `Codable` when you need per-entity state.
- Register custom components once with `Component.registerComponent()` before use.
- Mutate entities from documented RealityKit entry points such as `RealityView` closures, event handlers, and systems.

#### RealityView and Attachments

- Use `RealityView` to bridge SwiftUI and RealityKit.
- Load assets with `Entity(named:)` or `Entity(contentsOf:)` asynchronously and handle errors.
- Use the `RealityView` attachments closure when you want SwiftUI attachment entities defined alongside the view, and use `ViewAttachmentComponent` when a component-based attachment is the better fit.

#### Systems and Queries

- Use a custom `System` for continuous, per-frame behavior.
- Query entities with `EntityQuery` + `QueryPredicate` and process them in `update(context:)`.
- Use `SystemDependency` to control update order when multiple systems interact.

### Components Reference

Use this table to decide which component reference file to load when implementing RealityKit features:

#### Rendering and Appearance

| Component | When to Use |
|-----------|-------------|
| [`ModelComponent`](references/modelcomponent.md) | When rendering 3D geometry with meshes and materials on entities. |
| [`ModelSortGroupComponent`](references/modelsortgroupcomponent.md) | When experiencing depth fighting (z-fighting) issues with overlapping geometry or need to control draw order. |
| [`OpacityComponent`](references/opacitycomponent.md) | When creating fade effects, making entities semi-transparent, or implementing visibility transitions. |
| [`AdaptiveResolutionComponent`](references/adaptiveresolutioncomponent.md) | When optimizing performance in large scenes by reducing render quality for distant objects. |
| [`ModelDebugOptionsComponent`](references/modeldebugoptionscomponent.md) | When debugging rendering issues, visualizing model geometry, or inspecting bounding boxes during development. |
| [`MeshInstancesComponent`](references/meshinstancescomponent.md) | When rendering many copies of the same mesh efficiently (trees, crowds, particle-like objects). |
| [`BlendShapeWeightsComponent`](references/blendshapeweightscomponent.md) | When implementing facial animation, character expressions, or morphing mesh deformations. |

#### User Interaction

| Component | When to Use |
|-----------|-------------|
| [`InputTargetComponent`](references/inputtargetcomponent.md) | When making entities interactive (tappable, draggable) or handling user input events. |
| [`ManipulationComponent`](references/manipulationcomponent.md) | When implementing built-in drag, rotate, and scale interactions with hand gestures or trackpad. |
| [`GestureComponent`](references/gesturecomponent.md) | When implementing custom gesture recognition beyond what ManipulationComponent provides. |
| [`HoverEffectComponent`](references/hovereffectcomponent.md) | When providing visual feedback when users look at or hover over interactive entities. For custom shader-driven hover effects on visionOS 26, pair with `HoverEffectComponent.ShaderHoverEffectInputs` and a Reality Composer Pro Shader Graph `Hover State (RealityKit)` node. |
| [`AccessibilityComponent`](references/accessibilitycomponent.md) | When making entities accessible to screen readers, VoiceOver, or other assistive technologies. |
| [`BillboardComponent`](references/billboardcomponent.md) | When creating 2D sprites, text labels, or UI elements that should always face the viewer. |

#### Anchoring and Spatial

| Component | When to Use |
|-----------|-------------|
| [`AnchoringComponent`](references/anchoringcomponent.md) | When anchoring virtual content to detected planes, tracked images, hand locations, or world targets. |
| [`ARKitAnchorComponent`](references/arkitanchorcomponent.md) | When accessing the underlying ARKit anchor data for an anchored entity. |
| [`SceneUnderstandingComponent`](references/sceneunderstandingcomponent.md) | When accessing scene understanding data like detected objects or room reconstruction. |
| [`DockingRegionComponent`](references/dockingregioncomponent.md) | When defining regions where content can automatically dock or snap into place. |
| [`ReferenceComponent`](references/referencecomponent.md) | When implementing lazy loading of external entity assets or referencing entities in other files. |
| [`AttachedTransformComponent`](references/attachedtransformcomponent.md) | When attaching an entity's transform to another entity for hierarchical positioning. |

#### Cameras

| Component | When to Use |
|-----------|-------------|
| [`PerspectiveCameraComponent`](references/perspectivecameracomponent.md) | When configuring a perspective camera with depth and field of view for 3D scenes. |
| [`OrthographicCameraComponent`](references/orthographiccameracomponent.md) | When configuring an orthographic camera without perspective distortion for 2D-like views. |
| [`ProjectiveTransformCameraComponent`](references/projectivetransformcameracomponent.md) | When implementing custom camera projection transforms for specialized rendering needs. |

#### Lighting and Shadows

| Component | When to Use |
|-----------|-------------|
| [`PointLightComponent`](references/pointlightcomponent.md) | When adding an omnidirectional point light that radiates in all directions from a position. |
| [`DirectionalLightComponent`](references/directionallightcomponent.md) | When adding a directional light with parallel rays (like sunlight) for consistent scene lighting. |
| [`SpotLightComponent`](references/spotlightcomponent.md) | When adding a cone-shaped spotlight for focused, directional lighting effects. |
| [`ImageBasedLightComponent`](references/imagebasedlightcomponent.md) | When applying environment lighting from HDR textures for realistic reflections and ambient lighting. |
| [`ImageBasedLightReceiverComponent`](references/imagebasedlightreceivercomponent.md) | When enabling entities to receive and respond to image-based lighting in the scene. |
| [`GroundingShadowComponent`](references/groundingshadowcomponent.md) | When adding grounding shadows to visually anchor floating content to surfaces. |
| [`DynamicLightShadowComponent`](references/dynamiclightshadowcomponent.md) | When enabling real-time dynamic shadows cast by light sources onto entities. |
| [`EnvironmentLightingConfigurationComponent`](references/environmentlightingconfigurationcomponent.md) | When configuring environment lighting behavior, intensity, or blending modes. |
| [`VirtualEnvironmentProbeComponent`](references/virtualenvironmentprobecomponent.md) | When implementing reflection probes for accurate reflections in virtual environments. |

#### Audio

| Component | When to Use |
|-----------|-------------|
| [`SpatialAudioComponent`](references/spatialaudiocomponent.md) | When playing 3D positioned audio that changes based on listener position and orientation. |
| [`AmbientAudioComponent`](references/ambientaudiocomponent.md) | When playing non-directional ambient audio that doesn't change with listener position. |
| [`ChannelAudioComponent`](references/channelaudiocomponent.md) | When playing channel-based audio content (stereo, surround, etc.) without spatialization. |
| [`AudioLibraryComponent`](references/audiolibrarycomponent.md) | When storing and managing multiple audio resources for reuse across entities. |
| [`ReverbComponent`](references/reverbcomponent.md) | When applying reverb effects to an entity's audio for spatial acoustic simulation. |
| [`AudioMixGroupsComponent`](references/audiomixgroupscomponent.md) | When grouping audio sources for centralized mixing control and volume management. |

#### Animation and Character

| Component | When to Use |
|-----------|-------------|
| [`AnimationLibraryComponent`](references/animationlibrarycomponent.md) | When storing multiple animations (idle, walk, run) on a single entity for character animation. |
| [`CharacterControllerComponent`](references/charactercontrollercomponent.md) | When implementing character movement with physics, collision, and ground detection. |
| [`CharacterControllerStateComponent`](references/charactercontrollerstatecomponent.md) | When storing runtime state (velocity, grounded status) for a character controller. |
| [`SkeletalPosesComponent`](references/skeletalposescomponent.md) | When providing skeletal pose data for skeletal animation and bone transformations. |
| [`IKComponent`](references/ikcomponent.md) | When implementing inverse kinematics for procedural animation (e.g., reaching, pointing). |
| [`BodyTrackingComponent`](references/bodytrackingcomponent.md) | When integrating ARKit body tracking data to animate entities based on real-world body poses. |

#### Physics and Collision

| Component | When to Use |
|-----------|-------------|
| [`CollisionComponent`](references/collisioncomponent.md) | When defining collision shapes for hit testing, raycasting, or physics interactions. |
| [`PhysicsBodyComponent`](references/physicsbodycomponent.md) | When adding physical behavior (mass, gravity, forces) to entities for physics simulation. |
| [`PhysicsMotionComponent`](references/physicsmotioncomponent.md) | When controlling linear and angular velocity of physics bodies programmatically. |
| [`PhysicsSimulationComponent`](references/physicssimulationcomponent.md) | When configuring global physics simulation parameters like gravity or timestep. |
| [`ParticleEmitterComponent`](references/particleemittercomponent.md) | When emitting particle effects (smoke, sparks, debris) from an entity position. |
| [`ForceEffectComponent`](references/forceeffectcomponent.md) | When applying force fields (gravity wells, explosions) that affect multiple physics bodies. |
| [`PhysicsJointsComponent`](references/physicsjointscomponent.md) | When creating joints (hinges, springs) between physics bodies for articulated structures. |
| [`GeometricPinsComponent`](references/geometricpinscomponent.md) | When defining geometric attachment points for connecting entities at specific locations. |

#### Portals and Environments

| Component | When to Use |
|-----------|-------------|
| [`PortalComponent`](references/portalcomponent.md) | When creating portals that render a separate world or scene through an opening. |
| [`WorldComponent`](references/worldcomponent.md) | When designating an entity hierarchy as a separate renderable world for portal rendering. |
| [`PortalCrossingComponent`](references/portalcrossingcomponent.md) | When controlling behavior (teleportation, scene switching) when entities cross portal boundaries. |
| [`EnvironmentBlendingComponent`](references/environmentblendingcomponent.md) | When blending virtual content with the real environment for mixed reality experiences. |

#### Presentation and UI

| Component | When to Use |
|-----------|-------------|
| [`ViewAttachmentComponent`](references/viewattachmentcomponent.md) | When embedding SwiftUI views into 3D space for interactive UI elements or labels. |
| [`PresentationComponent`](references/presentationcomponent.md) | When presenting SwiftUI modals, sheets, or system UI from an entity interaction. |
| [`TextComponent`](references/textcomponent.md) | When rendering 3D text directly on entities without using SwiftUI views. |
| [`ImagePresentationComponent`](references/imagepresentationcomponent.md) | When displaying images or textures on entities in 3D space. |
| [`VideoPlayerComponent`](references/videoplayercomponent.md) | When playing video content on entity surfaces using AVPlayer. |

#### Tracking

| API | When to Use |
|-----|-------------|
| [`SpatialTrackingSession`](references/spatialtrackingsession.md) | When an entity needs anchor-derived transforms (plane, hand, image, world) without running an `ARKitSession` yourself. RealityKit drives the session and publishes results through `AnchoringComponent`. |

#### Networking and Sync

| Component | When to Use |
|-----------|-------------|
| [`SynchronizationComponent`](references/synchronizationcomponent.md) | When synchronizing entity state, transforms, and components across networked multiplayer sessions. For new visionOS 26 multi-user work, prefer the `shareplay-developer` skill (GroupActivities + `SystemCoordinator`) as the recommended path. |
| [`TransientComponent`](references/transientcomponent.md) | When marking entities as temporary, non-persistent, and excluded from network synchronization. |

### Systems Reference

Use this reference when implementing custom ECS behavior:

| System/API | When to Use |
|-----------|-------------|
| [`System and Component Creation`](references/systemandcomponentcreation.md) | When creating custom systems for continuous, per-frame behavior or custom components for per-entity state. |

### Implementation Patterns

#### RealityView Async Load

```swift
RealityView { content in
    do {
        let entity = try await Entity(named: "Scene")
        content.add(entity)
    } catch {
        print("Failed to load entity: \(error)")
    }
}
```

#### Interactive Entity Setup

Prefer `ManipulationComponent.configureEntity(_:hoverEffect:allowedInputTypes:collisionShapes:)`
— it installs `CollisionComponent`, `InputTargetComponent`, the hover effect,
and the manipulation component in one call with Apple's recommended defaults.

```swift
let entity = ModelEntity(mesh: .generateBox(size: 0.1))
ManipulationComponent.configureEntity(
    entity,
    hoverEffect: .spotlight(.init()),
    allowedInputTypes: .all,
    collisionShapes: [.generateBox(size: [0.1, 0.1, 0.1])]
)
```

Only fall back to manually setting `CollisionComponent`, `InputTargetComponent`,
and `ManipulationComponent` separately when you need to customize individual
component configurations that `configureEntity` does not expose.

#### Custom System Skeleton

```swift
import RealityKit

struct SpinComponent: Component, Codable {
    var speed: Float
}

struct SpinSystem: System {
    static let query = EntityQuery(where: .has(SpinComponent.self))

    init(scene: Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard let spin = entity.components[SpinComponent.self] else { continue }
            entity.transform.rotation *= simd_quatf(angle: spin.speed * Float(context.deltaTime), axis: [0, 1, 0])
        }
    }
}

SpinSystem.registerSystem()
```

### Pitfalls and Checks

- Always load assets asynchronously; avoid blocking the main actor.
- On visionOS, `ARView` is not available — it inherits from `UIView`/`NSView`. Always use `RealityView`.
- For draggable or tappable entities, prefer `ManipulationComponent.configureEntity(_:hoverEffect:allowedInputTypes:collisionShapes:)` over manually setting `CollisionComponent` + `InputTargetComponent` + `ManipulationComponent`.
- Use the `RealityView` update closure for state-driven content updates, and prefer a custom `System` for continuous per-frame behavior that spans many entities.
- Built-in mesh generation supports more than the basic primitives, including text and custom mesh content through `MeshResource` APIs.
