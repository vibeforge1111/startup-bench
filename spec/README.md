# TheStartupBench Spec Package v0.2

Status: Draft

Version: `0.2.0-draft`

Last updated: 2026-03-07

This package turns the RFC into an implementation baseline.

It is organized into:

- `benchmark_contract.md`: benchmark-wide rules, tracks, modes, and invariants
- `scenario_spec.md`: scenario structure, lifecycle, and authoring contract
- `state_model.md`: canonical business world state partitions and visibility model
- `scenario_primitives.md`: reusable primitive library and composition rules
- `tool_contract.md`: tool surface, request/response semantics, and permissions
- `tool_schema_catalog.md`: canonical tool envelopes and domain-specific payload conventions
- `scoring_contract.md`: scoring, constraints, reporting, and evaluator behavior
- `trace_spec.md`: run trace format and logging requirements
- `runner_contract.md`: canonical execution lifecycle and runtime components
- `evaluator_contract.md`: evaluator types, interfaces, and aggregation rules
- `validation_contract.md`: validation pipeline and leaderboard eligibility checks
- `leaderboard_protocol.md`: submission, verification, contamination, and leaderboard policy
- `hidden_eval_policy.md`: hidden test/fresh split operation, refresh cadence, and redaction policy
- `operator_eval_protocol.md`: founder/operator review capture, calibration rubric, and promotion bar
- `../docs/pack_lifecycle_changelog.md`: public pack promotion, retirement, and contamination ledger
- `../examples/official_eval_profile.json`: reference official evaluation settings bundle
- `../examples/minimal_run_manifest.json`: reference official run-manifest artifact

Machine-readable schemas:

- `../schemas/tsb_scenario.schema.json`
- `../schemas/tsb_world_state.schema.json`
- `../schemas/tsb_primitives.schema.json`
- `../schemas/tsb_tool_manifest.schema.json`
- `../schemas/tsb_tool_call.schema.json`
- `../schemas/tsb_tool_response.schema.json`
- `../schemas/tsb_evaluator_result.schema.json`
- `../schemas/tsb_score_report.schema.json`
- `../schemas/tsb_batch_report.schema.json`
- `../schemas/tsb_scenario_suite.schema.json`
- `../schemas/tsb_public_suite_manifest.schema.json`
- `../schemas/tsb_pack_changelog.schema.json`
- `../schemas/tsb_official_eval_profile.schema.json`
- `../schemas/tsb_run_manifest.schema.json`
- `../schemas/tsb_suite_report.schema.json`
- `../schemas/tsb_trace.schema.json`
- `../schemas/tsb_submission.schema.json`
- `../schemas/tsb_operator_review.schema.json`
- `../schemas/tsb_operator_review_summary.schema.json`

Example:

- `../examples/minimal_b2b_saas_scenario.json`
- `../examples/minimal_crisis_scenario.json`
- `../examples/minimal_0to1_scenario.json`
- `../examples/minimal_board_scenario.json`
- `../examples/minimal_scale_scenario.json`
- `../examples/dev_scenario_suite.json`
- `../examples/private_test_scenario_suite.json`
- `../examples/private_real_world_fresh_scenario_suite.json`
- `../examples/official_eval_profile.json`
- `../examples/minimal_run_manifest.json`
- `../examples/minimal_public_suite_manifest.json`
- `../examples/real_world_public_fresh_manifest.json`
- `../examples/public_pack_changelog.json`
- `../examples/minimal_submission.json`
- `../examples/minimal_operator_review.json`
- `../examples/minimal_operator_review_summary.json`
- `../examples/minimal_world_state.json`
- `../examples/minimal_primitives.json`
- `../examples/minimal_tool_manifest.json`
- `../examples/minimal_score_report.json`

## Package goals

This package should be sufficient to:

- implement a runner
- author scenarios
- validate traces
- evaluate official submissions
- define leaderboard-grade runs

Reference implementation status:

- a Python reference package now exists under `src/thestartupbench/`
- schema-backed validation is implemented
- dry-run and scripted-run artifact generation is implemented
- heuristic baseline and repeated-run campaign aggregation are implemented
- reusable primitive-based event execution is implemented in the reference runtime
- suite-level scenario-pack execution and reporting are implemented
- redacted public manifests and submission assembly are implemented
- suite promotion and pack lifecycle validation are implemented
- official evaluation profiles and run manifests are implemented
- operator review aggregation and calibration artifacts are implemented
- smoke tests exist under `tests/`

## Canonical terms

- `benchmark version`: version of the benchmark contract and official scenario bundle
- `scenario version`: version of an individual scenario definition
- `scaffold version`: version of the official runtime and tool harness
- `track`: benchmark family slice such as `b2b_saas` or `crisis`
- `mode`: `dev`, `test`, or `fresh`
- `run`: one evaluation execution of one model/config on one scenario/seed pair
- `submission`: one leaderboard package referencing many runs

## Normative language

The words `MUST`, `SHOULD`, and `MAY` are used normatively.

## Scope

This package does not lock:

- exact economic equations
- exact UI surfaces
- exact scenario content

It does lock:

- evaluation contract
- trace contract
- scenario structure
- leaderboard submission rules
