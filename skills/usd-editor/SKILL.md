---
name: usd-editor
description: Guide for modifying USD ASCII (.usda) files, including prims, properties, composition arcs, variants, and transforms. Use when editing or reviewing .usda files by hand.
---

# USD Editor

## Quick Start

Use this skill for minimal, text-level USD or USDA edits. Keep the change small
and preserve existing composition unless the task explicitly says otherwise.

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
| [`visionos-runtime-loading.md`](references/visionos-runtime-loading.md) | When the question is how the authored USD or USDZ actually loads and behaves in a visionOS app. |

## Workflow

1. Inspect the stage with `usdtree`, `usdcat --loadOnly`, or `usdcat --flatten`
   before editing, depending on the risk.
2. Locate the exact prim path and layer that owns the opinion.
3. Choose `over`, `def`, or a list edit deliberately.
4. Apply the minimum change needed.
5. Re-check paths, transforms, or composition edges that were touched.
6. Run the narrowest validation tool that matches the change, then run
   `usdchecker --arkit` for shipping visionOS USDZ assets.

## Guardrails

- Do not replace a prim with `def` when `over` is the correct edit.
- Avoid composition-arc changes unless they are explicitly requested.
- Do not hand-edit a `.usdz` package in place; inspect or unpack it, edit the
  source layer, rebuild the package, and validate the result.
- Preserve existing formatting and comments when possible.

## Output Expectations

Provide:
- the prim or path edited
- which reference files were used
- the exact class of USD change made
- the validation step used
- routing to `shadergraph-editor` or runtime testing if needed
