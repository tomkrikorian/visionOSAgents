# SwiftUI Scene Lifecycle on visionOS

Use this file when implementing or reviewing windows, volumes, immersive
spaces, launch behavior, or restoration on visionOS.

## Scene API Choices

- `Window`: one unique window surface.
- `WindowGroup`: multiple instances or ID-addressable window groups.
- Volumetric `WindowGroup`: bounded 3D content with `.windowStyle(.volumetric)`.
- `ImmersiveSpace`: unbounded immersive content.

Keep scene declarations in the app scene layer. Keep open/dismiss decisions in
a scene coordinator or root view when multiple controls can trigger the same
surface.

## Open and Dismiss Rules

- Use `openWindow(id:)` / `dismissWindow(id:)` for windows.
- Use `openImmersiveSpace(id:)` / `dismissImmersiveSpace()` for immersive
  spaces.
- Treat `openImmersiveSpace(id:)` result cases as state:
  `.opened`, `.userCancelled`, `.error`, and `@unknown default`.
- Track an explicit immersive phase so cancelled or failed opens do not leave
  controls disabled or out of sync.
- Only one immersive space can be open at a time.

## System-Mediated Behavior

- `defaultSize(...)` is an initial size hint; the system may clamp, restore, or
  adapt geometry.
- `defaultLaunchBehavior(...)` controls launch presentation preference.
- `restorationBehavior(...)` controls scene restoration.
- `windowResizability(...)` should match the intended sizing contract.
- `defaultWorldScaling(...)`, `supportedVolumeViewpoints(...)`,
  `onVolumeViewpointChange(...)`, and `volumeBaseplateVisibility(...)` are
  volume-specific tools; do not treat them as generic window modifiers.
