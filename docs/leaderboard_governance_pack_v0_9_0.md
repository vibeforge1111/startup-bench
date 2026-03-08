# Leaderboard Governance Pack v0.9.0

Last updated: 2026-03-08

## Purpose

This document defines the first concrete leaderboard governance pack for TheStartupBench.

Reference artifact:

- [leaderboard_governance_pack_v0_9_0.json](/C:/Users/USER/Desktop/startup-bench/examples/leaderboard_governance_pack_v0_9_0.json)

Official reporting window:

- [official_evaluation_window_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/official_evaluation_window_v0_9_0.md)

## Entry types

The governance pack defines three publication lanes:

- `hosted`: benchmark-operated runs under the frozen official profile and reporting window
- `self_reported`: externally produced runs that follow the reporting rules but live in a separate table
- `reference_baseline`: maintainer-published anchor systems that help interpret the benchmark

Hosted and self-reported entries must not be merged into one table during the same window.

## Contamination response

Active contamination flags:

- `clean`
- `possible_contamination`
- `known_contamination`

Operational rule:

- never clear or hide contamination concerns silently
- preserve flagged history in public records
- retire or invalidate entries when confirmed leakage or exploit use makes the ranking misleading

## Release notes

Release notes are required when:

- a new official window opens
- new hosted results are published
- contamination status changes
- an entry, pack, or window is retired

Minimum release-note content:

- benchmark version
- official window id
- entry type
- contamination flag
- retirement or invalidation reason when applicable

## Retirement rules

Entries may be retired when:

- hidden content leakage is confirmed
- benchmark-policy exploits are confirmed
- a material evaluator bug invalidates the result
- a later incompatible benchmark window supersedes the table

Packs may be retired when:

- contamination risk becomes material
- a fresh successor is promoted
- the public pack changelog records the transition and its reason

## Boundary

This governance pack is enough to support pre-human-calibration leaderboard operations during the current official window.

It is not yet the final public leaderboard constitution. The next hardening step is the hidden-pack rotation policy so retirements and promotions follow a tighter operational cadence.
