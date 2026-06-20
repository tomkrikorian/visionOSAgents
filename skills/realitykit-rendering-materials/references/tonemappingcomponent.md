# ToneMappingComponent


## Overview

A component that controls tone mapping with a filmic curve. Tone mapping compresses high-dynamic-range scene color into displayable range; this component exposes the curve's toe (dark end) and shoulder (highlight end) so you can tune contrast and highlight rolloff per scene, plus an exposure adjustment applied with it.

New in visionOS 27. Beta API: names and shapes may change before release.

## When to Use

- Tuning highlight rolloff when bright emissive content or strong lights clip harshly
- Lifting or crushing shadow detail for a stylized look
- Adjusting overall exposure of rendered content
- Matching the rendered look of content authored in another engine or grading tool

## How to Use

### Default Curve

```swift
import RealityKit

// Defaults: exposure 0.0, toeStrength 0.25, toeLength 0.37,
// shoulderStrength 1.0, shoulderLength 0.7, shoulderAngle 1.0
entity.components.set(ToneMappingComponent())
```

### Custom Curve

```swift
var toneMapping = ToneMappingComponent(
    exposure: 0.5,
    toeStrength: 0.3,
    toeLength: 0.4,
    shoulderStrength: 1.2,
    shoulderLength: 0.8,
    shoulderAngle: 1.0
)
entity.components.set(toneMapping)
```

### Adjust at Runtime

```swift
var toneMapping = entity.components[ToneMappingComponent.self]!
toneMapping.exposure += 0.25
entity.components.set(toneMapping)
```

## Key Properties

- `exposure: Float` - Exposure adjustment applied to scene color (default: 0.0)
- `toeStrength: Float` - How strongly the toe compresses darks (default: 0.25)
- `toeLength: Float` - How far the toe region extends (default: 0.37)
- `shoulderStrength: Float` - How strongly the shoulder compresses highlights (default: 1.0)
- `shoulderLength: Float` - How far the shoulder region extends (default: 0.7)
- `shoulderAngle: Float` - Shape of the shoulder transition (default: 1.0)

## Important Notes

- New in visionOS 27; also available on macOS 27, iOS 27, tvOS 27,
  and macCatalyst 27.
- The toe controls the dark end of the curve, the shoulder controls the bright
  end; strength values increase compression in that region.
- All-default values give the baseline filmic response; start from defaults
  and adjust one parameter at a time.
- Pairs naturally with `BloomComponent` / `BloomOptionsComponent` when tuning
  the look of bright content.

## Best Practices

- Adjust `exposure` first; only touch curve parameters when exposure alone
  cannot fix the look.
- Make small adjustments - the curve parameters interact, and large changes to
  one region shift perceived contrast in the other.
- Keep one tone-mapping configuration per scene look; toggle between presets
  rather than animating individual parameters per frame.
- Verify on device: passthrough blending on visionOS changes how tone-mapped
  content reads compared to the simulator.

## Related Components

- `BloomComponent` / `BloomOptionsComponent` - For glow on bright content
- `ImageBasedLightComponent` - For environment lighting feeding the curve
- `VirtualEnvironmentProbeComponent` - For reflection environment control
