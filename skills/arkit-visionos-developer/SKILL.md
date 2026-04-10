---
name: arkit-visionos-developer
description: Build and debug ARKit features for visionOS 26, including ARKitSession setup, authorization, data providers (world tracking, plane detection, scene reconstruction, hand tracking), anchor processing, and RealityKit integration. Use when implementing ARKit workflows on visionOS or troubleshooting provider-specific space, privacy, and lifecycle behavior.
---

# ARKit visionOS Developer

## Quick Start

1. Identify the provider set first: world tracking, hand tracking, plane detection, scene reconstruction, or another specialized provider.
2. Add only the usage strings required by the providers you actually use.
3. Create a long-lived `ARKitSession` and request authorization before running it.
4. Load the right reference only after the provider set is known:
   - `world-tracking-provider.md` for device pose and world-space tracking
   - `hand-tracking-provider.md` for hand poses and gestures
   - `plane-detection-provider.md` for surface detection
   - `scene-reconstruction-provider.md` for mesh reconstruction
   - `REFERENCE.md` for session setup and general provider patterns
5. Keep anchor state in a model layer, and bridge into RealityKit only when you have a rendering target.
6. If the issue is app launch, test flow, simulator behavior, or signing, switch to the plugin's `build-run-debug` workflow skill.

## Tracks

### Session Setup

Use this track when you are starting a new ARKit experience.

- Keep one long-lived `ARKitSession` per experience.
- Build the provider list explicitly instead of overloading a shared session.
- Request authorization before `run(_:)`.
- Stop the session and cancel tasks on teardown.

### Provider Selection

Use this track when you are deciding which sensor or spatial feed to use.

- Choose providers based on the feature, not by default.
- Load the provider reference that matches the behavior you need.
- Expect each provider to have its own presentation and privacy constraints.

### Anchor Processing

Use this track when provider updates need to drive scene state.

- Consume `anchorUpdates` and reconcile added, updated, and removed anchors.
- Normalize anchor IDs in your own state model.
- Treat ARKit streams as authoritative and keep rendering logic separate.

### RealityKit Bridge

Use this track when ARKit data needs to become visible scene content.

- Map anchors to RealityKit entities only after the model layer has stable state.
- Use `ARKitAnchorComponent` when you need backing anchor data on an entity.
- Hand off rendering details to the RealityKit skill when the task is scene composition rather than tracking.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When you need session setup, authorization, and general provider patterns. |
| [`WorldTrackingProvider`](references/world-tracking-provider.md) | When tracking device position and orientation in 3D space. |
| [`HandTrackingProvider`](references/hand-tracking-provider.md) | When tracking hand poses and gestures for interaction. |
| [`PlaneDetectionProvider`](references/plane-detection-provider.md) | When detecting horizontal and vertical surfaces. |
| [`SceneReconstructionProvider`](references/scene-reconstruction-provider.md) | When creating detailed 3D mesh reconstructions of the environment. |
| [`ImageTrackingProvider`](references/image-tracking-provider.md) | When tracking known 2D images in the environment. |
| [`ObjectTrackingProvider`](references/object-tracking-provider.md) | When tracking 3D objects in the environment. |
| [`RoomTrackingProvider`](references/room-tracking-provider.md) | When tracking room boundaries and room-scale experiences. |
| [`SharedCoordinateSpaceProvider`](references/shared-coordinate-space-provider.md) | When sharing coordinate spaces across multiple sessions. |

## Guardrails

- Keep a strong reference to `ARKitSession` for the full lifetime of the experience.
- Request authorization before running providers that need it.
- Do not block the main actor while awaiting provider updates.
- Do not assume every provider has the same presentation requirements.
- Stop the session on teardown and cancel any observation tasks.
- Route launch, build, simulator, and codesign problems to the plugin's `build-run-debug` workflow skill instead of expanding this skill with execution steps.

## Information About the Skill

### Core Concepts

#### ARKitSession Lifecycle

- Keep a strong reference to the session; call `run(_:)` with providers, stop on teardown.
- Sessions stop automatically on deinit, so maintain references throughout the immersive experience.

#### Authorization

- Use `requestAuthorization(for:)` or `queryAuthorization(for:)` and handle denied states gracefully.
- Request authorization before running the session with providers that require it.

#### Data Providers

- Choose providers for world tracking, plane detection, scene reconstruction, and hand tracking based on the feature set.
- Providers expose `anchorUpdates` streams that you consume to process anchors.

#### Anchors and Updates

- Consume provider `anchorUpdates` and reconcile added, updated, and removed anchors.
- Normalize anchor IDs to your own state model for reliable entity updates.

#### RealityKit Bridge

- Use `ARKitAnchorComponent` to inspect backing ARKit data on entities when needed.
- Treat ARKit streams as authoritative and keep rendering logic in RealityKit.

### Implementation Patterns

- Prefer one session per immersive experience and reuse providers when possible.
- Normalize anchor IDs to your own state model for reliable entity updates.
- Treat ARKit streams as authoritative and keep rendering logic in RealityKit.

### Provider References

| Provider | When to Use |
|----------|-------------|
| [`WorldTrackingProvider`](references/world-tracking-provider.md) | When tracking device position and orientation in 3D space. |
| [`HandTrackingProvider`](references/hand-tracking-provider.md) | When tracking hand poses and gestures for interaction. |
| [`PlaneDetectionProvider`](references/plane-detection-provider.md) | When detecting horizontal and vertical surfaces (floors, walls, tables). |
| [`SceneReconstructionProvider`](references/scene-reconstruction-provider.md) | When creating detailed 3D mesh reconstructions of the environment. |
| [`ImageTrackingProvider`](references/image-tracking-provider.md) | When tracking known 2D images in the environment. |
| [`ObjectTrackingProvider`](references/object-tracking-provider.md) | When tracking 3D objects in the environment. |
| [`RoomTrackingProvider`](references/room-tracking-provider.md) | When tracking room boundaries and room-scale experiences. |
| [`AccessoryTrackingProvider`](references/accessory-tracking-provider.md) | When tracking Apple Vision Pro accessories. |
| [`BarcodeDetectionProvider`](references/barcode-detection-provider.md) | When detecting and reading barcodes in the environment. |
| [`CameraFrameProvider`](references/camera-frame-provider.md) | When accessing raw camera frames for custom processing. |
| [`CameraRegionProvider`](references/camera-region-provider.md) | When accessing camera frames from specific regions. |
| [`EnvironmentLightEstimationProvider`](references/environment-light-estimation-provider.md) | When estimating ambient lighting conditions. |
| [`SharedCoordinateSpaceProvider`](references/shared-coordinate-space-provider.md) | When sharing coordinate spaces across multiple sessions. |
| [`StereoPropertiesProvider`](references/stereo-properties-provider.md) | When accessing stereo camera properties. |

### General ARKit Patterns

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When implementing ARKit session setup, authorization, and general provider patterns. |

### Pitfalls and Checks

- On visionOS, `ARView` is **not available** — it inherits from `UIView`/`NSView`, neither of which exist on visionOS. Always use `RealityView` for presentation and `ARKitSession` for tracking data. If you are porting iOS/macOS code that used `ARView` hit-testing or overlays, migrate to `RealityViewContent` and `Entity.hitTest(_:query:mask:)`.
- Do not assume every ARKit provider has the same presentation requirements; check the provider-specific guidance before choosing Shared Space, a volumetric window, or an immersive space.
- Do not block the main actor while awaiting provider updates.
- Do not drop session references; ARKit stops sessions on deinit.
