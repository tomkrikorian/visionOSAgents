---
name: arkit-camera-access-providers
description: "Build and debug ARKit camera access providers for visionOS 27: CameraFrameProvider and CameraRegionProvider. Use when accessing camera frame streams, region-scoped camera content, custom computer-vision pipelines, or troubleshooting camera-access authorization, entitlement, enterprise, format, and support issues."
---

# ARKit Camera Access Providers

## Quick Start

1. Confirm the task needs ARKit camera data, not a rendered RealityKit or
   SwiftUI snapshot.
2. Choose full camera frame access or region-scoped camera capture.
3. Check support, privacy text, entitlement, and enterprise constraints before
   debugging update delivery.
4. Keep frame handling off the SwiftUI body path and avoid retaining stale
   frame buffers beyond the API contract.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`session-basics.md`](../arkit-visionos-developer/references/session-basics.md) | When setting up `ARKitSession`, authorization, events, or teardown. |
| [`camera-frame-provider.md`](../arkit-visionos-developer/references/camera-frame-provider.md) | When using `CameraFrameProvider` and `cameraFrameUpdates(for:)`. |
| [`camera-region-provider.md`](../arkit-visionos-developer/references/camera-region-provider.md) | When using `CameraRegionProvider` and `CameraRegionAnchor`. |

## Workflow

1. Verify the camera-access requirement and target OS/device support.
2. Confirm Info.plist text, entitlement/profile, and enterprise requirements.
3. Select camera format or region definition deliberately.
4. Request provider authorizations, run the provider, and process updates in a
   dedicated model or pipeline object.

## Guardrails

- Do not assume all camera providers are generally available; treat missing
  entitlement/profile support as a first-class blocker.
- Do not widen camera access when a narrower region or non-camera API satisfies
  the feature.
- Do not route camera provider build, signing, or provisioning failures here;
  use `$signing-entitlements` or `$build-run-debug`.

## Output Expectations

Provide:
- which camera provider was chosen and why
- support, privacy, entitlement, and enterprise checks
- which camera references were used
- the frame or region processing model
