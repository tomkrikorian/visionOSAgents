# GroupActivities Patterns

Use this reference for the small set of SharePlay decisions that usually matter
before opening sample code. If the task needs complete sample excerpts, use
[`../samples/groupactivities-samples.md`](../samples/groupactivities-samples.md).

## Pattern Map

| Pattern | Use |
|---|---|
| Launch-only co-location | Configure `SystemCoordinator` for group immersive-space presence, then join without adding state sync. Load `visionos-immersive-space.md` and `spatial-coordination.md`. |
| Shared lightweight state | Define one small `GroupActivity` payload and use `GroupSessionMessenger` for short-lived state updates. Load `activity-definition.md`, `group-session-lifecycle.md`, and `messaging-journal.md`. |
| Late-joiner recovery | Use `GroupSessionJournal` or a compact snapshot message so new participants can reconstruct state. Load `messaging-journal.md`. |
| Share sheet fallback | Use `prepareForActivation()` and present the appropriate sharing surface when activation is not preferred. Load `activation-ui.md`. |
| Spatial coordination | Configure `SystemCoordinator` before `join()` and keep immersive scene setup separate from message sync. Load `spatial-coordination.md`. |

## Guardrails

- Keep activity payloads small, `Codable`, and specific to the experience.
- Join only after local UI and state are ready to receive session events.
- Add messaging or journals only when the experience has real shared state.
- Treat sample code as reference material; modernize observation and
  concurrency with `coding-standards-enforcer` before copying patterns into new
  code.

## Sample Escalation

Open [`../samples/groupactivities-samples.md`](../samples/groupactivities-samples.md)
only when you need fuller sample-backed flows for:

- defining a `GroupActivity` with transferable metadata
- observing and configuring sessions
- synchronizing state with messenger and journal
- comparing Apple GuessTogether or DrawTogether sample structure
