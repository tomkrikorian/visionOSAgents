# Textures and rendering (glass, paper, accented)

## Widget textures

Widgets offered by a visionOS app can specify a texture for the widget’s coating layer:

- `.glass` — reflective, glass-like coating.
- `.paper` — matte, poster-like coating.

Use:

```swift
.widgetTexture(.glass) // or .paper
```

## Practical guidance

- **Glass**: treat backgrounds and contrast carefully; avoid “busy” visuals behind small text.
- **Paper**: works well for poster-like visuals; consider larger typography and bolder imagery.

## Accented rendering / user color themes

People can customize widgets with color themes and rendering modes (for example, an “accented” appearance). Ensure your widget still reads well when backgrounds are removed or simplified.

Practical checks:

- Verify primary text remains legible in high-contrast themes.
- Avoid relying on subtle gradients for information hierarchy.
- Confirm important affordances still read when your background is replaced.

## Primary sources (Apple)

- WidgetKit updates (Vision Pro + Liquid Glass notes): https://developer.apple.com/documentation/updates/widgetkit
- `WidgetTexture`: https://developer.apple.com/documentation/widgetkit/widgettexture
