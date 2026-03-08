# Model Review Wave 001

Last updated: 2026-03-09

## Purpose

This wave is the explicit synthetic-panel lane for `Codex`, `Claude`, and `Gemini`.

It exists to shadow-review the promoted strategy families before additional human calibration spend. It is not a replacement for human operator review.

Reference manifest:

- [operator_model_review_wave_001_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_model_review_wave_001_manifest.json)

## Included target

### 1. Promoted strategy shadow review

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

- these promoted strategy slices are the most important remaining calibration surface
- a synthetic panel can identify obvious evaluator-vs-operator disagreement before more human review bandwidth is spent
- the target overlaps the live human wave cleanly, so any later human returns can be compared against the same families

## Intended synthetic panel

Use exactly one independent review from each:

- `codex_reviewer_001`
- `claude_reviewer_001`
- `gemini_reviewer_001`

All three should review the exact same exported bundles independently.

## Suggested execution

One-command launcher:

```powershell
powershell -File scripts/launch_model_review_wave_001.ps1
```

This emits:

- `tmp_model_review_wave_001/calibration_study_run.json`
- `tmp_model_review_wave_001_bundles/model_review_prompt_export.json`

Each scenario bundle contains:

- `prompt.md`
- `context.json`
- `review_template.json`
- `trace.json`
- `score_report.json`

## What to send each model

Send each model:

- the scenario-specific `prompt.md`
- the matching `context.json`
- the matching `review_template.json`

Hard rules:

- review independently
- use only packet-visible information
- do not assume hidden simulator state
- return valid JSON only
- use the assigned reviewer id for that lane

## Provider-specific prompt packets

If you want ready-to-send packets with the reviewer id already filled in:

```powershell
powershell -File scripts/export_model_review_wave_001_provider_packets.ps1 -Provider claude
powershell -File scripts/export_model_review_wave_001_provider_packets.ps1 -Provider gemini
```

This emits:

- `tmp_model_review_wave_001_provider_packets/claude/provider_prompt_export.json`
- `tmp_model_review_wave_001_provider_packets/gemini/provider_prompt_export.json`

Each provider folder contains one subfolder per scenario with:

- `prompt.md`
- `context.json`
- `review_template.json`

## After model outputs come back

Save each raw response under a directory like:

- `tmp_model_review_wave_001_raw/codex`
- `tmp_model_review_wave_001_raw/claude`
- `tmp_model_review_wave_001_raw/gemini`

Then compile:

```powershell
powershell -File scripts/compile_model_review_wave_001.ps1 -RawReviewsDir tmp_model_review_wave_001_raw
```

Equivalent manual commands:

```bash
python -m thestartupbench import-model-reviews tmp_model_review_wave_001_raw --output-dir tmp_model_review_wave_001_results/import
python -m thestartupbench compile-calibration-study examples/operator_model_review_wave_001_manifest.json --study-run-dir tmp_model_review_wave_001 --review-paths <review-json-paths> --output-dir tmp_model_review_wave_001_results/report
```

## Decision rule after the wave

If all three model reviewers disagree with the benchmark scorer in the same direction on a family, escalate that family before making stronger maturity claims.

If the model panel disagrees sharply with itself, log that as a synthetic-panel disagreement cluster and defer to human review rather than smoothing it away.

If the model panel broadly agrees with the benchmark, treat that as triage support only, not as a substitute for operator evidence.
