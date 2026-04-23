# Samples

Use this file when a repo sample is the fastest way to align on the desired
effect.

- [`samples/ShaderSamplesScene.usda`](../samples/ShaderSamplesScene.usda):
  single scene that references the other samples
- [`samples/OutlineShader.usda`](../samples/OutlineShader.usda): outline via
  geometry expansion
- [`samples/FresnelShader.usda`](../samples/FresnelShader.usda): rim or
  Fresnel glow
- [`samples/GradientShader.usda`](../samples/GradientShader.usda): distance
  gradient
- [`samples/LavaShader.usda`](../samples/LavaShader.usda): animated emissive
  lava
- [`samples/DissolveShader.usda`](../samples/DissolveShader.usda): dissolve
  threshold effect
- [`samples/VertexDisplacementShader.usda`](../samples/VertexDisplacementShader.usda):
  vertex displacement
- [`samples/NormalCorrectionShader.usda`](../samples/NormalCorrectionShader.usda):
  displaced geometry with corrected normals
- [`samples/ToonShader.usda`](../samples/ToonShader.usda): toon shading
- [`samples/PBRToonShader.usda`](../samples/PBRToonShader.usda): PBR-to-toon
  banding workflow

Some samples reference external assets. Keep or update those asset paths when
copying them into a project.

## Selection Notes

- Use `GradientShader.usda`, `DissolveShader.usda`, and `ToonShader.usda` when
  you need examples with promoted inputs wired into graph nodes.
- Use `VertexDisplacementShader.usda` or `NormalCorrectionShader.usda` when the
  effect changes geometry rather than only surface color.
- After copying a sample, inspect the material prim path and top-level
  `inputs:<Name>` parameters before writing Swift runtime code.
- Validate copied or packaged samples through `usd-editor` with
  `usdchecker --arkit` when they are destined for a visionOS app bundle.
