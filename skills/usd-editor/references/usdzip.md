# usdzip

Use this when creating or inspecting USDZ packages.

## What It Does

`usdzip` creates `.usdz` packages and can list or dump contents of existing packages.

## Basic Usage

```bash
usdzip [OPTIONS] [usdzFile] [inputFiles...]
```

## Common Options

- `-r`, `--recurse`: Recursively include subdirectories.
- `-a`, `--asset PATH`: Package an asset root layer and its dependencies.
- `--arkitAsset PATH`: Package and transform for RealityKit requirements.
- `-c`, `--checkCompliance`: Validate inputs before packaging.
- `-l`, `--list [FILE|-]`: List contents to a file or stdout.
- `-d`, `--dump [FILE|-]`: Dump contents to a file or stdout.
- `-v`, `--verbose`: Verbose output while adding files.

## Examples

Create a package from a root layer and textures:

```bash
usdzip Model.usdz Model.usda textures/*
```

Package a root layer and dependencies:

```bash
usdzip -a Model.usda Model.usdz
```

Package for RealityKit constraints:

```bash
usdzip --arkitAsset Model.usda Model.usdz
```

Check compliance while packaging explicit inputs:

```bash
usdzip -c Model.usdz Model.usda textures/*
```

List package contents:

```bash
usdzip -l Model.usdz
```

Dump package contents for inspection:

```bash
usdzip -d - Model.usdz
```

## visionOS Notes

- Prefer `--arkitAsset` when building a standalone USDZ for RealityKit; it
  gathers dependencies and may transform data to satisfy RealityKit packaging
  requirements.
- Run `usdchecker --arkit --strict Model.usdz` after packaging even when
  `usdzip -c` succeeds.
- Keep the root layer and asset paths deterministic. Runtime bundle loading is
  sensitive to package names and case.
