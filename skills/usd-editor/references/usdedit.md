# usdedit

Use this when you need the official text-editing workflow for a USD-readable file instead of manually converting formats yourself.

## What It Does

`usdedit` converts a USD-readable file to a temporary `.usda` representation, opens it in your editor, and writes the edited result back to the original format when you save and quit.

## Basic Usage

```bash
usdedit [OPTIONS] usdFileName
```

## Common Options

- `-n`, `--noeffect`: Open the temporary file without writing changes back.
- `-f`, `--forceWrite`: Write back even if the file timestamp changed.
- `-p`, `--prefix PREFIX`: Use a custom prefix for the temporary file.

## Examples

Edit a binary `.usdc` asset through a temporary text file:

```bash
usdedit Model.usdc
```

Inspect how a package-backed asset would look as text without saving changes:

```bash
usdedit --noeffect Model.usdz
```
