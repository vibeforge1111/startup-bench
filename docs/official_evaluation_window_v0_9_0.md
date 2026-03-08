# Official Evaluation Window v0.9.0

Last updated: 2026-03-08

## Purpose

This document freezes the first official reporting window for TheStartupBench.

Reference artifact:

- [official_eval_window_v0_9_0.json](/C:/Users/USER/Desktop/startup-bench/examples/official_eval_window_v0_9_0.json)

Frozen official profile:

- [official_eval_profile.json](/C:/Users/USER/Desktop/startup-bench/examples/official_eval_profile.json)

Frozen pack set:

- [frozen_active_packs.md](/C:/Users/USER/Desktop/startup-bench/docs/frozen_active_packs.md)

## Window

- window id: `official-window-v0.9.0-precalibration-2026-03-15-to-2026-04-12`
- freeze label: `v0.9-precalibration-window-001`
- window start: `2026-03-15`
- window end: `2026-04-12`

This is a pre-human-calibration reporting window. It is suitable for benchmark operations discipline and early public comparison, but it is not a release-candidate leaderboard freeze.

## Hosted vs self-reported

### Hosted

Hosted entries are benchmark-operated runs under the frozen official profile.

Rules:

- use only the frozen settings in [official_eval_profile.json](/C:/Users/USER/Desktop/startup-bench/examples/official_eval_profile.json)
- allowed runner types are `baseline` and `script`
- hidden traces may remain private
- published results must still include score, repeat count, runtime/cost summary, and contamination status

### Self-reported

Self-reported entries are allowed during this window, but they must be published separately from hosted results.

Rules:

- emit a run manifest with the frozen profile
- include a submission artifact
- declare contamination status
- report cost and runtime
- do not merge self-reported entries into the hosted ranking table

## Reporting rules

- report `test` and `fresh` separately
- minimum repeated runs: `5`
- declared seeds are required
- publish SEM or confidence intervals
- do not mix results from a different freeze label into this window

## Recommended commands

```bash
python -m thestartupbench show-official-profile examples/official_eval_profile.json
python -m thestartupbench emit-run-manifest examples/official_eval_profile.json --model-id <model-id> --provider <provider> --runner-type <baseline|script> --output-path <run-manifest-path>
```

## Freeze boundary

This window closes on `2026-04-12`.

After that date:

- new reported results should move to a new official evaluation window artifact
- hidden-pack or evaluator changes should not be backfilled into this window without an adjudicated public note
- hosted and self-reported entries from a later window should not be merged into this window's table
