# Entity Loading and Stored Entities

Use this file when loading Reality Composer Pro, USD, USDZ, `.reality`, or
package-bundled RealityKit content into a visionOS app.

## API Choice

- Use `Entity.load(named:in:)` or `Entity(named:in:)` when loading a named
  stored entity from a bundle.
- Use `Entity.init(contentsOf:withName:)` when you have an explicit file URL
  and need direct control over the loaded asset name.
- Use `Model3D` for simple SwiftUI asset presentation.
- Use `RealityView` when the loaded content needs RealityKit components,
  systems, attachments, event subscriptions, or scene-graph mutation.

## Ownership Rules

- Load assets asynchronously.
- Keep entity creation in `RealityView` make closures or a dedicated model /
  RealityKit owner.
- Keep update-time mutation in `RealityView` update closures, event handlers, or
  RealityKit systems.
- Do not load heavy assets repeatedly from SwiftUI body recomputation.
- Inspect the built bundle when a named entity does not resolve; source-tree
  presence alone does not prove the asset is available to RealityKit.

## Stored Entity Pitfalls

- Match the stored entity name exactly.
- Confirm the target bundle is the bundle that owns the RealityKit resource.
- Prefer explicit URL loading when bundle lookup ambiguity is the issue.
- Treat generated `.reality` / `.rkassets` output as the runtime artifact that
  RealityKit sees.
