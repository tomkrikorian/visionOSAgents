# Group Session Lifecycle

Use this file when joining, observing, or presenting a SharePlay session.

## What To Track

- `GroupSession.state`
- `activeParticipants`
- `isLocallyInitiated`
- foreground presentation needs

## Lifecycle Order

1. Observe `YourActivity.sessions()` from a long-lived task owned by app or
   scene state.
2. For each new session, build a session controller that holds strong
   references to `GroupSession`, `GroupSessionMessenger`, `GroupSessionJournal`,
   and any observation tasks.
3. Prepare local UI and local state before joining; if the activity is spatial,
   await `session.systemCoordinator` and configure it before `join()`.
4. Start state, participant, messenger, and journal observers before joining so
   no early updates are missed.
5. Call `session.join()` once per accepted session.
6. On `.invalidated`, cancel observation tasks, clear strong references, and
   reset local shared-state affordances.

## Rules

- Configure the session before `join()`.
- Join only after the UI and local state are ready.
- Call `leave()` when the local user leaves the activity UI.
- Call `end()` only when the action should end the activity for all
  participants.
- Do not call `leave()` or `end()` after the session is already invalidated.
- Use `View.groupActivityAssociation(_:)` and
  `GroupActivityAssociationInteraction` when tying a SwiftUI scene to the
  active session.
