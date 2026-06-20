# Audio Playback Groups and Simulated Acoustics


## Overview

Two audio additions: `AudioPlaybackGroupController` plays multiple audio
resources on multiple entities as one sample-accurate group (with scheduled
start via `AVAudioTime`), and simulated acoustics computes reverb from actual
room geometry (`ReverbMeshResource` + `Reverb.simulated(mesh:materials:)`)
with frequency-dependent surface materials. New in visionOS 27. Also
on iOS, macOS, macCatalyst, and tvOS 27.

## When to Use

- Stems/layers that must start and stay in sample-accurate sync
- Scheduling playback at a precise host time (multi-device sync, beat sync)
- Group-wide gain, fade, speed, and seek control
- Reverb that matches a modeled room instead of a generic preset
- Per-surface acoustic materials (absorption/scattering by frequency)

## How to Use

### Grouped Playback

```swift
import RealityKit

let controller = try Audio.playAudio([
    (drumsResource, drumsEntity),
    (bassResource, bassEntity),
    (leadResource, leadEntity),
])

controller.gain = -6
controller.fade(to: 0, duration: 2.0)
controller.seek(to: .seconds(30))
controller.speed = 1.0
```

Prepare without starting: `Audio.prepareAudio(_:)` then `controller.play()`.
Schedule a precise start:

```swift
import AVFAudio

let startTime = AVAudioTime(hostTime: mach_absolute_time() + delayTicks)
let controller = try Audio.playAudio(resourcesAndEntities, at: startTime)
// or on an existing controller: try controller.play(at: startTime)
```

Single-entity scheduled start also exists:
`try entity.playAudio(resource, at: avAudioTime)`.

Completion event:

```swift
scene.subscribe(to: AudioEvents.PlaybackGroupCompleted.self) { event in
    // event.playbackController
}
```

### Simulated Acoustics

```swift
// Geometry for the acoustic simulation (not rendered)
let room = ReverbMeshResource.shoebox(size: [6, 3, 4])

// Frequency-dependent surface response: [frequency: coefficient]
let plaster = Audio.Material(
    name: "plaster",
    absorption: [125: 0.10, 1000: 0.06, 4000: 0.04],
    scattering: .uniform(0.3))

reverbEntity.components.set(
    ReverbComponent(reverb: .simulated(mesh: room, materials: [plaster])))
```

`ReverbMeshResource` sources: `init(positions:triangleIndices:materials:)`
(per-triangle material indices), `init(from: MeshResource)`,
`init(from: [MeshDescriptor])`, and primitives `plane(width:depth:)`,
`box(size:)`, `shoebox(size:)`.

## Key Properties

### AudioPlaybackGroupController (@MainActor)

- `resourcesAndEntities: [(AudioResource, Entity)]` - the group members
- `play()` / `play(at: AVAudioTime)` / `pause()` / `stop()` / `isPlaying`
- `gain: Audio.Decibel`, `fade(to:duration:)`
- `speed: Double`, `seek(to: Duration)`, `playbackPosition: TimeInterval`
- `Identifiable` with `id: UInt64`

### Audio.Absorption / Audio.Scattering

- `init(_ coefficients: [Float])` or `init(_ coefficientByFrequency:
  [Float: Float])`; dictionary-literal syntax works directly
- `.default`, `.uniform(_:)`, `scaled(by:)` (frequency-dependent scalar)

### Audio.Material

- `init(name:absorption:scattering:)`
- `scalingAbsorption(by:)`, `scalingScattering(by:)` derive variants

## Important Notes

- New in visionOS 27. Beta API: names and shapes may change before
  release.
- The group factories and `play(at:)` throw - handle scheduling failures
  (e.g. a start time already in the past).
- Spatialization still comes from each entity's own audio component
  (`SpatialAudioComponent`, `ChannelAudioComponent`, `AmbientAudioComponent`);
  the group controller only synchronizes transport.
- Keep reverb meshes coarse - acoustic simulation does not need render-level
  detail.

## Related Components

- `ReverbComponent` - where a `Reverb` value (including `.simulated`) is set
- `SpatialAudioComponent` - per-entity spatial playback parameters
- `AudioMixGroupsComponent` - mix-group gain control across entities
- `AmbientAudioComponent` / `ChannelAudioComponent` - non-spatial sources
