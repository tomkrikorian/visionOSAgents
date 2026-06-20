---
name: arkit-hand-tracking-provider
description: Build and debug HandTrackingProvider on visionOS 27. Use when implementing hand anchors, hand joint transforms, custom hand gestures, hand-driven interactions, hand visualizations, or troubleshooting hand-tracking authorization, support, and lifecycle behavior.
---

# ARKit Hand Tracking Provider

## Quick Start

1. Confirm the task needs raw hand/joint data; use SwiftUI or RealityKit
   gestures when high-level interaction is enough.
2. Load the shared session guidance and the hand provider reference.
3. Add hands privacy text and request the provider's required authorizations.
4. Keep joint processing in a model layer, then bridge to SwiftUI or RealityKit
   only where needed.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`session-basics.md`](../arkit-visionos-developer/references/session-basics.md) | When setting up `ARKitSession`, authorization, event handling, or teardown. |
| [`hand-tracking-provider.md`](../arkit-visionos-developer/references/hand-tracking-provider.md) | When using `HandTrackingProvider`, `HandAnchor`, or joint transforms. |
| [`anchor-processing.md`](../arkit-visionos-developer/references/anchor-processing.md) | When reconciling hand anchor updates into app state. |
| [`realitykit-bridge.md`](../arkit-visionos-developer/references/realitykit-bridge.md) | When visualizing hands or driving RealityKit entities. |

## Workflow

1. Check `HandTrackingProvider.isSupported`.
2. Request `HandTrackingProvider.requiredAuthorizations`.
3. Run the provider in a long-lived `ARKitSession`.
4. Process update sequences off the SwiftUI body path.
5. Cancel the update task and stop the session on teardown.

## Guardrails

- Do not use raw hand tracking for ordinary taps, drags, or gaze-targeted UI
  that platform gestures already handle.
- Do not assume both hands or every joint are always tracked.
- Treat hand-tracking denial as a feature-level unavailable state, not as an
  app launch failure.

## Output Expectations

Provide:
- whether raw hand tracking is actually required
- which hand provider references were used
- the authorization and unsupported-device behavior
- the joint processing and rendering path
