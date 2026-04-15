# APMP And Spatial Video

Use this file when the content is more than flat video.

## APMP

Apple Projected Media Profile (APMP) is the visionOS profile for projected and
immersive video content. Use
`AVAssetPlaybackConfigurationOption.appleImmersiveVideo` when the asset should
play as Apple immersive video.

## Spatial Video

Spatial video on Apple Vision Pro uses MV-HEVC. Use
`VideoPlayerComponent.spatialVideoMode` when the source supports stereo output.

Progressive mode does not apply to standard spatial video the same way it does
to immersive media experiences.
