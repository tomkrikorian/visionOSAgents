---
name: shadergraph-editor
description: Author, load, and troubleshoot Reality Composer Pro Shader Graph materials for RealityKit on visionOS. Use when building Shader Graph materials, exposing promoted inputs for runtime control, debugging exported USD and MaterialX interop, or building shader graphs programmatically in Swift on visionOS 27.
---

# ShaderGraph Editor

## Quick Start

Default to Reality Composer Pro. Use raw USD or MaterialX inspection only when
debugging exports or interoperability.

1. Decide whether the task is node selection, runtime parameter control,
   export debugging, or sample selection.
2. Identify whether the material is authored in Reality Composer Pro, loaded
   from USD / `.reality`, intentionally created from MaterialX data, or built
   programmatically with the visionOS 27 `ShaderGraph` API.
3. Load only the matching reference files.
4. Route text-level USD structure edits to `usd-editor`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`references/shadergraph-node-reference.md`](references/shadergraph-node-reference.md) | When choosing RealityKit Shader Graph nodes by category. |
| [`references/runtime-api.md`](references/runtime-api.md) | When loading `ShaderGraphMaterial`, working with promoted inputs, or updating parameters at runtime. |
| [`references/programmatic-shader-graphs.md`](references/programmatic-shader-graphs.md) | When building shader graphs in Swift with the `ShaderGraph` API (new in visionOS 27), `ShaderGraphMaterial.Program`, `PortalMaterial.Program`, `LightingModel`, or PBR subsurface scattering. |
| [`references/export-debug.md`](references/export-debug.md) | When inspecting exported USD or MaterialX, or when a graph fails to load or render as expected. |
| [`references/samples.md`](references/samples.md) | When selecting the closest repo sample before authoring a new effect from scratch. |
| [`references/apple-material-boundaries.md`](references/apple-material-boundaries.md) | When deciding whether to author in Reality Composer Pro, load a `ShaderGraphMaterial`, or debug named material/resource failures. |

## Workflow

1. Start from the closest existing sample when possible.
2. Author or refine the graph in Reality Composer Pro.
3. Promote the inputs that need runtime control.
4. Load entire authored entities with RealityKit entity-loading APIs, or load a
   standalone material with `ShaderGraphMaterial` only when the app needs the
   material itself.
5. Match material prim paths, file names, bundle names, and promoted parameter
   names exactly.
6. Load and update the material through the runtime API.
7. Inspect exports only when the normal authoring path stops explaining the
   failure.

## When To Switch Skills

- Switch to `usd-editor` when the task is really about prim paths,
  composition, or text-level USD authoring.
- Switch to `realitykit-visionos-developer` when the blocker is entity setup,
  material application, or scene integration rather than graph authoring.

## Guardrails

- Treat Reality Composer Pro as the default authoring surface.
- Keep Shader Graph material structure in Reality Composer Pro unless the task
  is explicitly USD / MaterialX export repair.
- Use official RealityKit material APIs such as `ShaderGraphMaterial`,
  `MaterialParameters.Value`, and `TextureResource`; do not introduce
  undocumented material-resource types.
- For USD-backed materials, `ShaderGraphMaterial` names are full material prim
  paths such as `/Root/MyMaterial`, not informal display labels.
- Do not treat exported `info:id` strings or raw graph layout as stable public
  API unless Apple documents them directly.

## Output Expectations

Provide:
- the selected effect or sample starting point
- which references were used
- how the material is authored or loaded
- whether the issue is a graph problem, runtime problem, or export problem
- explicit routing to `usd-editor` or RealityKit work if needed
