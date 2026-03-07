# Contributing

This repo is open to technical contributors, scenario authors, evaluator reviewers, and future calibration volunteers.

Current benchmark state:

- `v0.9-precalibration`
- usable for research and improvement work
- not yet a final public benchmark release

## Good Contribution Areas

High-value contributions right now:

- hidden scenario authoring
- runtime/world-model improvements
- evaluator regression tests
- baseline policy improvements
- documentation and onboarding cleanup
- benchmark governance and release hygiene

## What To Read First

- [docs/getting_started.md](/C:/Users/USER/Desktop/startup-bench/docs/getting_started.md)
- [docs/benchmark_status.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_status.md)
- [docs/benchmark_known_issues.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_known_issues.md)
- [docs/testing_coverage.md](/C:/Users/USER/Desktop/startup-bench/docs/testing_coverage.md)
- [spec/README.md](/C:/Users/USER/Desktop/startup-bench/spec/README.md)

## Ground Rules

- keep changes tightly scoped
- prefer extending existing mechanics over inventing new one-off logic
- preserve hidden-pack integrity
- do not commit local `tmp_*` artifacts or scratch files
- add or update tests when behavior changes
- keep benchmark claims conservative

## Before Opening A PR Or Sharing A Patch

Run at minimum:

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m thestartupbench check-pack-changelog examples/public_pack_changelog.json
```

If you changed a hidden suite, also run:

```bash
python -m thestartupbench check-suite-family <test-suite> <fresh-suite>
```

## Scenario Authoring Guidance

Prefer:

- reusing existing tool surfaces
- event-model primitives that map to real operating tradeoffs
- hidden scenarios that test one main lesson cleanly

Avoid:

- purely narrative scenarios with no programmatic consequences
- overly gameable one-turn tricks
- duplicating existing hidden slices with only cosmetic wording changes

## Calibration Contributions

Human calibration is not the same as normal benchmarking.

If you want to help later with calibration, read:

- [docs/human_review_wave_001.md](/C:/Users/USER/Desktop/startup-bench/docs/human_review_wave_001.md)
- [docs/reviewer_manual.md](/C:/Users/USER/Desktop/startup-bench/docs/reviewer_manual.md)
- [docs/calibration_taskforce_strategy.md](/C:/Users/USER/Desktop/startup-bench/docs/calibration_taskforce_strategy.md)

## Current Priority

The repo's biggest remaining gap is not core plumbing. It is benchmark scale and eventual human/operator validation.

So the strongest contributions are the ones that improve:

- hidden corpus breadth
- evaluator confidence
- onboarding clarity
- benchmark governance
