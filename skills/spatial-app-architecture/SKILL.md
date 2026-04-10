---
name: spatial-app-architecture
description: Choose and refactor visionOS app architecture across surfaces, scene boundaries, state ownership, and file layout. Use when deciding window vs volume vs immersive space, splitting a feature across scenes, cleaning up a monolithic spatial root, or defining the ownership map before implementing SwiftUI or RealityKit details.
---

# Spatial App Architecture

## Quick Start

Use this skill for architecture questions, not API questions.

### Use this skill when

- you need to choose the right surface: window, volume, immersive space, or a
  mixed flow
- you are deciding which state is app-wide, scene-scoped, immersive-scoped, or
  view-local
- a root file owns too many concerns and needs a refactor plan
- you need a file/module plan before writing or splitting SwiftUI code

### Switch away from this skill when

- the surface and ownership model are already chosen, and you need to implement
  `RealityView`, `Model3D`, attachments, or spatial gestures
  -> use `spatial-swiftui-developer`
- the work is entity/component/system heavy
  -> use `realitykit-visionos-developer`
- the work depends on ARKit providers, anchors, or tracked-world behavior
  -> use `arkit-visionos-developer`
- the work depends on SharePlay group lifecycle or shared immersive presence
  -> use `shareplay-developer`
- the architecture is settled and the next step is build/run/debug validation
  -> use `build-run-debug`

## Tracks

### 1. Greenfield

Use this track when you are shaping a new feature or app slice.

- classify the user job first: browsing, editing, utility, spatial object,
  shared activity, or immersive experience
- choose the smallest surface that matches the job
- decide the ownership boundary before writing view code
- sketch the file/module layout before implementing UI details

### 2. Surface and Lifecycle

Use this track when the main question is how the feature appears or moves.

- choose between window, volume, and immersive space by lifecycle needs, not by
  novelty
- decide whether the surface launches automatically or opens on demand
- define who owns `openImmersiveSpace` / `dismissImmersiveSpace`
- keep transitions explicit and keep state that must survive transitions outside
  leaf controls

### 3. Brownfield Refactor

Use this track when the app already exists and the structure is the problem.

- identify which file currently owns too many concerns
- separate scene selection, feature composition, state ownership, and platform
  glue
- pull immersive lifecycle and RealityKit mutation up to explicit owners
- split the refactor into small slices that preserve behavior

## Workflow

1. Classify the feature by user job and current or intended surface.
2. Choose the owning surface model: window, volume, immersive space, or a
   combination.
3. Assign state ownership boundaries: app, scene, immersive, feature, view.
4. Choose a file/module shape that matches the ownership model.
5. Define the implementation handoff: SwiftUI, RealityKit, ARKit, SharePlay, or
   build/debug.
6. If this is a refactor, sequence the extraction so behavior stays stable.
7. Verify the structure with `build-run-debug` after the first usable slice.

## Surface Selection

- Use a normal window when the feature is mostly textual, navigational, or
  utility-oriented.
- Use a volumetric window when the content should feel spatial but still live
  in a bounded container.
- Use an immersive space when the feature needs unbounded presence, tracked
  world context, or a dedicated lifecycle.
- Do not force a feature into immersion just because the platform allows it.
- If the experience has multiple surfaces, define the launch surface first and
  keep the entry path simple.

## Ownership Model

Choose the narrowest ownership scope that matches the problem.

| Scope | Owns |
| --- | --- |
| App | top-level scene declarations, app-wide dependency injection, persistent preferences |
| Scene | navigation, presentation state, scene-local selection, immersive entry/exit coordination |
| Feature model/coordinator | async work, service coordination, long-lived feature state |
| Reality controller/system | entity graph mutation, component updates, simulation behavior |
| View | ephemeral local UI state and intent dispatch |

### State placement defaults

- `@State`: local control state and small scene-owned observable models
- `@Binding`: parent-owned value passed into a child
- `@SceneStorage`: scene-local restoration when it genuinely fits
- `@AppStorage`: app-wide preference or toggle
- `@Environment(Type.self)`: shared service/coordinator or read-only app
  context, following the project standard
- Do not keep immersive lifecycle ownership or long-lived entity ownership in
  transient leaf views.

## Recommended File Shapes

Choose one shape and apply it consistently in the slice you are touching.

### Layered scene-first shape

- `App/<AppName>App.swift`
- `Scenes/<Feature>Scene.swift`
- `Views/<Feature>RootView.swift`
- `Views/<Feature>DetailView.swift`
- `Models/*.swift`
- `Stores/*.swift`
- `Services/*.swift`
- `Support/*.swift`

Use this when the codebase is already layered or when multiple scenes share the
same services and models.

### Feature-sliced shape

- `App/<AppName>App.swift`
- `Scenes/MainWindowScene.swift`
- `Scenes/ImmersiveRootScene.swift`
- `Features/<Feature>/<Feature>View.swift`
- `Features/<Feature>/<Feature>Model.swift`
- `Reality/<Feature>RealityController.swift`

Use this when the work is brownfield refactor of a large feature or when one
spatial feature has strong ownership boundaries that deserve to stay together.

If the repo already has a stronger convention, preserve it rather than forcing a
new global layout.

## Refactor Playbook

1. Identify the current root owner and list the concerns it mixes.
2. Freeze the scene boundary first.
3. Move state to the correct owner before splitting views further.
4. Extract immersive lifecycle and RealityKit mutation into named owners.
5. Split files by responsibility, not by arbitrary line count.
6. Re-run build and launch after each meaningful extraction slice.

## Anti-Patterns

- one giant `ContentView` owning every surface and lifecycle
- scene selection, state ownership, networking, and RealityKit mutation in one
  file
- leaf controls that quietly own immersive entry or dismissal
- unstable top-level branching between unrelated roots
- forcing iOS-style stacked navigation onto a spatial flow without reason
- choosing `RealityView` or ARKit before the surface and ownership model are
  clear

## Output Expectations

Provide:

- the chosen surface model and why
- the ownership map: app, scene, feature model/coordinator, reality owner, view
- the proposed file/module shape
- the refactor slices, if this is brownfield work
- the next implementation handoff:
  `spatial-swiftui-developer`, `realitykit-visionos-developer`,
  `arkit-visionos-developer`, `shareplay-developer`, or `build-run-debug`

