# Widget Animation and Performance on visionOS

Field-tested guidance for animated widgets on Apple Vision Pro. WidgetKit does
not support real-time animation — every technique here works within that
constraint using timeline entries, crossfade behavior, and careful budgeting.

These findings are based on community testing with complex generative-art
widgets (12+ animated Canvas-based widgets in a single extension). They
cover undocumented WidgetKit behavior discovered through trial and error on
Apple Vision Pro hardware.

---

## Timeline-Entry Animation (Public API, Recommended)

This is the only Apple-supported path for animated widgets. It uses standard
`TimelineProvider` entries to drive visual change over time.

### Architecture

1. `TimelineProvider.getTimeline()` generates **300 entries at 1-second
   intervals** over 5 minutes, with reload policy `.atEnd` for immediate
   reload when the timeline expires.
2. Each entry carries a `Date` that the widget view reads as its animation
   clock.
3. Pass the entry date to Canvas or other drawing views via a custom
   `EnvironmentKey` so the rendering code treats it as the time parameter.
4. Apply `.animation(.linear(duration: 1.0), value: animationDate)` on the
   Canvas so SwiftUI crossfades between consecutive snapshots.

```swift
struct AnimatedWidgetProvider: TimelineProvider {
    func getTimeline(in context: Context,
                     completion: @escaping (Timeline<AnimatedEntry>) -> Void) {
        let now = Date()
        let entries = (0..<300).map { i in
            AnimatedEntry(date: now.addingTimeInterval(Double(i)))
        }
        completion(Timeline(entries: entries, policy: .atEnd))
    }
    // ...
}
```

```swift
struct AnimatedCanvasView: View {
    let animationDate: Date

    var body: some View {
        Canvas { context, size in
            let t = animationDate.timeIntervalSinceReferenceDate
            // Use `t` as the time parameter for all drawing
            // ...
        }
        .animation(.linear(duration: 1.0), value: animationDate)
    }
}
```

### The Crossfade Is Not Interpolation

`.animation()` on a `Canvas` does **not** interpolate individual draw calls.
SwiftUI crossfades the **entire Canvas bitmap** — the old frame fades out
while the new frame fades in over the animation duration. This is a critical
distinction:

- **Progressive drawing works well.** Elements added each frame blend in
  naturally through the crossfade.
- **Small movements look smooth.** When drawn elements shift only 2–3 pixels
  per frame, the crossfade acts as motion blur and the result appears to run
  at ~30 fps.
- **Large movements cause ghosting.** If elements jump many pixels between
  frames, both the old and new positions are visible simultaneously during
  the crossfade.

### Tuning for Perceived Smoothness

| Parameter | Too fast (ghosting) | Sweet spot | Too slow (static) |
|-----------|---------------------|------------|-------------------|
| Element movement | >8 px/frame | 2–3 px/frame | <0.5 px/frame |
| Orbital / cycle period | <5 s | 60–130 s | >200 s |
| Hue rotation | >0.1/frame | 0.005–0.05/frame | <0.001/frame |

Design animations so each frame differs only slightly from the previous one.
Slow Lissajous curves, gentle hue shifts, and progressive-drawing patterns
all work well within the crossfade model.

### What Does NOT Work

- **`TimelineView(.animation)`** — WidgetKit throttles this to ~10–20 second
  updates on visionOS. The widget appears frozen between updates.
- **`Date()` in widget views** — Captures render time, not display time.
  WidgetKit may render entries ahead of time and cache them. The date will
  not progress as expected at display time.
- **0.5-second intervals over 5 minutes (600 entries)** — Causes widgets to
  stop rendering entirely in testing. 300 entries at 1-second intervals is
  the reliable ceiling for a 5-minute window.

### Frame Delivery Is Inconsistent

On Vision Pro, frame delivery from the timeline is not perfectly regular.
Widgets occasionally receive a burst of smooth delivery (perceived as
butter-smooth animation) followed by periods of dropped or delayed frames.
This appears to be a system-level scheduling behavior. Reducing per-frame
computation cost increases the frequency of smooth-delivery windows.

### Practical Frame Rate Ceiling (~2 fps for Complex Widgets)

| Interval | Effective FPS | Entries (2 min) | Result |
|----------|---------------|-----------------|--------|
| 1.0 s | ~1 fps | 120 | Choppy, occasional smooth bursts |
| 0.5 s | ~2 fps | 240 | Visible improvement, good trade-off |
| 0.25 s | ~4 fps | 480 | No improvement over 2 fps on device |

The system caps effective delivery at ~2 fps for non-trivial Canvas widgets.
Going faster wastes entries without improving perceived animation. **0.5 s
intervals is the practical sweet spot** for heavier widgets that need the
best frame rate possible.

### Per-Widget Timeline Providers

Each widget configuration can use its own `TimelineProvider` with different
intervals and durations. Give heavier widgets a faster frame rate without
penalizing the rest of the bundle:

- Shorter interval (0.5 s instead of 1.0 s) for the animation-heavy widget.
- Shorter total duration (2 minutes instead of 5) to keep entry count
  reasonable.
- Match the Canvas `.animation(.linear(duration:))` to the provider's
  interval so the crossfade timing lines up.

---

## Why Apple's Clock Widget Looks Smoother

Apple's system clock widget achieves ~20 fps smooth rotation using a
**private API**: `_ClockHandRotationEffect`. This is a SwiftUI modifier that
performs genuine rotation interpolation at the display's native refresh rate
inside WidgetKit — real smooth animation, not crossfade.

This API was briefly exposed as a public symbol in Xcode 12–13 and hidden
again in Xcode 14. It is still present in the WidgetKit framework and used
by Apple's own widgets.

**Do not use this API in shipping code.** It is private, undocumented, and
subject to App Store review rejection. It is mentioned here so you
understand why the system clock looks fundamentally smoother than your
timeline-based animation — the system widgets use a rendering path that
third-party widgets cannot access through public API.

More broadly, SwiftUI can interpolate animatable view properties (rotation,
offset, scale, opacity) at native refresh rate. Canvas draw calls are
imperative and opaque to SwiftUI's animation system, so only bitmap
crossfade is possible for Canvas-based content.

---

## Advanced Community Techniques

These techniques use 100% public API but exploit undocumented WidgetKit
behavior in creative ways. They are **not recommended for production** — they
are fragile, may break across OS versions, and push WidgetKit well beyond
its intended use. They are documented here for awareness only.

### Timer Mask Animation (~30 fps, ~5 s loops)

Uses `Text(.date, style: .timer)` — a self-updating label that counts
up/down every second without code re-execution. By replacing font glyphs
with animation frames and using font ligatures to map two-digit sequences
(00–59) to unique glyphs, developers can clip the timer label to show only
specific digits and layer multiple offset timers as masks for content.

Limit: ~150–200 timer instances before the system stops rendering them.
At 30 fps, that yields about 5 seconds of unique frames.

Community references:
- <https://github.com/TopWidgets/SwingAnimation>
- <https://github.com/tangtiancheng/DouYinWidgetAnimation>

### Timer + Font Cycling (~30 fps, ~30 s loops)

Extends the timer-mask approach by creating N custom fonts (e.g., 16), each
containing every Nth frame as ligatures. N timers cycle through their
respective fonts as the seconds advance, producing longer animation loops.

Community references:
- Same repos as above; the technique was developed iteratively from timer
  masks.

### When to Use What

| Technique | FPS | Duration | Dynamic? | API | Best for |
|-----------|-----|----------|----------|-----|----------|
| Timeline crossfade | 1–2 | Unlimited | Yes (generative) | Public | Generative art, data viz |
| Timer mask | ~30 | ~5 s | Yes (images) | Public (fragile) | Short sprite loops |
| Timer + font cycling | ~30 | ~30 s | No (pre-baked) | Public (fragile) | Pre-rendered loops |

For most visionOS widgets, **timeline-entry crossfade is the right choice**.
It is the only technique that works reliably across OS versions, supports
dynamic/generative content, and stays within Apple's intended WidgetKit
usage model.

---

## Bundle Limits

### ~12 Widget Configurations Per WidgetBundle

At 15 widget configurations in a single `WidgetBundle`, individual widgets
silently fail to render. The extension does not crash — some widgets display
while others show stale cached snapshots. Reducing to 12 resolves the issue
immediately.

Apple does not document a hard limit. The practical ceiling is approximately
12 for widgets with non-trivial rendering.

### Shared Resource Budget Across the Extension

The widget extension is a single process. All widgets share its memory and
CPU budget. A computationally heavy Widget A can cause Widget B to fail even
if Widget B is lightweight on its own. Test with all widgets placed
simultaneously, not just one at a time.

---

## Computation Budget Guidelines

Empirical limits for Canvas-based widgets sharing a 12-widget extension on
Apple Vision Pro:

| Metric | Safe | Risky | Causes failures |
|--------|------|-------|-----------------|
| Path segments per frame (single widget) | <3,000 | 3,000–6,000 | >10,000 |
| Timeline entries per reload | ≤300 (1 s × 5 min) | — | 600 (0.5 s × 5 min) |
| Widget configurations in bundle | ≤12 | 13–14 | 15+ |
| Trig calls per frame (sin/cos) | <5,000 | 5,000–10,000 | >15,000 |

These limits are **shared across the extension**. Two widgets each doing
3,000 path segments may work individually but fail when both are placed on
the wall at the same time.

---

## visionOS-Specific Gotchas

### `.systemLarge` Is Not Supported for Native visionOS Apps

Use `.systemExtraLargePortrait` for the extra-large family on native visionOS
widgets. Compatible iOS apps running on visionOS should continue to use
`.systemExtraLarge`. Declaring `.systemLarge` in a native visionOS target has
no effect.

Supported families for native visionOS widgets: `.systemSmall`,
`.systemMedium`, `.systemExtraLargePortrait`.

### Widget Caching Is Aggressive

After deploying updated code, widgets on the wall may continue showing old
renders for an extended period. To reliably see changes during development:

1. Clean build (Cmd+Shift+K in Xcode).
2. Delete the app from the device or simulator.
3. Rebuild and install.
4. Re-add the widget to the home view.

### SourceKit False Positives

macOS SourceKit cannot always resolve visionOS-only types (`WidgetTexture`,
`LevelOfDetail`, `WidgetMountingStyle`, etc.). "Cannot find type in scope"
errors in Xcode are expected during development and do not affect device
builds. Build against the visionOS SDK to confirm compilation.
