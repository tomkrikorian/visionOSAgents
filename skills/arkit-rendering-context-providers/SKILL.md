---
name: arkit-rendering-context-providers
description: "Build and debug ARKit rendering-context providers for visionOS 27: EnvironmentLightEstimationProvider, StereoPropertiesProvider, and VisualFidelityProvider. Use when matching virtual lighting to the environment, informing custom stereo rendering, coaching device fit, or tuning foveated field of view."
---

# ARKit Rendering Context Providers

## Quick Start

1. Identify whether the rendering problem needs lighting, stereo viewpoint
   properties, or visual fidelity/device-fit data.
2. Load the shared ARKit session guidance, then only the matching provider
   reference.
3. Keep these providers as rendering inputs; do not mix them with anchor
   ownership unless the task also uses a spatial provider.
4. Route RealityKit component or material implementation details to
   `$realitykit-visionos-developer` or `$shadergraph-editor`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`session-basics.md`](../arkit-visionos-developer/references/session-basics.md) | When setting up `ARKitSession`, authorization, events, or teardown. |
| [`environment-light-estimation-provider.md`](../arkit-visionos-developer/references/environment-light-estimation-provider.md) | When using `EnvironmentLightEstimationProvider` and environment probes. |
| [`stereo-properties-provider.md`](../arkit-visionos-developer/references/stereo-properties-provider.md) | When using `StereoPropertiesProvider` for custom stereo rendering inputs. |
| [`visual-fidelity-provider.md`](../arkit-visionos-developer/references/visual-fidelity-provider.md) | When using `VisualFidelityProvider` for device-fit status or foveated field of view. |
| [`realitykit-bridge.md`](../arkit-visionos-developer/references/realitykit-bridge.md) | When provider output needs to drive RealityKit entities or rendering state. |

## Workflow

1. Check provider support and required authorizations.
2. Decide how the rendering pipeline consumes provider output.
3. Run only the provider needed for the rendering signal.
4. Observe update sequences and store the latest rendering context in a model
   object that rendering code can consume.

## Guardrails

- Do not present visual-fidelity coaching unless that is the intended user
  experience.
- Keep custom stereo-rendering decisions isolated from SwiftUI layout code.
- Treat environment lighting as an input to rendering, not as a replacement for
  authored material or Shader Graph work.

## Output Expectations

Provide:
- the rendering-context provider selected
- which provider references were used
- support, authorization, and beta-API caveats
- how the app consumes the provider output
