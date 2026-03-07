# Trace Specification

## 1. Trace purpose

The trace is the canonical artifact for replay, audit, debugging, and leaderboard verification.

Every official run MUST emit one trace file matching the trace schema.

## 2. Required top-level sections

- `trace_version`
- `benchmark`
- `scenario`
- `agent`
- `runtime`
- `turns`
- `state_snapshots`
- `evaluation`

## 3. Benchmark section

Required fields:

- `benchmark_name`
- `benchmark_version`
- `scaffold_version`

## 4. Scenario section

Required fields:

- `scenario_id`
- `scenario_version`
- `track`
- `mode`
- `seed`

## 5. Agent section

Required fields:

- `model_id`
- `provider`
- `agent_config_hash`
- `system_prompt_hash`

Optional fields:

- `agent_name`
- `agent_version`
- `source_url`

## 6. Runtime section

Required fields:

- `started_at`
- `ended_at`
- `wall_clock_seconds`
- `api_cost_usd`
- `total_tool_calls`

## 7. Turn records

Each turn MUST include:

- `turn_index`
- `sim_time_before`
- `sim_time_after`
- `observations`
- `actions`
- `events`
- `notes`

Each action SHOULD include:

- `tool_name`
- `request_id`
- `arguments`
- `response`
- `status`

## 8. State snapshots

The trace MUST include at least:

- initial snapshot
- final snapshot

It SHOULD also include:

- milestone snapshots
- snapshot hashes after mutating turns

## 9. Evaluation section

Required fields:

- `scenario_score`
- `outcome_score`
- `constraint_score`
- `subscores`
- `violations`
- `pass`

If semantic judges are used, include:

- `judge_versions`
- `judge_inputs_hashes`

## 10. Integrity requirements

The trace SHOULD support:

- deterministic replay
- hash-based integrity checks
- scenario/evaluator compatibility checks

