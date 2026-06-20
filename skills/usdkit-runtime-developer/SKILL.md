---
name: usdkit-runtime-developer
description: Build USDKit runtime editing flows on visionOS 27, macOS 27, or iOS 27. Use when Swift code imports USDKit, opens or creates USDStage and USDLayer values, edits USDPrim attributes, observes USDStage.ObjectsDidChange, exports runtime USD packages, or bridges live stages through RealityKit USDStageComponent.
---

# USDKit Runtime Developer

## Quick Start

Use this skill for in-process USD stage work from Swift. For hand-authored
`.usda` edits, package inspection, CLI conversion, or `usdchecker` validation,
switch to `$usd-editor`.

1. Confirm the target uses the 27 SDKs and can `import USDKit`.
2. Decide whether the task belongs to runtime USDKit or the `usd*` command-line
   asset pipeline.
3. Load the USDKit decision reference, then the USDKit framework reference.
4. Keep `USDStage`, `USDPrim`, `USDLayer`, and nested property work on one
   actor; these types are not Sendable.
5. For live RealityKit display, use `USDStageComponent` from the RealityKit
   skill; for Spatial Preview streaming, keep `$spatial-preview-developer`.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`usdkit-vs-cli.md`](references/usdkit-vs-cli.md) | When choosing between runtime USDKit and the command-line USD pipeline. |
| [`usdkit-framework.md`](references/usdkit-framework.md) | When using `USDStage`, `USDPrim`, `USDLayer`, observers, export, or package APIs. |
| [`visionos-runtime-loading.md`](../usd-editor/references/visionos-runtime-loading.md) | When checking how authored USD or USDZ content loads inside a visionOS app. |
| [`apple-runtime-boundaries.md`](../usd-editor/references/apple-runtime-boundaries.md) | When deciding whether to edit authored USD, load through RealityKit, or validate for Apple platforms. |

## Workflow

1. Identify the owner: runtime Swift-edited stage, authored asset, or package
   pipeline.
2. Use USDKit for in-process stage editing, observation, live rendering, or
   runtime package export.
3. Keep CLI validation in the asset pipeline; USDKit does not replace
   `usdchecker --arkit --strict`.
4. Preserve authored assets as source of truth unless the task is explicitly
   procedural or runtime-generated.

## Guardrails

- Do not use USDKit just to inspect or batch-convert files in CI; use the CLI
  tools through `$usd-editor`.
- Do not assume beta USDKit symbols are stable; re-check the installed 27 SDK
  before shipping.
- Do not recreate authored Reality Composer Pro content in Swift unless the
  feature explicitly requires procedural authoring.

## Output Expectations

Provide:
- why USDKit is the right runtime path
- which USDKit references were used
- the `USDStage` / `USDLayer` / `USDPrim` ownership model
- observer, actor, export, and validation considerations
