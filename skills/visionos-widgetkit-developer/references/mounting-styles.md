# Mounting styles (elevated vs recessed)

## Mental model

On visionOS, widgets sit on top of surfaces by default (elevated). On vertical surfaces, widgets can also appear recessed (embedded into a wall-like portal).

This has practical implications:

- Background treatments can look very different in recessed mode.
- Any “depth illusion” design might only work when recessed.
- If your widget only supports recessed, users can’t place it on horizontal surfaces.

## Implementation

Configure mounting support using `supportedMountingStyles` on your widget configuration:

```swift
.supportedMountingStyles([.elevated, .recessed])
```

Or restrict it:

```swift
.supportedMountingStyles([.recessed])
```

## Design guidance (pragmatic)

- If your widget includes imagery intended to align like a “window,” consider recessed-only.
- Avoid small “chrome” elements at the edges; recessed mode can make borders feel cramped.
- Test both styles early: it’s easy to design an elevated widget that looks broken recessed.

## Primary sources (Apple)

- Updating your widgets for visionOS (mounting styles section): https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- `WidgetMountingStyle`: https://developer.apple.com/documentation/widgetkit/widgetmountingstyle

