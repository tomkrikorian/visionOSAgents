# AmbientAudioComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/ambientaudiocomponent)

## Overview

A component that designates an entity for ambient audio playback. Ambient audio is especially designed for multi-channel audio representing environments such that each audio channel is played from a fixed direction. Unlike spatial audio, ambient audio sources do not apply further reverb or spatial effects beyond fixed directional output.

## When to Use

- Playing background music or environmental audio that doesn't need precise spatial localization
- Creating ambient soundscapes for immersive environments
- Playing multi-channel audio where each channel has a fixed direction
- Adding non-directional background audio to scenes
- Implementing environmental sounds that should remain consistent regardless of listener position

## How to Use

### Basic Setup

```swift
import RealityKit

func playAmbientMusic(from entity: Entity) async throws {
    let resource = try await AudioFileResource(
        named: "AmbientMusic",
        configuration: .init(
            loadingStrategy: .stream,
            shouldLoop: true
        )
    )
    entity.components.set(AmbientAudioComponent())
    entity.playAudio(resource)
}
```

### With Streaming Audio

```swift
// For large ambient audio files, use streaming
let resource = try await AudioFileResource(
    named: "EnvironmentSound",
    configuration: .init(
        loadingStrategy: .stream,  // Stream for large files
        shouldLoop: true
    )
)
entity.components.set(AmbientAudioComponent())
entity.playAudio(resource)
```

## Key Properties

- No configurable properties - the component itself designates the entity for ambient audio playback
- Audio behavior is determined by the `AudioFileResource` configuration and the component type

## Important Notes

- Ambient audio sources do not apply further reverb or spatial effects beyond fixed directional output
- Multi-channel audio files play with each channel from a fixed direction
- Use for environmental sounds, musical ambience, or background audio that doesn't need precise spatial localization
- Available on visionOS, iOS, and other Apple platforms
- Works with `AudioFileResource` for loading and playing audio files

## Best Practices

- Use streaming loading strategy for large ambient audio files to save memory
- Use preload strategy for low-latency ambient sounds if needed
- Set `shouldLoop: true` for continuous ambient audio
- Use multi-channel audio files with embedded channel layout for proper rendering
- Combine with `AudioMixGroupsComponent` for centralized volume control
- Use for background music or environmental sounds that should remain consistent

## Related Components

- `SpatialAudioComponent` - For 3D spatialized audio with position and directivity
- `ChannelAudioComponent` - For channel-based audio that bypasses spatial effects
- `ReverbComponent` - For adding reverb effects (note: ambient audio doesn't apply additional reverb)
- `AudioMixGroupsComponent` - For grouping and controlling audio volume levels
