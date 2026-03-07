# Reviewer Manual

Last updated: 2026-03-07

## Purpose

This manual is for founders and operators reviewing TheStartupBench study packets.

You are not grading a model for style. You are helping test whether the benchmark's automated scoring matches real startup judgment.

## What you review

You will receive a review packet containing:

- target family and study id
- scenario ids and track labels
- scenario summaries
- runner identity
- fixed seed and run configuration
- trace or replay references
- scoring rubric

You should evaluate the business quality of the run, not whether you personally would use identical wording.

## What good reviewing looks like

Good review behavior:

- judge outcomes and reasoning quality together
- focus on major business tradeoffs
- penalize reckless actions even if they create short-term upside
- reward durable judgment under uncertainty
- flag benchmark-specific gaming patterns

Bad review behavior:

- overfocusing on formatting or tone
- rewarding confident nonsense
- penalizing reasonable ambiguity handling
- importing assumptions not visible in the packet

## Rubric

Each review includes five rubric scores from `1` to `5`.

### 1. Survival and risk management

`1`: creates serious existential or governance risk  
`3`: acceptable but misses important risk controls  
`5`: protects company survival while preserving room to operate

### 2. Capital allocation

`1`: wastes capital or takes unjustified financial risk  
`3`: roughly acceptable but inefficient or weakly prioritized  
`5`: allocates money and founder attention with strong discipline

### 3. Customer trust

`1`: damages trust, communication, or reliability badly  
`3`: acceptable but not strong under pressure  
`5`: protects trust and handles customers credibly

### 4. People leadership

`1`: creates avoidable org stress, confusion, or morale damage  
`3`: acceptable but narrow or incomplete people handling  
`5`: manages team tradeoffs, workload, and leadership communication well

### 5. Strategic quality

`1`: short-term or incoherent decisions that weaken the company  
`3`: locally reasonable but strategically limited  
`5`: decisions are well sequenced, durable, and aligned with company reality

## Overall recommendation

Choose one:

- `pass`
- `borderline`
- `fail`

Interpretation:

- `pass`: the run shows operator-quality judgment for the scenario
- `borderline`: some decisions are plausible, but quality is not benchmark-trustworthy
- `fail`: the run is materially bad, reckless, or strategically unsound

## How to detect benchmark-gaming

Flag benchmark-gaming when the run appears to optimize the benchmark rather than operate the company well.

Examples:

- defaulting to price hikes in obviously fragile trust conditions
- hiring automatically because open roles exist
- ignoring customer or team damage while preserving headline metrics
- making actions that only make sense if the agent knows the evaluator
- repeating one canned playbook across different scenario types

## Review process

1. Read the packet summary first.
2. Read the trace or replay without scoring immediately.
3. Ask: what was the core business problem?
4. Ask: did the run identify the real problem or only the visible symptom?
5. Score the five rubric dimensions.
6. Choose `pass`, `borderline`, or `fail`.
7. Add notes:
   - strengths
   - weaknesses
   - recommended actions
   - gaming signals

## Notes guidance

Strong notes are concrete.

Useful:

- "Protected trust by slowing monetization until support load stabilized."
- "Ignored treasury concentration risk and treated cash as fully liquid."
- "Looked benchmark-shaped: defaulted to cost cutting without re-evaluating demand."

Weak:

- "Felt good."
- "Reasonable overall."
- "Maybe too aggressive."

## Independence rules

Please do:

- submit your own judgment independently
- avoid discussing hidden scenarios before submission
- disclose if you know the scenario source or think you recognize it

Please do not:

- coordinate scores with other reviewers before first submission
- infer hidden state from how you think the benchmark works
- optimize your review to match expected consensus

## If the scenario feels wrong

If a packet feels unrealistic, underspecified, or unfair:

- say so explicitly
- explain what information is missing
- explain whether the flaw is in the scenario, the run, or the benchmark framing

That feedback is valuable. It is part of benchmark hardening.

## Expected reviewer mindset

Review as if you were assessing whether this run reflects credible startup operation under uncertainty.

You are not being asked:

- "would I do exactly this?"

You are being asked:

- "is this decision process good enough that a serious benchmark should reward it?"
