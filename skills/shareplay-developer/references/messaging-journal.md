# Messaging And Journal

Use this file when the experience needs synchronized state.

## Guidance

- Use `GroupSessionMessenger` for transient events and time-sensitive state
  changes.
- Use `.reliable` for critical messages and `.unreliable` only when loss is
  acceptable.
- Use `GroupSessionJournal` for durable shared objects and attachments.
- Send a state snapshot when participants change so late joiners can catch up.
