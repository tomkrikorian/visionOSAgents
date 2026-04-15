# Runtime API

Use this file when the material needs to be loaded or controlled from Swift.

```swift
import RealityKit
import RealityKitContent

func loadGlowMaterial(name: String) async throws -> ShaderGraphMaterial {
    var material = try await ShaderGraphMaterial(
        named: "/Root/\(name)",
        from: "Materials.usda",
        in: realityKitContentBundle
    )

    try material.setParameter(name: "glowStrength", value: .float(1.5))
    try material.setParameter(name: "baseColor", value: .color(.systemBlue))
    return material
}
```

For hot paths, cache the `ParameterHandle` from `parameterHandle(forName:)` and
use the handle-based setter instead of repeated name lookup.

On visionOS, `ShaderGraphMaterial` is the first-class custom material path. Do
not add `CustomMaterial`-style flows from iOS or macOS code.
