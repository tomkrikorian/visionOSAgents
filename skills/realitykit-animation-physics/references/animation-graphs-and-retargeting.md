# Animation Graphs, Retargeting, and Mesh Deformers


## Overview

A character-animation toolchain: declarative skeletons (`SkeletonResource`),
skeleton-to-skeleton retargeting (`RetargetingConfiguration`), data-driven
animation state machines (`AnimationGraphResource` +
`AnimationGraphComponent`), root-motion extraction, and a GPU/CPU mesh-deformer
stack (`MeshDeformerComponent`). New in visionOS 27. Also on iOS,
macOS, macCatalyst, and tvOS 27.

## When to Use

- Playing one character's animations on a differently proportioned skeleton
- State-machine-driven character animation (idle/walk/run with transitions)
- Driving entity movement from animation root motion
- Custom blend-shape/skinning/subdivision deformation pipelines
- Building skeletons in code instead of importing them

## How to Use

### Declare a Skeleton

```swift
import RealityKit

let root = try SkeletonResource.Joint("root") {
    try SkeletonResource.Joint("spine",
                               restPoseTransform: Transform(translation: [0, 0.5, 0])) {
        try SkeletonResource.Joint("head")
    }
}
let skeleton = try SkeletonResource(named: "biped", rootJoint: root)
```

`SkeletonResource(from: MeshResource.Skeleton)` converts an imported skeleton.
`AnimationEvaluation(ikResources:blendMasks:)` attaches IK and
`BlendMask(name:jointWeights:)` masks. `IKRig(named:rootJoint:)` builds a rig
from the same joint tree.

### Retarget Animation Between Skeletons

```swift
let config = try RetargetingConfiguration.automatchBiped(
    sourceSkeleton, to: targetSkeleton)
// Quadruped variant: RetargetingConfiguration.automatchQuadruped(...)
// Overloads accept sourceTransform/targetTransform and per-joint
// jointOffsets: [String: simd_quatf].

// Apply while processing a sampled joint animation:
let definition = try sampledAnimation.processAndCreateAnimation(
    retargeting: config, operations: [], name: "walk-retargeted")
let resource = try AnimationResource.generate(with: definition)
```

### Extract Root Motion

```swift
let definition = try sampledAnimation.processAndCreateAnimation(
    for: skeleton,
    operations: [.extractRootMotion(jointName: "root", options: .translationXZ)],
    name: "walk-in-place")
```

`RootMotionOptions`: `translationX/Y/Z`, `rotationX/Y/Z`, `translationXZ`
(default), `extractAll`. Other operations: `removeAnimation(for:)`,
`convertToAdditive(baseAnimation:)`, `convertToAdditiveUsingRestPose()`,
`convertToAdditiveUsingFirstSample()`.

At playback, subscribe to `AnimationEvents.RootMotionDidUpdate` - it carries
`entity`, `rootMotionTransform`, `deltaTime`, and a settable
`suppressesAutomaticApplication` flag for applying motion yourself (e.g.
through a character controller).

### Animation Graphs (State Machines)

```swift
let errors = AnimationGraphResource.validate(
    definition: data, nodeResourceMapping: clips, skeletonResource: skeleton)
guard errors.isEmpty else { return }

let graph = try AnimationGraphResource(
    definition: data, nodeResourceMapping: clips, skeletonResource: skeleton)
entity.components.set(AnimationGraphComponent(graph: graph))
```

`definition` is authored graph data; `nodeResourceMapping: [Int:
AnimationResource]` binds clip nodes to animations. `parameterNames` lists the
graph's parameters. At runtime the component exposes read-only state:
`activeNodes`, `activeStateMachineNodes` (`currentState`, `previousState`,
`lastTransition`), `activeClipNodes` (`currentCycle`), `activeTags`.

### Mesh Deformer Stacks

```swift
let stack = MeshDeformationStack(
    deformers: [BlendShapeDeformer(),
                SkinningDeformer(skinsTangentFrame: true),
                RenormalizationDeformer()],
    targets: [.all])
entity.components.set(try MeshDeformerComponent(from: [stack]))
```

Built-in deformers: `BlendShapeDeformer`, `SkinningDeformer(skinsTangentFrame:)`,
`OpenSubdivisionDeformer`, `RenormalizationDeformer`,
`CalculateBoundingBoxDeformer`. `MeshScope` targets: `.all`,
`.model(name:part:)`, `.instance(name:part:)`. Conform a type to the
`MeshDeformer` protocol (static `mode`/`type`, `deform(parameter:encoder:)` for
GPU or `deform(parameter:)` for CPU, `options`) for custom deformers.

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- `RetargetingConfiguration` is `@MainActor`; resource initializers `throw`.
- Always run `AnimationGraphResource.validate(...)` /
  `BehaviorTreeResource.validate(...)`-style checks before constructing from
  raw definition data - validation returns human-readable error strings.
- Deformer order in a `MeshDeformationStack` matters: blend shapes, then
  skinning, then renormalization is the conventional order.

## Related Components

- `BlendShapeWeightsComponent` - direct blend-shape weight control
- `IKComponent` / `SkeletalPosesComponent` - lower-level pose access
- `AnimationLibraryComponent` - storing clips on an entity
- `CharacterControllerComponent` - consume extracted root motion for movement
