# Buttons and Controls

Use this file when implementing visible SwiftUI controls in a visionOS window,
volume, ornament, toolbar, form, or spatial attachment.

## Button Shape Policy

Every visible button-like control in visionOS SwiftUI should make its shape
intentional with `.buttonBorderShape(...)`.

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
the custom background or component name. Do not leave the shape accidental.

## Implementation Checklist

- Pick the button style and border shape together.
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
