# Benchmark Task Board

Last updated: 2026-03-08

This board is the human-readable execution view of the benchmark maturity program in [benchmark_maturity_plan.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_maturity_plan.md).

Machine-readable source of truth:

- [benchmark_task_ledger.json](/C:/Users/USER/Desktop/startup-bench/examples/benchmark_task_ledger.json)

## Active milestones

### v0.9.5

Objective:

- stabilize the benchmark as a serious internal benchmark candidate

Success targets:

- hidden `test` inventory >= `50`
- strategy hidden pack broadened further across long-horizon tracks
- official task system adopted for all benchmark-grade work
- calibration execution moved from protocol to active wave planning

### v0.10.0

Objective:

- become a community-credible benchmark candidate

Success targets:

- hidden `test` inventory >= `75`
- hidden `fresh` inventory >= `40`
- operator calibration completed for promoted packs
- official evaluation operations documented and frozen for one reporting window

## In Progress

- `BT-005` operator calibration wave 002
  - milestone: `v0.10.0`
  - focus: wave launched and reviewer packets exported for founder, ops, and product reviewers; next step is collecting returns and logging score-vs-operator disagreements

## Completed

- `BT-001` benchmark maturity plan
  - milestone: `v0.9.5`
  - focus: published deeper maturity assessment and implementation sequence

- `BT-002` benchmark task system
  - milestone: `v0.9.5`
  - focus: established the task ledger and board as the execution source of truth

- `BT-003` hidden corpus expansion to `50`
  - milestone: `v0.9.5`
  - focus: added seven new hidden `test` scenarios across the operator pack to reach `50` active hidden `test` scenarios benchmark-wide

- `BT-004` strategy pack expansion
  - milestone: `v0.9.5`
  - focus: broadened long-horizon coverage across board, product, scale, and GTM with valid hidden `test` and `fresh` variants

- `BT-010` scale-finance interaction strategy family
  - milestone: `v0.9.5`
  - focus: added a new long-horizon scale scenario plus hidden `test` and `fresh` variants, and promoted the strategy pack metadata

- `BT-009` second `0to1` ambiguity expansion batch
  - milestone: `v0.9.5`
  - focus: added three new hidden `0to1` scenario families plus a new public dev slice, and promoted the coverage pack metadata

- `BT-006` official evaluation window freeze
  - milestone: `v0.10.0`
  - focus: froze the first official reporting window, documented hosted vs self-reported rules, and linked the frozen active pack set

## Ready

- `BT-007` leaderboard governance pack
  - milestone: `v0.10.0`
  - focus: entry types, contamination handling, release notes, and retirement rules

- `BT-008` hidden pack rotation policy
  - milestone: `v0.10.0`
  - focus: define refresh cadence and pack replacement rules

## Next up by priority

1. strategy pack depth in product, board, scale, and gtm
2. calibration execution and operator review collection
3. leaderboard operations and contamination workflow
4. hidden pack rotation policy
5. external benchmark adoption materials

## Operating rules

- every benchmark-grade change should reference a task id
- every pack promotion should map back to completed tasks
- milestone status should be reviewed after each pack promotion batch
- the JSON ledger is authoritative if this board drifts
