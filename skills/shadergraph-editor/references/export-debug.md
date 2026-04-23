# Export Debug

Use this file when the graph loads incorrectly, renders incorrectly, or needs
interop inspection.

## Rules

- Treat exported USD and MaterialX as debugging artifacts, not the default
  authoring surface.
- Compare a broken export to a known-good sample when translation issues are
  suspected.
- For runtime controls, confirm the promoted input is exported as a material
  parameter and appears in `ShaderGraphMaterial.parameterNames`.
- Inspect top-level `inputs:<Name>` values and their connections before
  assuming Swift-side `setParameter` is broken.
- Do not hand-edit raw `info:id` node identifiers, node positions, or graph UI
  metadata unless the task is explicitly an export repair.
- Hand prim-level edits back to `usd-editor` when the problem is really about
  paths, composition, or text-level stage structure.
