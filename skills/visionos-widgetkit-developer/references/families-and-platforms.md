# Families And Platforms

Use this file when deciding which widget families are valid on visionOS.

## Rules

- Native visionOS widgets use visionOS-supported system families and should be
  declared explicitly with `supportedFamilies(_:)`.
- For extra-large Vision Pro widgets, use
  `WidgetFamily.systemExtraLargePortrait`.
- Compatible iOS apps running on visionOS should continue to use
  `systemExtraLarge`.
- Do not use `.systemLarge` as a substitute for the Vision Pro extra-large
  portrait family. It is a large family, not the extra-large visionOS form.
- If a widget extension is shared across native visionOS and compatible
  iOS/iPadOS targets, branch the family list by target instead of applying the
  same extra-large family everywhere.

StandBy and watch complications do not apply on visionOS.

## Native Vision Pro Checklist

- Confirm the target is a native visionOS widget extension before selecting
  `.systemExtraLargePortrait`.
- Test every declared family in both distance states; a good small layout is
  rarely a good extra-large portrait layout with only scale changes.
- Keep family-specific view branches small and data-compatible so the timeline
  entry type remains shared.

## Primary sources (Apple)

- Updating your widgets for visionOS: https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- `WidgetFamily.systemExtraLargePortrait`: https://developer.apple.com/documentation/widgetkit/widgetfamily/systemextralargeportrait
