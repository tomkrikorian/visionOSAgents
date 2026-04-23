# Architecture Anti-Patterns

Use this file when you need to explain why the current structure is unstable.

- One giant `ContentView` owns every surface and lifecycle.
- Scene selection, state ownership, networking, and RealityKit mutation sit in
  one file.
- Leaf controls quietly own immersive entry or dismissal.
- Top-level branching swaps between unrelated roots without a stable owner.
- The design forces iOS-style stacked navigation onto a spatial flow without a
  strong reason.
- The team chose `RealityView` or ARKit before deciding the surface and
  ownership model.
- A volume is treated like a disposable preview even though it owns workflow
  state that must survive window updates.
- `openImmersiveSpace` is called from several leaf buttons with no shared
  session state or failure handling.
- Attachments contain the inspector for the whole app instead of a compact
  in-scene control or label.
- `RealityView` update closures start asset loads or add duplicate root
  entities on every state change.
