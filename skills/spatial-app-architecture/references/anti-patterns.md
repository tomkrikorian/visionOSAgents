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
