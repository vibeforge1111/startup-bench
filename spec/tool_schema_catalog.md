# Tool Schema Catalog

## 1. Purpose

This document refines the generic tool contract into canonical request and response shapes expected by the reference runner.

It defines shared envelopes plus domain-specific payload conventions.

## 2. Shared request envelope

Every tool request SHOULD use this envelope:

- `tool_name`
- `request_id`
- `arguments`
- `reason` optional
- `expected_outcome` optional

## 3. Shared response envelope

Every tool response SHOULD use this envelope:

- `ok`
- `request_id`
- `tool_name`
- `timestamp`
- `result`
- `error_code` optional
- `error_message` optional
- `state_delta_summary` optional

## 4. Read tool conventions

Read tools SHOULD:

- avoid mutating state
- return query metadata
- support paginated or filtered result sets where relevant

Recommended result keys:

- `items`
- `total_count`
- `filters_applied`
- `generated_at`

## 5. Write tool conventions

Write tools SHOULD:

- emit the target entity ids
- emit policy or approval status
- emit visible effect summary

Recommended result keys:

- `updated_entities`
- `pending_approvals`
- `visible_effects`
- `warnings`

## 6. Canonical tool families

### 6.1 `metrics.query`

Arguments SHOULD include:

- `metric_ids`
- `time_range`
- `group_by` optional
- `filters` optional

### 6.2 `sales.pipeline.update`

Arguments SHOULD include:

- `opportunity_id`
- `action`
- `fields`

### 6.3 `sales.pricing.propose`

Arguments SHOULD include:

- `plan_id` or `segment_id`
- `price_change`
- `effective_date`
- `rationale`

### 6.4 `finance.plan.write`

Arguments SHOULD include:

- `budget_changes`
- `headcount_changes` optional
- `cost_actions` optional
- `revenue_actions` optional

### 6.5 `people.hiring.update`

Arguments SHOULD include:

- `role_id`
- `action`
- `candidate_id` optional
- `compensation` optional

### 6.6 `ops.incident.respond`

Arguments SHOULD include:

- `incident_id`
- `response_action`
- `owner`
- `customer_comms_plan` optional

### 6.7 `board.update`

Arguments SHOULD include:

- `update_type`
- `summary`
- `forecast`
- `asks` optional

### 6.8 `sim.advance`

Arguments SHOULD include:

- `advance_by`
- `unit`
- `reason` optional

Result SHOULD include:

- `sim_time_before`
- `sim_time_after`
- `events_processed`
- `visible_updates`

## 7. Manifest requirement

The runner SHOULD expose a machine-readable manifest of active tools with:

- request schema
- response schema
- mutability class
- approval sensitivity
- budget sensitivity

