# Getting Started

This is the fastest way to understand and run `TheStartupBench` without reading the whole repo.

## What This Repo Is

`TheStartupBench` is a pre-human-calibration benchmark for evaluating how well models and agents operate a startup under uncertainty.

Current state:

- executable reference runtime
- hidden `test` and `fresh` packs
- canary anti-gaming packs
- official eval profile and run-manifest artifacts
- synthetic calibration completed on the highest-risk evaluator gaps
- human review workflow prepared, but not yet broadly run

This means:

- good for research and technical contributors now
- not yet a finished public benchmark leaderboard

## Install

From the repo root:

```bash
python -m pip install -e .
python -m thestartupbench version
```

Expected current version:

- `0.9.0`

## Fastest First Commands

Validate one scenario:

```bash
python -m thestartupbench validate scenario examples/minimal_b2b_saas_scenario.json
```

Run one baseline:

```bash
python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_out
```

Run the public dev suite:

```bash
python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_out
```

List baselines:

```bash
python -m thestartupbench list-baselines
```

## Which Files Matter

If you want to use the benchmark:

- [README.md](/C:/Users/USER/Desktop/startup-bench/README.md)
- [docs/evaluation_modes.md](/C:/Users/USER/Desktop/startup-bench/docs/evaluation_modes.md)
- [examples/official_eval_profile.json](/C:/Users/USER/Desktop/startup-bench/examples/official_eval_profile.json)

If you want to understand benchmark status:

- [docs/benchmark_status.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_status.md)
- [docs/benchmark_known_issues.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_known_issues.md)
- [docs/pack_lifecycle_changelog.md](/C:/Users/USER/Desktop/startup-bench/docs/pack_lifecycle_changelog.md)

If you want to contribute:

- [CONTRIBUTING.md](/C:/Users/USER/Desktop/startup-bench/CONTRIBUTING.md)
- [docs/testing_coverage.md](/C:/Users/USER/Desktop/startup-bench/docs/testing_coverage.md)
- [spec/README.md](/C:/Users/USER/Desktop/startup-bench/spec/README.md)

If you want to help calibrate later:

- [docs/human_review_wave_001.md](/C:/Users/USER/Desktop/startup-bench/docs/human_review_wave_001.md)
- [docs/reviewer_manual.md](/C:/Users/USER/Desktop/startup-bench/docs/reviewer_manual.md)
- [docs/calibration_taskforce_strategy.md](/C:/Users/USER/Desktop/startup-bench/docs/calibration_taskforce_strategy.md)

## Current Evaluation Surface

Public/example tracks:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `finance`
- `gtm`
- `people`
- `product`
- `scale`

Current built-in baselines:

- `heuristic_b2b_operator`
- `heuristic_governance_operator`
- `heuristic_liquidity_operator`
- `heuristic_long_horizon_operator`
- `heuristic_market_aware_operator`
- `heuristic_resilient_operator`

## Current Limitations

Be explicit about these when sharing the repo:

- hidden corpus is still prototype-scale, not benchmark-scale
- human/operator calibration is not complete yet
- this is a strong reference benchmark implementation, not a final public leaderboard benchmark

## Next Step

If you only do one thing next, do this:

```bash
python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_out
```

Then inspect:

- `tmp_out/suite_report.json`
- `tmp_out/run_manifest.json`
