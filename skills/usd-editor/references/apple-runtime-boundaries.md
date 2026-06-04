# Apple USD and RealityKit Boundaries

Use this reference when deciding whether to edit authored USD / Reality Composer
Pro content, load an asset through RealityKit, or validate USDZ output for an
Apple-platform app.

## Loading Boundary Pointer

This file owns authored USD / Reality Composer Pro ownership and validation.
For RealityKit stored-entity loading APIs, exact bundle lookup rules, and
runtime resource checks, load
[`entity-loading-and-stored-entities.md`](../../realitykit-visionos-developer/references/entity-loading-and-stored-entities.md).

## Authored Asset Ownership

- If geometry, transforms, hierarchy, materials, animations, or composition arcs
  are authored in USD or Reality Composer Pro, edit the owning layer or project
  asset and reload it through RealityKit.
- Do not recreate authored prims, meshes, materials, or animation structure in
  Swift only to work around an asset edit. Use Swift for runtime state, event
  handling, component setup, and procedural content that is intentionally
  generated at runtime.
- When a named Reality Composer Pro scene or USD prim fails to load, first check
  the exact name, case, target bundle, package resources, and generated runtime
  artifact before changing Swift logic.

## USD and USDZ Validation

Run validation at the layer and final package levels:

```bash
usdcat --loadOnly Scene.usda
usdzip --arkitAsset Scene.usda Scene.usdz
usdchecker --arkit --strict Scene.usdz
```

- `usdcat --loadOnly` is a parse and dependency-loading check for the source
  stage.
- `usdzip --arkitAsset` packages an Apple-platform USDZ from a source layer.
- `usdchecker --arkit --strict` validates the final asset with
  RealityKit-focused rules and treats warnings as failures.
- Do not hand-edit a `.usdz` archive in place. Inspect or unpack it, edit the
  source layer, rebuild the package, and validate the rebuilt package.
