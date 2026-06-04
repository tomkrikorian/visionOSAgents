# Buttons and Controls

Use this file when implementing visible SwiftUI controls in a visionOS window,
volume, ornament, toolbar, form, or spatial attachment.

## Button Shape Policy

Native visionOS toolbar icon actions should use a semantic `Label` and hide
only the visible title:

```swift
Button {
    importPackage()
} label: {
    Label("Import Package", systemImage: "square.and.arrow.down")
        .labelStyle(.iconOnly)
}
```

This keeps the title available to accessibility and lets visionOS synthesize
the expected round toolbar button. Do not use a bare `Image(systemName:)` for
icon-only toolbar actions, and do not add a manual border shape unless the
control is outside the native toolbar treatment.

Every visible button-like control outside native toolbar slots should make its
shape intentional with `.buttonBorderShape(...)`. When a visionOS button needs
a custom control outline, use SwiftUI's `buttonBorderShape(_:)` API instead of
trying to create the button shape with `clipShape`, `cornerRadius`, or only a
custom background.

Apply the rule to:

- `Button`
- `NavigationLink` when it is visually presented as a button
- `ShareLink`
- App-intent-backed widget `Button` controls
- custom reusable controls whose root interaction is button-like

Use `.circle` for icon-only buttons, compact toolbar actions, and controls where
the hit target is visually circular. Use `.capsule` for short text actions that
should read as pills. Use `.roundedRectangle(radius:)` for wider rows, form
actions, and rectangular controls that should align with the surrounding surface
radius.

If a control uses `.buttonStyle(.plain)` because the entire row, card, or
custom surface owns the visual treatment, keep the shape decision explicit in
the custom background or component name. Do not leave the shape accidental, and
do not use `.plain` as a workaround for a missing `buttonBorderShape(_:)` on a
bordered visionOS button.

## Implementation Checklist

- Pick the button style and border shape together.
- For `.buttonStyle(.bordered)` and `.buttonStyle(.borderedProminent)`, add
  `.buttonBorderShape(...)` whenever the desired shape is not the system
  default.
- Check toolbar items, account/profile actions, destructive actions, share
  actions, onboarding controls, and settings forms.
- Include `NavigationLink` and `ShareLink` in the same audit as `Button`.
- For widgets, apply the same shape rule to interactive `Button(intent:)`
  controls.
- Verify text and icon content still fits after the shape is applied.

## Review Probe

Use a code search like this during review, then inspect each visible call site:

```bash
rg "Button\\b|NavigationLink|ShareLink|buttonBorderShape" .
```

Controls that are invisible, preview-only, or not presented as a button can be
excluded, but the reason should be clear from the surrounding code.
