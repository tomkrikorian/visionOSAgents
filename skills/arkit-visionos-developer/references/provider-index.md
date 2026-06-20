# ARKit Provider Map

Load this file first when you need to decide which provider reference to open.

## Shared Guidance

- Use [session-basics.md](session-basics.md) for shared session,
  authorization, and lifecycle rules.
- Use [anchor-processing.md](anchor-processing.md) for anchor update
  reconciliation and state ownership.
- Use [realitykit-bridge.md](realitykit-bridge.md) for mapping model-layer
  state into RealityKit entities.

## Provider-Focused Skills

- Use `$arkit-spatial-tracking-providers` for world tracking, plane detection,
  scene reconstruction, room tracking, and shared coordinate spaces.
- Use `$arkit-hand-tracking-provider` for hands, joints, hand-driven
  interactions, and hand visualizations.
- Use `$arkit-reference-tracking-providers` for known images, reference
  objects, barcodes, and accessories.
- Use `$arkit-camera-access-providers` for camera frames and camera regions.
- Use `$arkit-rendering-context-providers` for environment lighting, stereo
  properties, visual fidelity, device-fit status, and foveated field of view.

## Provider Guides

- [accessory-tracking-provider.md](accessory-tracking-provider.md) —
  accessory tracking through `AccessoryTrackingProvider`.
- [barcode-detection-provider.md](barcode-detection-provider.md) —
  barcode anchors through `BarcodeDetectionProvider`; requires the barcode
  detection entitlement.
- [camera-frame-provider.md](camera-frame-provider.md) — camera frame access
  through `CameraFrameProvider`; check entitlement and enterprise constraints.
- [camera-region-provider.md](camera-region-provider.md) — region-scoped
  camera capture through `CameraRegionProvider`; check entitlement and
  enterprise constraints.
- [environment-light-estimation-provider.md](environment-light-estimation-provider.md) —
  environment lighting through `EnvironmentLightEstimationProvider`.
- [hand-tracking-provider.md](hand-tracking-provider.md) — hand and joint data
  through `HandTrackingProvider`; requires hands usage privacy text.
- [image-tracking-provider.md](image-tracking-provider.md) — known image
  anchors through `ImageTrackingProvider`.
- [object-tracking-provider.md](object-tracking-provider.md) — reference object
  anchors through `ObjectTrackingProvider`.
- [plane-detection-provider.md](plane-detection-provider.md) — horizontal and
  vertical plane anchors through `PlaneDetectionProvider`.
- [room-tracking-provider.md](room-tracking-provider.md) — room boundaries and
  room-scale state through `RoomTrackingProvider`.
- [scene-reconstruction-provider.md](scene-reconstruction-provider.md) —
  mesh anchors through `SceneReconstructionProvider`.
- [shared-coordinate-space-provider.md](shared-coordinate-space-provider.md) —
  multi-participant coordinate spaces through `SharedCoordinateSpaceProvider`.
- [stereo-properties-provider.md](stereo-properties-provider.md) — stereo
  viewpoint properties through `StereoPropertiesProvider`.
- [visual-fidelity-provider.md](visual-fidelity-provider.md) — device-fit
  status and foveated field-of-view control through `VisualFidelityProvider`;
  new in visionOS 27.
- [world-tracking-provider.md](world-tracking-provider.md) — device pose and
  world anchors through `WorldTrackingProvider`.

## Provider API Matrix

| Task | Provider | Update Shape | Key Checks |
|------|----------|--------------|------------|
| Device pose or world anchors | `WorldTrackingProvider` | `anchorUpdates`, `queryDeviceAnchor(...)` | `isSupported`, `requiredAuthorizations`, session state |
| Horizontal/vertical planes | `PlaneDetectionProvider` | `PlaneAnchor` updates | `isSupported`, alignment set, authorization result |
| Scene mesh reconstruction | `SceneReconstructionProvider` | `MeshAnchor` updates | `isSupported`, modes, authorization result |
| Hands and joints | `HandTrackingProvider` | `HandAnchor` updates | `isSupported`, `NSHandsTrackingUsageDescription`, authorization result |
| Known 2D images | `ImageTrackingProvider` | `ImageAnchor` updates | reference image set, `isSupported`, authorization result |
| Reference objects | `ObjectTrackingProvider` | `ObjectAnchor` updates | reference object set, `isSupported`, authorization result |
| Room-scale context | `RoomTrackingProvider` | room updates | `isSupported`, presentation requirements, authorization result |
| Accessories | `AccessoryTrackingProvider` | accessory anchor updates | supported accessories, entitlement/profile requirements |
| Barcodes | `BarcodeDetectionProvider` | `BarcodeAnchor` updates | symbologies, entitlement/profile requirements |
| Camera frames | `CameraFrameProvider` | camera frame updates | entitlement/profile requirements, device support |
| Camera regions | `CameraRegionProvider` | `CameraRegionAnchor` updates | entitlement/profile requirements, region definition |
| Lighting | `EnvironmentLightEstimationProvider` | environment probe updates | `isSupported`, authorization result |
| Shared coordinates | `SharedCoordinateSpaceProvider` | provider events and coordinate data | `isSupported`, session topology |
| Stereo properties | `StereoPropertiesProvider` | stereo property snapshots | `isSupported`, rendering pipeline need |
| Device fit and field of view | `VisualFidelityProvider` | `fidelityDataUpdates`, `FieldOfViewAnchor` updates | `isSupported`, authorization result |

For every provider, verify support first, request the provider's
`requiredAuthorizations`, observe `ARKitSession.Events`, and stop/cancel update
tasks on teardown. Recreate providers before retrying `ARKitSession.run(_:)`
after a thrown run or stopped provider state.
