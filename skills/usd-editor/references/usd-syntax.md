# USD Syntax Essentials

Use this as a quick reminder of USD ASCII (.usda) syntax when making edits.

## Core Structure

- Blocks use `def`, `over`, or `class` with a prim type and name.
- Metadata can appear in parentheses right after the prim declaration.
- Indentation is for readability; keep the existing style.

```usda
def Xform "Root" (
    kind = "component"
)
{
    # child prims and properties
}
```

## Properties

- **Attributes** use `type name = value`.
- **Relationships** use `rel name = </Path>`.
- **Connections** use `type name.connect = </Path.outputs:foo>`.

```usda
float3 displayColor = (1, 0, 0)
rel material:binding = </Materials/Mat>
color3f inputs:diffuseColor.connect = </Textures/Diffuse.outputs:rgb>
```

## Values and Paths

- **SdfPath**: `</Root/Child>` or `</Root/Mat.outputs:surface>`
- **Asset path**: `@textures/albedo.png@`
- **Arrays**: `int[] myInts = [1, 2, 3]`
- **Tokens** are unquoted identifiers; **strings** are quoted.

## List Editing

Use list ops to modify lists without replacing them:

```usda
prepend references = @model.usd@
append payload = @payload.usd@
```
