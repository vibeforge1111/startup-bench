# Hidden Pack Rotation Policy v0.9.0

Last updated: 2026-03-08

## Purpose

This document defines the first concrete hidden-pack rotation policy for TheStartupBench.

Reference artifact:

- [hidden_pack_rotation_policy_v0_9_0.json](/C:/Users/USER/Desktop/startup-bench/examples/hidden_pack_rotation_policy_v0_9_0.json)

Official reporting window:

- [official_evaluation_window_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/official_evaluation_window_v0_9_0.md)

Lifecycle history:

- [pack_lifecycle_changelog.md](/C:/Users/USER/Desktop/startup-bench/docs/pack_lifecycle_changelog.md)

## Cadence

- refresh each hidden `fresh` family at least once per reporting quarter or before the next official window opens
- do not rotate active hidden `test` packs inside a frozen official window unless contamination or a critical invalidation forces it
- review canary freshness before each new official window
- review the active hidden families monthly even if no pack is promoted or retired

## Retirement triggers

Retire a hidden pack when:

- leakage or material inferability is confirmed
- the official window closes and a successor pack set is ready
- a critical evaluator bug changes the meaning of the pack materially
- a promoted fresh successor makes the active pack stale
- coverage drift makes the pack misleading for its intended track mix

## Promotion rules

Fresh to test promotion requires:

- distinct hidden ids and files
- validation, lint, and smoke coverage
- exploit or canary review without unresolved gaming signals
- redacted public manifest updates

Successor activation requires:

- retiring the prior pack in the public changelog first
- updating frozen active packs and official-window references
- preserving legacy history rather than deleting old references

## Operational rule

Pack rotation is not just a scenario authoring action. It is a benchmark-governance event.

Every rotation should update:

- [public_pack_changelog.json](/C:/Users/USER/Desktop/startup-bench/examples/public_pack_changelog.json)
- [pack_lifecycle_changelog.md](/C:/Users/USER/Desktop/startup-bench/docs/pack_lifecycle_changelog.md)
- [frozen_active_packs.md](/C:/Users/USER/Desktop/startup-bench/docs/frozen_active_packs.md) when the official window changes
- benchmark status and task tracking if the rotation changes benchmark claims

## Boundary

This policy is enough to make hidden-pack rotation operational for the current pre-human-calibration benchmark phase.

The next missing piece is exercising the policy in practice across a later official window, not inventing a more complex policy surface.
