---
name: usd-editor
description: Guide for modifying USD ASCII (.usda) files and command-line USD workflows, including prims, properties, composition arcs, variants, transforms, usdcat, usdchecker, usdrecord, usdtree, usdzip, and usdedit. Use when editing or reviewing .usda files by hand, validating USD/USDZ assets, or working in an asset pipeline outside runtime Swift USDKit.
---

# USD Editor

## Quick Start

Use this skill for minimal, text-level USD or USDA edits and command-line USD
inspection, conversion, packaging, rendering, and validation. Keep the change
small and preserve existing composition unless the task explicitly says
otherwise.

When authored Reality Composer Pro or USD content owns the scene, geometry,
transform, animation, or material, keep that authored surface as the source of
truth. Use Swift and RealityKit to load or adjust runtime state; do not recreate
authored USD content in Swift unless the request is explicitly procedural.

If Swift code needs to open, edit, observe, or export stages in-process with
`USDStage`, `USDPrim`, or `USDLayer`, switch to `$usdkit-runtime-developer`.

If the change is material- or shader-specific for RealityKit, prefer
`shadergraph-editor`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`usd-syntax`](references/usd-syntax.md) | When you need a refresher on .usda syntax, values, and path formats. |
| [`prims-properties`](references/prims-properties.md) | When adding or editing prims, attributes, or relationships. |
| [`composition-variants`](references/composition-variants.md) | When touching sublayers, references, payloads, or variant sets. |
| [`transforms-units`](references/transforms-units.md) | When editing transforms, xformOps, or stage units and up-axis metadata. |
| [`time-samples`](references/time-samples.md) | When modifying animated or time-sampled properties. |
| [`command-line-tools`](references/command-line-tools.md) | When you need a quick reference for common USD command-line tools. |
| [`usdcat`](references/usdcat.md) | When converting, flattening, or inspecting USD files. |
| [`usdchecker`](references/usdchecker.md) | When validating USD or USDZ assets, including RealityKit-focused checks. |
| [`usdrecord`](references/usdrecord.md) | When rendering images from USD files. |
| [`usdtree`](references/usdtree.md) | When inspecting the prim hierarchy of a USD file. |
| [`usdzip`](references/usdzip.md) | When creating or inspecting USDZ packages. |
| [`usdedit`](references/usdedit.md) | When you need the official text-editing workflow for a USD-readable file. |
| [`visionos-runtime-loading.md`](references/visionos-runtime-loading.md) | When the question is how authored USD or USDZ actually loads and behaves in a visionOS app. |
| [`apple-runtime-boundaries.md`](references/apple-runtime-boundaries.md) | When deciding whether to edit authored USD / Reality Composer Pro content, load it through RealityKit, or validate it for Apple platforms. |

## Workflow

1. Identify the owner: authored USD / Reality Composer Pro asset, package
   resource, or runtime-only Swift-generated content.
2. Inspect the stage with `usdtree`, `usdcat --loadOnly`, or `usdcat --flatten`
   before editing, depending on the risk.
3. Locate the exact prim path and layer that owns the opinion.
4. Choose `over`, `def`, or a list edit deliberately.
5. Apply the minimum change needed.
6. Re-check paths, transforms, or composition edges that were touched.
7. Run the narrowest validation tool that matches the change, then run
   `usdchecker --arkit` for shipping visionOS USDZ assets.

## Guardrails

- Do not replace a prim with `def` when `over` is the correct edit.
- Avoid composition-arc changes unless they are explicitly requested.
- If a RealityKit app loads the asset with `Entity(named:in:)`,
  `Entity(contentsOf:withName:)`, or a generated Reality Composer Pro content
  bundle, prefer fixing the authored asset and validating the bundle/package
  over building a parallel Swift scene graph.
- Do not hand-edit a `.usdz` package in place; inspect or unpack it, edit the
  source layer, rebuild the package, and validate the result.
- Validate final Apple-platform USDZ output with `usdchecker --arkit --strict`,
  not just a source-layer parse check.
- Preserve existing formatting and comments when possible.

## Output Expectations

Provide:
- the prim or path edited
- which reference files were used
- the exact class of USD change made
- the validation step used
- routing to `$usdkit-runtime-developer`, `shadergraph-editor`, or runtime
  testing if needed
