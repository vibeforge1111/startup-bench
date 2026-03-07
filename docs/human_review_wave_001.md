# Human Review Wave 001

Last updated: 2026-03-07

## Purpose

This wave is the first real human/operator calibration pass after the synthetic-panel corrections.

It is intentionally narrower than the broader hidden-pack calibration manifest. The goal is not broad coverage. The goal is to verify that the benchmark behaves sensibly on the exact slices where:

- synthetic reviewers found evaluator mistakes
- evaluator corrections were applied
- one governance-heavy scenario still deserves closer human scrutiny

Reference manifest:

- [operator_human_review_wave_001_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_001_manifest.json)

## Included targets

### 1. Canary confirmation

Suite:

- [human_review_wave_001_canary_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/human_review_wave_001_canary_suite.json)

Scenarios:

- `hidden_canary_pricing_trap_test_001`
- `hidden_canary_hiring_trap_test_001`

Reason:

- both required evaluator corrections
- both now align with the synthetic panel
- human reviewers should confirm that the corrected benchmark behavior is genuinely better

### 2. Strategy validation

Suite:

- [human_review_wave_001_strategy_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/human_review_wave_001_strategy_suite.json)

Scenarios:

- `hidden_board_stakeholder_conflict_test_001`
- `hidden_product_delayed_consequence_test_001`
- `hidden_scale_multi_quarter_test_001`

Reason:

- product and scale slices looked healthy under synthetic review
- board slice passed but remains a governance-severity watchlist
- human founders/operators are the right tool for that governance question

### 3. Real-world crisis confirmation

Suite:

- [human_review_wave_001_real_world_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/human_review_wave_001_real_world_suite.json)

Scenarios:

- `real_world_zoom_security_freeze_test_001`
- `real_world_brex_svb_treasury_shock_test_001`

Reason:

- both required evaluator corrections
- both now align with the synthetic panel at recommendation level
- human review should confirm that the corrections improved benchmark behavior rather than just mimicking model preferences

## Review bar

Minimum:

- `2` credible operators per target family

Preferred:

- `3` operators per target family
- at least one founder/CEO
- at least one finance/ops reviewer
- at least one product/growth reviewer where relevant

## What to watch closely

### Governance watchlist

`hidden_board_stakeholder_conflict_test_001` should be watched for:

- whether templated board updates are being scored too generously
- whether unresolved incidents are underweighted in governance-heavy scenarios
- whether human reviewers agree with Claude’s harsher governance read

### Crisis correction transfer

The two real-world crisis slices should be watched for:

- whether human reviewers also want the Zoom run scored `borderline`
- whether human reviewers also want the Brex run scored `borderline`
- whether the new evaluator penalties feel directionally correct rather than benchmark-specific

## Suggested execution

```bash
python -m thestartupbench run-calibration-study examples/operator_human_review_wave_001_manifest.json --output-dir tmp_human_wave_001
python -m thestartupbench assign-reviewers examples/operator_human_review_wave_001_manifest.json --study-run-dir tmp_human_wave_001 --roster-path examples/reviewer_roster_template.csv --output-dir tmp_human_wave_001
python -m thestartupbench export-review-forms tmp_human_wave_001/review_assignments.json --output-dir tmp_human_wave_001
```

After reviewers submit forms:

```bash
python -m thestartupbench import-review-forms tmp_human_wave_001 --output-dir tmp_human_wave_001_import
python -m thestartupbench compile-calibration-study examples/operator_human_review_wave_001_manifest.json --study-run-dir tmp_human_wave_001 --review-paths <review-json-paths> --output-dir tmp_human_wave_001_report
```

## Decision rule after the wave

If the wave agrees with the corrected benchmark on canary and real-world crisis slices, and does not strongly reject the board-scenario pass recommendation, then the benchmark should move from:

- synthetic-calibrated prototype

to:

- human-reviewed release candidate for the calibrated slices
