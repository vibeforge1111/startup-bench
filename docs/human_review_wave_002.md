# Human Review Wave 002

Last updated: 2026-03-08

## Purpose

This wave is the second real human/operator calibration pass.

It is narrower than the full hidden strategy pack and more focused than wave 001. The goal is to verify that the promoted strategy families added after the first human wave behave sensibly under real operator review before those slices inherit stronger calibration claims.

Reference manifest:

- [operator_human_review_wave_002_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_002_manifest.json)

Reviewer handoff copy:

- [reviewer_outreach_wave_002.md](/C:/Users/USER/Desktop/startup-bench/docs/reviewer_outreach_wave_002.md)

## Included target

### 1. Promoted strategy families

Suite:

- [human_review_wave_002_strategy_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/human_review_wave_002_strategy_suite.json)

Scenarios:

- `hidden_board_financing_truth_test_001`
- `hidden_board_incident_truth_test_001`
- `hidden_scale_platform_sequence_test_001`
- `hidden_product_migration_sequence_test_001`
- `hidden_board_product_truth_test_001`
- `hidden_gtm_multi_quarter_sequence_test_001`
- `hidden_scale_finance_tradeoff_test_001`

Reason:

- these strategy slices were promoted after wave 001 and should not be treated as calibrated by default
- together they cover the newest board, product, scale, GTM, and finance-interaction strategy additions
- this is the cleanest next human wave because it tests benchmark depth growth without drifting into legal or jurisdiction-specific judgment

## Review bar

Minimum:

- `2` credible operators for the target family

Preferred:

- `3` operators for the target family
- at least one founder or CEO
- at least one finance or ops reviewer
- at least one product, growth, or GTM reviewer

## What to watch closely

### Financing truth

`hidden_board_financing_truth_test_001` and `hidden_scale_finance_tradeoff_test_001` should be watched for:

- whether the benchmark rewards explicit financing realism over narrative management
- whether dilution, pacing, and runway tradeoffs feel directionally correct
- whether the evaluator is too forgiving when operators defer painful capital-quality choices

### Board and product readiness truth

`hidden_board_incident_truth_test_001` and `hidden_board_product_truth_test_001` should be watched for:

- whether board communication quality is being rewarded only when it is paired with real operational follow-through
- whether unresolved readiness and trust gaps are penalized hard enough
- whether the benchmark is accidentally over-rewarding polished updates

### Multi-quarter sequencing

`hidden_scale_platform_sequence_test_001`, `hidden_product_migration_sequence_test_001`, and `hidden_gtm_multi_quarter_sequence_test_001` should be watched for:

- whether long-horizon tradeoffs look like real sequencing rather than benchmark-shaped cleanup loops
- whether delayed consequences are scored strongly enough
- whether operators agree with the benchmark on when to invest early versus defer

## Suggested execution

One-command launcher:

```powershell
powershell -File scripts/launch_human_review_wave_002.ps1
```

Equivalent manual commands:

```bash
python -m thestartupbench run-calibration-study examples/operator_human_review_wave_002_manifest.json --output-dir tmp_human_wave_002
python -m thestartupbench assign-reviewers examples/operator_human_review_wave_002_manifest.json --study-run-dir tmp_human_wave_002 --roster-path examples/reviewer_roster_template.csv --output-dir tmp_human_wave_002
python -m thestartupbench export-review-forms tmp_human_wave_002/review_assignments.json --output-dir tmp_human_wave_002
```

After reviewers submit forms:

```bash
python -m thestartupbench import-review-forms tmp_human_wave_002 --output-dir tmp_human_wave_002_results/import
python -m thestartupbench compile-calibration-study examples/operator_human_review_wave_002_manifest.json --study-run-dir tmp_human_wave_002 --review-paths <review-json-paths> --output-dir tmp_human_wave_002_results/report
```

PowerShell helper:

```powershell
powershell -File scripts/compile_human_review_wave_002.ps1 -CompletedFormsDir <folder-with-returned-csvs>
```

After the human study report exists, compare it against the completed synthetic panel:

```powershell
powershell -File scripts/compare_model_vs_human_wave_002.ps1
```

Current live wave-002 run directory:

- `tmp_human_wave_002`

Current exported reviewer packets:

- `founder_001`
- `ops_001`
- `product_001`

## Decision rule after the wave

If operators broadly agree that these promoted strategy slices are directionally sound, then the benchmark can claim stronger human-reviewed coverage for the expanded strategy pack.

If disagreement is material, the benchmark should:

- log the disagreement explicitly
- revise evaluator logic or scenario mechanics where needed
- keep the affected family out of stronger maturity claims until the disagreement is understood
