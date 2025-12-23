# ReverbComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/reverbcomponent)

## Overview

A component that applies acoustic environments (reverb presets) to spatial audio within a scene. It lets you define how sounds behave acoustically based on the configured environment. The component uses preset-based reverb to simulate different acoustic spaces.

## When to Use

- Adding reverb effects to spatial audio in immersive environments
- Simulating different acoustic spaces (rooms, halls, outdoor areas)
- Creating realistic audio experiences that match visual environments
- Applying environmental reverb to spatial audio sources
- Enhancing immersion in visionOS experiences

## How to Use

### Basic Setup

```swift
import RealityKit

// Apply reverb preset to an entity
let studio = try await Entity(named: "Studio", in: studioBundle)
studio.components.set(
    ReverbComponent(reverb: .preset(.veryLargeRoom))
)
rootEntity.addChild(studio)
```

### Different Reverb Presets

```swift
// Small room reverb
entity.components.set(
    ReverbComponent(reverb: .preset(.smallRoom))
)

// Medium room reverb
entity.components.set(
    ReverbComponent(reverb: .preset(.mediumRoom))
)

// Large room reverb
entity.components.set(
    ReverbComponent(reverb: .preset(.largeRoom))
)

// Very large room reverb
entity.components.set(
    ReverbComponent(reverb: .preset(.veryLargeRoom))
)
```

### Hierarchy-Based Reverb

```swift
// Reverb is inherited from the nearest ancestor entity
// Place reverb component on a parent entity to affect all children
let roomEntity = Entity()
roomEntity.components.set(
    ReverbComponent(reverb: .preset(.mediumRoom))
)

// All child entities will use this reverb
let soundSource = Entity()
roomEntity.addChild(soundSource)
// soundSource will use mediumRoom reverb
```

## Key Properties

- `reverb: ReverbComponent.Reverb` - The reverb configuration, typically using `.preset()` with a reverb preset type

### Reverb Presets

- `.smallRoom` - Small room acoustic environment
- `.mediumRoom` - Medium room acoustic environment
- `.largeRoom` - Large room acoustic environment
- `.veryLargeRoom` - Very large room acoustic environment

## Important Notes

- Only one reverb component is active at a time per entity
- The nearest reverb component in an entity's ancestry determines the spatial audio reverb behavior
- In mixed immersion (visionOS 1), spatial audio is reverberated according to real-world acoustics
- In visionOS 2+, the system supports progressive immersive environments (blending real acoustics with preset reverb) and full immersive environments (only preset is used)
- Reverb presets are more usable in immersive spaces than in mixed reality
- Available primarily on visionOS, especially with features introduced in visionOS 2

## Best Practices

- Use reverb presets that match your visual environment
- Place reverb components on parent entities to affect multiple child entities
- Use different reverb for different areas of your scene
- Consider the immersion level when choosing reverb (mixed vs full immersive)
- Test reverb levels to avoid overwhelming the audio mix
- Combine with `SpatialAudioComponent` for complete spatial audio setup
- Update reverb dynamically when transitioning between environments

## Related Components

- `SpatialAudioComponent` - Reverb is applied to spatial audio sources
- `AmbientAudioComponent` - Note: ambient audio doesn't apply additional reverb
- `ImageBasedLightComponent` - Often used together for complete environmental setup
