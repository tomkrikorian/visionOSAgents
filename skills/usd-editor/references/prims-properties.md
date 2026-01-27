# Prims and Properties

Use this when adding or modifying prims, attributes, and relationships.

## Specifiers

- **def**: Create a new prim definition.
- **over**: Modify an existing prim without redefining it.
- **class**: Define a reusable prim template (rare in app assets).

```usda
over "Mesh"
{
    token visibility = "invisible"
}
```

## Attributes

Attributes store typed data. Preserve the existing type when editing.

```usda
float roughness = 0.3
point3f[] points = [(0, 0, 0), (1, 0, 0)]
custom string notes = "Author note"
```

## Relationships

Relationships point to other prims or properties.

```usda
rel material:binding = </Materials/Mat>
rel collection:colliders = </Root/ColliderGroup>
```

## Connections

Connections link one attribute to another attribute's output.

```usda
color3f inputs:diffuseColor.connect = </Textures/Diffuse.outputs:rgb>
```

## Variability and Custom Properties

- Use `uniform` for properties that do not vary over time.
- Use `custom` for non-schema properties.

```usda
uniform token purpose = "render"
custom float myCustomValue = 1.0
```
