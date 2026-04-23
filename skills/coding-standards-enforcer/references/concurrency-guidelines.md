# Concurrency Guidelines

Use this file when the change touches actor isolation, `Sendable`, or async
execution structure.

## Core Mental Model

- `MainActor` owns UI-bound state and view-facing coordination.
- `actor` types own isolated mutable state that is not inherently UI-bound.
- `Sendable` marks values that can cross isolation domains safely.
- `nonisolated` code cannot reach back into isolated mutable state.

## Strict Concurrency Defaults

Swift 6.2 strict concurrency does not make arbitrary code `@MainActor` by
default. SwiftUI view `body` is `@MainActor`, and broader default isolation
depends on build settings such as `SWIFT_DEFAULT_ACTOR_ISOLATION`.

When diagnosing concurrency issues:

- Inspect the target's actual Swift language version and build settings before
  assuming default actor isolation.
- If `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` is enabled, still move CPU,
  file, network, or parsing work out of the main actor with explicit isolation
  such as a dedicated actor, a nonisolated helper, or `@concurrent` when the
  function can safely run off the caller's actor.
- If default main-actor isolation is not enabled, annotate UI-owned mutable
  state explicitly instead of relying on SwiftUI call sites to paper over the
  boundary.
- Treat every strict-concurrency warning as a design question first: what owns
  the mutable state, and what crosses an isolation boundary?

## Preferred Async Structure

Use structured concurrency first:

```swift
async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
let profile = Profile(avatar: try await avatar, banner: try await banner)
```

Use task groups when you need dynamic fan-out:

```swift
let values = try await withThrowingTaskGroup(
    of: (String, String).self,
    returning: [String: String].self
) { group in
    group.addTask { ("avatarURL", try await fetchAvatarURL()) }
    group.addTask { ("bio", try await fetchBioText()) }

    var collected: [String: String] = [:]
    for try await (key, value) in group {
        collected[key] = value
    }
    return collected
}
```

Use unstructured `Task {}` only when the lifecycle is genuinely tied to the
current actor or view.

## Isolation Choices

```swift
@MainActor
final class ViewModel {
    var items: [Item] = []
}

actor BankAccount {
    var balance: Double = 0
    func deposit(_ amount: Double) { balance += amount }
}
```

- Choose `@MainActor` when a type owns UI-facing mutable state.
- Choose a dedicated `actor` when the state is shared or background-oriented.
- Prefer annotating the owning type or function instead of sprinkling
  `MainActor.run`.
- Use `nonisolated` only for members that do not need isolated mutable state.
- Use `@concurrent` for async functions that should not inherit the caller's
  actor, after confirming captured values are safe to cross isolation.

## Approachable Concurrency Settings

- `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` keeps UI code on the main actor
  by default.
- `SWIFT_APPROACHABLE_CONCURRENCY = YES` enables migration aids such as outward
  actor inference and inferred sendability changes.

```swift
@concurrent func processLargeFile() async { }
```

## Sendable Guidance

```swift
struct User: Sendable {
    let id: Int
    let name: String
}

final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]
}
```

- Prefer value types or immutable reference types for `Sendable` data.
- Use `@unchecked Sendable` only when you can explain and defend the safety.
- Do not capture non-`Sendable` reference types in detached or concurrent work
  just to quiet a diagnostic. Move the operation behind an actor, snapshot the
  required value data, or make the type genuinely thread-safe.

## Common Mistakes

- Treating `async` as automatic background execution.
- Replacing structure with `Task.detached` too early.
- Blocking async code with semaphores or `DispatchGroup.wait()`.
- Creating actors when a simple `@MainActor` owner is enough.
- Forgetting to cancel long-lived tasks on teardown.
- Adding broad `@MainActor` to services or data models that should run
  independently of UI state.
