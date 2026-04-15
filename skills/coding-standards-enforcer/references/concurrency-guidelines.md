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

## Common Mistakes

- Treating `async` as automatic background execution.
- Replacing structure with `Task.detached` too early.
- Blocking async code with semaphores or `DispatchGroup.wait()`.
- Creating actors when a simple `@MainActor` owner is enough.
- Forgetting to cancel long-lived tasks on teardown.
