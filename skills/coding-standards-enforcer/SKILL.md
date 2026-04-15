---
name: coding-standards-enforcer
description: Enforce repository coding standards for Swift 6.2 strict concurrency, actor isolation, @Observable models, SWIFT_APPROACHABLE_CONCURRENCY, @concurrent functions, and modern Swift APIs across visionOS app code. Use when reviewing, writing, or migrating Swift code in this plugin's scope.
---

# Coding Standards Enforcer

## Quick Start

Use this skill whenever Swift source changes are in scope and the question is
whether the code matches the repository's concurrency, observation, and modern
API standards.

1. Classify the work first:
   - isolation / actor / `Sendable` problem
   - view-model / observation / ownership problem
   - modern API / style / safety cleanup
2. Load only the reference files that match that category.
3. Review the changed code in this order:
   - compiler diagnostics and isolation boundaries
   - ownership and observation model
   - API modernization and safety
4. Fix or flag deviations explicitly; do not leave standards violations implied.

## Load References When

| Reference | When to Use |
|-----------|-------------|
| [`references/standards-review-map.md`](references/standards-review-map.md) | When you need the review order, routing, and repo-level standards map. |
| [`references/concurrency-guidelines.md`](references/concurrency-guidelines.md) | When the work touches actors, `@MainActor`, `Sendable`, `Task`, `async let`, task groups, or strict concurrency diagnostics. |
| [`references/observation-modeling.md`](references/observation-modeling.md) | When the work touches `@Observable`, view models, `@State`, `@Binding`, environment injection, or Combine-to-Observation migration. |
| [`references/modern-swift-apis.md`](references/modern-swift-apis.md) | When the work is about API modernization, Foundation replacements, formatting, string matching, force unwraps, or Swift-native style. |

## Workflow

1. Inspect the changed Swift files and note the primary failure class.
2. Load the narrowest relevant reference file or files.
3. Apply the minimum change that restores compliance.
4. Rebuild or rerun the affected test scope if available.
5. Summarize what was fixed, what was intentionally left alone, and any
   remaining migration debt.

## When To Switch Skills

- Switch to `spatial-app-architecture` when the core problem is scene
  ownership, feature decomposition, or state placement across surfaces.
- Switch to `build-run-debug` when the main blocker is a build failure or a
  runtime issue that still needs reproduction after standards fixes.
- Switch to `test-triage` when the work is primarily about narrowing a failing
  test scope rather than correcting standards violations directly.

## Guardrails

- Do not impose a blanket `@MainActor` policy. The isolation choice has to
  match ownership and runtime behavior.
- Do not "fix" concurrency warnings by introducing unnecessary `Task.detached`,
  `DispatchQueue.main.async`, or `@unchecked Sendable`.
- Do not modernize APIs mechanically if it changes semantics.

## Output Expectations

Provide:
- the files or symbols reviewed
- which standards category was applied
- the concrete violations fixed or still present
- the validation step used
- the next skill to use if the blocker is no longer a standards question
