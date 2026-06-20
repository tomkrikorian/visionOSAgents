---
name: swiftui-chart3d-developer
description: Build SwiftUI Chart3D and Swift Charts 3D visualizations for visionOS 27 and Apple platforms. Use when implementing Chart3D, SurfacePlot, 3D PointMark, RuleMark, RectangleMark, Chart3DPose, 3D chart scales, axis labels, camera projection, or spatial data-visualization interactions.
---

# SwiftUI Chart3D Developer

## Quick Start

Use this skill for Swift Charts 3D visualization work. For windows,
`RealityView`, `Model3D`, attachments, gestures outside charts, or immersive
scene lifecycle, switch to `$spatial-swiftui-developer`.

1. Confirm the third dimension adds meaningful information; prefer 2D charts
   when depth does not improve interpretation.
2. Choose the chart form: 3D marks for sampled data or `SurfacePlot` for
   `y = f(x, z)` surfaces.
3. Bind `Chart3DPose` when the chart needs a stable initial view or interactive
   rotation state.
4. Set explicit x/y/z domains and labels so the plot volume remains readable.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`charts-3d.md`](references/charts-3d.md) | When implementing `Chart3D`, `SurfacePlot`, 3D marks, scales, axes, pose, or camera projection. |

## Workflow

1. Define x, y, and z semantics before writing marks.
2. Choose marks, surface style, chart scales, and axis labels.
3. Add pose and projection only when they improve interpretation.
4. Keep chart state in SwiftUI and avoid mixing Chart3D with RealityKit scene
   ownership unless the surrounding view requires it.

## Guardrails

- Do not use `Chart3D` for novelty; a 2D chart is often clearer.
- Do not leave unlabeled axes or implicit domains for production charts.
- Do not route general spatial UI layout questions here; use
  `$spatial-swiftui-developer`.

## Output Expectations

Provide:
- why `Chart3D` is warranted
- which chart reference was used
- the marks, surface, scales, labels, and pose chosen
- the fallback to 2D or spatial SwiftUI routing if applicable
