# RealityKit Reference Map

Load this file from `realitykit-visionos-developer` when you need to decide
which RealityKit skill or detailed component file to open next. Categories
marked "new in visionOS 27" cover beta API; names may change before release.

## Core Scene, Entity, Input, and Spatial References

These stay with `realitykit-visionos-developer`:

- Component choice:
  [`component-selection.md`](component-selection.md)
- Entity and asset loading:
  [`entity-loading-and-stored-entities.md`](entity-loading-and-stored-entities.md)
- Interaction:
  [`inputtargetcomponent.md`](inputtargetcomponent.md),
  [`manipulationcomponent.md`](manipulationcomponent.md),
  [`gesturecomponent.md`](gesturecomponent.md),
  [`hovereffectcomponent.md`](hovereffectcomponent.md),
  [`accessibilitycomponent.md`](accessibilitycomponent.md),
  [`billboardcomponent.md`](billboardcomponent.md)
- Anchoring and spatial:
  [`anchoringcomponent.md`](anchoringcomponent.md),
  [`arkitanchorcomponent.md`](arkitanchorcomponent.md),
  [`sceneunderstandingcomponent.md`](sceneunderstandingcomponent.md),
  [`dockingregioncomponent.md`](dockingregioncomponent.md),
  [`referencecomponent.md`](referencecomponent.md),
  [`attachedtransformcomponent.md`](attachedtransformcomponent.md),
  [`spatialtrackingsession.md`](spatialtrackingsession.md)
- Presentation and attachments:
  [`viewattachmentcomponent.md`](viewattachmentcomponent.md),
  [`presentationcomponent.md`](presentationcomponent.md),
  [`textcomponent.md`](textcomponent.md),
  [`imagepresentationcomponent.md`](imagepresentationcomponent.md),
  [`videoplayercomponent.md`](videoplayercomponent.md)
- Portals and environments:
  [`portalcomponent.md`](portalcomponent.md),
  [`worldcomponent.md`](worldcomponent.md),
  [`portalcrossingcomponent.md`](portalcrossingcomponent.md),
  [`environmentblendingcomponent.md`](environmentblendingcomponent.md),
  [`portal-volumes-and-accessory-anchoring.md`](portal-volumes-and-accessory-anchoring.md)
- Networking and sync:
  [`synchronizationcomponent.md`](synchronizationcomponent.md),
  [`transientcomponent.md`](transientcomponent.md)
- USD bridge:
  [`usdstagecomponent.md`](usdstagecomponent.md)

## Focused RealityKit Skills

- Rendering and materials:
  `realitykit-rendering-materials`
  - [`modelcomponent.md`](../../realitykit-rendering-materials/references/modelcomponent.md)
  - [`modelsortgroupcomponent.md`](../../realitykit-rendering-materials/references/modelsortgroupcomponent.md)
  - [`opacitycomponent.md`](../../realitykit-rendering-materials/references/opacitycomponent.md)
  - [`adaptiveresolutioncomponent.md`](../../realitykit-rendering-materials/references/adaptiveresolutioncomponent.md)
  - [`meshinstancescomponent.md`](../../realitykit-rendering-materials/references/meshinstancescomponent.md)
  - New in visionOS 27:
    [`gaussiansplatcomponent.md`](../../realitykit-rendering-materials/references/gaussiansplatcomponent.md),
    [`tonemappingcomponent.md`](../../realitykit-rendering-materials/references/tonemappingcomponent.md),
    [`bloomcomponent.md`](../../realitykit-rendering-materials/references/bloomcomponent.md),
    [`physicallybaseddecalcomponent.md`](../../realitykit-rendering-materials/references/physicallybaseddecalcomponent.md),
    [`clippingcomponent.md`](../../realitykit-rendering-materials/references/clippingcomponent.md),
    [`levelofdetailcomponent.md`](../../realitykit-rendering-materials/references/levelofdetailcomponent.md),
    [`occlusioncullingcomponent.md`](../../realitykit-rendering-materials/references/occlusioncullingcomponent.md)
- Cameras, lighting, shadows, and probes:
  `realitykit-rendering-materials`
  - [`perspectivecameracomponent.md`](../../realitykit-rendering-materials/references/perspectivecameracomponent.md)
  - [`orthographiccameracomponent.md`](../../realitykit-rendering-materials/references/orthographiccameracomponent.md)
  - [`projectivetransformcameracomponent.md`](../../realitykit-rendering-materials/references/projectivetransformcameracomponent.md)
  - [`pointlightcomponent.md`](../../realitykit-rendering-materials/references/pointlightcomponent.md)
  - [`directionallightcomponent.md`](../../realitykit-rendering-materials/references/directionallightcomponent.md)
  - [`spotlightcomponent.md`](../../realitykit-rendering-materials/references/spotlightcomponent.md)
  - [`imagebasedlightcomponent.md`](../../realitykit-rendering-materials/references/imagebasedlightcomponent.md)
  - [`imagebasedlightreceivercomponent.md`](../../realitykit-rendering-materials/references/imagebasedlightreceivercomponent.md)
  - [`groundingshadowcomponent.md`](../../realitykit-rendering-materials/references/groundingshadowcomponent.md)
  - [`dynamiclightshadowcomponent.md`](../../realitykit-rendering-materials/references/dynamiclightshadowcomponent.md)
  - [`environmentlightingconfigurationcomponent.md`](../../realitykit-rendering-materials/references/environmentlightingconfigurationcomponent.md)
  - [`virtualenvironmentprobecomponent.md`](../../realitykit-rendering-materials/references/virtualenvironmentprobecomponent.md)
  - New in visionOS 27:
    [`render-layers-and-shadows.md`](../../realitykit-rendering-materials/references/render-layers-and-shadows.md),
    [`lightmaps-and-probes.md`](../../realitykit-rendering-materials/references/lightmaps-and-probes.md)
- Animation, characters, navigation, and physics:
  `realitykit-animation-physics`
  - [`animationlibrarycomponent.md`](../../realitykit-animation-physics/references/animationlibrarycomponent.md)
  - [`blendshapeweightscomponent.md`](../../realitykit-animation-physics/references/blendshapeweightscomponent.md)
  - [`charactercontrollercomponent.md`](../../realitykit-animation-physics/references/charactercontrollercomponent.md)
  - [`charactercontrollerstatecomponent.md`](../../realitykit-animation-physics/references/charactercontrollerstatecomponent.md)
  - [`skeletalposescomponent.md`](../../realitykit-animation-physics/references/skeletalposescomponent.md)
  - [`ikcomponent.md`](../../realitykit-animation-physics/references/ikcomponent.md)
  - [`bodytrackingcomponent.md`](../../realitykit-animation-physics/references/bodytrackingcomponent.md)
  - [`collisioncomponent.md`](../../realitykit-animation-physics/references/collisioncomponent.md)
  - [`physicsbodycomponent.md`](../../realitykit-animation-physics/references/physicsbodycomponent.md)
  - [`physicsmotioncomponent.md`](../../realitykit-animation-physics/references/physicsmotioncomponent.md)
  - [`physicssimulationcomponent.md`](../../realitykit-animation-physics/references/physicssimulationcomponent.md)
  - [`particleemittercomponent.md`](../../realitykit-animation-physics/references/particleemittercomponent.md)
  - [`forceeffectcomponent.md`](../../realitykit-animation-physics/references/forceeffectcomponent.md)
  - [`physicsjointscomponent.md`](../../realitykit-animation-physics/references/physicsjointscomponent.md)
  - [`geometricpinscomponent.md`](../../realitykit-animation-physics/references/geometricpinscomponent.md)
  - New in visionOS 27:
    [`animation-graphs-and-retargeting.md`](../../realitykit-animation-physics/references/animation-graphs-and-retargeting.md),
    [`navigation-and-behavior-trees.md`](../../realitykit-animation-physics/references/navigation-and-behavior-trees.md),
    [`cloth-simulation.md`](../../realitykit-animation-physics/references/cloth-simulation.md),
    [`compute-graph-particles.md`](../../realitykit-animation-physics/references/compute-graph-particles.md)
- Audio:
  `realitykit-audio-spatial`
  - [`spatialaudiocomponent.md`](../../realitykit-audio-spatial/references/spatialaudiocomponent.md)
  - [`ambientaudiocomponent.md`](../../realitykit-audio-spatial/references/ambientaudiocomponent.md)
  - [`channelaudiocomponent.md`](../../realitykit-audio-spatial/references/channelaudiocomponent.md)
  - [`audiolibrarycomponent.md`](../../realitykit-audio-spatial/references/audiolibrarycomponent.md)
  - [`reverbcomponent.md`](../../realitykit-audio-spatial/references/reverbcomponent.md)
  - [`audiomixgroupscomponent.md`](../../realitykit-audio-spatial/references/audiomixgroupscomponent.md)
  - New in visionOS 27:
    [`audio-groups-and-acoustics.md`](../../realitykit-audio-spatial/references/audio-groups-and-acoustics.md)
- Custom ECS:
  `realitykit-ecs-systems`
  - [`custom-components.md`](../../realitykit-ecs-systems/references/custom-components.md)
  - [`custom-systems.md`](../../realitykit-ecs-systems/references/custom-systems.md)
  - [`systemandcomponentcreation.md`](../../realitykit-ecs-systems/references/systemandcomponentcreation.md)
