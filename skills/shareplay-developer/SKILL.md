---
name: shareplay-developer
description: Build, integrate, and troubleshoot SharePlay GroupActivities features for visionOS 26, including GroupActivity definitions, activation flows, GroupSession lifecycle, messaging and journals, ShareLink and SharePlay UI surfaces, and spatial coordination.
---

# SharePlay Developer

## Quick Start

1. Decide whether this experience is launch-only co-location or shared state sync.
2. Add the Group Activities capability and the required entitlement before you build any UI around the session.
3. Define one `GroupActivity` per experience and keep the payload minimal and `Codable`.
4. Load the right reference only after you know the workflow:
   - `visionos-immersive-space.md` for same-space immersive experiences without sync
   - `activation-ui.md` for activation and start-button flow
   - `REFERENCE.md` for GroupActivities patterns and examples
5. Configure `SystemCoordinator` before joining whenever spatial personas or immersive spaces are involved.
6. If the issue is app launch, test flow, simulator behavior, or signing, switch to the plugin's `build-run-debug` workflow skill.

## Tracks

### Launch-Only Same Space

Use this track when participants should enter the same immersive space, but you do not need live state sync yet.

- Define lightweight `GroupActivity` metadata.
- Set `supportsGroupImmersiveSpace = true` when the session should coordinate a group immersive experience.
- Use `.immersiveEnvironmentBehavior(.coexist)` only when the system immersive environment should remain visible.
- Call `join()` only after the session has been configured and the UI is ready.

### Shared State Sync

Use this track when participants must share state, messages, or durable data.

- Keep session payloads minimal.
- Use `GroupSessionMessenger` for transient events.
- Use `GroupSessionJournal` for durable shared objects.
- Send a state snapshot when participants change so late joiners catch up.

### Start Surface

Use this track when you are deciding how the user starts SharePlay.

- Use `activate()` when FaceTime is active and the app should join that call.
- Use `ShareLink` or `GroupActivitySharingController` when the user needs an explicit sharing surface.
- Use `GroupActivityTransferRepresentation` only when the activity should be startable from transferable surfaces.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When you need GroupActivities-focused patterns and examples. |
| [`visionos-immersive-space.md`](references/visionos-immersive-space.md) | When implementing launch-only SharePlay for a visionOS immersive space. |
| [`activation-ui.md`](references/activation-ui.md) | When wiring the SharePlay entry point or start button flow. |

## Guardrails

- Keep `GroupActivity` data small and `Codable`.
- Store strong references to `GroupSession`, `GroupSessionMessenger`, and `GroupSessionJournal`.
- Configure `SystemCoordinator` before `join()` when using spatial coordination.
- Do not treat `.immersiveEnvironmentBehavior(.coexist)` as the coordination API.
- Join only after the UI and local state are ready.
- Route launch, test, or debugging problems to the plugin's `build-run-debug` workflow skill instead of expanding this skill with execution steps.

## Information About the Skill

### Core Concepts

#### Activity Definition

- Use `GroupActivity` to define the shareable experience and keep payloads minimal.
- Provide `GroupActivity.metadata` with title, subtitle, preview image, and fallback URL.
- Set `GroupActivityMetadata.type` to a matching `ActivityType` value.
- Use `GroupActivityActivationResult` from `prepareForActivation()` to decide activation.
- Use `GroupActivityTransferRepresentation` when starting the activity from `ShareLink`, a share sheet, or another transferable surface.

#### Session Lifecycle and Participants

- Use `GroupSession` to manage the live activity; call `join()`, `leave()`, or `end()`.
- Observe `GroupSession.state`, `activeParticipants`, and `isLocallyInitiated` to drive UI.
- Use `View.groupActivityAssociation(_:)` and `GroupActivityAssociationInteraction` to tie a SwiftUI scene to the active session instead of hard-coding scene identifiers.
- Call `GroupSession.requestForegroundPresentation()` when the activity needs the app visible.
- Use `GroupSession.postEvent(_:)` for transient session-wide notices such as playback state changes (no system-level `showNotice` API exists on visionOS).

#### Messaging and Transfer

- Use `GroupSessionMessenger` for time-sensitive messages and state changes.
- Use `.reliable` delivery for critical state and `.unreliable` for high-frequency updates.
- Use `GroupSessionJournal` for attachments and other data objects that should remain available to current and later participants.

#### UI Surfaces to Start SharePlay

- Use `ShareLink` with `Transferable` + `GroupActivityTransferRepresentation` in SwiftUI.
- Use `GroupActivitySharingController` in UIKit when no FaceTime call is active.
- Use `NSItemProvider.registerGroupActivity(...)` in share sheets when needed.

#### visionOS Spatial Coordination

- Use `SystemCoordinator` from `GroupSession.systemCoordinator` (async property) for spatial layout.
- Set `spatialTemplatePreference` and `supportsGroupImmersiveSpace` on `SystemCoordinator.Configuration` before join.
- Use `localParticipantStates` and `remoteParticipantStates` to track poses.
- Use `View.groupActivityAssociation(_:)` and `GroupActivityAssociationInteraction` to associate a SwiftUI scene with the session instead of hard-coding scene identifiers.
- On visionOS 26, iterate `SystemCoordinator.groupImmersionStyle` (an `AsyncSequence` of `SystemCoordinator.GroupImmersionStyles` values) to react when the group immersion style changes and align the local immersive experience with remote participants.
- For immersive spaces, use `Scene.immersiveEnvironmentBehavior(.coexist)` only when you want the system immersive environment to remain visible; participant co-location comes from `SystemCoordinator` configuration, not from the environment behavior modifier.

### Reference Files

| Reference                                 | When to Use                                                         |
| ----------------------------------------- | ------------------------------------------------------------------- |
| [`REFERENCE.md`](references/REFERENCE.md) | When you need GroupActivities-focused patterns and examples. |
| [`visionos-immersive-space.md`](references/visionos-immersive-space.md) | When implementing launch-only SharePlay for a visionOS immersive space. |
| [`activation-ui.md`](references/activation-ui.md) | When wiring the SharePlay entry point or start button flow. |

### Implementation Patterns

- Send a full state snapshot when new participants join.
- Keep UI state separate from shared game state to reduce message churn.
- Use `GroupSessionMessenger` for transient actions and `GroupSessionJournal` for durable data.
- Prefer AVFoundation coordinated playback for media sync.

### Pitfalls and Checks

- Keep `GroupActivity` data minimal; send state changes via messenger or journal.
- Store strong references to `GroupSession`, `GroupSessionMessenger`, and `GroupSessionJournal`.
- Join only when UI and state are ready; call `leave()` on teardown.
- Handle late joiners by sending the current state snapshot on `activeParticipants` change.
- For visionOS group immersive space: if participants don't colocate, verify `supportsGroupImmersiveSpace`, the selected spatial template, and that `SystemCoordinator` is configured before `join()`.
