# Programmatic Shader Graphs

Use this file when the shader graph itself must be built in Swift instead of
authored in Reality Composer Pro. New in visionOS 27. The API ships
as the `ShaderGraph` module re-exported through `RealityKit`, so a plain
`import RealityKit` is enough. This is beta API: names and shapes may change
before release.

## When To Build Graphs in Code

- Keep Reality Composer Pro as the default authoring surface. Hand-authored
  materials, promoted inputs, and `ShaderGraphMaterial.init(named:from:in:)`
  loading are unchanged.
- Build graphs in code only when graph structure is decided at runtime:
  generated node networks, materials assembled from runtime data, or tools
  that cannot ship a `.usda`.
- For static materials, author in Reality Composer Pro or load MaterialX
  data with `ShaderGraphMaterial(materialXLabel:data:)` instead of building
  a graph in code.

## Building a Graph

`ShaderGraph` is a node-and-edge container. Node definitions come from a
MaterialX `ShaderGraph.NodeLibrary` (versions `.materialX138` and
`.materialX139`). Discover definitions with `definition(named:)` or
`definitions(function:input:)` / `definitions(function:output:)`; do not
hardcode definition identifiers you have not confirmed exist in the targeted
library version.

```swift
import RealityKit

func makeMaterial(surfaceNodeName: String) async throws
    -> ShaderGraphMaterial?
{
    let graph = try ShaderGraph(
        named: "GeneratedMaterial",
        inputs: [],
        outputs: [.init(name: "out", type: .surfaceShader)]
    )

    // Discover the definition; do not hardcode unverified identifiers.
    let library = ShaderGraph.NodeLibrary(version: .materialX139)
    guard let definition = library.definition(named: surfaceNodeName) else {
        return nil
    }

    let surface = try graph.addNode(try library.makeNode(from: definition))
    try graph.connect(surface, to: graph.results.name, inputPort: "out")

    if let input = definition.inputs.first(where: { $0.type == .float3 }) {
        let tint = try graph.addConstant(
            .float3([0.0, 0.38, 1.0]), named: "tint")
        try graph.connect(tint, to: surface, inputPort: input.name)
    }

    let descriptor = ShaderGraphMaterial.Program.Descriptor(
        shaderGraph: graph,
        lightingModel: .lit(diffuseModel: .hammon, specularModel: .ggx)
    )
    let program = try await ShaderGraphMaterial.Program(descriptor: descriptor)
    return ShaderGraphMaterial(program: program)
}
```

Graph API surface:

- `ShaderGraph(named:inputs:outputs:)` declares the graph interface;
  `graph.arguments` and `graph.results` are the nodes that carry it.
- `addNode(_:)` returns the node key (`String`); `updateNode(_:forKey:)`,
  `removeNode(_:)`, and `replace(nodes:edges:)` mutate the graph.
- `connect(_:outputPort:to:inputPort:)` takes node keys or `Node` values;
  `addEdge(_:)` / `removeEdge(_:)` take an explicit
  `Edge(outputNode:outputPort:inputNode:inputPort:)`.
- `addConstant(_:named:)` inserts a `ShaderGraph.Value` constant node. Cases
  cover `.bool`, `.int`, `.float`, `.string`, vectors (`.float2`–`.float4`,
  half and int variants), and matrices.
- `ShaderGraph.DataType` includes `.surfaceShader`, `.geometryModifier`,
  `.postLightingShader`, and `.texture` alongside the scalar/vector types.
- `Node.data` is `.definition(NodeDefinition)`, `.graph(ShaderGraph)` for
  subgraphs, or `.constant(Value)`.
- `primvarMappings: [String: TextureCoordinate]` binds primvar names to UV
  sets `.uv0`–`.uv7`; `functionConstantInputs: [String]` lists inputs
  compiled as Metal function constants (supply them via descriptor
  `constantValues`).
- `encode()` / `ShaderGraph(from: Data)` round-trip a graph as `Data`.

## ShaderGraphMaterial.Program

`Program.Descriptor` fields: `shaderGraph`, `lightingModel`,
`isColorDitheringEnabled` (default `false`), `blendMode`
(`MaterialParameterTypes.BlendMode?`, `.alpha` / `.add`), `inputValues`
(`[String: MaterialParameters.Value]`), and `constantValues`
(`MTLFunctionConstantValues`). `Descriptor(inferredFrom:)` derives settings
from the graph and throws if it cannot. Compile with
`Program(descriptor:) async throws`, then `ShaderGraphMaterial(program:)`.
The material keeps a readable/writable `program` property, and the promoted
parameter flow from `runtime-api.md` applies unchanged.

## LightingModel

`LightingModel` is `.lit(LitLightingModel)`, `.hair(HairLightingModel)`, or
`.unlit(UnlitLightingModel)`, with factories showing the defaults:

```swift
let model = LightingModel.lit(
    diffuseModel: .hammon,   // .hammon, .lambertian, .orenNayar
    specularModel: .ggx,     // .ggx, .blinnPhong, .sheen, .anisotropicGGX
    isSubsurfaceScatteringEnabled: false,
    isMultiscatteringEnabled: true,
    isBentNormalEnabled: false,
    isClearcoatEnabled: false
)
// Also: LightingModel.hair(), LightingModel.unlit(isTonemappingEnabled: true)
```

## PortalMaterial.Program

`PortalMaterial.Program.Descriptor(shaderGraph:inputValues:constantValues:)`
has no lighting model. Compile with `Program(descriptor:) async throws` and
build with `PortalMaterial(program:)`. On visionOS 27, `PortalMaterial` also
gains `parameterHandle(name:)`, `setParameter(name:value:)` /
`setParameter(handle:value:)`, and `getParameter`, matching the
`ShaderGraphMaterial` parameter flow.

## PBR Subsurface Scattering

`PhysicallyBasedMaterial` gains subsurface slots on visionOS 27:

```swift
var pbr = PhysicallyBasedMaterial()
pbr.subsurfaceWeight = 1.0
pbr.subsurfaceColor = .init(
    color: CGColor(red: 0.9, green: 0.4, blue: 0.35, alpha: 1.0))
pbr.subsurfaceRadius = 0.5
pbr.subsurfaceScatterAnisotropy = 0.0
```

- `subsurfaceWeight`, `subsurfaceRadius`, and `subsurfaceScatterAnisotropy`
  hold a `Float` scale plus optional texture and accept float literals.
- `subsurfaceColor` and `subsurfaceRadiusScale` hold a `CGColor` plus
  optional texture.
- `bentNormal` is a new texture-only slot in the same visionOS 27 extension.

## Guardrails

- Do not use underscore-prefixed `ShaderGraph` module types such as
  `_Proto_ShaderNodeGraph`; they are not stable API.
- Validate before mutating in tooling code: `canAddNode(_:)`,
  `canAddEdge(_:)`, `validateAddingNode(_:)`, `validateAddingEdge(_:)`.
- Check `NodeDefinition.isAvailable(on:version:)` when a graph must load on
  more than one platform or OS version.
