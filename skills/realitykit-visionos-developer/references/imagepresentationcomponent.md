# ImagePresentationComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/imagepresentationcomponent)

## Overview

A component that displays images in 3D space using three types: standard 2D images/photos, spatial photos, and spatial scenes. Spatial scenes are generated from 2D or spatial photos into 3D geometry offering motion parallax, creating immersive viewing experiences. The component supports multiple viewing modes for different rendering styles.

## When to Use

- Displaying photos or images in 3D space
- Presenting spatial photos with depth information
- Creating immersive image viewing experiences
- Displaying spatial scenes with motion parallax
- Showing images in visionOS immersive spaces
- Creating photo galleries or image viewers in 3D

## How to Use

### Basic Setup

```swift
import RealityKit

// Load image from URL
let component = try await ImagePresentationComponent(contentsOf: imageURL)
entity.components.set(component)
```

### With Viewing Mode

```swift
// Create component and set viewing mode
let component = try await ImagePresentationComponent(contentsOf: imageURL)
component.desiredViewingMode = .spatialStereoImmersive
entity.components.set(component)
```

### Spatial Scene Generation

```swift
// Generate spatial scene from image
let component = try await ImagePresentationComponent(contentsOf: imageURL)

// Generate spatial scene (async operation)
let spatialScene = try await Spatial3DImage.generate(from: imageURL)

// Set viewing mode to spatial scene
component.desiredViewingMode = .spatial3DImmersive
entity.components.set(component)
```

### With Spatial3DImage

```swift
// Create from Spatial3DImage instance
let spatialImage = Spatial3DImage(...)
let component = ImagePresentationComponent(spatialImage: spatialImage)
component.desiredViewingMode = .spatial3DImmersive
entity.components.set(component)
```

## Key Properties

- `desiredViewingMode: ImagePresentationComponent.ViewingMode` - The desired viewing mode for the image

### Viewing Modes

- `.mono` - Standard 2D image display
- `.spatial3D` - Spatial 3D viewing
- `.spatial3DImmersive` - Immersive spatial 3D viewing
- `.spatialStereo` - Stereo spatial viewing
- `.spatialStereoImmersive` - Immersive stereo spatial viewing

## Important Notes

- Supports standard 2D images, spatial photos, and spatial scenes
- Spatial scenes are generated from images and provide motion parallax
- If you choose a spatial scene mode before generation, the component shows a progress UI
- Available viewing modes depend on the image type and generation status
- Introduced in recent RealityKit updates (WWDC 2025)
- Available on visionOS and other Apple platforms

## Best Practices

- Use appropriate viewing mode for your image type
- Generate spatial scenes for immersive experiences
- Handle loading states when generating spatial scenes
- Test viewing modes on target devices
- Consider user comfort when using immersive modes
- Use spatial images for best immersive experience
- Load images asynchronously to avoid blocking

## Related Components

- `VideoPlayerComponent` - For video playback in 3D space
- `PresentationComponent` - For SwiftUI modal presentations
- `ModelComponent` - Alternative for displaying images as textures
