# RealityKit Systems (visionOS)

RealityKit systems drive per-frame behavior in the ECS. Use this list to find the core system APIs and supporting utilities.

## System APIs

- System
- System.registerSystem()
- SystemDependency
- SystemUpdateCondition
- SceneUpdateContext

## Query and filtering

- EntityQuery
- QueryPredicate
- QueryResult

## Scene and event utilities

- Scenes (ECS scenes)
- Events (ECS events)
- Entity actions

## Notes

- Systems are global per scene and are created automatically after registration.
- Use `SystemDependency` to order systems that rely on each other.
- Store per-entity state in components, not in the system instance.
