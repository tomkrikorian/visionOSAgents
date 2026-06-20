# Comfort mitigation

## What the system can report

RealityKit reports video comfort mitigation actions via:

- `VideoPlayerEvents.VideoComfortMitigationDidOccur`

The `comfortMitigation` value can indicate actions like:

- pause playback
- reduce immersion
- continue playback

## Best practices

- Treat mitigation as a UX event: update UI immediately so the user understands what happened.
- If immersion is reduced, provide a clear path to continue in portal/lower immersion.
- Don’t fight the system: align your experience with what the system is doing to keep users comfortable.
