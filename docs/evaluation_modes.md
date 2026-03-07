# Evaluation Modes

`TheStartupBench` supports three distinct evaluation modes. They should not be mixed up.

## 1. Automated Benchmark Runs

This is the default benchmark path.

Flow:

- run a model or baseline on a scenario or suite
- emit trace, score report, suite report, and optional submission artifact
- evaluate with programmatic scoring

Use this for:

- baseline comparisons
- model benchmarking
- dev-suite iteration
- hidden-pack runs under controlled settings

Key commands:

```bash
python -m thestartupbench run-baseline ...
python -m thestartupbench run-suite ...
python -m thestartupbench emit-run-manifest ...
python -m thestartupbench build-submission ...
```

## 2. Calibration And Audit Runs

This mode checks whether the benchmark itself is rewarding the right behavior.

Flow:

- run a curated hidden study wave
- export review packets
- collect synthetic and/or human reviews
- compare benchmark scores to reviewer judgment

Use this for:

- evaluator audits
- scenario promotion decisions
- watchlist adjudication
- pre-human and post-human calibration work

Key commands:

```bash
python -m thestartupbench run-calibration-study ...
python -m thestartupbench export-model-review-bundles ...
python -m thestartupbench import-model-reviews ...
python -m thestartupbench import-review-forms ...
python -m thestartupbench compile-calibration-study ...
```

Important:

- calibration is not the same thing as normal benchmark scoring
- human review is used to validate benchmark quality, not to grade every run

## 3. Human Review Operations

This is the workflow for founder/operator review waves.

Flow:

- prepare a study run
- assign reviewers
- export forms
- collect filled forms
- import them back into benchmark artifacts

Use this for:

- founder/operator taskforces
- targeted review of governance, crisis, or canary slices
- validating whether the automated benchmark matches real startup judgment

Key commands:

```bash
python -m thestartupbench assign-reviewers ...
python -m thestartupbench export-review-forms ...
python -m thestartupbench import-review-forms ...
powershell -File scripts/compile_human_review_wave_001.ps1 -CompletedFormsDir ...
```

## Recommended Usage Right Now

Current repo state is `pre-human-calibration`.

That means:

- use automated runs freely
- use calibration runs to inspect evaluator behavior
- treat human review as the next validation layer, not as a prerequisite for trying the benchmark

## What Not To Do

Do not:

- present synthetic panel agreement as equivalent to human/operator validation
- treat hidden-pack scores as public benchmark truth without the benchmark's documented caveats
- mix dev-suite exploratory runs with official-style evaluation claims
