# AudioLibraryComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/audiolibrarycomponent)

## Overview

A component that stores multiple audio resources for reuse across entities in a scene. This component allows you to manage a collection of audio files that can be played by entities without reloading the resources each time.

## When to Use

- Storing multiple audio resources for reuse across multiple entities
- Managing a collection of sound effects or audio clips
- Reducing memory usage by sharing audio resources
- Creating audio libraries for games or interactive experiences
- Organizing audio assets for easy access and playback

## How to Use

### Basic Setup

```swift
import RealityKit

// Create audio resources
let sound1 = try await AudioFileResource(named: "Sound1")
let sound2 = try await AudioFileResource(named: "Sound2")
let sound3 = try await AudioFileResource(named: "Sound3")

// Create library component with multiple resources
let library = AudioLibraryComponent(resources: [sound1, sound2, sound3])
entity.components.set(library)
```

### Accessing Audio from Library

```swift
// Get audio resource from library
if let library = entity.components[AudioLibraryComponent.self],
   let sound = library.resources.first(where: { $0.name == "Sound1" }) {
    entity.playAudio(sound)
}
```

## Key Properties

- `resources: [AudioFileResource]` - Array of audio file resources stored in the library

## Important Notes

- Audio resources are stored in the component and can be shared across entities
- Resources are loaded when the component is created
- Use this component to avoid reloading the same audio files multiple times
- Resources can be accessed by name or index
- Available on visionOS, iOS, and other Apple platforms

## Best Practices

- Store commonly used audio resources in a library component
- Use preload strategy for frequently played sounds
- Use streaming for large audio files that are played less frequently
- Organize audio resources logically (e.g., by category or scene)
- Share the library component across entities that need the same audio
- Consider memory usage when storing many large audio files

## Related Components

- `SpatialAudioComponent` - For playing spatialized audio from library resources
- `AmbientAudioComponent` - For playing ambient audio from library resources
- `ChannelAudioComponent` - For playing channel-based audio from library resources
- `AudioMixGroupsComponent` - For grouping audio resources for volume control
