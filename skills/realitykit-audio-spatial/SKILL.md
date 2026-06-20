---
name: realitykit-audio-spatial
description: Implement and debug RealityKit spatial audio, ambient audio, channel audio, audio libraries, audio mix groups, reverb, grouped playback, and acoustic simulation on visionOS 27. Use when a RealityKit task is primarily about placing sound in 3D, loading or organizing audio resources, controlling channel or ambient playback, mixing groups, room acoustics, or audio behavior tied to RealityKit entities.
---

# RealityKit Audio Spatial

## Quick Start

1. Decide whether the task is entity-placed spatial audio, ambient/channel
   playback, reusable audio libraries, mix groups, reverb, or acoustic
   simulation.
2. Load the matching audio reference file only.
3. Keep audio resource loading asynchronous and entity ownership explicit.
4. Route entity loading, anchoring, interaction, or attachment setup to
   `realitykit-visionos-developer`.
5. Route animation or physics triggers for audio events to
   `realitykit-animation-physics`, and custom trigger systems to
   `realitykit-ecs-systems`.

## Load References When

| Reference | When to Use |
|---|---|
| [`references/spatialaudiocomponent.md`](references/spatialaudiocomponent.md) | Place sound in 3D space on a RealityKit entity. |
| [`references/ambientaudiocomponent.md`](references/ambientaudiocomponent.md) | Add non-positional ambient audio. |
| [`references/channelaudiocomponent.md`](references/channelaudiocomponent.md) | Control channel-oriented audio playback. |
| [`references/audiolibrarycomponent.md`](references/audiolibrarycomponent.md) | Use reusable audio libraries. |
| [`references/audiomixgroupscomponent.md`](references/audiomixgroupscomponent.md) | Organize playback with mix groups. |
| [`references/reverbcomponent.md`](references/reverbcomponent.md) | Add or tune reverb. |
| [`references/audio-groups-and-acoustics.md`](references/audio-groups-and-acoustics.md) | Use grouped playback or simulated room acoustics. |

## Cross-Routing

- Use `realitykit-visionos-developer` for entity ownership, asset loading,
  anchors, input, attachments, portals, or synchronization around audio
  entities.
- Use `realitykit-animation-physics` when audio is triggered by character,
  collision, physics, particle, or cloth behavior.
- Use `realitykit-ecs-systems` when audio behavior needs custom per-frame
  query logic.

## Guardrails

- Keep audio resource and file loading off the synchronous UI path.
- Decide whether audio should be positional, ambient, channel-based, grouped,
  or acoustically simulated before adding components.
- Treat visionOS 27 audio group and acoustics additions as beta API; re-check
  symbols against the installed SDK.
- Verify audio behavior on device when spatialization, acoustics, or output
  routing matters.

## Output Expectations

Provide:

- the audio category
- which audio references were used
- the selected component or resource ownership path
- the spatialization, grouping, or acoustics constraint
- the next device or runtime validation step
