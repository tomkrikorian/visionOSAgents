# usdextract

Use this when extracting files from USD-compatible packages.

## What It Does

`usdextract` extracts file(s) from `.usdz`, `.glb`, or `.gltf` inputs.

## Basic Usage

```bash
usdextract [OPTIONS] inputFile
```

## Common Options

- `-o`, `--out DIR`: Output directory for extracted files.

## Examples

Extract a USDZ package to a folder:

```bash
usdextract -o Extracted Model.usdz
```

Extract a GLB into a directory:

```bash
usdextract -o Extracted Model.glb
```
