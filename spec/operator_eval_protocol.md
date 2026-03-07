# Operator Evaluation Protocol

## 1. Goal

This protocol defines how founder and operator reviews should be captured so human calibration is reproducible and auditable rather than anecdotal.

## 2. Reviewer pool

Each promoted calibration study SHOULD include at least:

- one founder or CEO
- one product or growth operator
- one finance, ops, or people operator

Reviewers SHOULD have direct startup operating experience in the target stage where possible.

## 3. Review unit

One operator review is one reviewer scoring one run on one scenario.

Required context:

- scenario id
- track
- split
- scenario pack version
- runner type
- runner id
- seed
- trace or replay reference

## 4. Rubric

The core rubric uses five 1-to-5 scores:

- survival and risk management
- capital allocation quality
- customer trust handling
- people leadership quality
- strategic quality

The reviewer MUST also assign one overall recommendation:

- `pass`
- `borderline`
- `fail`

## 5. Notes and exploit review

Review notes SHOULD capture:

- strengths
- weaknesses
- recommended actions
- benchmark-gaming signals

If a reviewer believes a run looks benchmark-specific rather than operator-quality, that suspicion should be recorded in `benchmark_gaming_signals`.

## 6. Aggregation

Calibration summaries SHOULD report:

- review count
- reviewer count
- scenario count
- mean rubric scores overall
- recommendation distribution
- per-scenario disagreement flags

Disagreement is a feature, not a bug. Hidden canary scenarios are expected to stress this surface.

## 7. Promotion bar

A scenario family SHOULD NOT be promoted to official benchmark use unless:

- at least two operators review a representative sample
- reviewers agree the scenario is understandable and solvable
- major exploit signals are documented
- scoring behavior is directionally aligned with operator judgment

## 8. Current artifact support

The reference repo now includes:

- review schema: [tsb_operator_review.schema.json](/C:/Users/USER/Desktop/startup-bench/schemas/tsb_operator_review.schema.json)
- summary schema: [tsb_operator_review_summary.schema.json](/C:/Users/USER/Desktop/startup-bench/schemas/tsb_operator_review_summary.schema.json)
- example review: [minimal_operator_review.json](/C:/Users/USER/Desktop/startup-bench/examples/minimal_operator_review.json)
- example summary: [minimal_operator_review_summary.json](/C:/Users/USER/Desktop/startup-bench/examples/minimal_operator_review_summary.json)

## 9. Practical next step

The next benchmark-hardening step is to collect operator reviews on:

- hidden canary pack
- hidden strategy pack
- real-world crisis test pack

That gives calibration signal on exploit resistance, long-horizon judgment, and crisis response quality.
