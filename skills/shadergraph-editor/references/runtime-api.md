# Runtime API

Use this file when the material needs to be loaded or controlled from Swift.

```swift
import CoreGraphics
import RealityKit
import RealityKitContent

func loadGlowMaterial(name: String) async throws -> ShaderGraphMaterial {
    var material = try await ShaderGraphMaterial(
        named: "/Root/\(name)",
        from: "Materials.usda",
        in: realityKitContentBundle
    )

    try material.setParameter(name: "glowStrength", value: .float(1.5))
    try material.setParameter(
        name: "baseColor",
        value: .color(CGColor(red: 0.0, green: 0.38, blue: 1.0, alpha: 1.0))
    )
    return material
}
```

## Promoted Inputs

- Promote constants in Reality Composer Pro for every value Swift needs to
  control at runtime.
- Match promoted input names exactly; names are case-sensitive.
- Use `material.parameterNames` to confirm the exported material exposes the
  expected controls before setting them.
- Use the `MaterialParameters.Value` case that matches the promoted input type:
  `.bool`, `.float`, `.int`, `.simd2Float`, `.simd3Float`, `.simd4Float`,
  `.float4x4`, `.color`, `.texture`, or `.textureResource`.

## Updating Materials on Entities

Materials are value types inside `ModelComponent.materials`. Mutate a copy and
write the component back to the entity.

```swift
func updatePromotedParameter(
    on entity: Entity,
    name: String,
    value: MaterialParameters.Value
) throws {
    guard var model = entity.components[ModelComponent.self] else { return }

    model.materials = try model.materials.map { material in
        guard var shader = material as? ShaderGraphMaterial else {
            return material
        }
        guard shader.parameterNames.contains(name) else {
            return material
        }

        try shader.setParameter(name: name, value: value)
        return shader
    }

    entity.components.set(model)
}
```

For hot paths, cache the `MaterialParameters.Handle` from
`ShaderGraphMaterial.parameterHandle(name:)` and use the handle-based setter
instead of repeated name lookup.

```swift
let glowHandle = ShaderGraphMaterial.parameterHandle(name: "glowStrength")
try material.setParameter(handle: glowHandle, value: .float(2.0))
```

On visionOS, `ShaderGraphMaterial` is the first-class custom material path. Do
not add `CustomMaterial`-style flows from iOS or macOS code unless the project
already has a tested platform-specific reason.
