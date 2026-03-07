# Pre-Freeze Checklist

Last updated: 2026-03-07

Use this checklist before cutting a pre-human or release-candidate benchmark tag.

## Control Plane

- schemas are stable for the freeze window
- official eval profile is stable for the freeze window
- run/submission/report artifacts are stable for the freeze window
- review packet and operator review formats are stable for the freeze window

## Hidden Packs

- each hidden family passes `check-suite-family`
- public manifests match the active hidden pack versions
- pack lifecycle changelog is current
- any retired or superseded pack versions are recorded

## Evaluator State

- recent evaluator mutations are tied to adjudicated evidence
- open evaluator watchlist items are recorded in [benchmark_known_issues.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_known_issues.md)
- no unresolved critical evaluator drift is known

## Corpus State

- pack composition is documented in [benchmark_status.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_status.md)
- newly added hidden scenarios have validation and suite coverage
- fresh/test variants are distinct in ids and files

## Verification

- `python -m unittest discover -s tests -p "test_*.py"` passes
- key hidden suites run successfully
- suite-report and submission artifacts validate

## Calibration State

- synthetic calibration outcomes are up to date in [calibration_outcomes.md](/C:/Users/USER/Desktop/startup-bench/docs/calibration_outcomes.md)
- adjudication decisions are logged in [evaluator_adjudication_log.md](/C:/Users/USER/Desktop/startup-bench/docs/evaluator_adjudication_log.md)
- any deferred items are explicit

## Freeze Decision

- pre-human freeze: allowed if human calibration is pending but the control plane and known evaluator issues are stable
- release candidate freeze: allowed only after human/operator review and adjudication
