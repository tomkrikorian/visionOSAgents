# usdcrush

Use this when reducing the size of USD assets by compressing content.

## What It Does

`usdcrush` writes a compressed version of a USD file.

## Basic Usage

```bash
usdcrush [OPTIONS] inputFile
```

## Common Options

- `-o`, `--out FILE`: Output file path (required).
- `-c`, `--compatibility widest|latest`: Controls compression vs compatibility.
- `-t`, `--textureQuality 0-100`: Texture quality hint.

## Examples

Compress a USDZ file:

```bash
usdcrush -o Model_Compressed.usdz Model.usdz
```

Use widest compatibility with lower texture quality:

```bash
usdcrush -o Model_Compressed.usdz -c widest -t 70 Model.usdz
```
