# Benchmark Contract

## 1. Benchmark identity

Name: `TheStartupBench`

Short name: `TSB`

Version namespace:

- benchmark version: `major.minor.patch`
- scenario pack version: `major.minor.patch`
- scaffold version: `major.minor.patch`

## 2. Primary objective

TSB measures whether an agent can operate a startup-like business over time under uncertainty across multiple business functions using constrained tools and auditable actions.

## 3. Tracks

Official track IDs:

- `0to1`
- `b2b_saas`
- `consumer`
- `deeptech`
- `marketplace`
- `crisis`
- `scale`
- `board`
- `gtm`
- `finance`
- `people`
- `product`

Each scenario MUST belong to exactly one primary track.

Each scenario MAY include secondary tags such as:

- `pricing`
- `fundraising`
- `hiring`
- `incident_response`
- `retention`
- `enterprise_sales`
- `regulation`

## 4. Evaluation modes

Modes:

- `dev`: public scenarios and public evaluator details
- `test`: official leaderboard scenarios with hidden content or hidden evaluator internals
- `fresh`: recently added scenarios intended to reduce contamination risk

Leaderboard-grade evaluations SHOULD use `test` and MAY separately report `fresh`.

## 5. Benchmark invariants

All official scenarios MUST satisfy:

- partial observability
- explicit state transitions
- bounded action space
- seeded reproducibility
- programmatic evaluation for most scored outcomes
- auditable final scorecard

Official evaluation MUST NOT depend primarily on free-form LLM judging.

## 6. Benchmark world requirements

Each official scenario MUST model at least:

- finance
- product or service state
- customers or demand side
- team capacity
- market or external environment
- stakeholder constraints

Each official scenario SHOULD model delayed consequences rather than immediate reward only.

## 7. Official runtime requirements

The official scaffold MUST:

- enforce tool permissions
- timestamp actions
- log all tool calls and outputs
- persist state transitions
- emit trace artifacts matching the trace schema
- expose benchmark, scenario, and scaffold versions in all outputs

## 8. Randomness policy

Each run MUST specify:

- scenario id
- scenario version
- run seed
- model id
- agent configuration hash

Seeded randomness MUST be sufficient for exact replay within a benchmark version.

## 9. Repeated-run policy

Leaderboard-grade submissions MUST include repeated runs.

Baseline recommendation:

- `n >= 5` runs per evaluated scenario slice for stochastic agents

Reported metrics MUST include mean and a variance estimate.

## 10. Human baselines

An official benchmark release SHOULD include:

- random baseline
- trivial scripted baseline
- strong scripted baseline
- non-expert human baseline
- domain-operator baseline

## 11. Compatibility policy

Minor benchmark versions MAY add tracks, scenario metadata, and new optional fields.

Major benchmark versions MAY change:

- scoring contract
- required trace fields
- leaderboard policy

Patch versions MUST only fix bugs or clarify requirements.
