---
name: arkit-spatial-tracking-providers
description: "Build and debug ARKit spatial tracking providers for visionOS 27: WorldTrackingProvider, PlaneDetectionProvider, SceneReconstructionProvider, RoomTrackingProvider, and SharedCoordinateSpaceProvider. Use when implementing world anchors, device pose queries, surface placement, mesh reconstruction, room context, or shared coordinate spaces."
---

# ARKit Spatial Tracking Providers

## Quick Start

1. Identify the spatial signal: device/world pose, detected planes, scene
   meshes, room state, or shared coordinates.
2. Load the shared ARKit session guidance first, then only the provider
   reference that matches the task.
3. Keep anchor reconciliation in a model layer; bridge to RealityKit only after
   model state is stable.
4. For provider selection across unrelated ARKit capabilities, switch back to
   `$arkit-visionos-developer`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`session-basics.md`](../arkit-visionos-developer/references/session-basics.md) | When setting up `ARKitSession`, authorization, events, run retries, or teardown. |
| [`anchor-processing.md`](../arkit-visionos-developer/references/anchor-processing.md) | When reconciling anchor IDs, `anchorUpdates`, and model-layer state. |
| [`realitykit-bridge.md`](../arkit-visionos-developer/references/realitykit-bridge.md) | When spatial state needs to become visible RealityKit content. |
| [`world-tracking-provider.md`](../arkit-visionos-developer/references/world-tracking-provider.md) | When using `WorldTrackingProvider` for device pose or world anchors. |
| [`plane-detection-provider.md`](../arkit-visionos-developer/references/plane-detection-provider.md) | When using `PlaneDetectionProvider` for horizontal or vertical surfaces. |
| [`scene-reconstruction-provider.md`](../arkit-visionos-developer/references/scene-reconstruction-provider.md) | When using `SceneReconstructionProvider` for mesh anchors. |
| [`room-tracking-provider.md`](../arkit-visionos-developer/references/room-tracking-provider.md) | When using `RoomTrackingProvider` for room-scale context. |
| [`shared-coordinate-space-provider.md`](../arkit-visionos-developer/references/shared-coordinate-space-provider.md) | When using `SharedCoordinateSpaceProvider` for multi-participant coordinate spaces. |

## Workflow

1. Check provider support and required authorizations before constructing the
   run list.
2. Build the provider list explicitly; do not hide unrelated providers in a
   shared session helper.
3. Start the long-lived `ARKitSession`, observe `session.events`, and cancel
   update tasks on teardown.
4. Recreate provider instances before retrying `run(_:)` after a thrown run or
   stopped provider state.

## Guardrails

- Use `WorldTrackingProvider` for world-locked content and pose queries, not
  for surface semantics that belong to plane or mesh providers.
- Treat plane, mesh, room, and shared-coordinate data as different coordinate
  contracts; do not merge them without an explicit model-layer boundary.
- Do not block the main actor while awaiting provider update sequences.

## Output Expectations

Provide:
- the spatial provider set chosen
- which shared and provider references were used
- the authorization and session lifecycle model
- the anchor state model and RealityKit bridge if applicable
