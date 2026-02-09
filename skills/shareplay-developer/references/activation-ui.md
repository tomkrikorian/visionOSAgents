# SharePlay Activation UI (Start Button Patterns)

SharePlay activation has two practical branches:

1. A FaceTime call is active and the system prefers direct activation.
2. No eligible call is active, so you must present a share sheet to start one.

## Pattern: SwiftUI button + `prepareForActivation()`

```swift
import GroupActivities
import SwiftUI

struct StartSharePlayButton: View {
    @State private var isPresentingShareSheet = false
    @State private var pendingActivity: MyImmersiveActivity?

    var body: some View {
        Button("Start SharePlay") {
            Task { @MainActor in
                await start()
            }
        }
        .sheet(isPresented: $isPresentingShareSheet) {
            if let activity = pendingActivity {
                SharePlaySharingSheet(activity: activity)
            }
        }
    }

    @MainActor
    private func start() async {
        let activity = MyImmersiveActivity()
        let result = await activity.prepareForActivation()

        switch result {
        case .activationPreferred:
            _ = try? await activity.activate()
        case .activationDisabled:
            pendingActivity = activity
            isPresentingShareSheet = true
        case .cancelled:
            break
        @unknown default:
            break
        }
    }
}
```

## Pattern: UIKit share sheet wrapper (`GroupActivitySharingController`)

Use this in a `.sheet` when activation is disabled (no active FaceTime call) so the user can invite others.

```swift
import GroupActivities
import SwiftUI
import UIKit

struct SharePlaySharingSheet: UIViewControllerRepresentable {
    let activity: MyImmersiveActivity

    func makeUIViewController(context: Context) -> UIViewController {
        (try? GroupActivitySharingController(activity)) ?? UIViewController()
    }

    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {
        _ = uiViewController
    }
}
```

## Notes

- `prepareForActivation()` is usually the simplest decision point for a Start button.
- `GroupStateObserver.isEligibleForGroupSession` can be used for gating, but you still need the share sheet fallback when activation is disabled.

