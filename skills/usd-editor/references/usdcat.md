# usdcat

Use this when converting, flattening, or inspecting USD files.

## What It Does

`usdcat` writes USD files as text to stdout or to a specified output file. It can also flatten stages and perform quick load checks.

## Basic Usage

```bash
usdcat [OPTIONS] inputFiles...
```

## Common Options

- `-o`, `--out FILE`: Write output to a file instead of stdout.
- `--usdFormat usda|usdc`: Choose the underlying format for `.usd` output.
- `-l`, `--loadOnly`: Load and report `OK` or `ERR` for each input.
- `-f`, `--flatten`: Flatten the composed stage.
- `--flattenLayerStack`: Flatten only the layer stack (no composition arcs).
- `--mask PRIMPATH[,PRIMPATH...]`: Limit population to selected prims (requires `--flatten`).
- `--layerMetadata`: Load only layer metadata (cannot be combined with flatten options).
- `--skipSourceFileComment`: Skip source comments when flattening.

## Examples

Write a stage to stdout:

```bash
usdcat Scene.usda
```

Convert to binary `.usdc`:

```bash
usdcat -o Scene.usdc Scene.usda
```

Flatten a stage:

```bash
usdcat --flatten -o SceneFlat.usda Scene.usda
```
