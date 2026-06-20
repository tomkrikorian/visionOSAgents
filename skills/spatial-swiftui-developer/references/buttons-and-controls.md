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

## Hover Effect Shape

The gaze hover highlight has its own shape, separate from the visual
background. Get it from the right lever:

**Buttons (any style, including `.plain` and `.borderless`):** the button's
built-in hover effect takes its shape from `.buttonBorderShape(...)`, not from
`contentShape`. Adding `.contentShape(.hoverEffect, ...)` or an extra
`.hoverEffect()` outside a `Button` does NOT reshape the button's own
highlight — it leaves the system default (an oversized rounded rectangle) and
the mismatch reads as broken polish. The card recipe is:

```swift
Button(action: select) {
    cardContent
        .padding(16)
}
.buttonStyle(.borderless)
.buttonBorderShape(.roundedRectangle(radius: 20))
.background(.regularMaterial, in: RoundedRectangle(cornerRadius: 20))
```

Keep the border-shape radius and the background radius in lockstep; when one
changes, change both.

**Non-button hover surfaces** (custom views that opt in with
`.hoverEffect()`): pin the highlight to the visual shape with
`.contentShape(.hoverEffect, ...)` placed before `.hoverEffect()`:

```swift
customSurface
    .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 20))
    .contentShape(.hoverEffect, .rect(cornerRadius: 20))
    .hoverEffect()
```

Match the shape kind exactly in both cases: `.roundedRectangle(radius:)` /
`.rect(cornerRadius:)` against a `RoundedRectangle` background, `.capsule`
against a capsule, `.circle` against a circular control.

## Implementation Checklist

- Pick the button style and border shape together.
- For `.buttonStyle(.bordered)` and `.buttonStyle(.borderedProminent)`, add
  `.buttonBorderShape(...)` whenever the desired shape is not the system
  default.
- For card-like buttons with custom backgrounds, set
  `.buttonBorderShape(.roundedRectangle(radius:))` matching the background
  radius — that is what shapes the button's hover highlight.
- For non-button hover surfaces, pair `.hoverEffect()` with a
  `.contentShape(.hoverEffect, ...)` that matches the background shape.
- Check toolbar items, account/profile actions, destructive actions, share
  actions, onboarding controls, and settings forms.
- Include `NavigationLink` and `ShareLink` in the same audit as `Button`.
- For widgets, apply the same shape rule to interactive `Button(intent:)`
  controls.
- Verify text and icon content still fits after the shape is applied.

## Review Probe

Use a code search like this during review, then inspect each visible call site:

```bash
rg "Button\\b|NavigationLink|ShareLink|buttonBorderShape|hoverEffect|contentShape" .
```

Controls that are invisible, preview-only, or not presented as a button can be
excluded, but the reason should be clear from the surrounding code.
