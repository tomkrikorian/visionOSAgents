# Activity Definition

Use this file when defining the `GroupActivity` itself.

## Rules

- Keep payloads minimal and `Codable`.
- Fill in `GroupActivity.metadata` with the correct activity type, title, and
  fallback URL when needed.
- Use `GroupActivityTransferRepresentation` when the activity should be
  startable from `ShareLink`, a share sheet, or another transferable surface.

## Activation Decision

Use `prepareForActivation()` to decide whether the app should call
`activate()` immediately or fall back to an explicit sharing surface.
