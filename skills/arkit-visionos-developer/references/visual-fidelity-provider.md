# VisualFidelityProvider

## Context

VisualFidelityProvider reports how well the device fits the wearer and lets you trade rendering fidelity for performance by constraining the foveated field of view. It publishes `VisualFidelityData` snapshots (device-fit status) and `FieldOfViewAnchor` updates (per-eye field-of-view polygons). New in visionOS 27. Beta API: names and shapes may change before release.

For shared session setup, authorization, and lifecycle rules, see [session-basics.md](session-basics.md). For model-layer reconciliation, see [anchor-processing.md](anchor-processing.md).

## Key API

- `VisualFidelityProvider(fieldOfView:requestDeviceFitUpdates:presentCoachingAlerts:)` — all parameters optional; pass a `FieldOfView` to constrain foveation, `requestDeviceFitUpdates: true` to receive fit status, and `presentCoachingAlerts: true` to let the system show fit coaching UI.
- `VisualFidelityProvider.FieldOfView` — presets `presetA` through `presetD`, or a custom `polygon(points: [simd_float2])`; check `isValid` before relying on a custom polygon.
- `fidelityDataUpdates` — async sequence of `VisualFidelityData` with `timestamp`, `deviceFitStatus`, and `isFieldOfViewValid`.
- `DeviceFitStatus` — `.valid`, `.eyesAbove`, `.eyesBelow`, `.eyesLeft`, `.eyesRight`.
- `anchorUpdates` — `FieldOfViewAnchor` updates with `leftPolygonPoints` and `rightPolygonPoints` (`[simd_float4]`) plus `originFromAnchorTransform`.

## Best Practices

- Check `VisualFidelityProvider.isSupported` before creating the provider.
- Request `requiredAuthorizations` before running the session and handle denied states.
- Pass `requestDeviceFitUpdates: true` only when you act on fit status; otherwise skip it to reduce noise.
- Prefer `presentCoachingAlerts: true` for system fit coaching unless you need custom UI driven by `deviceFitStatus`.
- Validate custom polygons with `FieldOfView.isValid` and watch `isFieldOfViewValid` in fidelity data updates.
- Shared session and lifecycle rules live in [session-basics.md](session-basics.md). Keep this file focused on provider-specific behavior.

## Code Examples

```swift
import ARKit

@MainActor
final class VisualFidelityModel {
    private let session = ARKitSession()
    private var provider: VisualFidelityProvider?

    func start() async {
        guard VisualFidelityProvider.isSupported else { return }
        let provider = VisualFidelityProvider(
            fieldOfView: .presetA,
            requestDeviceFitUpdates: true,
            presentCoachingAlerts: false
        )
        self.provider = provider

        let results = await session.requestAuthorization(for: VisualFidelityProvider.requiredAuthorizations)
        guard results.values.allSatisfy({ $0 == .allowed }) else { return }

        do {
            try await session.run([provider])
        } catch {
            print("Visual fidelity failed: \(error)")
            return
        }

        Task {
            for await data in provider.fidelityDataUpdates {
                handleFidelityData(data)
            }
        }

        Task {
            for await update in provider.anchorUpdates {
                switch update.event {
                case .added, .updated:
                    handleFieldOfViewAnchor(update.anchor)
                case .removed:
                    removeFieldOfViewAnchor(update.anchor.id)
                }
            }
        }
    }

    private func handleFidelityData(_ data: VisualFidelityData) {
        switch data.deviceFitStatus {
        case .valid:
            break
        case .eyesAbove, .eyesBelow, .eyesLeft, .eyesRight:
            // Show custom fit coaching, or rely on
            // presentCoachingAlerts: true instead.
            break
        @unknown default:
            break
        }
    }

    private func handleFieldOfViewAnchor(_ anchor: FieldOfViewAnchor) {}

    private func removeFieldOfViewAnchor(_ id: FieldOfViewAnchor.ID) {}
}
```
