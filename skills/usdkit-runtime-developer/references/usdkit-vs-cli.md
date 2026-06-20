# USDKit vs Command-Line Tools

Use this when choosing between the `usd*` CLI flow and the USDKit framework
for a USD task. USDKit is new in visionOS 27 / macOS 27 / iOS 27. The split
is batch/CI/asset-pipeline work (CLI) vs in-process, runtime stage work
(USDKit).

## Decision Table

| Situation | Use |
|-----------|-----|
| Batch conversion, CI checks, asset pipelines | `usdcat`, `usdchecker`, `usdzip` |
| One-off inspection of files on disk | `usdtree`, `usdcat --flatten` |
| Editing stage content at app runtime | USDKit |
| Live rendering of an editable stage in RealityKit | USDKit + `USDStageComponent` |
| Reacting to stage changes in-process | USDKit `addObserver(for:using:)` |
| Validating shipping USDZ output | `usdchecker --arkit --strict` |

## Keep the CLI When

- The asset is authored content fixed at build time; edit the source layer
  and validate with `usdchecker` through `$usd-editor`.
- The work runs in CI or a content pipeline on machines without the 27 SDKs.
- You only need to look: `usdtree` and `usdcat` are faster than writing a
  Swift inspection harness.

## Use USDKit When

- The app must open, edit, and save USD stages while running: `definePrim`,
  `overridePrim`, typed attribute writes, layer field and time-sample edits.
- The app needs to react to edits via `USDStage.ObjectsDidChange` instead of
  re-parsing files.
- The app renders a stage live and keeps editing it; pair the stage with the
  RealityKit bridge (below) instead of exporting and reloading USDZ.
- The app generates a package at runtime: `exportPackage(to:options:)` is the
  in-process counterpart of `usdzip`. Still run `usdchecker --arkit --strict`
  on anything that ships.

There is no in-process replacement for `usdchecker`; validation stays on the
CLI.

## RealityKit Bridge

`import USDKit` plus `import RealityKit` auto-loads a bridge overlay whose
`USDStageComponent` renders a live `USDStage` on an `Entity`, re-rendering as
the stage changes. That bridge belongs to the realitykit skill; see
[`usdstagecomponent`](../../realitykit-visionos-developer/references/usdstagecomponent.md).

USDKit is beta API: names and shapes may change before release. When in
doubt, default to the CLI flow and authored-asset edits.
