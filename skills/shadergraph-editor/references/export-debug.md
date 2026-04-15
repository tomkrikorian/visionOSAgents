# Export Debug

Use this file when the graph loads incorrectly, renders incorrectly, or needs
interop inspection.

## Rules

- Treat exported USD and MaterialX as debugging artifacts, not the default
  authoring surface.
- Compare a broken export to a known-good sample when translation issues are
  suspected.
- Hand prim-level edits back to `usd-editor` when the problem is really about
  paths, composition, or text-level stage structure.
