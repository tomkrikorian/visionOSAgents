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

Read the rendering mode from the environment when the view needs different
treatments:

```swift
@Environment(\.widgetRenderingMode) private var widgetRenderingMode
```

Practical checks:

- Verify primary text remains legible in high-contrast themes.
- Avoid relying on subtle gradients for information hierarchy.
- Confirm important affordances still read when your background is replaced.
- Mark image and decorative layers deliberately for accented or full-color
  rendering instead of assuming the system preserves the original artwork.
- Test the widget with realistic wallpaper, surface, and distance conditions;
  a texture that works in the preview canvas can fail on a vertical wall.

## Texture Choice

- Choose `.glass` when the widget should feel ambient and lightweight.
- Choose `.paper` when the content behaves more like a poster, document, or
  art board and needs a matte coating.
- Avoid encoding essential state purely in material or background color because
  rendering modes can transform both.

## Primary sources (Apple)

- WidgetKit updates (Vision Pro + Liquid Glass notes): https://developer.apple.com/documentation/updates/widgetkit
- `WidgetTexture`: https://developer.apple.com/documentation/widgetkit/widgettexture
- Optimizing your widget for accented rendering mode and Liquid Glass: https://developer.apple.com/documentation/widgetkit/optimizing-your-widget-for-accented-rendering-mode-and-liquid-glass
- `WidgetRenderingMode`: https://developer.apple.com/documentation/widgetkit/widgetrenderingmode
