# Refactor Playbook

Use this file when the app already exists and the structure is the problem.

## Sequence

1. Identify the current root owner and list the concerns it mixes.
2. Freeze the scene boundary first: app declaration, launch scene, secondary
   windows/volumes, and immersive spaces.
3. Add a thin compatibility adapter if existing call sites are noisy, then move
   state to the correct owner before splitting views further.
4. Extract immersive lifecycle into a scene/session coordinator with explicit
   intents (`open`, `dismiss`) and phases (`closed`, `opening`, `open`,
   `failed`) when the current code needs them.
5. Extract RealityKit mutation into a named controller or system. Keep
   `RealityView` closures as the bridge, not the whole feature brain.
6. Split files by responsibility, not by arbitrary line count.
7. Replace broad globals with explicit environment injection only after the new
   owner exists.
8. Re-run build and launch after each meaningful extraction slice.

## Refactor Slices

- **Scene slice**: move `WindowGroup`, `Window`, `ImmersiveSpace`, launch
  behavior, and scene IDs into obvious app/scene files.
- **State slice**: move selection, loading, preferences, and immersive status to
  the ownership level that actually needs to persist them.
- **Reality slice**: move entity lookup, component writes, subscriptions,
  attachments placement, and animation control into a Reality owner.
- **View slice**: leave views with layout, local controls, bindings, and intent
  dispatch.
- **Verification slice**: build, launch, open/dismiss every surface, and confirm
  the old entry path still works.

## Review Checks

- Can a reader name the owner of each scene and each long-lived model?
- Can the immersive space be opened, fail, and dismiss without stranded state?
- Are attachments created by SwiftUI but positioned by the Reality owner?
- Did the refactor avoid mixing visual cleanup with ownership changes?
- Does each extracted file have a reason beyond reducing line count?

## Goal

Keep behavior stable while making ownership and scene boundaries explicit.
