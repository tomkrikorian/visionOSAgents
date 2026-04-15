---
name: arkit-visionos-developer
description: Build and debug ARKit features for visionOS 26, including ARKitSession setup, authorization, data providers (world tracking, plane detection, scene reconstruction, hand tracking), anchor processing, and RealityKit integration. Use when implementing ARKit workflows on visionOS or troubleshooting provider-specific space, privacy, and lifecycle behavior.
---

# ARKit visionOS Developer

## Quick Start

1. Identify the provider set first: world tracking, hand tracking, plane
   detection, scene reconstruction, or another specialized provider.
2. Add only the usage strings required by the providers you actually use.
3. Create a long-lived `ARKitSession` and request authorization before running
   it.
4. Load the shared session, anchor, or bridge references first, then load only
   the provider files you actually need.
5. Keep anchor state in a model layer, and bridge into RealityKit only when
   you have a rendering target.
6. If the issue is app launch, test flow, simulator behavior, or signing,
   switch to `build-run-debug` or `signing-entitlements`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`references/provider-index.md`](references/provider-index.md) | When you need the provider map and routing guidance. |
| [`references/session-basics.md`](references/session-basics.md) | When setting up `ARKitSession`, authorization, or shared lifecycle rules. |
| [`references/anchor-processing.md`](references/anchor-processing.md) | When reconciling `anchorUpdates`, IDs, and model-layer state. |
| [`references/realitykit-bridge.md`](references/realitykit-bridge.md) | When ARKit data needs to become visible RealityKit scene content. |
| [`references/world-tracking-provider.md`](references/world-tracking-provider.md) | When tracking device pose or world anchors. |
| [`references/hand-tracking-provider.md`](references/hand-tracking-provider.md) | When tracking hands and joints. |
| [`references/plane-detection-provider.md`](references/plane-detection-provider.md) | When detecting horizontal or vertical planes. |
| [`references/scene-reconstruction-provider.md`](references/scene-reconstruction-provider.md) | When consuming mesh reconstruction. |
| [`references/image-tracking-provider.md`](references/image-tracking-provider.md) | When tracking known 2D images. |
| [`references/object-tracking-provider.md`](references/object-tracking-provider.md) | When tracking 3D objects. |
| [`references/room-tracking-provider.md`](references/room-tracking-provider.md) | When tracking room boundaries and room-scale features. |
| [`references/accessory-tracking-provider.md`](references/accessory-tracking-provider.md) | When tracking supported accessories. |
| [`references/barcode-detection-provider.md`](references/barcode-detection-provider.md) | When detecting and reading barcodes. |
| [`references/camera-frame-provider.md`](references/camera-frame-provider.md) | When accessing raw camera frames. |
| [`references/camera-region-provider.md`](references/camera-region-provider.md) | When reading region-scoped camera content. |
| [`references/environment-light-estimation-provider.md`](references/environment-light-estimation-provider.md) | When estimating ambient lighting. |
| [`references/shared-coordinate-space-provider.md`](references/shared-coordinate-space-provider.md) | When sharing coordinate spaces across participants or sessions. |
| [`references/stereo-properties-provider.md`](references/stereo-properties-provider.md) | When working with stereo camera properties. |

## Workflow

1. Choose the provider set.
2. Load the shared session and lifecycle guidance first.
3. Add only the provider references that match the task.
4. Keep anchor reconciliation in a model layer.
5. Bridge into RealityKit only after the model layer has stable state.

## Guardrails

- Keep a strong reference to `ARKitSession` for the full lifetime of the
  experience.
- Request authorization before running providers that need it.
- Do not block the main actor while awaiting provider updates.
- Do not assume every provider has the same presentation requirements.
- Route launch, build, simulator, and codesign problems out to the execution
  skills instead of expanding this skill with run-loop detail.

## Output Expectations

Provide:
- the chosen provider set
- which shared and provider references were used
- the session and anchor-processing model
- the RealityKit bridge plan if applicable
- the next skill to use if the blocker is execution, signing, or scene work
