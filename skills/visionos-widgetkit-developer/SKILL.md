---
name: visionos-widgetkit-developer
description: Build and debug WidgetKit widgets for Apple Vision Pro (visionOS), including mounting styles (elevated/recessed), textures (glass/paper), proximity-aware layouts via LevelOfDetail, interactive widgets with AppIntents, widget rendering modes (accented/fullColor), and timeline update troubleshooting. (visionOS widgets are pinned spatial objects, not watch complications.)
---

# visionOS WidgetKit Developer

## Quick Start

Treat visionOS widgets as spatial objects first, not as small 2D surfaces.

1. Decide the platform and family scope first.
2. Define both close and far layouts before polishing visuals.
3. Treat timeline entries, shared storage, and App Intents as the integration
   boundary; do not depend on live host-app state.
4. Load only the reference files that match the current problem.

## Load References When

| Reference | When to Use |
|---|---|
| [`widget-overview.md`](references/widget-overview.md) | Overview, decision points, and a quick checklist for Vision Pro widgets. |
| [`families-and-platforms.md`](references/families-and-platforms.md) | When choosing native visionOS families, compatible iOS families, or extra-large widget support. |
| [`mounting-styles.md`](references/mounting-styles.md) | When deciding elevated vs recessed support and avoiding layout breakage. |
| [`textures-and-rendering.md`](references/textures-and-rendering.md) | When choosing glass vs paper, and ensuring legibility in different render modes. |
| [`proximity-levelofdetail.md`](references/proximity-levelofdetail.md) | When implementing near/far layouts using `LevelOfDetail`. |
| [`interactive-widgets.md`](references/interactive-widgets.md) | When adding `Button`, `Toggle`, or `AppIntent`-driven interactions to a widget. |
| [`debugging-and-updates.md`](references/debugging-and-updates.md) | When widgets don’t refresh, don’t appear, or appear stale or broken. |
| [`widget-animation.md`](references/widget-animation.md) | When animating widget content using timeline entries and Canvas crossfade, tuning frame rate, or hitting bundle or computation budget limits. |

## Workflow

1. Confirm the widget platform and family set.
2. Choose mounting style, texture, and near/far layout strategy.
3. Decide the data path: timeline-only, App Group/shared storage, background
   URL session, or WidgetKit push notification.
4. Add interaction only if the widget still stays glanceable.
5. Verify timelines, reloads, rendering modes, and extension logs after the
   structure is set.

## Guardrails

- Always consider `.simplified` for distance readability.
- Use native visionOS families intentionally; extra-large native visionOS
  widgets use `.systemExtraLargePortrait`, while compatible iOS/iPadOS widgets
  keep `.systemExtraLarge`.
- Do not assume recessed mode works without explicit layout checks.
- Avoid dense, low-contrast layouts.
- Use `Link` or `widgetURL(_:)` for open-app navigation; reserve `Button` and
  `Toggle` for real `AppIntent` actions.
- Keep widget configurations per `WidgetBundle` within the practical limit.

## Output Expectations

Provide:
- the widget platform and family scope
- which references were used
- the chosen presentation strategy
- the main rendering, interaction, or timeline constraint
- the next validation step
