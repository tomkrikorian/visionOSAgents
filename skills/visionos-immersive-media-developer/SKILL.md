---
name: visionos-immersive-media-developer
description: Implement immersive and spatial video experiences on Apple Vision Pro (visionOS 26), including AVKit AVExperienceController, RealityKit VideoPlayerComponent setup, Apple Projected Media Profile (APMP), portal/progressive/full immersive viewing modes, transitions and events, comfort mitigation, and Apple Immersive Video authoring workflows.
---

# visionOS Immersive Media Developer

## Description and Goals

This skill provides a practical playbook for building **immersive and spatial media** experiences on **Apple Vision Pro**. On visionOS 26 start with **AVKit `AVExperienceController`** when the system player experience fits your app — it is the canonical API for moving an `AVPlayerViewController` between window, inline, expanded, and immersive presentations. Use RealityKit’s `VideoPlayerComponent` when you need custom placement, custom environments, or deeper scene integration for video playback that can move between **window/portal** playback and **immersive** playback.

It also outlines how Apple’s **ImmersiveMediaSupport** framework and **Apple Projected Media Profile (APMP)** fit into authoring and packaging **Apple Immersive Video** content.

### Goals

- Help you choose the right playback surface (2D window, portal, progressive immersive, full immersive).
- Implement RealityKit video playback using `VideoPlayerComponent` correctly.
- Handle immersive viewing mode transitions safely (including scene transitions when needed).
- Respond to video playback events and comfort mitigation events on visionOS 26+.
- Provide a foundation for Apple Immersive Video authoring workflows where relevant.

## What This Skill Should Do

When asked to add immersive/spatial video to a visionOS app, this skill should:

1. **Clarify the media experience**
   - Is this a “video on a surface” experience, a portal, or full immersive playback?
   - Is the content mono, stereo, spatial video, or immersive media?
   - Do you need passthrough tinting, captions/subtitles, or multi-user playback sync?
2. **Pick a playback architecture**
   - Prefer AVKit **`AVExperienceController`** (visionOS 26+) with `AVPlayerViewController` when the system playback interface matches the product requirements. `AVExperienceController` is the API that moves the player between `window`, `inline`, `expanded`, and `immersive` experiences and handles `AutomaticTransitionToImmersive`.
   - **Migration note**: once an `AVExperienceController` is attached to an `AVPlayerViewController`, that view controller's presentation APIs (`present`, `setVideoPresentationStyle`, etc.) are no longer honored. All experience changes must go through the experience controller. Do not mix the two.
   - Use RealityKit `VideoPlayerComponent` when the experience needs custom placement, custom environments, or scene-aware playback behavior inside an entity graph.
   - Escalate to CompositorServices only for custom engines or bespoke full-space rendering.
3. **Implement playback + UI**
   - Create a video entity, attach `VideoPlayerComponent`, and manage UI affordances.
   - Handle immersive-viewing mode transitions (portal ↔ immersive space).
4. **Handle events and comfort**
   - Subscribe to `VideoPlayerEvents` for viewing mode changes, transitions, and comfort mitigation.
5. **Validate comfort and accessibility**
   - Provide clear exit paths, reduce motion where appropriate, and support captions.

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

## Information About the Skill

### Core Concepts

#### Choose AVKit first, then RealityKit when needed

AVKit provides the preferred system playback experience on visionOS. On
visionOS 26, use `AVExperienceController` (AVKit) together with
`AVPlayerViewController` to move the player between window, inline, expanded,
and immersive experiences. Use RealityKit’s `VideoPlayerComponent` when you
need the video to participate directly in a custom 3D scene, custom
environment, or bespoke interaction model.

#### AVExperienceController (visionOS 26+)

`AVExperienceController` is the AVKit API that controls how a
`AVPlayerViewController` presents itself across visionOS placements. Keep the
following in mind:

- Build an `AVExperienceController.Configuration` that enumerates the
  experiences your app supports (for example a window experience plus an
  immersive experience).
- `AVExperienceController.ExpandedConfiguration` and its
  `AutomaticTransitionToImmersive` option drive the hands-off promotion from
  expanded playback into immersive mode.
- Once the experience controller is attached, **do not** continue to drive
  presentation through `AVPlayerViewController` directly — that will silently
  no-op. All transitions must go through the experience controller.

#### Apple Projected Media Profile (APMP)

APMP is Apple's visionOS 26 profile for projected/wide-FOV and immersive video
content. Use the playback configuration option
`AVAssetPlaybackConfigurationOption.appleImmersiveVideo` to tell AVFoundation
that the asset should play back as immersive Apple video. APMP is the path for
180/360 projected video and Apple Immersive Video content that ships with an
APMP conformant asset.

#### Spatial / MV-HEVC video

Spatial Video on Apple Vision Pro is delivered as MV-HEVC. Use
`VideoPlayerComponent.spatialVideoMode` to switch a RealityKit video entity
between mono and stereo output when the source is spatial. When reading or
converting spatial video files outside of playback, see Apple's
"Reading multiview 3D video files" and "Converting side-by-side 3D video to
multiview HEVC and spatial video" documentation as the canonical pipeline.

#### Immersive viewing modes

For immersive media types, visionOS supports multiple immersive viewing modes:

- **Portal**: immersive media rendered as a portal window matching the containing entity transform.
- **Progressive**: partial-to-full coverage controlled via the Digital Crown (not used for Spatial Video).
- **Full**: immersive media fills the field of view.

You should treat switching between these modes as a **scene orchestration** problem as well as a component configuration problem.

#### Comfort mitigation (visionOS 26+)

visionOS can detect video comfort violations and trigger mitigation. Your app should subscribe to the event and respond:

- pause playback
- reduce immersion
- continue (play) depending on what the system reports and what UX you want

#### Authoring / packaging Apple Immersive Video

The **ImmersiveMediaSupport** framework provides tools and a workflow for authoring and packaging Apple Immersive Video content (typically as part of a content pipeline, not day-to-day app UI).

### Reference Tables

| Reference | When to Use |
|---|---|
| [`REFERENCE.md`](references/REFERENCE.md) | Decision tree: window vs portal vs progressive vs full immersive playback. |
| [`videoplayercomponent-basics.md`](references/videoplayercomponent-basics.md) | When you need to set up `VideoPlayerComponent` + `AVPlayer` correctly. |
| [`immersive-viewing-modes.md`](references/immersive-viewing-modes.md) | When implementing portal/progressive/full modes and related scene transitions. |
| [`events-and-transitions.md`](references/events-and-transitions.md) | When responding to `VideoPlayerEvents` and managing UI during transitions. |
| [`comfort-mitigation.md`](references/comfort-mitigation.md) | When handling comfort violations and mitigation strategies on visionOS 26+. |
| [`apple-immersive-video-authoring.md`](references/apple-immersive-video-authoring.md) | When you need Apple Immersive Video authoring/packaging references. |

### Implementation Patterns

#### Basic VideoPlayerComponent setup

```swift
import AVFoundation
import RealityKit

let videoEntity = Entity()
let player = AVPlayer(url: url)

var video = VideoPlayerComponent(avPlayer: player)
video.isPassthroughTintingEnabled = true
// video.spatialVideoMode = .stereo  // uncomment when the source is MV-HEVC spatial video

videoEntity.components.set(video)
player.play()
```

#### Immersive playback with AVExperienceController (visionOS 26+)

```swift
import AVKit
import AVFoundation

let item = AVPlayerItem(
  asset: AVURLAsset(url: url),
  automaticallyLoadedAssetKeys: [.playable]
)
item.playbackConfigurationOptions = [.appleImmersiveVideo]

let player = AVPlayer(playerItem: item)
let controller = AVPlayerViewController()
controller.player = player

var configuration = AVExperienceController.Configuration()
// Configure the window and immersive experiences your app supports,
// including ExpandedConfiguration.AutomaticTransitionToImmersive if the
// app wants expanded playback to promote itself into immersive mode.
let experienceController = try AVExperienceController(
  playerViewController: controller,
  configuration: configuration
)

// From this point forward, drive all presentation through `experienceController`.
// Calling `controller.present(...)` or setting `controller.videoGravity` for
// presentation purposes no longer has effect.
```

#### Subscribe to immersive viewing mode transitions

```swift
import RealityKit

var subscription: EventSubscription?

subscription = content.subscribe(to: VideoPlayerEvents.ImmersiveViewingModeWillTransition.self) { event in
    // Disable non-essential UI while transitioning.
}
```

#### Subscribe to comfort mitigation (visionOS 26+)

```swift
subscription = content.subscribe(to: VideoPlayerEvents.VideoComfortMitigationDidOccur.self) { event in
    switch event.comfortMitigation {
    case .pause:
        // Update UI to indicate playback paused.
        break
    case .reduceImmersion:
        // Offer a UI path back to portal / lower immersion.
        break
    case .play:
        break
    }
}
```

### Pitfalls and Checks

- Don’t treat immersive mode switching as “just a property change”; you may need to transition between window scenes and immersive spaces deliberately.
- Make sure you have an obvious “exit” affordance from immersive playback.
- Always test Spatial Video vs immersive media behavior (they differ; progressive isn’t used for Spatial Video).
- Subscribe to transitions/events early; many UX issues appear only during mode changes.
- For visionOS 26+, handle comfort mitigation events and align your UI with the system’s mitigation choice.
