---
name: visionos-widgetkit-developer
description: Build and debug WidgetKit widgets for Apple Vision Pro (visionOS), including mounting styles (elevated/recessed), textures (glass/paper), proximity-aware layouts via LevelOfDetail, interactive widgets with AppIntents, widget rendering modes (accented/fullColor), and timeline update troubleshooting. (visionOS widgets are pinned spatial objects, not watch complications.)
---

# visionOS WidgetKit Developer

## Description and Goals

This skill helps you design, implement, and troubleshoot **WidgetKit widgets for Apple Vision Pro**. On visionOS, widgets are spatial objects that people pin to real surfaces, and they can be viewed from different distances. visionOS adds widget-specific capabilities like **mounting styles** (elevated vs recessed), **textures** (glass vs paper), and **proximity-aware layouts** via `LevelOfDetail`.

### Goals

- Help you choose the right widget strategy for a native visionOS app on Vision Pro.
- Implement visionOS-specific widget presentation: mounting styles, textures, and families.
- Ensure glanceability at distance using `LevelOfDetail`-driven layouts.
- Provide a practical debugging checklist for timelines, refreshes, and rendering issues.

## What This Skill Should Do

When you ask to build or debug a Vision Pro widget, this skill should:

1. **Clarify scope and platform**: Is this a native visionOS widget, and which widget families must it support on Vision Pro?
2. **Choose layout strategy**: Define a “default” layout (close) and a “simplified” layout (far) using `@Environment(\.levelOfDetail)`.
3. **Configure visionOS widget presentation**:
   - Set `supportedMountingStyles` (elevated/recessed) appropriately.
   - Choose `widgetTexture` (glass/paper) where available/appropriate.
   - Split widgets into separate configurations when different families need different supported mounting styles.
4. **Validate legibility and content density**: Ensure the simplified layout remains readable from across the room.
5. **Handle updates**: Implement a sound timeline strategy and define when/how the widget reloads.
6. **Debug and iterate**: Provide concrete checks for common failure modes (missing families, bad Info.plist, broken layouts in recessed mode, stale timelines).

Load the most relevant reference file(s) below based on the specific issue.

## Information About the Skill

### Core Concepts

#### Widgets in visionOS are spatial objects

On Vision Pro, widgets are pinned to horizontal or vertical surfaces and behave like physical objects in the room. This changes how you design for legibility, contrast, and layout compared to 2D-only platforms.

#### Mounting styles: elevated vs recessed

On vertical surfaces, a widget can appear **recessed** (embedded into a wall) or **elevated** (sitting on top of the surface). Elevated is the default style because it works on both horizontal and vertical surfaces; recessed applies only on vertical surfaces.

#### Textures: glass vs paper

For widgets your visionOS app offers, you can typically choose a **glass** or **paper** texture. This affects background treatment, contrast, and how “poster-like” your widget feels.

#### Proximity awareness with `LevelOfDetail`

visionOS can change a widget’s `LevelOfDetail` based on **user proximity**. Treat this as a first-class requirement:

- `.default`: more information, smaller typography, richer layout.
- `.simplified`: less information, larger typography, fewer elements, more contrast.

#### Family support for extra-large widgets

For native visionOS widgets, use `WidgetFamily.systemExtraLargePortrait` when
you need the extra-large family on Vision Pro. Compatible iOS apps running on
visionOS should continue to use `systemExtraLarge`.

> StandBy and watch complications do not apply on visionOS. visionOS widgets
> are pinned spatial objects that participate in the room, not Watch
> complications and not iOS StandBy mode.

#### Rendering modes and accented rendering

visionOS renders widgets in multiple modes depending on background treatment
and mounting. Use `@Environment(\.widgetRenderingMode)` to branch layout when
the mode changes, and use `widgetAccentedRenderingMode(_:)` to declare how the
widget should participate in accented rendering. See Apple's
"Preparing widgets for additional contexts and appearances" for the full list
of modes.

#### Interactive widgets

visionOS widgets can be interactive by hosting `Button` and `Toggle` controls
backed by `AppIntent` (via `AppIntentControlValueProvider` and related types).
Keep the interaction surface small — a widget is glanceable, not a full
control surface — and route richer flows into the host app via a deep link or
`openAppIntent`.

### Reference Tables

| Reference | When to Use |
|---|---|
| [`REFERENCE.md`](references/REFERENCE.md) | Overview, decision points, and a quick checklist for Vision Pro widgets. |
| [`mounting-styles.md`](references/mounting-styles.md) | When deciding elevated vs recessed support and avoiding layout breakage. |
| [`textures-and-rendering.md`](references/textures-and-rendering.md) | When choosing glass vs paper, and ensuring legibility in different render modes. |
| [`proximity-levelofdetail.md`](references/proximity-levelofdetail.md) | When implementing near/far layouts using `LevelOfDetail`. |
| [`debugging-and-updates.md`](references/debugging-and-updates.md) | When widgets don’t refresh, don’t appear, or appear stale/broken. |

### Implementation Patterns

#### Configure a visionOS widget with mounting + texture

```swift
import SwiftUI
import WidgetKit

struct MyVisionOSWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "MyVisionOSWidget", provider: Provider()) { entry in
            MyWidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Glanceable info in your space.")
        .supportedMountingStyles([.elevated, .recessed])
        .widgetTexture(.glass)
        // Choose families intentionally; create a separate widget configuration
        // if a different family set needs different mounting-style support.
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}
```

#### Proximity-aware widget layout

```swift
import SwiftUI
import WidgetKit

struct MyWidgetView: View {
    @Environment(\.levelOfDetail) private var levelOfDetail
    @Environment(\.widgetRenderingMode) private var renderingMode
    let entry: Provider.Entry

    var body: some View {
        if levelOfDetail == .simplified {
            SimplifiedView(entry: entry)
        } else {
            DetailedView(entry: entry)
        }
    }
}
```

#### Interactive widget with AppIntent

```swift
import AppIntents
import SwiftUI
import WidgetKit

struct ToggleFavoriteIntent: AppIntent {
    static var title: LocalizedStringResource = "Toggle Favorite"
    @Parameter(title: "Item ID") var itemID: String

    func perform() async throws -> some IntentResult {
        // Mutate store, then request timeline reload for the kind.
        return .result()
    }
}

struct FavoritesWidgetView: View {
    let entry: Provider.Entry
    var body: some View {
        Button(intent: ToggleFavoriteIntent(itemID: entry.itemID)) {
            Label("Favorite", systemImage: entry.isFavorite ? "star.fill" : "star")
        }
    }
}
```

### Pitfalls and Checks

- Don’t ship a single dense layout: always consider `.simplified` for distance readability.
- Don’t assume recessed mode “just works”: test layouts and backgrounds in recessed mounting.
- Avoid tiny typography and low-contrast UI; pinned widgets are often viewed from far away.
- Don’t forget to include the right widget families, including `systemExtraLargePortrait` when you need an extra-large Vision Pro widget.
- If timelines seem stale, confirm your timeline policy and reload strategy.
