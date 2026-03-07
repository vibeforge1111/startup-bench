# Calibration Taskforce Strategy

Last updated: 2026-03-07

## Goal

This document explains how to run a real human calibration taskforce for TheStartupBench.

The benchmark itself stays automated. The taskforce exists to:

- calibrate automated scoring against real operator judgment
- catch evaluator mistakes before benchmark promotion
- detect benchmark-gaming patterns that automated checks miss
- create credible human/operator baselines for publication

## What the taskforce is for

The taskforce should not review every benchmark run.

It should review:

- new hidden pack families before promotion
- canary scenarios and exploit-sensitive scenarios
- long-horizon strategy scenarios
- crisis scenarios with unclear tradeoffs
- any scenario family where automated scores and human judgment diverge

## Recommended team shape

Small serious taskforce:

- `1` benchmark lead
- `1` study ops coordinator
- `1` adjudication lead
- `6` to `12` reviewers

Healthy reviewer mix:

- founders or CEOs
- product or growth operators
- finance, ops, or people operators
- optional subject-matter reviewers for legal/compliance-heavy scenarios

Recommended minimum launch shape:

- `2` founders
- `2` product/growth operators
- `2` finance/ops/people operators

That is enough to run a first credible study wave without making the process too heavy.

## Roles

Benchmark lead:

- owns study scope
- decides which scenario families require calibration
- approves promotion or rejection decisions

Study ops coordinator:

- prepares study runs and review packets
- schedules reviewers
- tracks completion and missing reviews

Adjudication lead:

- reviews disagreement cases
- identifies evaluator flaws vs reviewer misunderstandings
- decides whether a scenario needs revision, quarantine, or promotion delay

Reviewers:

- review assigned packets independently
- provide rubric scores and notes
- flag benchmark-gaming behavior

## Operating model

Use study waves.

Each wave should:

1. choose 1 to 3 target hidden packs
2. run fixed benchmark artifacts with pinned seeds and turn caps
3. produce review packets
4. assign at least 2 reviewers per target family
5. collect operator reviews independently
6. compile calibration reports
7. adjudicate disagreement and promotion status

Do not let reviewers discuss scenarios with each other before independent submission.

## Recommended cadence

For an early benchmark:

- run one full calibration wave for every major hidden-pack family
- run a smaller spot-check wave whenever evaluator logic changes
- run a fresh canary audit before public benchmark claims or leaderboard launches

Practical cadence:

- monthly for active benchmark development
- quarterly once the benchmark is stable

## Reviewer recruiting strategy

Good sources:

- startup founders in your network
- early operators at seed to Series C companies
- PMs, growth leads, CFO/finance leads, people/ops leads
- former startup operators with pattern recognition across multiple companies

Prefer operators who:

- have owned real tradeoffs, not just advised on them
- have seen failure modes, not only growth phases
- can explain why a decision is bad even if it looks superficially reasonable

Avoid overconcentrating reviewers from one company, one function, or one stage.

## Onboarding flow

Recommended onboarding:

1. share a short benchmark overview
2. explain that the benchmark is automated and they are calibrating it
3. train reviewers on one public example packet
4. review one practice run together
5. then assign hidden-pack work independently

Reviewers should receive:

- the reviewer manual
- the review packet
- rubric definitions
- confidentiality and conflict-of-interest rules
- turnaround expectations

## Quality controls

Require:

- independent first-pass reviews
- explicit note fields for strengths, weaknesses, and gaming signals
- reviewer identity and role metadata
- scenario-level disagreement tracking
- adjudication when rubric gaps are large

Escalate any target family when:

- recommendation agreement falls below `0.67`
- mean rubric gap exceeds the current gate
- reviewers flag benchmark-gaming behavior
- reviewers say the scenario is underspecified or unrealistic

## Compensation and incentives

Treat this like expert evaluation work, not casual feedback.

Reasonable models:

- paid hourly review sessions
- fixed stipend per study wave
- advisory credit plus stipend

Do not rely only on unpaid favors if you want consistent, benchmark-grade calibration.

## Confidentiality and leakage rules

For hidden packs:

- reviewers should not receive raw hidden scenario files
- reviewers should work from generated review packets and traces
- reviewers should agree not to share scenario details publicly
- any suspected leak should trigger pack review

## What success looks like

The taskforce is working if:

- study waves complete on time
- reviewer disagreement is understandable and actionable
- evaluator flaws are caught before leaderboard claims
- scenario promotions are evidence-backed
- you can publish a credible operator-calibration section in benchmark documentation

## Immediate recommended setup

If you want to start now, use this initial structure:

- `1` benchmark lead
- `1` ops coordinator
- `6` reviewers
- Wave 001 on:
  - canary hidden pack
  - strategy hidden pack
  - real-world hidden pack

That is the smallest serious taskforce I would recommend.
