# Coding Standards Reference Map

Load this file first when the work spans multiple standards areas or when you
need the review order before diving into a narrower topic.

## Review Order

1. Resolve compiler and strict-concurrency diagnostics first.
2. Confirm ownership and isolation boundaries.
3. Check observation and state-model choices.
4. Modernize APIs and style only after behavior is stable.
5. Re-run the smallest relevant build or test scope.

## Topic Routing

- Use [concurrency-guidelines.md](concurrency-guidelines.md) for actor
  isolation, `Sendable`, `Task`, `async let`, task groups, and strict
  concurrency migration.
- Use [observation-modeling.md](observation-modeling.md) for `@Observable`,
  view-model ownership, state placement, and Combine migration.
- Use [modern-swift-apis.md](modern-swift-apis.md) for Swift-native APIs,
  Foundation modernization, formatting, filtering, and force-unwrap policy.

## Repo-Level Expectations

- Favor Swift concurrency over GCD for new asynchronous application code.
- Verify Swift 6.2 language mode and default-actor-isolation build settings
  before choosing an isolation fix.
- Keep UI-owned mutable state on the main actor when it truly owns UI behavior.
- Use Observation in new SwiftUI code; treat new `ObservableObject`,
  `@StateObject`, and `@ObservedObject` usage as a standards violation unless a
  concrete compatibility blocker is documented.
- Treat `@StateObject` or `@ObservedObject` around an `@Observable` model as a
  standards violation; use `@State`, `@Bindable`, or typed environment instead.
- Treat force unwraps, `try!`, and `@unchecked Sendable` as exceptions that
  require a strong justification.
- For visionOS SwiftUI surfaces, audit visible `Button`, button-like
  `NavigationLink`, `ShareLink`, and widget AppIntent button usage for an
  intentional `.buttonBorderShape(...)`; see
  [buttons-and-controls.md](../../spatial-swiftui-developer/references/buttons-and-controls.md).
