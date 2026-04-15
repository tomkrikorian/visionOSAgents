# Group Session Lifecycle

Use this file when joining, observing, or presenting a SharePlay session.

## What To Track

- `GroupSession.state`
- `activeParticipants`
- `isLocallyInitiated`
- foreground presentation needs

## Rules

- Configure the session before `join()`.
- Join only after the UI and local state are ready.
- Call `leave()` or `end()` deliberately on teardown.
- Use `View.groupActivityAssociation(_:)` and
  `GroupActivityAssociationInteraction` when tying a SwiftUI scene to the
  active session.
