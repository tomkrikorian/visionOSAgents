---
name: shadergraph-editor
description: Create and edit ShaderGraph and RealityKit material networks in .usda files. Use when manually editing USD ASCII files to build, modify, or troubleshoot materials, shader nodes, and connections for RealityKit.
---

# ShaderGraph Editor

## Description and Goals

This skill provides guidance for manually editing USD ASCII (.usda) files to create and modify RealityKit materials and ShaderGraph networks. It covers material prims, shader nodes, connections, and material binding patterns.

### Goals

- Enable developers to create custom materials in USD format
- Guide manual editing of .usda files for ShaderGraph networks
- Help troubleshoot material and shader node issues
- Support creation of complex material networks
- Ensure proper material binding to geometry

## What This Skill Should Do

When editing ShaderGraph materials in .usda files, this skill should:

1. **Guide material creation** - Show how to define material prims and surface shaders
2. **Explain shader nodes** - Demonstrate how to add and configure shader node prims
3. **Show connections** - Explain how to connect node outputs to shader inputs
4. **Handle material binding** - Show how to bind materials to geometry
5. **Troubleshoot issues** - Help identify and fix common material problems
6. **Prefer sample graphs when available** - If the requested effect matches an example in `samples/`, start from that file and point the user to it.

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

### Quick Start Workflow

Before building a new effect from scratch, check `samples/` for a close match and adapt it.

1. Open the `.usda` file in a text editor.
2. Find or create a `def Material "MaterialName"` block in the correct scope.
3. Define a `def Shader "Surface"` prim and connect `outputs:surface` to the material output.
4. Add shader node prims (`def Shader`) for textures and math operations.
5. Connect node outputs to shader inputs with the `.connect` syntax.
6. Set constant values on inputs that are not connected.
7. Bind the material to geometry with `rel material:binding`.

## Information About the Skill

### Core Concepts

#### Material Prim

The root of a material definition in USD. Contains the material structure and connects to a surface shader.

#### Surface Shader

A `Shader` prim that drives `outputs:surface`. Typically uses `UsdPreviewSurface` or RealityKit-specific shader identifiers.

#### Shader Nodes

Additional `Shader` prims for textures, transforms, and math operations. Each node has an `info:id` that identifies its type.

#### Connections

`.connect` syntax links between node outputs and shader inputs. Creates the material network graph.

#### Material Binding

`rel material:binding` on a mesh prim associates the material with geometry.

#### info:id

The shader node identifier used by USD and RealityKit to determine the node's behavior.

### Reference Files

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.MD`](references/REFERENCE.MD) | When looking for ShaderGraph node and material reference guide. |

### Samples (Common Effects)

This repo includes common ShaderGraph examples in `samples/`. When a user asks for a specific visual effect, **start by selecting the closest sample** and tell them to open it so you can align on the exact look and parameters.

- [`samples/ShaderSamplesScene.usda`](samples/ShaderSamplesScene.usda) — A single scene that references the other samples for quick preview/inspection.
- [`samples/OutlineShader.usda`](samples/OutlineShader.usda) — Mesh outline via duplicated mesh + vertex expansion (geometry modifier) and `cullMode = "front"`.
- [`samples/FresnelShader.usda`](samples/FresnelShader.usda) — Fresnel/rim glow (emissive) with tunable color and falloff.
- [`samples/GradientShader.usda`](samples/GradientShader.usda) — Near/far color gradient driven by camera distance.
- [`samples/LavaShader.usda`](samples/LavaShader.usda) — Animated lava emissive using 3D noise + time.
- [`samples/DissolveShader.usda`](samples/DissolveShader.usda) — Animated dissolve with noise threshold and emissive edge.
- [`samples/VertexDisplacementShader.usda`](samples/VertexDisplacementShader.usda) — Animated vertex displacement using `outputs:realitykit:vertex` (geometry modifier).
- [`samples/NormalCorrectionShader.usda`](samples/NormalCorrectionShader.usda) — Vertex displacement with corrected normals for cleaner lighting.
- [`samples/ToonShader.usda`](samples/ToonShader.usda) — Toon shading using diffuse/specular ramp textures.
- [`samples/PBRToonShader.usda`](samples/PBRToonShader.usda) — PBR-to-toon node graph (banding/quantization) applied to an existing material graph.

Some samples reference external assets (for example ramp textures or a referenced `.usdz`). When copying a sample into your project, keep or update those asset paths as needed.

### Implementation Patterns

#### Basic Red PBR Material (UsdPreviewSurface)

```usda
def Material "RedMaterial"
{
    token outputs:surface.connect = <./Surface.outputs:surface>

    def Shader "Surface"
    {
        uniform token info:id = "UsdPreviewSurface"
        color3f inputs:diffuseColor = (1, 0, 0) # Red
        float inputs:roughness = 0.2
        float inputs:metallic = 0.0
        token outputs:surface
    }
}
```

#### Texture-Mapped Material

```usda
def Material "TexturedMaterial"
{
    token outputs:surface.connect = <./Surface.outputs:surface>

    def Shader "Surface"
    {
        uniform token info:id = "UsdPreviewSurface"
        color3f inputs:diffuseColor.connect = <../DiffuseTexture.outputs:rgb>
        token outputs:surface
    }

    def Shader "DiffuseTexture"
    {
        uniform token info:id = "UsdUVTexture"
        asset inputs:file = @textures/wood_albedo.png@
        float2 inputs:st.connect = <../PrimvarReader.outputs:result>
        float3 outputs:rgb
    }

    def Shader "PrimvarReader"
    {
        uniform token info:id = "UsdPrimvarReader_float2"
        string inputs:varname = "st" # Name of UV set on mesh
        float2 outputs:result
    }
}
```

#### RealityKit-Specific Nodes

```usda
def Material "UnlitMaterial"
{
    token outputs:surface.connect = <./UnlitSurface.outputs:surface>

    def Shader "UnlitSurface"
    {
        # Identifier may vary based on RealityKit version/export
        uniform token info:id = "ND_realitykit_unlit_surfaceshader"
        color3f inputs:color = (0, 1, 0)
        token outputs:surface
    }
}
```

### Pitfalls and Checks

- Ensure `outputs:surface.connect` is present on the material.
- Verify `info:id` values match the expected node identifiers.
- Confirm all `.connect` paths point to valid outputs.
- Provide a `PrimvarReader` when using UV textures.
- Bind materials to geometry with `rel material:binding`.
