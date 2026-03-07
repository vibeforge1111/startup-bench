# Model Reviewer Panel

Last updated: 2026-03-07

## Goal

This document explains how to use frontier models as a synthetic reviewer panel for TheStartupBench.

Recommended use:

- run automated benchmark evaluation as normal
- ask several frontier models to independently review the resulting packets
- compare their judgments to the benchmark scorer
- compare them to human reviewers when available

This is useful for:

- fast early calibration before a full human wave
- finding disagreement cases worth human adjudication
- stress-testing whether the evaluator is obviously misaligned

This is not a replacement for real human calibration.

## Best way to use it

Treat the model panel as a shadow lane, not the official human lane.

Use three lanes:

- automated benchmark score
- synthetic reviewer panel
- human/operator taskforce

The synthetic panel is strongest as:

- a pre-screen for suspicious scenarios
- a way to find disagreement clusters
- an additional signal before spending human review capacity

## Recommended panel setup

For a first synthetic wave:

- one Gemini run
- one Claude Opus run
- one GPT run

All three should review the same exact packet independently.

Keep fixed:

- the packet
- the trace
- the scoring rubric
- the output JSON format

Do not let one model see another model's review before submitting.

## What to send each model

Send:

- the reviewer manual
- the packet summary
- the trace or replay summary
- the required JSON output template

Ask the model to act as a startup operator reviewer, not as a benchmark optimizer.

## Output format

The easiest operational format is a valid operator-review JSON artifact.

That means each model should return a JSON object matching [tsb_operator_review.schema.json](/C:/Users/USER/Desktop/startup-bench/schemas/tsb_operator_review.schema.json#L1).

Use the fillable template:

- [operator_review_fill_template.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_review_fill_template.json#L1)

Then you can feed the saved JSON files directly into:

- `aggregate-operator-reviews`
- `build-calibration-report`
- `compile-calibration-study`

## Reviewer identity convention

Use stable synthetic reviewer ids like:

- `gemini_reviewer_001`
- `opus_reviewer_001`
- `gpt_reviewer_001`

Suggested reviewer metadata:

- role: `model_reviewer`
- functional_domain: `synthetic_panel`

If you want to simulate specialization, you can also create:

- `gpt_growth_reviewer_001`
- `opus_strategy_reviewer_001`
- `gemini_ops_reviewer_001`

but keep that explicit in metadata.

## Prompting guidance

Your prompt should say:

- review independently
- use only packet-visible information
- do not assume hidden benchmark rules
- score the five rubric dimensions
- choose `pass`, `borderline`, or `fail`
- provide concrete strengths, weaknesses, recommended actions, and gaming signals
- return valid JSON only

Do not ask the model to be optimistic, harsh, or consensus-seeking.

Ask it to be a sober operator reviewer.

## How to interpret synthetic panel results

Good uses:

- if all three models disagree with the benchmark scorer in the same direction, escalate that scenario family
- if models disagree wildly with each other, escalate for human adjudication
- if the synthetic panel converges with the human panel, confidence improves

Bad uses:

- promoting a scenario family because models agreed
- replacing real operators with models
- averaging model reviews and calling it a human baseline

## Recommended workflow

1. Run the target hidden study wave.
2. Export the packet and reviewer instructions.
3. Send the same material separately to Gemini, Opus, and GPT.
4. Save each returned JSON review as its own file.
5. Aggregate those reviews as a synthetic panel.
6. Compare synthetic panel judgments to benchmark scores.
7. Use the result to decide where to spend human review capacity.

## Strong warning

Synthetic reviewers are useful, but they share many benchmark-era priors and blind spots.

They are good for:

- fast coverage
- consistency checks
- disagreement surfacing

They are not good enough to be the final authority on whether the benchmark reflects real startup judgment.

Use them as force multipliers for the human taskforce, not substitutes for it.
