# usdchecker

Use this when validating USD or USDZ assets for compliance and platform constraints.

## What It Does

`usdchecker` validates a USD stage or USDZ package. It always runs general USD checks, and can run stricter checks for RealityKit compatibility with `--arkit`.

## Basic Usage

```bash
usdchecker [OPTIONS] [inputFile]
```

## Common Options

- `--arkit`: Apply RealityKit-focused validation rules.
- `-s`, `--skipVariants`: Validate only the default variant selections.
- `-p`, `--rootPackageOnly`: Validate only the root package (skip nested packages and dependencies).
- `-o`, `--out FILE`: Write failed checks to a file (use `stderr` to disable colored output).
- `--noAssetChecks`: Skip extra checks for safe asset referencing.
- `-d`, `--dumpRules`: Print the rules that would be checked.
- `-v`, `--verbose`: Verbose output.
- `-t`, `--strict`: Treat warnings as failures (non-zero exit).
- `--variantSets TEXT ...`: Validate all variants for the named variant sets.
- `--variants TEXT ...`: Validate specific variant combinations.
- `--disableVariantValidationLimit`: Remove the default cap on variant validation calls.

## Examples

Validate a USDZ for RealityKit:

```bash
usdchecker --arkit MyAsset.usdz
```

Write a strict report to a file:

```bash
usdchecker --strict -o report.txt Scene.usda
```

## Notes

- `usdchecker` only checks the first sample of time-sampled attributes.
- On Apple platforms, use `--arkit` for RealityKit constraints.
