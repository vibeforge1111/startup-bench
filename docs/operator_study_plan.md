# Operator Study Plan

Last updated: 2026-03-07

## Goal

This plan turns the new operator-review and calibration-report machinery into a concrete study sequence.

The current benchmark still lacks real founder/operator calibration. This document defines the minimum study wave needed to close that gap enough for a serious benchmark claim.

## Wave 001

Reference manifest: [operator_calibration_study_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_calibration_study_manifest.json)

Wave 001 targets:

- hidden canary test pack
- hidden strategy test pack
- hidden real-world test pack

These three families cover the benchmark's highest-risk methodology surfaces:

- exploit resistance
- long-horizon judgment
- crisis response under business pressure

## Reviewer mix

Minimum intended reviewer mix:

- founder or CEO
- product or growth operator
- finance, ops, or people operator

The current manifest sets reviewer quotas, but the practical rule is simpler: every target family should have at least two credible operator reviews before promotion.

## Required outputs

Every study target should produce:

- run trace artifacts
- score report artifacts
- operator reviews
- operator review summary
- calibration report

## Promotion gate

The current draft gate is:

- at least `2` reviewers per target family
- mean absolute rubric gap no worse than `0.75`
- recommendation agreement rate at least `0.67`

This is intentionally not permissive. If the evaluator disagrees with operators too often, the benchmark should not claim evaluator maturity.

## Why this matters

TheStartupBench is now closer to modern benchmark practice in two ways:

- hidden canary packs catch benchmark-specific overfitting
- operator studies let us test whether the scoring system agrees with actual startup operators

Without the second part, the benchmark can still look polished while being wrong in exactly the places that matter.

## Immediate next execution steps

1. Run the three target hidden suites with the intended baseline runners and fixed seed.
2. Collect at least two operator reviews per target family.
3. Aggregate reviews with `aggregate-operator-reviews`.
4. Compare the resulting review set against suite scores with `build-calibration-report`.
5. Record any scenario families where disagreement is high and either:
   - adjust evaluator logic
   - revise the scenario
   - mark the scenario family as not ready for promotion
