# Evaluator Contract

## 1. Purpose

The evaluator contract defines how TSB computes scores, detects violations, and emits score reports.

It exists to ensure:

- evaluator modularity
- reproducibility
- auditability
- leaderboard comparability

## 2. Evaluator types

TSB SHOULD support the following evaluator types:

- metric evaluator
- state-diff evaluator
- rule-violation evaluator
- semantic artifact evaluator
- aggregate scenario evaluator

## 3. Metric evaluator

A metric evaluator computes one score component from state, events, or derived metrics.

Examples:

- runway preservation
- churn reduction
- weighted pipeline quality
- incident resolution quality

Inputs MAY include:

- initial state
- final state
- intermediate snapshots
- event log
- action log

## 4. State-diff evaluator

A state-diff evaluator compares initial and final state or milestone states.

Examples:

- enterprise accounts increased
- trust score preserved
- morale improved
- budget remained compliant

## 5. Rule-violation evaluator

A rule-violation evaluator detects:

- bankruptcy
- unauthorized spend
- compliance breach
- SLA breach
- exploit signatures

Violations SHOULD be emitted as structured records, not only score penalties.

## 6. Semantic artifact evaluator

A semantic artifact evaluator is allowed only for outputs that cannot be scored well enough programmatically.

Examples:

- board memo
- customer escalation response
- pricing rationale
- hiring rubric

Semantic evaluators MUST:

- use versioned prompts or versioned non-LLM rubric logic
- emit artifact ids and rubric dimensions
- provide traceable rationale metadata
- remain a minority contributor to total score

## 7. Aggregate scenario evaluator

The aggregate scenario evaluator combines component outputs into:

- outcome score
- constraint score
- final scenario score
- pass flag
- violation summary

## 8. Evaluator input contract

Every evaluator SHOULD receive a normalized input envelope containing:

- benchmark version
- scenario id
- scenario version
- run metadata
- initial state
- final state
- milestone snapshots
- events
- actions
- derived metrics

## 9. Evaluator output contract

Every evaluator MUST emit:

- evaluator id
- evaluator version
- status
- outputs

Recommended output fields:

- component score
- confidence if applicable
- violations
- rationale metadata
- referenced artifact ids

## 10. Evaluator determinism

Metric and state-diff evaluators MUST be deterministic given the same inputs.

Semantic evaluators SHOULD be deterministic where possible.

If a semantic evaluator is stochastic, that MUST be:

- explicitly declared
- versioned
- bounded by repeated-run policy

## 11. Evaluator registry

The official scaffold SHOULD maintain an evaluator registry mapping:

- `evaluator_id`
- evaluator type
- version
- input schema
- output schema

## 12. Evaluation phases

Recommended evaluation phases:

- per-turn checks
- milestone checks
- terminal checks
- final score aggregation

## 13. Error handling

If an evaluator fails:

- the failure MUST be recorded
- the run SHOULD be marked non-leaderboard-grade unless fallback behavior is officially defined

## 14. Auditability

Official score reports SHOULD allow reviewers to trace:

- which evaluators contributed
- which artifacts they read
- which violations were triggered
- how the final score was assembled

