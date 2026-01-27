# usdtree

Use this when you need a hierarchical view of a USD file.

## What It Does

`usdtree` prints the prim hierarchy of a USD file. It can optionally flatten the stage and include attributes or metadata.

## Basic Usage

```bash
usdtree [OPTIONS] inputPath
```

## Common Options

- `-f`, `--flatten`: Compose the stage and show the flattened tree.
- `--flattenLayerStack`: Flatten only the layer stack (no composition arcs).
- `--unloaded`: Do not load payloads.
- `-a`, `--attributes`: Display authored attributes.
- `-m`, `--metadata`: Display authored metadata.
- `-s`, `--simple`: Only show prim names (no specifier/kind/active).
- `--mask PRIMPATH[,PRIMPATH...]`: Limit population to selected prims (requires `--flatten`).

## Examples

Show a simple tree:

```bash
usdtree Scene.usda
```

Show a flattened tree with attributes:

```bash
usdtree --flatten --attributes Scene.usda
```
