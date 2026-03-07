# Tool Contract

## 1. Tool philosophy

TSB tools represent business operating systems, not arbitrary shell access.

The agent MUST only interact with the scenario through declared tools and observation surfaces.

## 2. Tool families

Official tool families:

- `metrics.query`
- `metrics.report`
- `product.roadmap.read`
- `product.roadmap.write`
- `product.launch`
- `growth.experiment.create`
- `growth.experiment.review`
- `sales.pipeline.read`
- `sales.pipeline.update`
- `sales.pricing.propose`
- `finance.plan.read`
- `finance.plan.write`
- `finance.raise.propose`
- `people.hiring.read`
- `people.hiring.update`
- `people.org.propose`
- `ops.incident.read`
- `ops.incident.respond`
- `board.read`
- `board.update`
- `research.market.read`
- `notes.read`
- `notes.write`
- `sim.advance`

Official scenarios MAY use subsets of these.

## 3. Request contract

Every tool call MUST include:

- `tool_name`
- `request_id`
- `arguments`

Optional fields:

- `reason`
- `expected_outcome`

## 4. Response contract

Every tool response MUST include:

- `ok`
- `request_id`
- `tool_name`
- `timestamp`
- `result`

If the call mutates state, the response SHOULD include:

- `state_delta_summary`

If the call fails, the response MUST include:

- `error_code`
- `error_message`

## 5. Error model

Standard error classes:

- `invalid_request`
- `permission_denied`
- `policy_violation`
- `resource_conflict`
- `rate_limited`
- `not_found`
- `stale_view`
- `execution_failed`

## 6. Action budgets

Scenarios MAY impose:

- tool-call budgets
- write-action budgets
- high-impact action budgets

Budget usage MUST be visible in traces.

## 7. Shared-control interactions

When a tool affects another stakeholder, the tool MAY return:

- `pending_external_actor`
- `approval_required`
- `follow_up_needed`

This allows dual-control or stakeholder-mediated workflows.

## 8. Time advancement

`sim.advance` is the canonical time-advancement tool.

It MUST:

- advance the scenario clock
- process due events
- return visible deltas and surfaced events

It MUST NOT expose hidden evaluator internals.

## 9. Tool determinism

Given the same benchmark version, scenario version, seed, and preceding trace, tool outputs MUST be replayable.

## 10. Tool metadata

The official scaffold SHOULD expose a tool manifest containing:

- tool name
- description
- argument schema
- write or read classification
- policy notes
- side-effect classification

