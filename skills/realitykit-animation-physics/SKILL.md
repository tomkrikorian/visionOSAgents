---
name: realitykit-animation-physics
description: Implement and debug RealityKit animation, character controllers, skeletal poses, IK, body tracking, blendshapes, animation graphs, retargeting, root motion, navigation, behavior trees, collision, physics bodies, joints, forces, particles, compute simulations, and cloth on visionOS 27. Use when a RealityKit task is primarily about motion, character behavior, physical simulation, hit-test collision shape details, particle simulation, or animation/physics troubleshooting.
---

# RealityKit Animation Physics

## Quick Start

1. Decide whether the task is animation, character motion, navigation/behavior,
   collision, rigid physics, forces/joints, particles, compute simulation, or
   cloth.
2. Load the matching reference file only.
3. Use documented RealityKit animation and physics components before custom
   ECS update loops.
4. Switch to `realitykit-ecs-systems` when behavior needs custom per-frame
   processing across multiple entities.
5. Switch to `realitykit-visionos-developer` for general input, attachments,
   entity loading, anchoring, or non-physics component selection.

## Load References When

| Reference | When to Use |
|---|---|
| [`references/animationlibrarycomponent.md`](references/animationlibrarycomponent.md) | Work with loaded animation clips or animation libraries. |
| [`references/animation-graphs-and-retargeting.md`](references/animation-graphs-and-retargeting.md) | Use animation graphs, retargeting, root motion, or mesh deformers. |
| [`references/blendshapeweightscomponent.md`](references/blendshapeweightscomponent.md) | Drive blendshape weights for facial, character, or mesh deformation. |
| [`references/skeletalposescomponent.md`](references/skeletalposescomponent.md) | Inspect or set skeletal pose state. |
| [`references/ikcomponent.md`](references/ikcomponent.md) | Configure inverse kinematics. |
| [`references/bodytrackingcomponent.md`](references/bodytrackingcomponent.md) | Use body tracking component state. |
| [`references/charactercontrollercomponent.md`](references/charactercontrollercomponent.md) and [`references/charactercontrollerstatecomponent.md`](references/charactercontrollerstatecomponent.md) | Build character controller movement and inspect controller state. |
| [`references/navigation-and-behavior-trees.md`](references/navigation-and-behavior-trees.md) | Add navmesh pathfinding, agent steering, or behavior trees. |
| [`references/collisioncomponent.md`](references/collisioncomponent.md) | Define collision shapes for physics, contacts, hit testing, or input targeting. |
| [`references/physicsbodycomponent.md`](references/physicsbodycomponent.md), [`references/physicsmotioncomponent.md`](references/physicsmotioncomponent.md), [`references/physicssimulationcomponent.md`](references/physicssimulationcomponent.md) | Configure rigid-body physics, motion, and simulation behavior. |
| [`references/physicsjointscomponent.md`](references/physicsjointscomponent.md), [`references/forceeffectcomponent.md`](references/forceeffectcomponent.md), [`references/geometricpinscomponent.md`](references/geometricpinscomponent.md) | Configure joints, forces, and pinning. |
| [`references/particleemittercomponent.md`](references/particleemittercomponent.md) | Use built-in particle emitters. |
| [`references/compute-graph-particles.md`](references/compute-graph-particles.md) | Build GPU particles or compute simulations with `ComputeGraph`. |
| [`references/cloth-simulation.md`](references/cloth-simulation.md) | Simulate cloth bodies, cloth colliders, or cloth grabbing. |

## Cross-Routing

- Use `realitykit-rendering-materials` for visual appearance, materials,
  cameras, lights, shadows, splats, LOD, or post-processing.
- Use `realitykit-audio-spatial` for audio events tied to motion or physics.
- Use `realitykit-ecs-systems` for custom systems, component registration,
  update queries, or continuous multi-entity behavior.
- Use `realitykit-visionos-developer` for `InputTargetComponent`, gestures,
  `ManipulationComponent`, attachments, or asset-loading ownership.

## Guardrails

- Collision shapes serve both hit testing and physics; verify the intended
  owner before changing them.
- Keep continuous simulation behavior in RealityKit systems or documented
  components, not SwiftUI body code.
- Treat visionOS 27 animation, navigation, compute, and cloth additions as
  beta API; re-check symbols against the installed SDK.
- Validate simulation work with deterministic inputs where possible and note
  whether the check ran in simulator or on device.

## Output Expectations

Provide:

- the animation or physics category
- which references were used
- the component or system path chosen
- the motion, collision, or simulation constraint
- the next runtime validation step
