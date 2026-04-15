# Surface Selection

Use this file when the main question is which surface should own the feature.

## Heuristics

- Use a normal window when the feature is mostly textual, navigational, or
  utility-oriented.
- Use a volumetric window when the content should feel spatial but still live
  in a bounded container.
- Use an immersive space when the feature needs unbounded presence, tracked
  world context, or a dedicated lifecycle.
- If the experience spans multiple surfaces, define the launch surface first
  and keep the entry path simple.

## Lifecycle Questions

- Does the surface open automatically or on demand?
- Who owns `openImmersiveSpace` and `dismissImmersiveSpace`?
- Which state must survive the transition between surfaces?
