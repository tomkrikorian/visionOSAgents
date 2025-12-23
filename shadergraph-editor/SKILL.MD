---
name: shadergraph-editor
description: Create and edit shadeers and materials in .usda files 
license: MIT
metadata:
  author: Tom Krikorian
  version: "1.0"
---

# ShaderGraph Editing Guide for .usda Files

This guide explains how to manually edit `.usda` (USD ASCII) files to create and modify RealityKit materials and ShaderGraph networks.

## Step-by-step instructions

1.  **Open the `.usda` file** in a text editor (e.g., VS Code, Sublime Text).
2.  **Locate or Create a Material Prim**:
    *   Find a `def Material "MaterialName"` block.
    *   If creating new, ensure it is within the correct scope (usually under a model or root).
3.  **Define the Surface Shader**:
    *   Inside the Material, define a `def Shader "Surface"` prim.
    *   Set the `info:id` to the desired shader type (e.g., `UsdPreviewSurface` for standard PBR, or specific RealityKit identifiers if known).
    *   Connect the shader's output to the material's surface output: `token outputs:surface.connect = <./Surface.outputs:surface>`.
4.  **Add Shader Nodes**:
    *   Create additional `def Shader` prims for each node in your graph (e.g., textures, math operations).
    *   Give each node a unique name (e.g., `def Shader "DiffuseTexture"`).
    *   Set the `info:id` corresponding to the node function (e.g., `UsdUVTexture`, `UsdTransform2d`).
5.  **Connect Inputs and Outputs**:
    *   Use the `.connect` syntax to link node outputs to inputs.
    *   Example: `color3f inputs:diffuseColor.connect = <../DiffuseTexture.outputs:rgb>`.
6.  **Set Constant Values**:
    *   For inputs not connected to other nodes, set their values directly (e.g., `float inputs:roughness = 0.5`).
7.  **Bind Material to Geometry**:
    *   On your mesh prim (e.g., `def Mesh "Sphere"`), add the relationship: `rel material:binding = </Path/To/Material>`.

## Examples of inputs and outputs

### Example 1: Basic Red PBR Material (UsdPreviewSurface)

**Input (Concept):** A material that is red and slightly shiny.

**Output (.usda):**
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

### Example 2: Texture Mapped Material

**Input (Concept):** A material using a texture file for color.

**Output (.usda):**
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

### Example 3: RealityKit Specific Nodes (Conceptual)
*Note: RealityKit-specific nodes often use internal identifiers. It is recommended to prototype in Reality Composer Pro and export to USD to find exact `info:id` strings for nodes like "Unlit Surface (RealityKit)".*

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

## Documentation

To see all available nodes available in shadergraph, check the [the reference guide](references/REFERENCE.md) for details.

