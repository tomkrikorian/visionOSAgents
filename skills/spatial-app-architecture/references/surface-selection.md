# Surface Selection

Use this file when the main question is which surface should own the feature.

## Surface Defaults

| Surface | Use When | Avoid When |
| --- | --- | --- |
| Window | The job is textual, navigational, document-like, account/settings, or a control panel for spatial content. | The content must be inspected from multiple physical angles or needs depth as part of the task. |
| Volumetric window | The user manipulates or inspects a bounded 3D object, miniature scene, dashboard, configurator, or preview. | The scene needs world-scale presence, room context, or long-running immersive lifecycle. |
| ImmersiveSpace | The feature needs unbounded presence, world tracking, full or progressive immersion, spatial media, or a dedicated RealityKit/ARKit lifecycle. | It is only being chosen because 3D is available; keep ordinary tools and navigation in a window. |
| Mixed flow | A window launches or controls a volume or immersive space, and state must survive across surfaces. | The launch path requires several intermediate surfaces before the user reaches the main job. |

Treat a volume as a window scene with `windowStyle(.volumetric)`, not as a
lightweight immersive space. Treat `ImmersiveSpace` as a separate scene with
separate lifecycle, environment actions, and one-open-space-at-a-time behavior.

## Decision Sequence

1. Name the user job first: browse, edit, inspect, present, simulate, watch,
   collaborate, or debug.
2. Pick the least immersive surface that satisfies that job.
3. Decide the launch surface. Most apps should start in a normal window unless
   the product is inherently immersive.
4. Decide whether 3D content is bounded. Bounded content usually belongs in a
   volume or `RealityView` inside a window; unbounded content belongs in an
   immersive space.
5. Decide which scene owns open/dismiss actions before writing UI controls.
6. Write down what state must cross surface boundaries.

## Lifecycle Questions

- Does the surface open automatically or on demand?
- Who owns `openImmersiveSpace` and `dismissImmersiveSpace`?
- Which state must survive the transition between surfaces?
- Should the scene restore on relaunch, use `defaultLaunchBehavior`, or be
  suppressed until explicitly opened?
- Does the app need a unique `Window`, multiple `WindowGroup` instances, a
  volume, or exactly one immersive session?
- What happens when the immersive space fails to open, is dismissed externally,
  or is interrupted by another immersive experience?

## Common Surface Combinations

- **Window + volume**: window owns navigation, selection, and commands; volume
  owns bounded 3D preview or manipulation.
- **Window + immersive space**: window owns entry, exit, settings, and recovery;
  immersive scene owns presence, simulation, media, or ARKit/RealityKit runtime.
- **Volume + immersive space**: use only when a bounded 3D staging area has a
  clear handoff into a full environment. Do not make the user manage two 3D
  surfaces without a strong workflow reason.
- **Multiple windows**: use stable IDs and explicit ownership when independent
  tools or documents can coexist; avoid scattering one feature's lifecycle
  controls across several scenes.

## Output Shape

When answering, include:

- selected launch surface and secondary surfaces
- why the selected surface is the least immersive one that satisfies the job
- scene IDs and open/dismiss ownership if the feature spans scenes
- state that must cross surface boundaries
- the fallback path when opening a secondary surface fails
