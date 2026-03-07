# Scenario Primitive Library Specification

## 1. Purpose

Scenario primitives are reusable building blocks for constructing TSB scenarios with controlled diversity and difficulty.

They allow TSB to scale beyond manually written one-off cases while preserving interpretability.

## 2. Primitive categories

The primitive library SHOULD include the following categories:

- company primitives
- market primitives
- demand primitives
- product primitives
- team primitives
- finance primitives
- stakeholder primitives
- event primitives
- policy primitives
- risk primitives

## 3. Company primitives

Examples:

- stage: `pre_seed`, `seed`, `series_a`, `growth`
- business model: `b2b_saas`, `consumer_subscription`, `marketplace`, `deeptech_contracts`
- segment focus
- monetization model
- strategy archetype

## 4. Market primitives

Examples:

- market growth regime
- competitor density
- platform dependence
- regulatory sensitivity
- infrastructure cost pressure

## 5. Demand primitives

Examples:

- inbound demand profile
- enterprise pipeline strength
- virality strength
- retention sensitivity
- sales cycle length

## 6. Product primitives

Examples:

- roadmap debt level
- reliability posture
- onboarding quality
- experimentation maturity
- product complexity

## 7. Team primitives

Examples:

- functional headcount shape
- hiring throughput
- attrition sensitivity
- founder bottleneck
- management leverage

## 8. Finance primitives

Examples:

- runway band
- gross margin regime
- fundraising climate
- fixed-cost rigidity
- revenue concentration

## 9. Stakeholder primitives

Examples:

- board aggressiveness
- investor patience
- customer procurement friction
- employee trust sensitivity
- press sensitivity

## 10. Event primitives

Events SHOULD be composed from reusable event templates.

Examples:

- competitor launch
- churn wave
- outage
- security incident
- pricing shock
- key hire departure
- board escalation
- regulatory inquiry

Each event primitive SHOULD specify:

- trigger conditions
- probability or schedule
- direct state effects
- secondary propagation rules
- visibility delay

## 11. Policy primitives

Examples:

- spend approval threshold
- legal review requirement
- hiring freeze
- customer SLA commitments
- fundraising covenant

## 12. Risk primitives

Examples:

- concentration risk
- reliability risk
- compliance risk
- hiring risk
- platform risk

## 13. Primitive composition rules

Primitives MUST compose under compatibility rules.

Examples:

- a `consumer_viral_loop` primitive should not be paired with an enterprise-only sales motion unless explicitly intended
- a `deeptech_long_r_and_d` primitive should imply corresponding runway and milestone primitives
- a `severe_board_pressure` primitive should increase sensitivity in governance and financing paths

## 14. Primitive parameterization

Primitives SHOULD support parameters rather than fixed labels only.

Examples:

- runway weeks
- churn sensitivity coefficient
- procurement delay range
- incident severity

This makes scenario generation more expressive while staying structured.

## 15. Difficulty linkage

Primitive combinations SHOULD map to difficulty axes:

- ambiguity
- pressure
- coordination load
- delay to consequence
- downside asymmetry

Difficulty metadata SHOULD be generated from the primitive mix and then optionally adjusted by reviewers.

## 16. Scenario templates

Templates are higher-level compositions of primitives.

Examples:

- `runway_reset`
- `enterprise_push`
- `post_launch_instability`
- `board_pressure_reforecast`
- `growth_without_retention`
- `outage_during_renewal_cycle`

Templates SHOULD provide:

- required primitive slots
- optional primitive slots
- anti-conflict rules
- recommended evaluation components

## 17. Authoring modes

TSB SHOULD support:

- fully expert-authored scenarios
- template-assisted scenarios
- procedurally generated scenarios reviewed by humans

## 18. Promotion rules

A primitive-generated scenario SHOULD be promoted only if:

- compatibility checks pass
- evaluator checks pass
- human review passes
- exploit review passes

## 19. Implementation guidance

Maintain the primitive library as data, not embedded code logic.

Recommended structure:

- primitive catalog
- compatibility matrix
- template catalog
- difficulty derivation rules
- promotion metadata

