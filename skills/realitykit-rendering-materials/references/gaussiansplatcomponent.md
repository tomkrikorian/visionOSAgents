# GaussianSplatComponent


## Overview

A component that renders a 3D Gaussian splat scene from a `GaussianSplatResource`. Gaussian splatting reconstructs photorealistic captures as clouds of oriented, view-dependent Gaussians instead of triangle meshes. The resource is built from raw Metal buffers (one attribute stream per splat property) plus spherical-harmonics color data.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Displaying photorealistic scene captures produced by Gaussian-splat training pipelines
- Rendering scanned environments or objects where mesh reconstruction loses detail
- Showing volumetric, view-dependent content that PBR meshes cannot represent

## How to Use

### Build the Resource from Buffers

Each splat attribute is a `BufferDescriptor` over a `LowLevelBuffer` you fill
with decoded splat data (e.g. parsed from a PLY-style splat file).

```swift
import RealityKit
import Metal

// One descriptor per attribute stream.
let position = GaussianSplatResource.BufferDescriptor(
    buffer: positionBuffer,  // LowLevelBuffer
    format: .float3,
    stride: MemoryLayout<SIMD3<Float>>.stride,
    offset: 0
)
// Build scale, rotation, opacity, and sphericalHarmonics descriptors
// the same way, matching your decoded data layout.

let buffers = try GaussianSplatResource.BufferResource(
    count: splatCount,
    position: position,
    scale: scale,
    rotation: rotation,
    opacity: opacity,
    sphericalHarmonics: (shDescriptor, .second)  // SH degree of the data
)

let resource = GaussianSplatResource(buffers)
```

### Configure and Attach

```swift
resource.projectionMode = .perspective   // or .tangential
resource.sortingMode = .depth            // or .distance
resource.scaleActivation = .exponential  // .identity / .exponential / .sigmoid
resource.opacityActivation = .sigmoid

entity.components.set(GaussianSplatComponent(resource))
```

### Swap the Resource

```swift
var splats = entity.components[GaussianSplatComponent.self]!
splats.splatResource = otherResource
entity.components.set(splats)
```

## Key Properties

`GaussianSplatComponent`:
- `splatResource: GaussianSplatResource` - The splat scene to render

`GaussianSplatResource`:
- `bufferResource: BufferResource?` - The attribute buffers the resource was built from
- `scaleActivation / opacityActivation: ActivationFunction` - `.identity`, `.exponential`, `.sigmoid`; how stored scale/opacity values are decoded
- `projectionMode: ProjectionMode` - `.perspective` or `.tangential`
- `sortingMode: SortingMode` - `.depth` or `.distance` ordering for blending
- `colorSpace: CGColorSpace` - Color space of the splat color data

`GaussianSplatResource.BufferResource`:
- `count: Int` - Number of splats
- `position / scale / rotation / opacity / sphericalHarmonics: BufferDescriptor`
- `degree: SphericalHarmonicDegree` - `.zero`, `.first`, `.second`, `.third`

`GaussianSplatResource.BufferDescriptor`:
- `buffer: LowLevelBuffer`, `format: MTLAttributeFormat`, `stride: Int`, `offset: Int`

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, and tvOS 27.
- The interface exposes buffer-based construction only - there is no
  file-loading initializer on `GaussianSplatResource`, so decode splat files
  into `LowLevelBuffer`s yourself before building the resource.
- `BufferResource.init` is `@MainActor` and throws; build it on the main actor.
- Higher SH degrees store more view-dependent color data per splat and cost
  more memory; `.zero` is diffuse-only color.
- Activation functions must match how the training pipeline stored the data
  (commonly exponential scale and sigmoid opacity).
- Apple ships a sample project named "GaussianSplatsOnVisionOS" that
  demonstrates the full decode-and-render flow.

## Best Practices

- Match `format`, `stride`, and `offset` exactly to your decoded buffer layout;
  mismatches render garbage rather than erroring.
- Pick the lowest `SphericalHarmonicDegree` that preserves acceptable quality.
- Keep splat decoding off the main actor; only the `BufferResource` build and
  component mutation belong on it.
- Treat the resource as immutable scene data; swap `splatResource` to change
  captures instead of rebuilding buffers in place.

## Related Components

- `ModelComponent` - For triangle-mesh rendering
- `RenderLayerComponent` - For scoping lights and effects to specific content
- `OpacityComponent` - For hierarchy-level fading
