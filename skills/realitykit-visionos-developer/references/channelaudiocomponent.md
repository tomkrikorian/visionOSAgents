# ChannelAudioComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/channelaudiocomponent)

## Overview

A component that plays channel-based audio content that bypasses spatial effects. Channel audio is used for background music or UI audio that shouldn't be spatially located. Unlike spatial audio, channel audio doesn't change based on listener position or orientation.

## When to Use

- Playing background music that should remain consistent regardless of listener position
- Implementing UI sounds that shouldn't be spatially located
- Playing audio that needs to bypass spatialization entirely
- Creating non-spatial audio experiences
- Playing stereo or multichannel audio without spatial effects

## How to Use

### Basic Setup

```swift
import RealityKit

let resource = try await AudioFileResource(
    named: "BackgroundMusic",
    configuration: .init(
        loadingStrategy: .stream,
        shouldLoop: true
    )
)
entity.components.set(ChannelAudioComponent())
entity.playAudio(resource)
```

### UI Audio Example

```swift
// For UI sounds that shouldn't be spatialized
let clickSound = try await AudioFileResource(
    named: "UIClick",
    configuration: .init(loadingStrategy: .preload)
)
uiEntity.components.set(ChannelAudioComponent())
uiEntity.playAudio(clickSound)
```

## Key Properties

- No configurable properties - the component itself designates the entity for channel-based audio playback
- Audio behavior is determined by the `AudioFileResource` configuration

## Important Notes

- Channel audio bypasses all spatial effects - audio doesn't change with listener position
- Use for background music or UI audio that shouldn't be spatially located
- Available on visionOS, iOS, and other Apple platforms
- Works with stereo and multichannel audio files
- Audio channels are played without spatialization

## Best Practices

- Use for background music that should remain consistent
- Use for UI sounds that need to be non-spatial
- Use streaming for large audio files, preload for low-latency sounds
- Set `shouldLoop: true` for continuous background music
- Combine with `AudioMixGroupsComponent` for volume control
- Don't use for sounds that need spatial positioning - use `SpatialAudioComponent` instead

## Related Components

- `SpatialAudioComponent` - For 3D spatialized audio with position and directivity
- `AmbientAudioComponent` - For ambient audio with fixed directional channels
- `AudioMixGroupsComponent` - For grouping and controlling audio volume levels
