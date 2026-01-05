# Portals and Environments Components

Examples assume `import RealityKit` and an `Entity` named `entity`.

## PortalComponent
Goal: Defines a portal that renders a target world.

```swift
var portal = PortalComponent()
portal.target = <#Entity#>
entity.components.set(portal)
```

## WorldComponent
Goal: Designates an entity as a separate renderable world.

```swift
entity.components.set(WorldComponent())
```

## PortalCrossingComponent
Goal: Controls behavior when entities cross portal boundaries.

```swift
entity.components.set(PortalCrossingComponent())
```

## EnvironmentBlendingComponent
Goal: Blends virtual content with the real environment.

```swift
var blending = EnvironmentBlendingComponent()
blending.mode = <#BlendingMode#>
entity.components.set(blending)
```
