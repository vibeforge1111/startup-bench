# Reference Runner Contract

## 1. Purpose

The reference runner defines how a TSB scenario is executed end to end.

It is the canonical contract between:

- scenario definitions
- world-state engine
- tool system
- agent runtime
- evaluators
- trace emitter

The reference runner is not required to be the only implementation, but leaderboard-grade runs MUST be behaviorally compatible with it.

## 2. Core execution model

Each run executes the following lifecycle:

1. load benchmark configuration
2. load scenario definition
3. initialize world state from scenario and seed
4. derive visible observation surfaces
5. expose allowed tools
6. accept agent actions
7. validate actions against tool and policy rules
8. apply state transitions
9. process due events
10. advance simulation time when requested or required
11. emit trace records
12. stop on terminal condition
13. compute final evaluation

## 3. Canonical runtime components

The runner SHOULD be decomposed into:

- scenario loader
- world-state store
- observation projector
- tool router
- policy gate
- transition engine
- event engine
- evaluator adapter
- trace writer
- replay verifier

## 4. Scenario loader contract

The scenario loader MUST:

- validate scenario structure against the scenario schema
- resolve scenario version and benchmark version
- hydrate defaults if official defaults are allowed
- reject incompatible scenario/runner version pairs

## 5. World-state store contract

The world-state store MUST maintain:

- canonical mutable internal state
- visibility-aware projections
- state snapshot generation
- state diff generation

The world-state store SHOULD support:

- full snapshot retrieval
- partition-level retrieval
- diff by turn
- replay reconstruction

## 6. Observation projector contract

The observation projector maps internal state to agent-visible surfaces.

It MUST:

- respect field visibility classes
- respect refresh timing
- support delayed visibility
- include event-derived observations

It MUST NOT:

- leak latent or evaluator-only fields
- emit non-reproducible synthetic views

## 7. Tool router contract

The tool router MUST:

- expose only scenario-allowed tools
- validate request shape
- route tool requests to handlers
- normalize responses
- emit tool-call trace records

The tool router SHOULD support:

- tool manifest generation
- read/write classification
- side-effect classification

## 8. Policy gate contract

The policy gate MUST evaluate each write or high-impact action against:

- scenario policy constraints
- approval requirements
- budget limits
- action budgets
- role permissions if applicable

Policy gate decisions MUST be traceable.

## 9. Transition engine contract

The transition engine applies world mutations.

It MUST support:

- deterministic transitions
- seeded stochastic transitions
- stakeholder-mediated pending transitions
- derived metric recalculation

Each transition SHOULD produce:

- state diff
- affected partitions
- visible delta summary

## 10. Event engine contract

The event engine processes:

- scheduled events
- conditional events
- probabilistic events
- chained events

The event engine MUST:

- use seeded randomness where stochastic
- preserve event ordering rules
- record generated and consumed events in the trace

## 11. Time advancement contract

The runner MUST define a canonical simulation clock.

Minimum required fields:

- current simulated time
- turn index
- horizon end

Time MAY advance:

- explicitly via `sim.advance`
- automatically if the scenario defines forced progression rules

Automatic progression rules MUST be versioned and documented.

## 12. Turn semantics

A turn SHOULD contain:

- observation phase
- action phase
- validation phase
- mutation phase
- event phase
- trace emission phase

The runner MUST define whether multiple tool calls can occur within one turn.

Recommended default:

- multiple tool calls allowed within one agent turn
- time advances only on explicit `sim.advance` or forced scenario rules

## 13. Failure semantics

The runner MUST distinguish:

- invalid action
- tool execution failure
- policy rejection
- runtime error
- scenario hard failure
- evaluator failure

Hard runtime failures SHOULD invalidate the run if trace integrity is lost.

## 14. Replay contract

The runner SHOULD support deterministic replay from:

- scenario version
- benchmark version
- run seed
- action trace
- runner version

Replay SHOULD verify:

- matching final score
- matching final state hash
- matching event sequence

## 15. Integrity model

The runner SHOULD emit:

- state hashes
- trace hashes
- evaluator version identifiers
- manifest hashes for tool and scenario definitions

## 16. Extension policy

New runner features MAY be added if they do not break:

- existing scenario semantics
- trace compatibility guarantees
- scoring compatibility guarantees

Breaking behavioral changes require a benchmark or scaffold version bump.

