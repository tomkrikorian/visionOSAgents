# USDKit Framework

Use this when reading or authoring USD stages from Swift code instead of
hand-editing `.usda` or shelling out to `usd*` tools.

New in visionOS 27, macOS 27, and iOS 27. `import USDKit`.
This is beta API: names and shapes may change before release.

## OpenUSD Concept Mapping

| USDKit | OpenUSD |
|--------|---------|
| `USDStage` | UsdStage |
| `USDPrim` | UsdPrim |
| `USDPrim.Attribute` | UsdAttribute |
| `USDPrim.Attribute.ValueType` | SdfValueTypeName |
| `USDPrim.Predicate` | UsdPrimFlags predicates |
| `USDLayer` | SdfLayer |
| `USDLayer.Path` | SdfPath |
| `USDLayer.Spec` (and `USDPrim.Spec`, ...) | SdfSpec, SdfPrimSpec, ... |
| `USDLayer.AssetPath` | SdfAssetPath |
| `USDLayer.TimeOffset` | SdfLayerOffset |
| `USDLayer.ListOperation` | SdfListOp |
| `USDToken` | TfToken |
| `USDValue` | VtValue |

## USDStage

Open or create a composed stage:

```swift
let stage = try USDStage.open(url)                  // URL; FilePath overload exists
let inline = try USDStage(string: usdaText)         // parse .usda text
let empty = USDStage(displayName: "Scratch")        // anonymous in-memory stage
```

`USDStage.open(rootLayer:sessionLayer:options:)` accepts a root `USDLayer`
(the explicit `rootLayer:` label is required for the layer overload);
`OpenOptions` includes `.createNew`. `init(_:type:loadingPayloads:)` opens from
`Data` plus a `UTType`. `InitialLoadRule` is `.all` or `.none` (payloads).

Authoring and persistence:

```swift
let sphere = stage.definePrim(at: "/Root/Sphere", type: "Sphere")
stage.overridePrim(at: "/Root/Mesh")                // over, not def
stage.removePrim(at: "/Root/Old")
try stage.save()                                    // also saveSessionLayers(), reload()
```

`USDLayer.Path` is string-literal expressible, so prim paths read like `.usda`.

- Hierarchy: `pseudoRoot`, `defaultPrim`, `prim(at:)`, `attribute(at:)`,
  `relationship(at:)`, `descendants`, `allDescendants`, `descendants(where:)`.
- Metrics: `upAxis`, `metersPerUnit`, `timeCodesPerSecond`, `timeCodeRange`.
- Layer muting: `muteLayer(_:)`, `unmuteLayer(_:)`, `isLayerMuted(_:)` by
  layer identifier string.
- Edit target: `stage.editTarget` is settable, but `EditTarget` publicly
  exposes only `init()` and a read-only `layer` in this seed; do not assume a
  layer-targeting initializer exists.

Export:

```swift
try stage.exportFlattened(to: flatURL)
try stage.exportPackage(to: usdzURL,
                        options: [.preferSmallTextureFiles(quality: .medium)])
```

`ExportOptions` also has `.preferSmallTextureFiles` and
`.preferSmallMeshFiles`; `TextureQuality` is `.standard`, `.medium`, `.low`.
Still validate shipped packages with `usdchecker --arkit --strict`.

Change observation (keep the returned token alive):

```swift
let token = stage.addObserver(for: USDStage.ObjectsDidChange.self) { notice in
    // notice.resyncedPaths / notice.changedPaths: Collection of USDLayer.Path
}
```

## USDPrim

Typed attribute access uses a subscript; conforming value types include
`Bool`, the fixed-width integers, `Float`, `Double`, `String`, `USDToken`,
`USDLayer.AssetPath`, `USDLayer.PathExpression`, and `USDValue.Vec3d`:

```swift
sphere["radius", as: Double.self] = 0.25
let r = sphere["radius", as: Double.self]
```

- Create attributes: `makeAttribute(named:as:custom:variability:)` with an
  `Attribute.ValueType` such as `.float`, `.double3`, `.color3f`, `.token`.
- Schemas: `try prim.applyAPISchema("PhysicsRigidBodyAPI")`; an
  `instanceName:` overload exists for multiple-apply schemas.
- Traversal filters: `children(where:)` / `descendants(where:)` take a
  `Predicate` (`.isActive`, `.isDefined`, `.isModel`, `.isInstance`, ...,
  composable as array literals, negatable with `!`).
- References: `try prim.references.add("Asset.usdz")` — `add(_:)` takes a
  `USDLayer.AssetPath` and is the only stage-level reference edit. At the
  layer level `USDPrim.Spec.references` is read-only (`[USDPrim.Reference]?`);
  the only mutation is `clearReferences()` in this seed.
- Specs: `USDPrim.Spec`, `Attribute.Spec`, `Relationship.Spec`, and
  `VariantSetSpec` mirror Sdf*Spec for layer-level authoring (variants,
  payloads, inherits, relocates).

## USDLayer

```swift
let layer = try USDLayer.open("Scene.usda")          // identifier string
layer.subLayerPaths = ["Overrides.usda"]             // [AssetPath]
layer.setField(at: "/Root", name: "kind", value: USDToken("component"))
layer.setTimeSample(at: "/Root/Sphere.radius",
                    time: USDLayer.TimeCode(24), value: 0.5)
try layer.save()
```

- IO: `save()`, `reload()`, `clear()`, `export(to:)`,
  `importContents(from:)` (String or FilePath).
- Anonymous layers: `try USDLayer(displayName:)`; lookup with
  `find(identifier:)`.
- Fields and specs by path: `fields(at:)`, `field(at:name:)`, `spec(at:)`,
  `prim(at:)`, `specType(at:)`, `traverse(at:_:)`.
- Time samples: `allTimeSamples`, `timeSamples(at:)`, `timeSample(at:time:)`,
  `eraseTimeSample(at:time:)`.
- Layer metadata: `defaultPrim`, `startTimeCode`, `endTimeCode`,
  `timeCodesPerSecond`.

## Small Types

- `USDToken`: string-literal, `string`, namespace helpers
  (`namespaceComponents`, `strippingLeadingNamespace()`).
- `USDValue`: type-erased box; `init(_:)`, `get()`, `isHolding(_:)`,
  `typeName`, `isArrayValued`, `arraySize`.
- `ListOperation`: explicit/deleted/prepended/appended entries, the SdfListOp
  model behind composition-arc list edits.
- `AssetPath`: `authoredPath` vs `resolvedPath`. `TimeOffset`: `offset`,
  `scale` for layer time mapping.

## Caveats

- `USDStage`, `USDPrim`, `USDLayer`, and their nested attribute/property
  types are explicitly non-Sendable. Keep all stage work on one actor.
  `USDToken`, paths, and `USDValue.Vec3d` are Sendable.
- No typed schema classes (no UsdGeomMesh equivalent); use prim type tokens,
  attribute names, `ValueType`, and `applyAPISchema`.
- `USDTransformOperation.Kind` currently has only `.translate`
  (`addTransformOperation(type:)`); author other xformOps as attributes or
  keep them in the source `.usda`.
- No public array-typed `Attribute.Value` conformances yet; array values
  surface through `USDValue`.
