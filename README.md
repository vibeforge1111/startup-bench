# TheStartupBench

TheStartupBench is a benchmark project for evaluating how well agents and LLMs direct a startup under uncertainty.

Current release state:

- freeze label: `v0.9-precalibration`
- package version: `0.9.0`
- maturity: strong pre-human-calibration benchmark prototype

What this means:

- ready for technical contributors and early volunteers
- ready for research benchmarking
- not yet a finished public leaderboard benchmark

## Start Here

- Quick start: [docs/getting_started.md](/C:/Users/USER/Desktop/startup-bench/docs/getting_started.md)
- Evaluation flow: [docs/evaluation_modes.md](/C:/Users/USER/Desktop/startup-bench/docs/evaluation_modes.md)
- First Codex/Claude/Gemini trial: [docs/model_trial_wave_001.md](/C:/Users/USER/Desktop/startup-bench/docs/model_trial_wave_001.md)
- Full public dev trial: [docs/model_trial_wave_full_dev.md](/C:/Users/USER/Desktop/startup-bench/docs/model_trial_wave_full_dev.md)
- Contribution guide: [CONTRIBUTING.md](/C:/Users/USER/Desktop/startup-bench/CONTRIBUTING.md)
- Volunteer call: [docs/volunteer_call.md](/C:/Users/USER/Desktop/startup-bench/docs/volunteer_call.md)
- Founder/operator outreach: [docs/founder_operator_outreach.md](/C:/Users/USER/Desktop/startup-bench/docs/founder_operator_outreach.md)
- X post kit: [docs/x_post_kit.md](/C:/Users/USER/Desktop/startup-bench/docs/x_post_kit.md)

## Current Snapshot

- executable reference runtime
- hidden `test` and `fresh` packs
- canary anti-gaming packs
- official eval profile and run-manifest support
- multiple heuristic baseline families
- synthetic calibration completed on the clearest evaluator mismatches
- human review workflow prepared for later operator calibration

## Quick Commands

Install:

```bash
python -m pip install -e .
python -m thestartupbench version
```

Run one baseline:

```bash
python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_out
```

Run the public dev suite:

```bash
python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_out
```

Key documents:

- `THE_STARTUP_BENCH_RFC.md`
- `docs/getting_started.md`
- `docs/evaluation_modes.md`
- `docs/benchmark_status.md`
- `docs/sota_benchmark_audit.md`
- `docs/sota_reaudit.md`
- `docs/sota_task_roadmap.md`
- `docs/testing_coverage.md`
- `docs/pack_lifecycle_changelog.md`
- `docs/operator_study_plan.md`
- `docs/calibration_outcomes.md`
- `docs/human_review_wave_001.md`
- `docs/reviewer_outreach_wave_001.md`
- `docs/pre_human_calibration_execution_plan.md`
- `docs/frozen_active_packs.md`
- `docs/releases/v0.9-precalibration.md`
- `docs/benchmark_known_issues.md`
- `docs/evaluator_adjudication_log.md`
- `docs/pre_freeze_checklist.md`
- `docs/calibration_taskforce_strategy.md`
- `docs/reviewer_manual.md`
- `docs/model_reviewer_panel.md`
- `docs/model_review_prompt_guide.md`
- `CONTRIBUTING.md`
- `spec/README.md`
- `spec/benchmark_contract.md`
- `spec/scenario_spec.md`
- `spec/state_model.md`
- `spec/scenario_primitives.md`
- `spec/tool_contract.md`
- `spec/tool_schema_catalog.md`
- `spec/scoring_contract.md`
- `spec/trace_spec.md`
- `spec/runner_contract.md`
- `spec/evaluator_contract.md`
- `spec/validation_contract.md`
- `spec/leaderboard_protocol.md`
- `spec/hidden_eval_policy.md`
- `spec/operator_eval_protocol.md`

Artifacts:

- `schemas/tsb_scenario.schema.json`
- `schemas/tsb_world_state.schema.json`
- `schemas/tsb_primitives.schema.json`
- `schemas/tsb_tool_manifest.schema.json`
- `schemas/tsb_tool_call.schema.json`
- `schemas/tsb_tool_response.schema.json`
- `schemas/tsb_evaluator_result.schema.json`
- `schemas/tsb_score_report.schema.json`
- `schemas/tsb_batch_report.schema.json`
- `schemas/tsb_scenario_suite.schema.json`
- `schemas/tsb_public_suite_manifest.schema.json`
- `schemas/tsb_official_eval_profile.schema.json`
- `schemas/tsb_run_manifest.schema.json`
- `schemas/tsb_suite_report.schema.json`
- `schemas/tsb_trace.schema.json`
- `schemas/tsb_submission.schema.json`
- `schemas/tsb_operator_review.schema.json`
- `schemas/tsb_operator_review_summary.schema.json`
- `schemas/tsb_calibration_report.schema.json`
- `schemas/tsb_calibration_study.schema.json`
- `schemas/tsb_review_packet.schema.json`
- `schemas/tsb_calibration_study_run.schema.json`
- `schemas/tsb_calibration_study_report.schema.json`
- `schemas/tsb_review_assignments.schema.json`
- `schemas/tsb_review_form_export.schema.json`
- `schemas/tsb_review_form_import.schema.json`
- `examples/minimal_b2b_saas_scenario.json`
- `examples/minimal_crisis_scenario.json`
- `examples/minimal_0to1_scenario.json`
- `examples/minimal_board_scenario.json`
- `examples/minimal_gtm_scenario.json`
- `examples/minimal_finance_scenario.json`
- `examples/minimal_people_scenario.json`
- `examples/minimal_product_scenario.json`
- `examples/minimal_scale_scenario.json`
- `examples/dev_scenario_suite.json`
- `examples/private_test_scenario_suite.json`
- `examples/private_operator_test_scenario_suite.json`
- `examples/private_operator_fresh_scenario_suite.json`
- `examples/private_strategy_test_scenario_suite.json`
- `examples/private_strategy_fresh_scenario_suite.json`
- `examples/private_canary_test_scenario_suite.json`
- `examples/private_canary_fresh_scenario_suite.json`
- `examples/official_eval_profile.json`
- `examples/minimal_run_manifest.json`
- `examples/minimal_public_suite_manifest.json`
- `examples/minimal_submission.json`
- `examples/minimal_operator_review.json`
- `examples/minimal_operator_review_summary.json`
- `examples/minimal_calibration_report.json`
- `examples/operator_calibration_study_manifest.json`
- `examples/operator_human_review_wave_001_manifest.json`
- `examples/reviewer_roster_template.csv`
- `examples/operator_review_fill_template.json`
- `examples/minimal_world_state.json`
- `examples/minimal_primitives.json`
- `examples/minimal_tool_manifest.json`
- `examples/minimal_score_report.json`
- `examples/minimal_tool_script.json`

Implementation package:

- `pyproject.toml`
- `src/thestartupbench/`
- `tests/`

More CLI examples:

```bash
python -m thestartupbench version
python -m thestartupbench validate scenario examples/minimal_b2b_saas_scenario.json
python -m thestartupbench manifest examples/minimal_b2b_saas_scenario.json
python -m thestartupbench list-baselines
python -m thestartupbench lint-scenario examples/minimal_b2b_saas_scenario.json
python -m thestartupbench run-dry examples/minimal_b2b_saas_scenario.json --seed 1 --output-dir tmp_out
python -m thestartupbench run-script examples/minimal_b2b_saas_scenario.json examples/minimal_tool_script.json --seed 1 --output-dir tmp_out
python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_out
python -m thestartupbench run-campaign examples/minimal_crisis_scenario.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2,3 --max-turns 6 --output-dir tmp_out
python -m thestartupbench show-official-profile examples/official_eval_profile.json
python -m thestartupbench emit-run-manifest examples/dev_scenario_suite.json baseline --seeds 1,2,3,4,5 --baseline-id heuristic_resilient_operator --max-turns 8 --profile-path examples/official_eval_profile.json --output-dir tmp_out
python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_out
python -m thestartupbench redact-suite examples/private_test_scenario_suite.json --output-dir tmp_out
python -m thestartupbench check-suite-family examples/private_real_world_test_scenario_suite.json examples/private_real_world_fresh_scenario_suite.json
python -m thestartupbench check-suite-family examples/private_canary_test_scenario_suite.json examples/private_canary_fresh_scenario_suite.json
python -m thestartupbench aggregate-operator-reviews examples/minimal_operator_review.json --output-dir tmp_out
python -m thestartupbench build-calibration-report --suite-report-path tmp_out/suite_report.json --review-paths examples/minimal_operator_review.json --output-dir tmp_out
python -m thestartupbench run-calibration-study examples/operator_calibration_study_manifest.json --output-dir tmp_out
python -m thestartupbench assign-reviewers examples/operator_calibration_study_manifest.json --study-run-dir tmp_out --roster-path examples/reviewer_roster_template.csv --output-dir tmp_out
python -m thestartupbench export-review-forms tmp_out/review_assignments.json --output-dir tmp_out
python -m thestartupbench import-review-forms tmp_out --output-dir tmp_out
python -m thestartupbench export-model-review-bundles tmp_out --output-dir tmp_model_bundles
python -m thestartupbench import-model-reviews tmp_model_outputs --output-dir tmp_model_import
python -m thestartupbench compile-calibration-study examples/operator_calibration_study_manifest.json --study-run-dir tmp_out --review-paths examples/minimal_operator_review.json --output-dir tmp_out
powershell -File scripts/compile_human_review_wave_001.ps1 -CompletedFormsDir tmp_human_wave_completed_forms
python -m thestartupbench build-submission --suite-report-paths tmp_out/suite_report.json --model-id heuristic_resilient_operator --provider baseline --contamination-flag clean --output-dir tmp_out
python -m unittest discover -s tests -p "test_*.py"
```

Current reference runtime coverage:

- `metrics.query`
- `metrics.report`
- `product.roadmap.read`
- `product.roadmap.write`
- `sales.pipeline.read`
- `sales.pipeline.update`
- `sales.pricing.propose`
- `research.market.read`
- `finance.plan.read`
- `finance.plan.write`
- `finance.treasury.read`
- `finance.treasury.rebalance`
- `finance.raise.propose`
- `ops.incident.read`
- `ops.incident.respond`
- `ops.support.read`
- `ops.support.resolve`
- `people.hiring.read`
- `people.hiring.update`
- `people.org.read`
- `people.org.adjust`
- `legal.compliance.read`
- `legal.compliance.respond`
- `board.read`
- `board.update`
- `notes.read`
- `notes.write`
- `sim.advance`

Current state-transition coverage:

- tool handlers now route core mutations through a shared operation engine
- scheduled events may reference reusable `event_model.primitive_catalog` entries
- primitive operations currently support `set`, `increment`, `multiply`, `clamp`, and `append_unique`

Current built-in baselines:

- `heuristic_b2b_operator`
- `heuristic_governance_operator`
- `heuristic_liquidity_operator`
- `heuristic_long_horizon_operator`
- `heuristic_market_aware_operator`
- `heuristic_resilient_operator`

Current dev suite coverage:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `finance`
- `gtm`
- `people`
- `product`
- `scale`
