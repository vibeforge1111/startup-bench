# Calibration Outcomes

Last updated: 2026-03-07

## Scope

This document records the completed synthetic-panel calibration slices that were run with:

- Codex internal review
- Gemini synthetic review
- Claude synthetic review
- benchmark score and recommendation

The goal is to distinguish:

- slices that are now directionally calibrated
- slices that required evaluator corrections
- slices that remain on a watchlist for human review

## Completed slices

### Hidden canary test pack

#### `hidden_canary_pricing_trap_test_001`

Outcome:

- initial benchmark recommendation: `pass`
- synthetic panel recommendation: `borderline`
- status: corrected

Correction:

- penalized passive trust decline after adverse GTM backlash events
- penalized repeated support-alert neglect and rigid non-adaptive loops

Current status:

- benchmark recommendation: `borderline`
- panel recommendation: `borderline`
- calibration state: aligned

#### `hidden_canary_hiring_trap_test_001`

Outcome:

- initial benchmark recommendation: `pass`
- synthetic panel recommendation: `borderline`
- status: corrected

Correction:

- penalized passive soft-demand loops with unresolved hiring and finance posture

Current status:

- benchmark recommendation: `borderline`
- panel recommendation: `borderline`
- calibration state: aligned

### Hidden strategy test pack

#### `hidden_product_delayed_consequence_test_001`

Outcome:

- benchmark recommendation: `pass`
- synthetic panel recommendation: `pass`
- calibration state: healthy

Notes:

- benchmark and panel were already closely aligned
- no evaluator change required

#### `hidden_board_stakeholder_conflict_test_001`

Outcome:

- benchmark recommendation: `pass`
- synthetic panel recommendation: `pass`
- calibration state: healthy, watchlist

Notes:

- Claude was materially harsher on governance quality
- repeated templated board communication and under-addressed post-pushback follow-through remain concerns
- current evidence does not justify an evaluator mutation yet

#### `hidden_scale_multi_quarter_test_001`

Outcome:

- benchmark recommendation: `pass`
- synthetic panel recommendation: `pass`
- calibration state: healthy

Notes:

- strong agreement that early capacity investment and later cleanup were properly rewarded
- no evaluator change required

### Hidden real-world test pack

#### `real_world_zoom_security_freeze_test_001`

Outcome:

- initial benchmark recommendation: `pass`
- synthetic panel recommendation: `borderline`
- status: corrected

Correction:

- penalized security/trust-backlash crisis runs that:
  - skip product/security tradeoff actions
  - skip post-shock board follow-up
  - leave compliance pressure elevated without follow-up action
  - keep pushing pipeline through the trust backlash

Current status:

- benchmark recommendation: `borderline`
- panel recommendation: `borderline`
- calibration state: aligned

#### `real_world_brex_svb_treasury_shock_test_001`

Outcome:

- initial benchmark recommendation: `pass`
- synthetic panel recommendation: `borderline`
- status: corrected

Correction:

- penalized treasury-shock runs that:
  - do the initial rebalance
  - then skip finance follow-up planning
  - leave financing pressure and counterparty risk elevated
  - continue mechanical pipeline maintenance through the liquidity crisis

Current status:

- benchmark recommendation: `borderline`
- panel recommendation: `borderline`
- calibration state: aligned

## Summary judgment

Current synthetic-panel calibration status:

- corrected and aligned:
  - canary pricing trap
  - canary hiring trap
  - real-world Zoom security freeze
  - real-world Brex treasury shock
- healthy without correction:
  - strategy product delayed consequence
  - strategy scale multi-quarter
- healthy but on human-review watchlist:
  - strategy board stakeholder conflict

## What this means

The benchmark is now materially safer to hand to human operators for real calibration because:

- the clearest evaluator mismatches found by the synthetic panel were corrected
- the strategy family is mostly stable
- crisis handling is no longer obviously over-rewarded in two key real-world slices

This does not mean the benchmark is fully calibrated.

It means the benchmark is ready for:

- a first real founder/operator taskforce wave
- targeted human scrutiny on the governance watchlist scenario
- selective spot checks rather than another large synthetic pass

## Recommended next step

Run a curated human review wave over:

- both hidden canary scenarios
- all three hidden strategy scenarios
- the corrected Zoom and Brex real-world crisis scenarios

That is the minimum human wave needed to confirm that the synthetic corrections transferred in the right direction.
