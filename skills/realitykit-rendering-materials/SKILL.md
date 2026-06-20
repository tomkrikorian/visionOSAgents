---
name: realitykit-rendering-materials
description: Implement and debug RealityKit rendering, materials, lighting, cameras, visual effects, post-processing, render cost controls, Gaussian splats, decals, lightmaps, probes, LOD, and occlusion on visionOS 27. Use when a RealityKit task is primarily about visual appearance, mesh/material display, lights, shadows, tone mapping, bloom, camera projection, rendering performance, or choosing rendering components instead of animation, audio, interaction, or custom ECS behavior.
---

# RealityKit Rendering Materials

## Quick Start

1. Confirm the issue is visual: mesh display, material assignment, camera
   projection, lighting, shadows, post-processing, splats, decals, LOD,
   occlusion, or probes.
2. Load the narrowest rendering reference that matches the feature.
3. Route ShaderGraph or USDA material graph editing to `shadergraph-editor`.
4. Route local USD stage rendering through
   `realitykit-visionos-developer`; route USD authoring to `usd-editor`.
5. Validate on device or simulator with concrete visual checks, because many
   rendering issues are asset-, lighting-, or hardware-dependent.

## Load References When

| Reference | When to Use |
|---|---|
| [`references/modelcomponent.md`](references/modelcomponent.md) | Render meshes and assign RealityKit materials. |
| [`references/modeldebugoptionscomponent.md`](references/modeldebugoptionscomponent.md) | Inspect or debug model rendering output. |
| [`references/meshinstancescomponent.md`](references/meshinstancescomponent.md) | Reuse mesh instances efficiently. |
| [`references/modelsortgroupcomponent.md`](references/modelsortgroupcomponent.md) | Control model sorting for transparent or layered content. |
| [`references/opacitycomponent.md`](references/opacitycomponent.md) | Control entity opacity. |
| [`references/adaptiveresolutioncomponent.md`](references/adaptiveresolutioncomponent.md) | Manage adaptive resolution. |
| [`references/levelofdetailcomponent.md`](references/levelofdetailcomponent.md) | Select content by distance or detail tier. |
| [`references/occlusioncullingcomponent.md`](references/occlusioncullingcomponent.md) | Reduce render work for hidden content. |
| [`references/gaussiansplatcomponent.md`](references/gaussiansplatcomponent.md) | Render Gaussian splat captures. |
| [`references/physicallybaseddecalcomponent.md`](references/physicallybaseddecalcomponent.md) | Project physically based decals onto geometry. |
| [`references/clippingcomponent.md`](references/clippingcomponent.md) | Clip rendered geometry against bounds. |
| [`references/tonemappingcomponent.md`](references/tonemappingcomponent.md) and [`references/bloomcomponent.md`](references/bloomcomponent.md) | Tune tone mapping and bloom post-processing. |
| [`references/pointlightcomponent.md`](references/pointlightcomponent.md), [`references/directionallightcomponent.md`](references/directionallightcomponent.md), [`references/spotlightcomponent.md`](references/spotlightcomponent.md) | Add or debug direct lights. |
| [`references/imagebasedlightcomponent.md`](references/imagebasedlightcomponent.md) and [`references/imagebasedlightreceivercomponent.md`](references/imagebasedlightreceivercomponent.md) | Configure image-based lighting and receivers. |
| [`references/groundingshadowcomponent.md`](references/groundingshadowcomponent.md), [`references/dynamiclightshadowcomponent.md`](references/dynamiclightshadowcomponent.md), [`references/render-layers-and-shadows.md`](references/render-layers-and-shadows.md) | Tune grounding shadows, dynamic shadows, render layers, and per-light masks. |
| [`references/environmentlightingconfigurationcomponent.md`](references/environmentlightingconfigurationcomponent.md), [`references/virtualenvironmentprobecomponent.md`](references/virtualenvironmentprobecomponent.md), [`references/lightmaps-and-probes.md`](references/lightmaps-and-probes.md) | Configure environment lighting, virtual probes, baked lightmaps, and diffuse probes. |
| [`references/perspectivecameracomponent.md`](references/perspectivecameracomponent.md), [`references/orthographiccameracomponent.md`](references/orthographiccameracomponent.md), [`references/projectivetransformcameracomponent.md`](references/projectivetransformcameracomponent.md) | Work with RealityKit cameras and projection. |

## Cross-Routing

- Use `realitykit-visionos-developer` for entity loading, input, attachments,
  anchoring, portals, synchronization, and local `USDStageComponent`.
- Use `realitykit-animation-physics` when the visual issue is caused by
  animation, blendshape, particle, cloth, collision, or physics state.
- Use `realitykit-ecs-systems` when rendering state is driven by a custom
  component or per-frame system.
- Use `shadergraph-editor` for material graph source edits.

## Guardrails

- Treat visionOS 27 rendering additions as beta API; re-verify symbols against
  the installed SDK before shipping.
- Keep expensive material, mesh, and texture loading asynchronous.
- Validate visual changes with screenshots or simulator/device inspection when
  possible.
- Prefer documented RealityKit components before custom draw or update logic.

## Output Expectations

Provide:

- the rendering category
- which rendering reference files were used
- the chosen component or asset path
- the visual/performance constraint
- the next screenshot, simulator, or device validation step
