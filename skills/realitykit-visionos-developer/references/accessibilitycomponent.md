# AccessibilityComponent

**Reference:** [Apple Documentation](https://developer.apple.com/documentation/realitykit/accessibilitycomponent)

## Overview

Supplies accessibility metadata for assistive technologies. This component makes your RealityKit entities accessible to users with disabilities by providing labels, hints, and other accessibility information that screen readers and other assistive technologies can use.

## When to Use

- Making entities accessible to screen readers
- Providing labels for assistive technologies
- Supporting VoiceOver and other accessibility features
- Creating inclusive experiences
- Meeting accessibility requirements

## How to Use

### Basic Setup

```swift
import RealityKit

// Enable accessibility
entity.components.set(AccessibilityComponent())
```

### Real-World Example: Earth Entity Accessibility

This example from the Hello World sample shows a comprehensive accessibility setup:

```swift
import RealityKit

private func makeAxComponent(
    configuration: Configuration,
    satelliteConfiguration: [SatelliteEntity.Configuration],
    moonConfiguration: SatelliteEntity.Configuration?
) -> AccessibilityComponent {
    // Create an accessibility component
    var axComponent = AccessibilityComponent()
    axComponent.isAccessibilityElement = true

    // Add a label
    axComponent.label = "Earth model"

    // Add a value that describes the model's current state
    var axValueComponents = [String]()
    axValueComponents.append(configuration.currentSpeed != 0
                             ? "Rotating."
                             : "Not rotating.")
    axValueComponents.append(configuration.showSun
                             ? "The sun is shining."
                             : "The sun is not shining.")
    if configuration.showPoles {
        axValueComponents.append("The poles indicated.")
    }
    for item in satelliteConfiguration.map({ $0.name }) {
        axValueComponents.append("A \(item) orbits close to the earth.")
    }
    if moonConfiguration != nil {
        axValueComponents.append("The moon orbits at some distance from the earth.")
    }
    let axValue = axValueComponents.joined(separator: " ")
    axComponent.value = LocalizedStringResource(stringLiteral: axValue)

    // Add custom accessibility actions
    if !configuration.axActions.isEmpty {
        axComponent.customActions.append(contentsOf: configuration.axActions)
    }

    return axComponent
}

// Usage
components.set(makeAxComponent(
    configuration: configuration,
    satelliteConfiguration: satelliteConfiguration,
    moonConfiguration: moonConfiguration
))
```

### With Accessibility Label

```swift
// Create accessibility component with label
var accessibility = AccessibilityComponent()
accessibility.isAccessibilityElement = true
accessibility.label = "Interactive Earth Model"
accessibility.value = "Rotating at normal speed"
entity.components.set(accessibility)
```

### Custom Accessibility Actions

```swift
var accessibility = AccessibilityComponent()
accessibility.isAccessibilityElement = true
accessibility.label = "Earth Model"
accessibility.customActions = [
    "Rotate clockwise",
    "Rotate counterclockwise",
    "Zoom in",
    "Zoom out"
]
entity.components.set(accessibility)
```

## Key Properties

- `isAccessibilityElement: Bool` - Whether the entity is an accessibility element
- `label: String?` - A short label describing the entity
- `value: String?` - The current value or state of the entity
- `hint: String?` - A hint describing what actions are available
- `customActions: [LocalizedStringResource]` - Custom actions available to assistive technologies
- `traits: AccessibilityTraits` - Accessibility traits that describe the entity's behavior

## Important Notes

- Essential for making spatial experiences accessible
- Provides information to screen readers
- Supports VoiceOver on visionOS
- Important for inclusive design
- Should be added to interactive or important entities

## Best Practices

- Add to all interactive entities
- Provide clear, descriptive labels
- Include helpful hints for complex interactions
- Test with VoiceOver enabled
- Follow accessibility guidelines for spatial computing

## Related Components

- `InputTargetComponent` - Often used together for accessible interactions
- `ManipulationComponent` - Should have accessibility labels
