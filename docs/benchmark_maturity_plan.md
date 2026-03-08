# TheStartupBench Benchmark Maturity Plan

Last updated: 2026-03-08

## Purpose

This document is the deeper operating plan for moving TheStartupBench from a strong benchmark-shaped system to a benchmark that can credibly sit beside the commonly used frontier benchmark set.

It is narrower than [sota_task_roadmap.md](/C:/Users/USER/Desktop/startup-bench/docs/sota_task_roadmap.md) and more operational than [benchmark_status.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_status.md).

The goal is to answer three questions clearly:

1. where the benchmark is strong right now
2. where it is still below the benchmark bar set by commonly used systems
3. what concrete implementation sequence closes those gaps without compromising benchmark standards

## Current maturity read

### 1. Methodology

Current status: strong

Evidence:

- executable, stateful scenarios
- hidden `test` and hidden `fresh` splits
- canary pack support
- trace-aware, componentized evaluation
- explicit pack versioning and lifecycle tracking
- benchmark-governance policy docs

Assessment:

- this is already benchmark-grade methodology
- the current gap is not philosophy
- the current gap is maturity, corpus scale, calibration depth, and outside trust

### 2. Corpus scale

Current status: early but real

Current hidden `test` inventory across active packs:

- strategy: `10`
- coverage: `14`
- operator: `16`
- real-world: `8`
- canary: `2`
- total hidden `test`: `50`

Assessment:

- enough to be technically meaningful
- not enough to support strong category-default or leaderboard-default claims
- still vulnerable to overfitting by determined benchmark-focused systems

### 3. Coverage quality

Current status: broad and improving

Tracks with meaningful hidden coverage now:

- `board`
- `gtm`
- `finance`
- `people`
- `product`
- `scale`
- `0to1`
- `crisis`

Assessment:

- much stronger than the repo’s earlier state
- broad enough to claim real startup-operator coverage
- not yet deep enough in every track to claim benchmark-complete coverage

### 4. Evaluator quality

Current status: good foundation, still incomplete

Strengths:

- explicit component scoring
- active components now include:
  - `cash_efficiency`
  - `revenue_quality`
  - `customer_health`
  - `product_health`
  - `team_health`
  - `risk_management`
  - `strategic_coherence`
- trace-aware behavioral penalties
- bounded artifact evaluation for:
  - board updates
  - customer communication
  - hiring plans

Remaining gap:

- track-specific evaluator bundles are still uneven
- delayed-effect calibration is still limited
- human/operator alignment remains incomplete

### 5. Anti-gaming and benchmark integrity

Current status: structurally good, statistically still thin

Strengths:

- hidden `test`
- hidden `fresh`
- canaries
- public manifest redaction
- pack lifecycle tracking

Remaining gap:

- pack breadth still too small for robust exploit resistance
- contamination response is documented but not yet battle-tested
- refresh cadence is not yet an active benchmark operation

### 6. Calibration and external credibility

Current status: early

Strengths:

- operator review protocols exist
- synthetic and human handoff artifacts exist
- calibration machinery exists in the reference tooling

Remaining gap:

- not enough real operator baseline data
- not enough published disagreement analysis
- not enough repeated external usage to create benchmark trust

## Maturity rubric

| Area | Score | Meaning |
|---|---:|---|
| methodology | `8.5/10` | already benchmark-grade in structure |
| coverage breadth | `7.0/10` | broad startup surface, still uneven in depth |
| corpus scale | `4.5/10` | real but small |
| evaluator maturity | `6.5/10` | strong foundation, still under-calibrated |
| anti-gaming | `7.5/10` | good structure, not enough volume yet |
| leaderboard readiness | `5.0/10` | protocol exists, operations not mature enough |
| calibration maturity | `4.0/10` | tooling exists, evidence base still thin |
| external credibility | `3.5/10` | design is ahead of adoption |

## Benchmark tiers

### Tier A. Benchmark-shaped

Definition:

- executable benchmark
- hidden eval
- scoring decomposition
- basic governance

TheStartupBench status: achieved

### Tier B. Serious internal benchmark

Definition:

- enough hidden depth to compare systems credibly
- canaries and fresh packs
- stable evaluation protocol
- broad track coverage

TheStartupBench status: mostly achieved, but still thin on hidden volume

### Tier C. Community-credible benchmark

Definition:

- larger stable hidden corpus
- real calibration evidence
- contamination and retirement history
- repeated external usage

TheStartupBench status: not yet

### Tier D. Commonly used frontier benchmark

Definition:

- broadly cited
- externally adopted
- stable leaderboard norms
- established trust in scores and procedures

TheStartupBench status: not yet

## What must be true before stronger SOTA-style claims

The benchmark should not claim parity with the commonly used frontier benchmark set until all of the following are true:

1. hidden test inventory is at least `75-100` scenarios
2. every major track has at least `4-6` hidden `test` scenarios and matching fresh coverage
3. operator calibration exists for promoted families, not just protocols
4. an official evaluation profile is frozen for a real reporting window
5. contamination and pack retirement operations have been exercised in practice
6. repeated external model runs exist under the official protocol

## Implementation program

### Milestone v0.9.5

Objective:

- move from strong prototype to stable internal benchmark candidate

Exit targets:

- hidden `test` inventory >= `50`
- strategy pack expanded across `board`, `product`, `scale`, and `gtm`
- coverage pack expanded across all major startup-success surfaces already in scope
- evaluator regressions in place for every new family
- official benchmark task ledger and board in active use

### Milestone v0.10.0

Objective:

- reach community-credible benchmark candidate status

Exit targets:

- hidden `test` inventory >= `75`
- hidden `fresh` inventory >= `40`
- every major track has at least `4` hidden `test` slices
- operator calibration wave completed for promoted packs
- public benchmark ops docs frozen for one reporting cycle

### Milestone v1.0.0

Objective:

- become a defensible public benchmark release

Exit targets:

- hidden `test` inventory >= `100`
- hidden `fresh` refresh process live
- calibration gap reporting published
- official leaderboard entry policy operational
- at least one human/operator baseline published
- third-party reproduction or hosted-run evidence exists

## Workstreams and implementation focus

### Workstream 1. Corpus scale

Priority: highest

Implementation focus:

- add `36-61` more hidden `test` scenarios
- keep packs balanced by track rather than adding shallow volume
- expand the thinnest tracks first

Current biggest opportunities:

- `product`
- `scale`
- `0to1`
- `gtm`

### Workstream 2. Calibration

Priority: highest

Implementation focus:

- turn operator-review tooling into actual review waves
- record disagreements on scenario realism, solvability, and score direction
- gate pack promotion on calibration completion

Current execution artifact set:

- [operator_human_review_wave_002_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_002_manifest.json)
- [human_review_wave_002.md](/C:/Users/USER/Desktop/startup-bench/docs/human_review_wave_002.md)

### Workstream 3. Official benchmark operations

Priority: high

Implementation focus:

- freeze official evaluation settings for defined windows
- add pack-rotation and contamination-response procedures
- define leaderboard entry types and release notes

### Workstream 4. Evaluator hardening

Priority: high

Implementation focus:

- deepen track-specific evaluation logic
- add more delayed-effect regression cases
- ensure bounded semantic scoring remains minority-weighted

### Workstream 5. External benchmark credibility

Priority: medium

Implementation focus:

- improve docs for outside runs
- publish benchmark maturity and release notes clearly
- attract repeated benchmark usage from strong systems

## Highest-value next implementations

1. add another `11-15` hidden scenarios across `0to1`, `product`, `scale`, `gtm`, and `finance`
2. create the first formal benchmark task board and milestone tracker
3. define official pack-growth targets per milestone
4. run operator calibration wave against the promoted strategy pack
5. freeze a first stable evaluation window with current official profile

## Task system policy

The benchmark should now be managed with an explicit task system:

- all benchmark-grade work should map to a workstream
- every task should have:
  - milestone
  - owner
  - priority
  - status
  - benchmark risk
  - completion criteria
- scenario additions and benchmark-operation work should both be tracked
- pack promotions should link back to completed tasks

The source of truth for active benchmark execution is [benchmark_task_ledger.json](/C:/Users/USER/Desktop/startup-bench/examples/benchmark_task_ledger.json) and its human-readable companion [benchmark_task_board.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_task_board.md).

## Bottom line

TheStartupBench is already a serious benchmark-shaped system.

It is not yet at the maturity tier of the most commonly used frontier benchmarks because it still needs:

- more hidden volume
- more calibration evidence
- stronger benchmark operations
- more external use

The next phase is not inventing a better benchmark philosophy. It is disciplined execution against the maturity gaps above.
