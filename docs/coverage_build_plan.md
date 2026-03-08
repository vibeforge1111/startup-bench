# Coverage Build Plan

Last updated: 2026-03-08

This is the tactical execution plan for expanding TheStartupBench coverage while preserving the benchmark standards in [coverage_expansion_policy.md](/C:/Users/USER/Desktop/startup-bench/docs/coverage_expansion_policy.md).

This document is intentionally narrower than [sota_task_roadmap.md](/C:/Users/USER/Desktop/startup-bench/docs/sota_task_roadmap.md). The roadmap is the broad benchmark-hardening agenda. This plan is the near-term build sequence.

## Working rules

- ship in small commits
- keep each slice benchmark-auditable
- prefer runtime plus tests plus docs together
- promote new coverage from `dev` to hidden only after calibration gates
- keep near-term expansion away from jurisdiction-specific legal or regulatory interpretation

## Near-term scope boundary

For the current build phase, prioritize coverage that remains benchmark-safe and operationally auditable.

Preferred expansion areas:

- PMF and `0to1` depth
- fundraising and financing quality
- growth experimentation and launch quality
- people leadership and executive management quality
- communication quality under board, customer, and hiring pressure
- multi-quarter strategy and sequencing

De-prioritized for now:

- deep legal progression
- jurisdiction-specific regulatory interpretation
- scenario families that require scoring legal correctness rather than startup operator judgment

## Phase 1. Tool-surface closure

Objective:

- close existing gaps between documented tool surface and runtime behavior

Tasks:

1. implement `product.launch`
2. implement `growth.experiment.create`
3. implement `growth.experiment.review`
4. implement `people.org.propose`
5. add runtime tests and metric-report coverage
6. sync docs with the implemented tool count and domains

Status:

- started on 2026-03-08

Exit criteria:

- no cataloged benchmark tool used for official coverage is missing from the reference runtime

## Phase 2. PMF and 0-to-1 coverage

Objective:

- strengthen the benchmark on startup discovery rather than only post-PMF operation

Tasks:

1. add a richer `0to1` scenario family centered on PMF search
2. model experiment loops, false-positive demand, and founder-led sales tradeoffs
3. add at least one hidden `test` and one hidden `fresh` PMF variant
4. add evaluator logic for learning velocity, activation quality, and burn-vs-signal tradeoffs

Exit criteria:

- `0to1` is represented by a family, not a single illustrative scenario

## Phase 3. Financing realism

Objective:

- make startup survival and board decisions more realistic under financing pressure

Tasks:

1. add debt, bridge, and financing-term mechanics
2. add board-pressure scenarios where dilution, runway, and narrative quality conflict
3. add evaluator penalties for cosmetically improved survival that worsen financing quality
4. add hidden financing variants and calibration targets

Exit criteria:

- finance coverage includes more than burn control and treasury rebalancing

## Phase 4. Explicit score expansion

Objective:

- move from four active score dimensions toward a more complete startup-success scorecard

Tasks:

1. add explicit `product_health`
2. add explicit `team_health`
3. add explicit `risk_management`
4. keep semantic judging minority-weighted and audit-bound
5. add evaluator regression tests for score shifts and constraint thresholds

Exit criteria:

- key startup-success areas no longer rely only on indirect proxy scoring

## Phase 5. Hidden-pack and calibration expansion

Objective:

- ensure each new area is benchmark-grade rather than public-demo-only

Tasks:

1. add hidden `test` and `fresh` variants for new PMF and financing families
2. run exploit review on the new coverage
3. add operator review targets for PMF, finance, and communication-heavy runs
4. log any score-vs-operator disagreements before promotion

Exit criteria:

- new coverage areas participate in hidden evaluation and calibration, not just dev benchmarking

## Phase 6. Governance-ready promotion

Objective:

- convert expansion work into official benchmark coverage without compromising leaderboard quality

Tasks:

1. update pack lifecycle and benchmark status docs
2. version any scoring or pack-boundary changes
3. add smoke coverage for new scenario families
4. keep fresh/test separation explicit in public manifests

Exit criteria:

- the new coverage can be included in official claims without weakening benchmark integrity

## Near-term commit strategy

Recommended sequence:

1. process and policy docs
2. runtime/tool support
3. tests for each new mechanic
4. docs sync
5. scenario family additions
6. evaluator additions
7. hidden-pack additions
8. calibration artifacts

## Current focus

Current execution focus:

- keep extending benchmark-safe coverage families with small, versioned commits
- prioritize communication quality and growth experimentation depth over legal/regulatory expansion
- keep board-communication scoring rubric-bound and minority-weighted, starting with `board.update` completeness against live operating stress
- extend multi-quarter strategy and sequencing through the dedicated hidden strategy pack rather than diluting it into generic coverage packs
- keep strategy-pack additions focused on executable delayed-consequence and sequencing tradeoffs such as platform capacity, migration quality, hiring lead time, and renewal timing rather than memo-only strategy prompts
- extend board/product interaction coverage through truth-telling and launch-sequencing scenarios, not generic “board memo” judging
- extend GTM sequencing in the strategy pack through multi-quarter proof, reference, and channel-timing tradeoffs rather than short-window pipeline-only pressure
