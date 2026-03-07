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
- `scoring_contract.md`: scoring, constraints, reporting, and evaluator behavior
- `trace_spec.md`: run trace format and logging requirements
- `leaderboard_protocol.md`: submission, verification, contamination, and leaderboard policy

Machine-readable schemas:

- `../schemas/tsb_scenario.schema.json`
- `../schemas/tsb_world_state.schema.json`
- `../schemas/tsb_primitives.schema.json`
- `../schemas/tsb_trace.schema.json`
- `../schemas/tsb_submission.schema.json`

Example:

- `../examples/minimal_b2b_saas_scenario.json`
- `../examples/minimal_world_state.json`
- `../examples/minimal_primitives.json`

## Package goals

This package should be sufficient to:

- implement a runner
- author scenarios
- validate traces
- evaluate official submissions
- define leaderboard-grade runs

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
