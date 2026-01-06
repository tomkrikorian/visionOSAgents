# Networking and Sync Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## SynchronizationComponent
Goal: Synchronizes entity state across networked sessions.

```swift
entity.components.set(SynchronizationComponent())
```

## TransientComponent
Goal: Marks an entity as non-persistent and non-synced.

```swift
entity.components.set(TransientComponent())
```
