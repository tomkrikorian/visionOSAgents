# RealityKit Reference Map

Load this file first when you need to decide which detailed component file to
open next.

## Category Routing

- Rendering and appearance:
  `modelcomponent`, `modelsortgroupcomponent`, `opacitycomponent`,
  `adaptiveresolutioncomponent`, `meshinstancescomponent`,
  `blendshapeweightscomponent`
- Interaction:
  `inputtargetcomponent`, `manipulationcomponent`, `gesturecomponent`,
  `hovereffectcomponent`, `accessibilitycomponent`, `billboardcomponent`
- Anchoring and spatial:
  `anchoringcomponent`, `arkitanchorcomponent`,
  `sceneunderstandingcomponent`, `dockingregioncomponent`,
  `referencecomponent`, `attachedtransformcomponent`
- Cameras:
  `perspectivecameracomponent`, `orthographiccameracomponent`,
  `projectivetransformcameracomponent`
- Lighting and shadows:
  `pointlightcomponent`, `directionallightcomponent`, `spotlightcomponent`,
  `imagebasedlightcomponent`, `groundingshadowcomponent`,
  `dynamiclightshadowcomponent`, `environmentlightingconfigurationcomponent`,
  `virtualenvironmentprobecomponent`
- Audio:
  `spatialaudiocomponent`, `ambientaudiocomponent`,
  `channelaudiocomponent`, `audiolibrarycomponent`, `reverbcomponent`,
  `audiomixgroupscomponent`
- Animation and character:
  `animationlibrarycomponent`, `charactercontrollercomponent`,
  `charactercontrollerstatecomponent`, `skeletalposescomponent`,
  `ikcomponent`, `bodytrackingcomponent`
- Physics and collision:
  `collisioncomponent`, `physicsbodycomponent`, `physicsmotioncomponent`,
  `physicssimulationcomponent`, `particleemittercomponent`,
  `forceeffectcomponent`, `physicsjointscomponent`,
  `geometricpinscomponent`
- Portals and environments:
  `portalcomponent`, `worldcomponent`, `portalcrossingcomponent`,
  `environmentblendingcomponent`
- Presentation and UI:
  `viewattachmentcomponent`, `presentationcomponent`, `textcomponent`,
  `imagepresentationcomponent`, `videoplayercomponent`
- Tracking:
  `spatialtrackingsession`
- Networking and sync:
  `synchronizationcomponent`, `transientcomponent`

## Custom ECS Work

- Use [custom-components.md](custom-components.md) for per-entity data types.
- Use [custom-systems.md](custom-systems.md) for per-frame or query-driven
  behavior.
