---
name: arkit-visionos-developer
description: Build and debug ARKit features for visionOS, including ARKitSession setup, authorization, data providers (world tracking, plane detection, scene reconstruction, hand tracking), anchor processing, and RealityKit integration. Use when implementing ARKit workflows in immersive spaces or troubleshooting ARKit data access and provider behavior on visionOS.
---

# ARKit visionOS Developer

## Overview

Use this skill to implement ARKit-powered features on visionOS with ARKitSession and data providers, then bridge anchors into RealityKit content safely and efficiently.

## Quick start workflow

1. Add `NSWorldSensingUsageDescription` and `NSHandsTrackingUsageDescription` to `Info.plist` as needed.
2. Ensure the experience runs in a Full Space (ARKit data is unavailable in Shared Space).
3. Create a long-lived `ARKitSession` and the data providers you need.
4. Request authorization for provider-required data types before running the session.
5. Run the session with your providers and observe `anchorUpdates` streams.
6. Map anchors to RealityKit entities and keep state in a model layer.
7. Observe `ARKitSession.events` for authorization changes and errors.
8. Stop the session and cancel tasks when leaving the immersive space.

## Core concepts

- **ARKitSession lifecycle**: Keep a strong reference, call `run(_:)` with providers, stop on teardown.
- **Authorization**: Use `requestAuthorization(for:)` or `queryAuthorization(for:)` and handle denied states gracefully.
- **Data providers**: Choose providers for world tracking, plane detection, scene reconstruction, and hand tracking based on the feature set.
- **Anchors and updates**: Consume provider `anchorUpdates` and reconcile added, updated, and removed anchors.
- **RealityKit bridge**: Use `ARKitAnchorComponent` to inspect backing ARKit data on entities when needed.

## Implementation patterns

- Prefer one session per immersive experience and reuse providers when possible.
- Normalize anchor IDs to your own state model for reliable entity updates.
- Treat ARKit streams as authoritative and keep rendering logic in RealityKit.

## Pitfalls and checks

- Do not use `ARView` on visionOS; use `RealityView` and `ARKitSession` instead.
- Do not expect ARKit data in Shared Space; use Full Space only.
- Do not block the main actor while awaiting provider updates.
- Do not drop session references; ARKit stops sessions on deinit.

## References

- [references/DOCUMENTATION.DM](references/DOCUMENTATION.DM) - sosumi documentation paths for ARKit on visionOS.
- [references/REFERENCE.md](references/REFERENCE.md) - ARKit session and provider code patterns.
