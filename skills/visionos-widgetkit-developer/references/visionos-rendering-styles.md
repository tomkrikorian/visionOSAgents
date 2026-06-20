# visionOS Widget Rendering Styles

Use this file when adapting WidgetKit widgets for Apple Vision Pro rendering,
families, backgrounds, and button controls.

## Families and Platforms

- Native visionOS widgets can use visionOS-specific families such as
  `WidgetFamily.systemExtraLargePortrait`.
- Compatible iOS/iPadOS widgets keep their compatible families, including
  `systemExtraLarge`.
- Branch family declarations by platform when a shared widget extension targets
  more than one platform.

## Rendering Modes and Backgrounds

- Read `widgetRenderingMode` from the environment when the view needs to adapt
  full-color versus accented rendering.
- Use `containerBackground(for: .widget)` so the system can remove or adapt
  backgrounds in contexts that require it.
- Read `showsWidgetContainerBackground` from the environment when content must
  adapt to a removed background.
- Do not encode essential state only in subtle background color, gradients, or
  material choices; rendering modes can transform or remove those layers.
- Mark decorative image layers deliberately for accented or full-color
  behavior.

## visionOS Surface Treatment

- Choose `widgetTexture(.glass)` for ambient glass-like widgets.
- Choose `widgetTexture(.paper)` for poster/document-like widgets.
- Verify both close and far readability; distance can expose text and contrast
  problems that previews miss.

## Interactive Controls

- Use `Link` or `widgetURL(_:)` for navigation into the app.
- Use `Button(intent:)` or `Toggle(intent:)` only for real `AppIntent` work.
- For custom button shapes, use the shared policy in
  [`buttons-and-controls.md`](../../spatial-swiftui-developer/references/buttons-and-controls.md).
