# visionOS: SharePlay Group Immersive Space (Launch Only)

Use this recipe when you want participants to join the same immersive space (spatially coordinated) but you are not yet synchronizing any entities, state, or interactions.

## Minimum requirements

1. Entitlements/capabilities:
   - Enable Group Activities capability.
   - Ensure `com.apple.developer.group-session = true` is present.
2. Define a `GroupActivity` for the experience.
3. Observe sessions and configure `SystemCoordinator` before `join()`.
4. Set `.immersiveEnvironmentBehavior(.coexist)` on the `ImmersiveSpace` scene.

## GroupActivity

```swift
import CoreTransferable
import GroupActivities

struct MyImmersiveActivity: GroupActivity, Transferable, Sendable {
    static let activityIdentifier = "com.example.myapp.immersive"

    var metadata: GroupActivityMetadata {
        var metadata = GroupActivityMetadata()
        metadata.type = .generic
        metadata.title = "My Immersive Session"
        metadata.subtitle = "Join the space together"
        return metadata
    }

    static var transferRepresentation: some TransferRepresentation {
        GroupActivityTransferRepresentation { _ in
            MyImmersiveActivity()
        }
    }
}
```

## Session manager (observe, configure, join)

Keep the manager `@MainActor` and hold strong references to the session and messenger/journal (even if you are not using messenger yet).

```swift
import Combine
import GroupActivities
import Observation

@MainActor
@Observable
final class SharePlayManager {
    private var sessionTask: Task<Void, Never>?
    private var sessionStateCancellable: AnyCancellable?
    private var session: GroupSession<MyImmersiveActivity>?

    func start() {
        guard sessionTask == nil else { return }
        sessionTask = Task { [weak self] in
            for await session in MyImmersiveActivity.sessions() {
                await self?.configure(session)
            }
        }
    }

    func stop() {
        session?.leave()
        session = nil
        sessionStateCancellable?.cancel()
        sessionStateCancellable = nil
        sessionTask?.cancel()
        sessionTask = nil
    }

    private func configure(_ session: GroupSession<MyImmersiveActivity>) async {
        self.session = session

        if let coordinator = await session.systemCoordinator {
            var config = SystemCoordinator.Configuration()
            config.supportsGroupImmersiveSpace = true
            config.spatialTemplatePreference = .sideBySide
            coordinator.configuration = config
        }

        sessionStateCancellable?.cancel()
        sessionStateCancellable = session.$state.sink { [weak self] state in
            guard let self else { return }
            if case .invalidated = state {
                self.session = nil
                self.sessionStateCancellable?.cancel()
                self.sessionStateCancellable = nil
            }
        }

        session.join()
    }
}
```

## ImmersiveSpace scene requirements

```swift
ImmersiveSpace(id: "ImmersiveSpace") {
    ImmersiveView()
}
.immersiveEnvironmentBehavior(.coexist)
```

## Notes

- `SystemCoordinator.Configuration` must be set before `join()` for the system to spatially coordinate the session.
- `.sideBySide` is a safe default for “shared viewpoint” collaboration; you can choose another template later.
- This recipe intentionally does not send any messages or journals; add that once you need actual shared state.

