# Audio Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## SpatialAudioComponent
Goal: Plays audio positioned in 3D space.

```swift
entity.components.set(SpatialAudioComponent())
```

## AmbientAudioComponent
Goal: Plays non-directional ambient audio.

```swift
entity.components.set(AmbientAudioComponent())
```

## ChannelAudioComponent
Goal: Plays channel-based audio content.

```swift
entity.components.set(ChannelAudioComponent())
```

## AudioLibraryComponent
Goal: Stores multiple audio resources for reuse.

```swift
let library = AudioLibraryComponent(resources: <#AudioResources#>)
entity.components.set(library)
```

## ReverbComponent
Goal: Applies reverb to an entity's audio.

```swift
entity.components.set(ReverbComponent())
```

## AudioMixGroupsComponent
Goal: Groups audio for mixing control.

```swift
let mixGroups = AudioMixGroupsComponent(groups: <#AudioMixGroups#>)
entity.components.set(mixGroups)
```
