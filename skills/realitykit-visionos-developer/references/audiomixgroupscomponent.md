# AudioMixGroupsComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/audiomixgroupscomponent)

## Overview

A component that allows you to control multiple "mix groups" of audio in a scene. It enables you to adjust the gain (volume) of named audio categories collectively. Audio resources are assigned to mix groups using `mixGroupName` in their configuration, and this component controls the gain for all audio in each named group.

## When to Use

- Controlling volume levels for categories of audio (e.g., music, sound effects, voice)
- Implementing master volume controls for different audio types
- Creating audio mixing systems for games or interactive experiences
- Adjusting audio levels dynamically based on game state or user preferences
- Grouping related audio sources for centralized control

## How to Use

### Basic Setup

```swift
import RealityKit

// Load audio resources and assign them to mix groups
let musicResource = try await AudioFileResource(
    named: "BackgroundMusic",
    configuration: .init(
        loadingStrategy: .stream,
        shouldLoop: true,
        mixGroupName: "Music"  // Assign to "Music" group
    )
)

let sfxResource = try await AudioFileResource(
    named: "ClickSound",
    configuration: .init(
        loadingStrategy: .preload,
        mixGroupName: "SFX"  // Assign to "SFX" group
    )
)

// Create an audio mixer entity
let audioMixer = Entity()

// Function to update mix group gain
func updateMixGroup(named mixGroupName: String, to level: Audio.Decibel) {
    var mixGroup = AudioMixGroup(name: mixGroupName)
    mixGroup.gain = level
    let component = AudioMixGroupsComponent(mixGroups: [mixGroup])
    audioMixer.components.set(component)
}

// Update multiple groups
func updateMixGroups() {
    let musicGroup = AudioMixGroup(name: "Music")
    musicGroup.gain = -3.0  // Slightly quieter
    
    let sfxGroup = AudioMixGroup(name: "SFX")
    sfxGroup.gain = 0.0  // Normal volume
    
    let component = AudioMixGroupsComponent(mixGroups: [musicGroup, sfxGroup])
    audioMixer.components.set(component)
}
```

### Dynamic Volume Control

```swift
// Adjust music volume based on user preference
func setMusicVolume(_ volume: Float) {
    let decibelLevel = Audio.Decibel(volume * -20.0)  // Convert to decibels
    var musicGroup = AudioMixGroup(name: "Music")
    musicGroup.gain = decibelLevel
    let component = AudioMixGroupsComponent(mixGroups: [musicGroup])
    audioMixer.components.set(component)
}
```

## Key Properties

- `mixGroups: [AudioMixGroup]` - Array of mix groups, each with a name and gain level

### AudioMixGroup Properties

- `name: String` - The name of the mix group (must match `mixGroupName` in audio resources)
- `gain: Audio.Decibel` - The gain level for all audio in this group (0 dB = nominal, negative = quieter)

## Important Notes

- Gain is relative in decibels - zero (0 dB) is "nominal loudness"
- Negative values reduce volume, positive values increase volume (typically clamped)
- All audio resources with the same `mixGroupName` are affected uniformly
- The component can be updated at runtime by re-setting it on the entity
- Typically attached to a dedicated "audio mixer" entity in the scene
- Available on visionOS, iOS, and other Apple platforms

## Best Practices

- Use descriptive mix group names (e.g., "Music", "SFX", "Voice", "Ambient")
- Assign audio resources to mix groups using `mixGroupName` in their configuration
- Create a dedicated entity for the audio mixer component
- Update mix group gains dynamically based on game state or user preferences
- Use decibel values appropriately (0 dB = normal, -6 dB = half volume, -∞ = silence)
- Group related audio sources together for easier management
- Update the component when changing volume levels (re-set the component on the entity)

## Related Components

- `SpatialAudioComponent` - Audio resources in mix groups can be spatialized
- `AmbientAudioComponent` - Ambient audio can be assigned to mix groups
- `ChannelAudioComponent` - Channel audio can be assigned to mix groups
- `AudioFileResource` - Use `mixGroupName` in configuration to assign resources to groups
