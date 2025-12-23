# SpatialAudioComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/spatialaudiocomponent)

## Overview

A component that configures how sounds emit from an entity into a person's environment. The audio system continuously updates the position and orientation of spatial audio sources automatically, so sounds come from an entity wherever it goes and wherever it points. Spatial audio sources incorporate a person's environment acoustics so that they blend in naturally with the surrounding area.

## When to Use

- Playing 3D positioned audio from entities
- Creating immersive soundscapes
- Implementing directional audio cues
- Adding spatial audio feedback to interactions
- Creating realistic audio experiences

## How to Use

### Basic Spatial Audio

```swift
import RealityKit

// RealityKit audio playback is spatial by default
let entity = Entity()
let resource = try AudioFileResource.load(named: "MyAudioFile")
entity.playAudio(resource) // Audio is played spatially from entity
```

### Customizing Spatial Audio

```swift
// Adjust overall gain
entity.spatialAudio = SpatialAudioComponent(gain: -10)

// Reduce reverb
entity.spatialAudio?.reverbLevel = -6

// Configure directivity (beam pattern)
entity.spatialAudio?.directivity = .beam(focus: 0.5)
```

### Complete Setup

```swift
let spatialAudio = SpatialAudioComponent(
    gain: 0, // Overall level
    directLevel: 0, // Direct signal level
    reverbLevel: -3, // Reverb signal level
    directivity: .beam(focus: 0.5), // Radiation pattern
    distanceAttenuation: .rolloff(factor: 2) // Distance falloff
)
entity.components.set(spatialAudio)
```

### Handling Coordinate Conventions

```swift
// If your model uses +Z forward but audio projects along -Z
let audioSource = Entity()
audioSource.orientation = .init(angle: .pi, axis: [0, 1, 0]) // Rotate 180° about Y
audioSource.components.set(SpatialAudioComponent())
```

## Key Properties

- `gain: Decibel` - Overall level for all sounds that an entity emits (range: [-∞, 0])
- `directLevel: Decibel` - Level of the direct unreverberated signal
- `reverbLevel: Decibel` - Level of reverberated signal
- `directivity: SpatialAudioComponent.Directivity` - Radiation pattern for sound emission
- `distanceAttenuation: SpatialAudioComponent.DistanceAttenuation` - How sound level decreases with distance

## Important Notes

- Spatial audio sources emit only a single channel (mono)
- The engine mixes stereo or multichannel audio down to mono before spatialization
- Use mono source material to avoid unwanted mixdown artifacts
- Spatial audio sources project sounds along their negative z-axis
- Properties can be updated dynamically during runtime

## Directivity Patterns

- `.beam(focus: Float)` - Directional beam pattern (0 = omnidirectional, 1 = highly directional)
- Default is `.beam(focus: 0)` which projects sound evenly in all directions

## Distance Attenuation

- `.rolloff(factor: Float)` - Controls how sound level decreases with distance
- Higher factors mean faster falloff

## Best Practices

- Use mono audio files for spatial audio sources
- Adjust gain to balance audio levels in your scene
- Use directivity to create directional audio effects
- Configure distance attenuation for realistic audio falloff
- Update properties dynamically based on game state or user interaction
- Combine with `ReverbComponent` for additional reverb effects
- Position audio sources carefully relative to visual content

## Related Components

- `AmbientAudioComponent` - For non-directional ambient audio
- `ChannelAudioComponent` - For channel-based audio
- `ReverbComponent` - For additional reverb effects
- `AudioLibraryComponent` - For storing multiple audio resources
