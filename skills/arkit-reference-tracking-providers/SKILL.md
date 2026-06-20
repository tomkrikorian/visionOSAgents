---
name: arkit-reference-tracking-providers
description: "Build and debug ARKit reference and marker tracking providers for visionOS 27: ImageTrackingProvider, ObjectTrackingProvider, BarcodeDetectionProvider, and AccessoryTrackingProvider. Use when anchoring to known images, tracked 3D reference objects, barcodes, or supported accessories."
---

# ARKit Reference Tracking Providers

## Quick Start

1. Identify the physical reference: known image, reference object, barcode, or
   supported accessory.
2. Load the shared ARKit session guidance, then the matching provider file.
3. Confirm required authorizations, privacy text, entitlement, and profile
   requirements before debugging runtime data flow.
4. Keep tracked-reference state separate from RealityKit presentation state.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`session-basics.md`](../arkit-visionos-developer/references/session-basics.md) | When setting up `ARKitSession`, authorization, events, or teardown. |
| [`anchor-processing.md`](../arkit-visionos-developer/references/anchor-processing.md) | When reconciling reference anchor updates into app state. |
| [`realitykit-bridge.md`](../arkit-visionos-developer/references/realitykit-bridge.md) | When tracked references need visible RealityKit content. |
| [`image-tracking-provider.md`](../arkit-visionos-developer/references/image-tracking-provider.md) | When using `ImageTrackingProvider` with known 2D images. |
| [`object-tracking-provider.md`](../arkit-visionos-developer/references/object-tracking-provider.md) | When using `ObjectTrackingProvider` with 3D reference objects. |
| [`barcode-detection-provider.md`](../arkit-visionos-developer/references/barcode-detection-provider.md) | When using `BarcodeDetectionProvider`; check barcode entitlement first. |
| [`accessory-tracking-provider.md`](../arkit-visionos-developer/references/accessory-tracking-provider.md) | When using `AccessoryTrackingProvider` with supported accessories. |

## Workflow

1. Verify the reference asset or target set is correct before touching session
   code.
2. Check provider support and entitlements before interpreting missing updates.
3. Request only the required authorizations for the chosen provider set.
4. Store tracked anchors by stable IDs and remove stale model state on removed
   updates.

## Guardrails

- Do not treat entitlement-gated barcode or accessory data absence as a
  transform bug until signing/profile requirements are proven.
- For object tracking on visionOS 27, prefer the per-object high-frame-rate
  configuration over deprecated rate settings when the app needs it.
- Keep reference-image physical sizes and reference-object orientation
  accurate; bad source metadata causes unstable tracking.

## Output Expectations

Provide:
- the reference provider selected
- the reference assets, entitlement, and authorization checks
- which provider references were used
- the anchor reconciliation and RealityKit bridge plan
