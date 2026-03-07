# Scenario Specification

## 1. Scenario identity

Each scenario MUST define:

- `scenario_id`
- `scenario_version`
- `track`
- `mode`
- `title`
- `summary`
- `authoring_origin`

`scenario_id` MUST be stable across scenario versions.

## 2. Scenario structure

Each scenario MUST include the following top-level sections:

- `metadata`
- `initial_state`
- `latent_state`
- `observation_surfaces`
- `tools`
- `event_model`
- `policy_constraints`
- `terminal_conditions`
- `evaluation`

## 3. Metadata contract

Required metadata fields:

- `scenario_id`
- `scenario_version`
- `benchmark_version`
- `track`
- `mode`
- `difficulty`
- `time_horizon`
- `authoring_origin`
- `tags`

Recommended fields:

- `estimated_human_minutes`
- `industry`
- `business_model`
- `company_stage`
- `risk_profile`

## 4. Initial state

The visible initial state MUST capture the operator-facing world at turn 0.

At minimum it SHOULD include:

- company profile
- cash and finance state
- product state
- demand and customer state
- team state
- market state
- pending obligations

## 5. Latent state

Latent state contains hidden variables not directly visible to the agent.

Examples:

- true churn drivers
- true employee attrition risk
- competitor readiness
- enterprise procurement friction
- underlying product quality

Latent state MUST NOT be exposed through normal tools.

## 6. Observation surfaces

Observation surfaces are the structured views available to the agent.

Examples:

- dashboard
- CRM view
- support inbox
- board requests
- incident console
- hiring funnel
- analytics reports

Each surface MUST declare:

- `surface_id`
- `surface_type`
- `refresh_policy`
- `visible_fields`

## 7. Tools

Each scenario MUST reference allowed tool families from the tool contract.

Each scenario MAY further narrow:

- rate limits
- write permissions
- approval thresholds
- action budgets

## 8. Event model

Each scenario MUST define either:

- deterministic scheduled events
- a seeded event generator
- or both

Each event definition SHOULD specify:

- `event_type`
- `trigger`
- `visibility`
- `state_effects`
- `stakeholder_effects`

## 9. Policy constraints

Each scenario MUST define applicable policies and hard rules.

Examples:

- budget caps
- legal restrictions
- approval requirements
- customer SLA commitments
- board covenants

Policy constraints SHOULD be machine-checkable where possible.

## 10. Terminal conditions

Each scenario MUST define terminal conditions.

Required terminal classes:

- `horizon_end`
- `hard_failure`

Examples of hard failure:

- bankruptcy
- unrecoverable compliance breach
- catastrophic customer trust collapse

## 11. Evaluation section

Each scenario MUST define:

- primary score components
- hard constraints
- subscore groups
- evaluator references

Each scored component SHOULD specify:

- `component_id`
- `kind`
- `weight`
- `direction`
- `source`

## 12. Scenario authoring lifecycle

Recommended lifecycle:

- `draft`
- `internal_review`
- `human_validated`
- `dev_release`
- `hidden_test_release`
- `retired`

## 13. Fairness and quality gates

A scenario SHOULD NOT be promoted unless:

- human reviewers can solve it or explain why it is intentionally frontier-hard
- evaluator behavior is stable across replay
- no privileged fields leak into observations
- exploit review is completed

