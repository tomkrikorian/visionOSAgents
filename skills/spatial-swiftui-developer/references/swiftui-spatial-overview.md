# Spatial SwiftUI + RealityKit Code Patterns

Use the feature files below based on the API area you need.

## API Routing

- Use `Model3D` for simple model display, SwiftUI layout, phase-based loading,
  basic animation controls, and `manipulable()` interactions.
- Use `RealityView` when you need a custom entity graph, component mutation,
  attachments, systems, subscriptions, physics, custom placement, or mixed
  SwiftUI/RealityKit ownership.
- Use a normal window for controls, navigation, forms, document-style work, and
  status panels.
- Use a volumetric window when the 3D content is bounded and should keep a
  system-managed container.
- Use `ImmersiveSpace` when the scene needs unbounded presence, spatial media,
  ARKit/world context, or a dedicated immersive lifecycle.

If the answer depends on which surface owns the feature, switch to
`spatial-app-architecture` before choosing APIs.

## Feature files
- [model3d.md](model3d.md) - Model3D loading, assets, animation, and manipulable.
- [realityview.md](realityview.md) - RealityView setup, attachments, and RealityKit scene patterns.
- [interaction.md](interaction.md) - Gestures and manipulation patterns for spatial input.
- [windowing-immersion.md](windowing-immersion.md) - Window management and immersive space patterns.
- [spatial-layout.md](spatial-layout.md) - SwiftUI spatial layout APIs and debug tools.
- [charts-3d.md](charts-3d.md) - Chart3D and surface plot patterns.
