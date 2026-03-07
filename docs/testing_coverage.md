# TheStartupBench Testing And Smoke Coverage

Last updated: 2026-03-07

## Current Snapshot

Current automated test surface:

- `53` unit tests
- `12` test files
- all tests passing in the current tree

The test suite is strongest on schema validation, core runtime mutations, baseline execution, and suite/submission packaging. It is weakest on evaluator nuance, adversarial scenario behavior, and broader scenario-corpus regression coverage.

## Unit Test Inventory

### Validation and artifacts

- [test_validation.py](/C:/Users/USER/Desktop/startup-bench/tests/test_validation.py): `10` tests
- [test_validation.py](/C:/Users/USER/Desktop/startup-bench/tests/test_validation.py): `12` tests
  - validates example scenarios
  - validates world state and suite artifacts
  - validates public manifest and submission examples

### Core runner flows

- [test_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_runner.py): `4` tests
  - dry-run artifact emission
  - trace integrity
  - observation projection
  - tool manifest generation

- [test_script_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_script_runner.py): `3` tests
  - scripted execution emits valid artifacts
  - time advancement works
  - undeclared tool calls are rejected

### Runtime mechanics

- [test_runtime.py](/C:/Users/USER/Desktop/startup-bench/tests/test_runtime.py): `16` tests
  - finance plan write behavior
  - metrics querying and reporting
  - immutable read snapshots
  - roadmap updates
  - pipeline and pricing updates
  - scheduled event processing
  - board state updates
  - incident read/respond behavior
  - support backlog resolution
  - treasury rebalancing
  - financing proposals
  - org health adjustments
  - legal/compliance response

- [test_primitive_engine.py](/C:/Users/USER/Desktop/startup-bench/tests/test_primitive_engine.py): `3` tests
  - primitive application
  - primitive catalog resolution
  - dotted-path reads

- [test_scenario_lint.py](/C:/Users/USER/Desktop/startup-bench/tests/test_scenario_lint.py): `2` tests
  - positive lint pass
  - unknown primitive reference detection

### Baselines and aggregation

- [test_baseline_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_baseline_runner.py): `3` tests
  - baseline registry
  - baseline artifact emission and improvement over dry-run
  - resilient baseline outperforming generic baseline on crisis

- [test_campaign_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_campaign_runner.py): `2` tests
  - seed parsing
  - batch report emission

- [test_suite_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_suite_runner.py): `2` tests
  - suite report emission
  - resilient baseline improves suite pass rate

### Hidden-eval packaging

- [test_suite_manifest.py](/C:/Users/USER/Desktop/startup-bench/tests/test_suite_manifest.py): `1` test
- [test_suite_manifest.py](/C:/Users/USER/Desktop/startup-bench/tests/test_suite_manifest.py): `2` tests
  - redacted manifest generation

- [test_submission_builder.py](/C:/Users/USER/Desktop/startup-bench/tests/test_submission_builder.py): `1` test
  - submission assembly from suite report

### Real-world-derived scenario pack

- [test_real_world_scenarios.py](/C:/Users/USER/Desktop/startup-bench/tests/test_real_world_scenarios.py): `3` tests
  - validates the ten real-world-derived scenarios
  - lints the same scenario pack
  - runs the real-world suite with the resilient baseline

## Smoke Test Commands

Current note:

- from a raw checkout, the CLI currently needs `PYTHONPATH=src` or an editable install
- `python -m pip install -e .` was verified locally and enables clean-shell `python -m thestartupbench ...`

The following smoke commands are the minimum end-to-end checks worth preserving as a release gate:

```bash
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_b2b_saas_scenario.json
PYTHONPATH=src python -m thestartupbench lint-scenario examples/minimal_b2b_saas_scenario.json
PYTHONPATH=src python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-trace tmp_smoke/trace.json
PYTHONPATH=src python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench redact-suite examples/private_test_scenario_suite.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench build-submission --suite-report-paths tmp_smoke/suite_report.json --model-id heuristic_resilient_operator --provider baseline --contamination-flag clean --output-dir tmp_smoke
python -m unittest discover -s tests -p "test_*.py"
```

## Smoke Test Results Observed In This Tree

Observed on 2026-03-07:

- `validate scenario ...minimal_b2b_saas_scenario.json`: passed
- `lint-scenario ...minimal_b2b_saas_scenario.json`: passed
- `run-baseline ...minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6`: passed
  - emitted schema-valid trace and score report
  - observed crisis scenario score: `0.7459`
  - observed pass: `true`
- `check-trace tmp_smoke/trace.json`: passed
  - schema validation: `ok`
  - integrity validation: `ok`
- `run-suite ...dev_scenario_suite.json ... --seeds 1,2 --max-turns 4`: passed
  - scenario count: `5`
  - overall score mean: `0.7178`
  - overall pass-rate mean: `1.0`
- `run-suite ...real_world_crisis_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `10`
  - overall score mean: `0.719`
  - overall pass-rate mean: `1.0`
- `redact-suite ...private_real_world_test_scenario_suite.json`: passed
  - scenario count: `5`
  - scenario pack version: `real-world-test-pack-0.1.0`
- `run-suite ...private_real_world_test_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `5`
  - overall score mean: `0.7351`
  - overall pass-rate mean: `1.0`
- `redact-suite ...private_test_scenario_suite.json`: passed
- `build-submission ...tmp_smoke/suite_report.json ...`: passed
  - repeat count: `2`
  - model id: `heuristic_resilient_operator`
  - contamination flag: `clean`
- `python -m pip install -e .`: passed
- `python -m thestartupbench version`: passed
  - reported version: `0.1.0`
- `python -m unittest discover -s tests -p "test_*.py"`: passed
  - `53` tests
  - `12` files

## What Is Covered Well

Covered reasonably well:

- schema compliance for checked-in artifacts
- dry, scripted, baseline, campaign, and suite runner plumbing
- core runtime mutations for finance, sales, product, board, and crisis actions
- event primitive application
- redacted hidden-eval packaging
- submission assembly

## What Is Only Lightly Covered

Covered only lightly:

- scoring sensitivity and failure-threshold tuning
- interactions across multiple simultaneous crisis dimensions
- long-horizon compounding effects across many turns
- negative/adversarial scenario authoring cases beyond a few lint failures
- regression coverage for all current example scenarios under multiple seeds
- baseline stability across larger suite packs

## What Is Not Covered Yet

Not covered yet:

- human baseline reproducibility
- contamination and leaderboard workflow checks
- performance/load testing of the runner itself
- reproducibility across different environments
- semantic judging for communication artifacts

## Recommended Next Testing Additions

1. Add evaluator-focused tests that lock expected score behavior for edge cases and tradeoff-heavy scenarios.
2. Add multi-turn crisis regression tests with stacked events and delayed consequences.
3. Add suite-level regression snapshots so track coverage changes are deliberate.
4. Add tests for future people, fundraising, compliance, and market-state mechanics as those subsystems land.
5. Add artifact upload and branch-protection enforcement on top of the new CI workflow.

## Bottom Line

The current test surface is solid for a fast-moving prototype benchmark. It is not yet sufficient for benchmark-standard claims, because the highest-risk areas now are scenario breadth, evaluator quality, and benchmark governance rather than basic artifact validity or CLI execution.
