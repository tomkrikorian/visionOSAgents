# Composition Arcs and Variants

Use this when modifying sublayers, references, payloads, or variant sets.

## Sublayers (Layer Metadata)

Sublayers live in the root layer metadata, typically at the top of the file.

```usda
(
    subLayers = [
        @base.usda@
    ]
)
```

## References and Payloads (Prim Metadata)

References and payloads are usually authored as prim metadata.

```usda
def Xform "Model" (
    references = @model.usd@
)
{
}
```

Use list editing ops to avoid overwriting existing values:

```usda
prepend references = @extra.usd@
append payload = @lod.usd@
```

## Variants

Variant sets create alternate branches of content. Follow the existing pattern in the file.

```usda
def Xform "Model" (
    variantSets = "lod"
    variants = { string lod = "high" }
)
{
    variantSet "lod" = {
        "high" { }
        "low" { }
    }
}
```

## Guidance

- Avoid changing composition arcs unless explicitly requested.
- Prefer list editing when adding to existing lists.
- Preserve existing variant selections and naming conventions.
