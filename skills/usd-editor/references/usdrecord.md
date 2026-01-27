# usdrecord

Use this when rendering images from a USD file.

## What It Does

`usdrecord` renders images from a USD stage to a single image or a frame sequence.

## Basic Usage

```bash
usdrecord [OPTIONS] usdFilePath outputImagePath
```

`outputImagePath` must contain exactly one frame placeholder like `###` or `###.###` when rendering a range.

## Common Options

- `--camera`, `--cam`: Camera prim path or name to render from.
- `-f`, `--frames`: Frame spec or range (e.g. `101:110x2`).
- `-w`, `--imageWidth`: Output image width; height follows camera aspect.
- `-r`, `--renderer`: Hydra renderer plugin (e.g. `Metal`).
- `--mask PRIMPATH[,PRIMPATH...]`: Limit stage population to selected prims.
- `--purposes PURPOSE[,PURPOSE...]`: Include additional purposes beyond `default`.
- `--disableGpu`: Force CPU rendering and avoid GPU-only tasks.
- `--disableCameraLight`: Disable default camera lights.
- `--renderSettingsPrimPath`: Use a RenderSettings prim (overrides some args).
- `--renderPassPrimPath`: Use a RenderPass prim (overrides some args).

## Examples

Render a single frame:

```bash
usdrecord Scene.usda output.png
```

Render a frame range:

```bash
usdrecord Scene.usda frames.###.png --frames 1:60
```

Render from a specific camera:

```bash
usdrecord Scene.usda output.png --camera /Root/Camera --imageWidth 1920
```
