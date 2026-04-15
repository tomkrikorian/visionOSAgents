# Modern Swift APIs

Use this file when the work is about style, API modernization, or safety.

## Swift-Native API Preferences

- Prefer Swift-native alternatives where they exist, such as
  `replacing("hello", with: "world")` over
  `replacingOccurrences(of: "hello", with: "world")` when semantics match.
- Prefer modern Foundation conveniences such as `URL.documentsDirectory` and
  `appending(path:)`.
- Prefer Swift concurrency over GCD for new async application code.

## Formatting And Presentation

- Avoid C-style formatting in SwiftUI text.

```swift
Text(abs(change), format: .number.precision(.fractionLength(2)))
```

- Prefer static member lookup over explicit style type construction where the
  API supports it, for example `.circle` and `.borderedProminent`.

## Text Matching

- Use `localizedStandardContains()` for user-facing text filtering instead of
  plain `contains()`.

## Safety Rules

- Avoid force unwraps and `try!` unless failure is intentionally unrecoverable.
- Do not hide logic changes inside "cleanup" commits that claim to be only API
  modernization.
