# VideoPlayerComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/videoplayercomponent)

## Overview

A component that embeds video playback within RealityKit entities using immersive- and spatial-aware video rendering. It's ideal for visionOS immersive media experiences, supporting multiple immersive viewing modes for various video profiles including Apple Projected Media Profile (APMP), Apple Immersive Video, stereo, and spatial video.

## When to Use

- Playing video content in 3D space
- Creating immersive video experiences on visionOS
- Displaying spatial or stereo video content
- Implementing video players in immersive spaces
- Creating media viewing experiences
- Playing Apple Immersive Video content

## How to Use

### Basic Setup

```swift
import RealityKit
import AVFoundation

// Create AVPlayer
let player = AVPlayer(playerItem: AVPlayerItem(url: videoURL))

// Create video player component
var videoComponent = VideoPlayerComponent(avPlayer: player)
videoComponent.desiredImmersiveViewingMode = .portal
videoComponent.desiredViewingMode = .stereo

entity.components.set(videoComponent)
```

### Immersive Video

```swift
// Configure for immersive viewing
var videoComponent = VideoPlayerComponent(avPlayer: player)
videoComponent.desiredImmersiveViewingMode = .full
videoComponent.desiredViewingMode = .spatial
entity.components.set(videoComponent)
```

### Spatial Video

```swift
// Configure for spatial video with styling
var videoComponent = VideoPlayerComponent(avPlayer: player)
videoComponent.desiredSpatialVideoMode = .spatial
videoComponent.desiredImmersiveViewingMode = .progressive
entity.components.set(videoComponent)
```

## Key Properties

- `avPlayer: AVPlayer` - The AVPlayer instance for video playback
- `desiredViewingMode: VideoPlayerComponent.ViewingMode` - Desired viewing mode (read-only after setting)
- `desiredImmersiveViewingMode: VideoPlayerComponent.ImmersiveViewingMode` - Desired immersive viewing mode
- `desiredSpatialVideoMode: VideoPlayerComponent.SpatialVideoMode` - Desired spatial video mode

### Viewing Modes

- `.mono` - Standard mono video
- `.stereo` - Stereo video
- `.spatial` - Spatial video

### Immersive Viewing Modes

- `.portal` - Portal viewing mode
- `.progressive` - Progressive immersive viewing
- `.full` - Full immersive viewing

## Important Notes

- The component creates its own mesh and material to display video
- Default mesh height is 1 meter - scale uniformly to maintain aspect ratio
- Clipping or size issues may occur if video is larger than the window scene
- Supports comfort mitigations - automatic adjustments for high motion content
- Available on visionOS and other Apple platforms
- Introduced in WWDC 2025
- Works with AVPlayer and AVPlayerItem for video playback

## Best Practices

- Set appropriate viewing mode for your video content type
- Use immersive viewing modes for spatial or immersive video
- Scale the entity uniformly to maintain video aspect ratio
- Test video playback on target devices
- Consider comfort mitigations for high motion content
- Handle video loading and playback states appropriately
- Use appropriate immersive viewing mode for your experience type

## Related Components

- `ImagePresentationComponent` - For displaying images in 3D space
- `PresentationComponent` - For SwiftUI modal presentations
- `ModelComponent` - Alternative for video textures (less immersive)
