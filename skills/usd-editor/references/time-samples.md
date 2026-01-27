# Time Samples

Use this when working with animated or time-varying properties.

## Basic Time Samples

Author time samples on a property using `timeSamples`:

```usda
float opacity.timeSamples = {
    0: 0.0,
    1: 1.0
}
```

## Guidance

- Keep sample times consistent with existing animation timing.
- Preserve the property type when editing values.
- Avoid changing stage-wide timing metadata unless required.

```usda
(
    timeCodesPerSecond = 24
)
```
