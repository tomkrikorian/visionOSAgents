# Apple Shader Graph and RealityKit Material Boundaries

Use this reference when deciding whether to author a material in Reality
Composer Pro, load a `ShaderGraphMaterial` through RealityKit, or debug named
material and resource failures.

## Official Authoring Boundaries

- Reality Composer Pro is Apple's authoring surface for Shader Graph materials.
  Its Shader Graph editor creates node-based materials for RealityKit content.
- Reality Composer Pro exposes both `PhysicallyBasedMaterial` and
  `ShaderGraphMaterial`. Use Shader Graph when the material needs logic,
  stylized behavior, vertex displacement, or effects that would otherwise
  require shader code.
- Treat exported USD and MaterialX as runtime artifacts or debugging surfaces.
  Edit raw exported graph structure only for explicit export repair or
  interoperability work.

## Official Loading Boundaries

- When the app needs an entire authored entity that already contains materials,
  use
  [`entity-loading-and-stored-entities.md`](../../realitykit-visionos-developer/references/entity-loading-and-stored-entities.md)
  instead of repeating stored-entity loading guidance here.
- When the app needs a standalone shader graph material, use
  `ShaderGraphMaterial.init(named:from:in:)` for a bundle resource or
  `ShaderGraphMaterial.init(named:from:)` for a file URL.
- Apple's `ShaderGraphMaterial` docs list USD (`.usd`, `.usda`, `.usdc`,
  `.usdz`) and Reality (`.reality`) as supported formats for named material
  loading.
- For USD files, the `name` passed to `ShaderGraphMaterial` is the full material
  prim path, such as `/Root/MyMaterial`.

```swift
let material = try await ShaderGraphMaterial(
    named: "/Root/MyMaterial",
    from: "Materials.usda",
    in: materialBundle
)
```

## Runtime Parameter Boundaries

- Promote Shader Graph inputs in Reality Composer Pro before expecting Swift to
  control them.
- Check `ShaderGraphMaterial.parameterNames` before calling
  `setParameter(name:value:)`; promoted input names are exact and case
  sensitive.
- Use `MaterialParameters.Value` cases that match the promoted input type,
  including `.bool`, `.float`, `.int`, `.simd2Float`, `.simd3Float`,
  `.simd4Float`, `.float2x2`, `.float3x3`, `.float4x4`, `.color`,
  `.texture`, and `.textureResource`.
- Use `TextureResource` for texture resources in shader graph parameters.
- `ModelComponent.materials` stores material values. Mutate a material copy,
  replace it in the array, and set the updated `ModelComponent` back on the
  entity.

## Named Material and Resource Pitfalls

- Match the material prim path, USD or `.reality` filename, bundle, and case
  exactly.
- Confirm the resource is in the built bundle or generated Reality Composer Pro
  package, not only present in the source tree.
- Do not replace a missing named material with a hand-built Swift material until
  the authored material path, bundle resource, and promoted parameter names have
  been checked.
- Route prim paths, composition arcs, or source-layer edits to `usd-editor`.
