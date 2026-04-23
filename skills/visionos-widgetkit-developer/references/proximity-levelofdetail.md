# Proximity-aware layouts with LevelOfDetail

## Why this matters on Vision Pro

On visionOS, `LevelOfDetail` changes based on user proximity. You should assume:

- A small widget may be viewed from across a room.
- The system will animate between layouts when LoD changes.

## Implementation pattern

Use the environment value:

```swift
@Environment(\.levelOfDetail) private var levelOfDetail
```

Then branch your UI:

- `.default`: richer layout, more data density.
- `.simplified`: fewer elements, larger typography, stronger contrast.

Keep the two branches structurally compatible when possible. Large hierarchy
changes can make the system transition feel noisy as proximity changes.

```swift
var body: some View {
    switch levelOfDetail {
    case .simplified:
        CompactMetricView(entry: entry)
    default:
        DetailedMetricView(entry: entry)
    }
}
```

## Suggested heuristics

When `levelOfDetail == .simplified`:

- Increase primary text size (or choose fewer text elements).
- Prefer 1–2 key metrics over a dashboard.
- Replace small icons/labels with bold, single-purpose visuals.
- Avoid multi-column grids unless you can ensure readability.
- Keep controls obvious and sparse; distance mode is usually the wrong place
  for secondary actions.
- Validate text length with real localized content, not just placeholder
  English strings.

## Primary sources (Apple)

- Updating your widgets for visionOS (proximity section): https://developer.apple.com/documentation/widgetkit/updating-your-widgets-for-visionos
- `LevelOfDetail` docs: https://developer.apple.com/documentation/widgetkit/levelofdetail
