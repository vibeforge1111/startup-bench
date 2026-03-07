# TheStartupBench Testing And Smoke Coverage

Last updated: 2026-03-08

## Current Snapshot

Current automated test surface:

- `122` unit tests
- `24` test files
- all tests passing in the current tree

The test suite is strongest on schema validation, core runtime mutations, baseline execution, and suite/submission packaging. It is weakest on evaluator nuance, adversarial scenario behavior, and broader scenario-corpus regression coverage.

## Unit Test Inventory

### Validation and artifacts

- [test_validation.py](/C:/Users/USER/Desktop/startup-bench/tests/test_validation.py): `23` tests
  - validates example scenarios
  - validates world state and suite artifacts
  - validates public manifests, pack changelog, submission examples, operator-review summaries, calibration reports, and calibration-study manifests

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

- [test_runtime.py](/C:/Users/USER/Desktop/startup-bench/tests/test_runtime.py): `19` tests
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
  - hiring funnel updates
  - org health adjustments
  - legal/compliance response
  - market research reads
  - market and staffing weekly drift

- [test_primitive_engine.py](/C:/Users/USER/Desktop/startup-bench/tests/test_primitive_engine.py): `3` tests
  - primitive application
  - primitive catalog resolution
  - dotted-path reads

- [test_scenario_lint.py](/C:/Users/USER/Desktop/startup-bench/tests/test_scenario_lint.py): `2` tests
  - positive lint pass
  - unknown primitive reference detection

### Baselines and aggregation

- [test_evaluators.py](/C:/Users/USER/Desktop/startup-bench/tests/test_evaluators.py): `7` tests
  - GTM revenue and customer scores fall under stronger market and segment pressure
  - people-track strategic coherence improves after hiring and market-response actions
  - canary GTM pricing-trap penalty
  - canary people hiring-trap penalty
  - Zoom crisis penalty
  - Brex treasury-shock penalty
  - board/governance penalty for repeated boilerplate and missing follow-through

- [test_baseline_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_baseline_runner.py): `6` tests
  - baseline registry
  - baseline artifact emission and improvement over dry-run
  - resilient baseline outperforming generic baseline on crisis
  - market-aware baseline outperforming generic baseline on GTM
  - long-horizon baseline outperforming generic baseline on delayed-consequence product work
  - long-horizon baseline emits state-aware board updates on board-track work

- [test_campaign_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_campaign_runner.py): `2` tests
  - seed parsing
  - batch report emission

- [test_suite_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_suite_runner.py): `2` tests
  - suite report emission
  - resilient baseline improves suite pass rate

- [test_official_eval.py](/C:/Users/USER/Desktop/startup-bench/tests/test_official_eval.py): `4` tests
  - official profile loading
  - run-manifest generation
  - disallowed runner rejection
  - official-manifest-compatible suite flow

- [test_human_eval.py](/C:/Users/USER/Desktop/startup-bench/tests/test_human_eval.py): `3` tests
  - validates operator-review and summary examples
  - aggregates multiple operator reviews into a calibration summary
  - flags reviewer disagreement at the scenario level

- [test_calibration.py](/C:/Users/USER/Desktop/startup-bench/tests/test_calibration.py): `2` tests
  - aligns operator reviews to suite reports and emits a calibration report
  - validates the example calibration report artifact

- [test_study_runner.py](/C:/Users/USER/Desktop/startup-bench/tests/test_study_runner.py): `2` tests
  - runs an executable calibration study wave and emits review packets
  - compiles partial operator reviews into a study-level calibration report

- [test_reviewer_ops.py](/C:/Users/USER/Desktop/startup-bench/tests/test_reviewer_ops.py): `2` tests
  - assigns reviewers from a roster into a valid assignment manifest
  - exports reviewer-facing forms and imports a completed CSV back into valid operator-review JSON

- [test_model_reviewer_ops.py](/C:/Users/USER/Desktop/startup-bench/tests/test_model_reviewer_ops.py): `2` tests
  - exports scenario-scoped model-review prompt bundles from a calibration study run
  - imports fenced raw model outputs into valid operator-review JSON while reporting rejected files

### Hidden-eval packaging

- [test_suite_manifest.py](/C:/Users/USER/Desktop/startup-bench/tests/test_suite_manifest.py): `2` tests
  - redacted manifest generation

- [test_pack_ops.py](/C:/Users/USER/Desktop/startup-bench/tests/test_pack_ops.py): `5` tests
  - hidden split cloning is rejected by default
  - draft-only split cloning is explicit
  - distinct hidden `test` and `fresh` packs validate cleanly
  - duplicate hidden ids and paths are rejected
  - public pack changelog validates cleanly

- [test_submission_builder.py](/C:/Users/USER/Desktop/startup-bench/tests/test_submission_builder.py): `1` test
  - submission assembly from suite report

### Real-world-derived scenario pack

- [test_real_world_scenarios.py](/C:/Users/USER/Desktop/startup-bench/tests/test_real_world_scenarios.py): `3` tests
  - validates the ten real-world-derived scenarios
  - lints the same scenario pack
  - runs the real-world suite with the resilient baseline

### Hidden breadth packs

- [test_operator_hidden_suite.py](/C:/Users/USER/Desktop/startup-bench/tests/test_operator_hidden_suite.py): `4` tests
  - validates hidden operator `test` suite
  - runs hidden operator `test` suite
  - validates and runs hidden operator `fresh` suite
  - checks hidden operator `test` and `fresh` suite-family integrity

- [test_strategy_hidden_suite.py](/C:/Users/USER/Desktop/startup-bench/tests/test_strategy_hidden_suite.py): `4` tests
  - validates hidden strategy `test` suite
  - runs hidden strategy `test` suite with the long-horizon baseline
  - validates and runs hidden strategy `fresh` suite
  - checks hidden strategy `test` and `fresh` suite-family integrity

- [test_canary_hidden_suite.py](/C:/Users/USER/Desktop/startup-bench/tests/test_canary_hidden_suite.py): `4` tests
  - validates hidden canary `test` suite
  - runs hidden canary `test` suite with the market-aware baseline
  - validates and runs hidden canary `fresh` suite
  - checks hidden canary `test` and `fresh` suite-family integrity

## Smoke Test Commands

Current note:

- from a raw checkout, the CLI currently needs `PYTHONPATH=src` or an editable install
- `python -m pip install -e .` was verified locally and enables clean-shell `python -m thestartupbench ...`

The following smoke commands are the minimum end-to-end checks worth preserving as a release gate:

```bash
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_b2b_saas_scenario.json
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_gtm_scenario.json
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_finance_scenario.json
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_people_scenario.json
PYTHONPATH=src python -m thestartupbench validate scenario examples/minimal_product_scenario.json
PYTHONPATH=src python -m thestartupbench lint-scenario examples/minimal_b2b_saas_scenario.json
PYTHONPATH=src python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-trace tmp_smoke/trace.json
PYTHONPATH=src python -m thestartupbench show-official-profile examples/official_eval_profile.json
PYTHONPATH=src python -m thestartupbench emit-run-manifest examples/dev_scenario_suite.json baseline --seeds 1,2,3,4,5 --baseline-id heuristic_resilient_operator --max-turns 8 --profile-path examples/official_eval_profile.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench redact-suite examples/private_test_scenario_suite.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-suite-family examples/private_real_world_test_scenario_suite.json examples/private_real_world_fresh_scenario_suite.json
PYTHONPATH=src python -m thestartupbench check-suite-family examples/private_operator_test_scenario_suite.json examples/private_operator_fresh_scenario_suite.json
PYTHONPATH=src python -m thestartupbench run-suite examples/private_operator_test_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1 --max-turns 3 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench run-suite examples/private_operator_fresh_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1 --max-turns 3 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-suite-family examples/private_canary_test_scenario_suite.json examples/private_canary_fresh_scenario_suite.json
PYTHONPATH=src python -m thestartupbench run-suite examples/private_canary_test_scenario_suite.json baseline --baseline-id heuristic_market_aware_operator --seeds 1 --max-turns 4 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench run-suite examples/private_canary_fresh_scenario_suite.json baseline --baseline-id heuristic_market_aware_operator --seeds 1 --max-turns 4 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-suite-family examples/private_strategy_test_scenario_suite.json examples/private_strategy_fresh_scenario_suite.json
PYTHONPATH=src python -m thestartupbench run-suite examples/private_strategy_test_scenario_suite.json baseline --baseline-id heuristic_long_horizon_operator --seeds 1 --max-turns 6 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench run-suite examples/private_strategy_fresh_scenario_suite.json baseline --baseline-id heuristic_long_horizon_operator --seeds 1 --max-turns 6 --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench redact-suite examples/private_real_world_fresh_scenario_suite.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench redact-suite examples/private_operator_fresh_scenario_suite.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench check-pack-changelog examples/public_pack_changelog.json
PYTHONPATH=src python -m thestartupbench aggregate-operator-reviews examples/minimal_operator_review.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench build-calibration-report --suite-report-path tmp_smoke/suite_report.json --review-paths examples/minimal_operator_review.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench run-calibration-study examples/operator_calibration_study_manifest.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench assign-reviewers examples/operator_calibration_study_manifest.json --study-run-dir tmp_smoke --roster-path examples/reviewer_roster_template.csv --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench export-review-forms tmp_smoke/review_assignments.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench export-model-review-bundles tmp_smoke --output-dir tmp_model_review_bundles
PYTHONPATH=src python -m thestartupbench import-model-reviews tmp_model_raw --output-dir tmp_model_import
PYTHONPATH=src python -m thestartupbench compile-calibration-study examples/operator_calibration_study_manifest.json --study-run-dir tmp_smoke --review-paths examples/minimal_operator_review.json --output-dir tmp_smoke
PYTHONPATH=src python -m thestartupbench build-submission --suite-report-paths tmp_smoke/suite_report.json --model-id heuristic_resilient_operator --provider baseline --contamination-flag clean --output-dir tmp_smoke
python -m unittest discover -s tests -p "test_*.py"
```

## Smoke Test Results Observed In This Tree

Observed on 2026-03-08:

- `validate scenario ...minimal_b2b_saas_scenario.json`: passed
- `lint-scenario ...minimal_b2b_saas_scenario.json`: passed
- `run-baseline ...minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6`: passed
  - emitted schema-valid trace and score report
  - observed crisis scenario score: `0.7459`
  - observed pass: `true`
- `check-trace tmp_smoke/trace.json`: passed
  - schema validation: `ok`
  - integrity validation: `ok`
- `show-official-profile ...official_eval_profile.json`: passed
  - hosted evaluation: `true`
  - allowed runner types: `baseline`, `script`
- `emit-run-manifest ...dev_scenario_suite.json baseline --seeds 1,2,3,4,5 ...`: passed
  - repeated run count: `5`
  - profile id: `official-hosted-v0.9.0`
- `run-suite ...dev_scenario_suite.json ... --seeds 1,2 --max-turns 4 --profile-path ...`: passed
  - scenario count: `9`
  - overall score mean: `0.7257`
  - overall pass-rate mean: `1.0`
  - emitted run manifest alongside suite report
- `run-suite ...real_world_crisis_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `10`
  - overall score mean: `0.719`
  - overall pass-rate mean: `1.0`
- `redact-suite ...private_real_world_test_scenario_suite.json`: passed
  - scenario count: `8`
  - scenario pack version: `real-world-test-pack-0.3.0`
- `run-suite ...private_real_world_test_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `8`
  - overall score mean: `0.7093`
  - overall pass-rate mean: `1.0`
- `run-suite ...private_real_world_fresh_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `8`
  - overall score mean: `0.6943`
  - overall pass-rate mean: `0.875`
- `check-suite-family ...private_real_world_test_scenario_suite.json ...private_real_world_fresh_scenario_suite.json`: passed
  - suite count: `2`
  - issues: `0`
- `check-suite-family ...private_operator_test_scenario_suite.json ...private_operator_fresh_scenario_suite.json`: passed
  - suite count: `2`
  - issues: `0`
- `run-suite ...private_operator_test_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `9`
  - overall score mean: `0.7393`
  - overall pass-rate mean: `1.0`
- `run-suite ...private_operator_fresh_scenario_suite.json ... --seeds 1 --max-turns 3`: passed
  - scenario count: `9`
  - overall score mean: `0.7261`
  - overall pass-rate mean: `1.0`
- `check-suite-family ...private_canary_test_scenario_suite.json ...private_canary_fresh_scenario_suite.json`: passed
  - suite count: `2`
  - issues: `0`
- `run-suite ...private_canary_test_scenario_suite.json ...heuristic_market_aware_operator --seeds 1 --max-turns 4`: passed
  - scenario count: `2`
  - overall score mean: `0.6469`
  - overall pass-rate mean: `1.0`
- `run-suite ...private_canary_fresh_scenario_suite.json ...heuristic_market_aware_operator --seeds 1 --max-turns 4`: passed
  - scenario count: `2`
  - overall score mean: `0.6084`
  - overall pass-rate mean: `1.0`
- `check-suite-family ...private_strategy_test_scenario_suite.json ...private_strategy_fresh_scenario_suite.json`: passed
  - suite count: `2`
  - issues: `0`
- `run-suite ...private_strategy_test_scenario_suite.json ...heuristic_governance_operator --seeds 1 --max-turns 6`: passed
  - scenario count: `5`
  - overall score mean: `0.763`
  - overall pass-rate mean: `1.0`
- `run-suite ...private_strategy_fresh_scenario_suite.json ...heuristic_governance_operator --seeds 1 --max-turns 6`: passed
  - scenario count: `5`
  - overall score mean: `0.7588`
  - overall pass-rate mean: `1.0`
- `promote-suite ...private_real_world_test_scenario_suite.json --split fresh --scenario-pack-version real-world-fresh-pack-0.2.0`: correctly rejected by default
  - result: `ok: false`
  - reason: hidden split cloning now requires explicit draft-only override
- `check-pack-changelog ...public_pack_changelog.json`: passed
  - changelog entry count: `25`
  - validation: `ok`
- `aggregate-operator-reviews ...minimal_operator_review.json`: passed
  - review count: `1`
  - reviewer count: `1`
  - scenario count: `1`
- `build-calibration-report --suite-report-path ... --review-paths ...minimal_operator_review.json`: passed
  - matched scenario count: `1`
  - mean absolute rubric gap: `0.0684`
  - recommendation agreement rate: `1.0`
- `run-calibration-study ...operator_calibration_study_manifest.json`: passed
  - target count: `3`
  - canary, strategy, and real-world review packets emitted
- `assign-reviewers ...operator_calibration_study_manifest.json --roster-path ...reviewer_roster_template.csv`: passed
  - assignment count: `6`
  - founder, product, and ops reviewers were distributed across the target families
- `export-review-forms ...review_assignments.json`: passed
  - reviewer count: `3`
  - reviewer-facing Markdown and CSV forms emitted
- `export-model-review-bundles tmp_smoke --output-dir tmp_model_review_bundles`: passed
  - bundle count: `10`
  - scenario-scoped prompt bundles emitted
- `import-model-reviews tmp_model_raw --output-dir tmp_model_import`: passed with one intentional rejection
  - imported review count: `1`
  - rejected file count: `1`
  - fenced JSON response normalized into a valid operator-review artifact
- `compile-calibration-study ...operator_calibration_study_manifest.json ...minimal_operator_review.json`: passed
  - completed target count: `1`
  - pending target count: `2`
  - mean absolute rubric gap: `0.0684`
  - recommendation agreement rate: `1.0`
- `redact-suite ...private_test_scenario_suite.json`: passed
- `build-submission ...tmp_smoke/suite_report.json ...`: passed
  - repeat count: `2`
  - model id: `heuristic_resilient_operator`
  - contamination flag: `clean`
- `python -m pip install -e .`: passed
- `python -m thestartupbench version`: passed
  - reported version: `0.9.0`
- `python -m unittest discover -s tests -p "test_*.py"`: passed
  - `122` tests
  - `24` files

## What Is Covered Well

Covered reasonably well:

- schema compliance for checked-in artifacts
- dry, scripted, baseline, campaign, and suite runner plumbing
- core runtime mutations for finance, sales, product, board, and crisis actions
- first-pass runtime mutations for hiring funnels, customer segments, and market/competitor drift
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
