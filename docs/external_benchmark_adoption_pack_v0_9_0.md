# External Benchmark Adoption Pack v0.9.0

Last updated: 2026-03-08

## Purpose

This document defines the supported external-use path for TheStartupBench during the current pre-human-calibration window.

Reference artifact:

- [external_benchmark_adoption_pack_v0_9_0.json](/C:/Users/USER/Desktop/startup-bench/examples/external_benchmark_adoption_pack_v0_9_0.json)

Supporting governance artifacts:

- [official_evaluation_window_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/official_evaluation_window_v0_9_0.md)
- [leaderboard_governance_pack_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/leaderboard_governance_pack_v0_9_0.md)
- [frozen_active_packs.md](/C:/Users/USER/Desktop/startup-bench/docs/frozen_active_packs.md)

## Who this is for

- external research teams that want a self-reported result path
- model providers that want a documented publication lane during the frozen window
- community users that want local benchmark reference runs without leaderboard claims

## Supported paths

### Hosted reference

Hosted results are benchmark-operated only.

Use this lane as a reference for comparison, not as a request path for external submissions.

### Self-reported window run

This is the supported publication lane for outside users.

Minimum expectation:

- use the frozen official profile
- emit a run manifest
- build a submission artifact
- disclose repeats, seeds, cost, runtime, and contamination status
- publish into the self-reported table only

### Local reference use

This lane is for debugging, adapters, method checks, and non-leaderboard sharing.

It is explicitly not an official benchmark entry path.

## Non-claims

External users should not claim:

- hosted benchmark status
- hidden-trace access
- official leaderboard placement without benchmark-operated execution
- that the current window is a final public benchmark release

Self-reported results are allowed. They are not benchmark-certified beyond the frozen-window reporting rules.

## Why this exists

The benchmark now has enough operational structure to support disciplined outside use, but not enough maturity to justify loose public claims.

This pack is the boundary:

- it makes outside usage easier
- it keeps reporting disciplined
- it prevents benchmark-maturity inflation
