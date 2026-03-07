# TheStartupBench SOTA Task Roadmap

Last updated: 2026-03-07

## Goal

This roadmap translates the benchmark audit into concrete build tasks required to move TheStartupBench from strong prototype to benchmark-standard candidate.

## Workstream 1. Hidden-Eval Integrity

### Objective

Make hidden evaluation genuinely contamination-resistant and operationally trustworthy.

### Tasks

1. Replace the current checked-in `fresh` pack with truly distinct hidden scenarios.
2. Enforce a rule that `fresh` scenario ids and files cannot duplicate `test` scenario ids and files.
3. Add pack-lineage metadata:
   - origin family
   - predecessor
   - successor
   - contamination status
   - retirement reason
4. Add canary scenarios designed to detect benchmark-specific overfitting.
5. Add a contamination adjudication workflow and required public incident log.
6. Add a private review checklist for promotion from draft to `test` or `fresh`.
7. Add CI checks that reject duplicate hidden refs, reused scenario ids, and illegal split cloning.

### Exit criteria

- no hidden pack is a split-only clone of another pack
- contamination events can be logged and retired cleanly
- fresh-pack generation creates genuinely new hidden content

## Workstream 2. Official Evaluation Discipline

### Objective

Make scores comparable across models and submissions.

### Tasks

1. Define an official scaffold bundle:
   - system prompt policy
   - tool policy
   - context policy
   - retry policy
   - timeout policy
2. Define official default hyperparameter policy for hosted evaluation.
3. Add official run manifests that record:
   - benchmark version
   - pack version
   - scaffold version
   - prompt policy version
   - model settings
4. Add suite-level uncertainty reporting:
   - SEM
   - confidence intervals
   - pass@k where appropriate
5. Separate public self-reported runs from official hosted runs in leaderboard outputs.
6. Add benchmark freeze rules for official reporting windows.

### Exit criteria

- two different users running the same model under official settings produce comparable reports
- official leaderboard entries are clearly distinguishable from ad hoc runs

## Workstream 3. Scenario Corpus Scale

### Objective

Grow from illustrative suites to a benchmark-scale corpus.

### Tasks

1. Establish target v1 corpus minimums:
   - `dev`: at least 100 scenarios
   - `test`: at least 100 hidden scenarios
   - `fresh`: at least 30 hidden scenarios per refresh cycle
2. Build scenario families for:
   - `0to1`
   - `product`
   - `gtm`
   - `finance`
   - `people`
   - `board`
   - `crisis`
   - `scale`
3. Add difficulty tiers:
   - easy
   - normal
   - hard
   - frontier
4. Add scenario templates and generators so new scenarios are created from primitives rather than hand-authored from scratch.
5. Add scenario review tags:
   - solvability confidence
   - realism confidence
   - benchmark exploit risk
   - calibration notes

### Exit criteria

- no single track dominates the benchmark identity
- corpus size is large enough that leaderboard noise is materially reduced

## Workstream 4. Startup World Realism

### Objective

Make the environment closer to actual startup operation rather than simplified management gameplay.

### Tasks

1. Expand hiring mechanics:
   - pipeline stages
   - sourcing channels
   - close rates
   - backfill delays
2. Expand customer model:
   - segments
   - retention curves
   - expansion
   - support load coupling
3. Expand finance model:
   - debt
   - dilution
   - cap table changes
   - financing terms
4. Expand market model:
   - competitor launches
   - pricing pressure
   - macro shocks
   - supplier dependency
5. Expand people model:
   - morale propagation
   - attrition risk
   - manager bandwidth
   - reorg consequences
6. Expand legal/compliance model:
   - investigation states
   - breach reporting timelines
   - contractual obligations

### Exit criteria

- state transitions produce believable second-order effects
- multiple “locally good” actions can still create long-term harm

## Workstream 5. Evaluator Quality

### Objective

Make scoring more robust, auditable, and aligned with expert expectations.

### Tasks

1. Convert the score into explicit components:
   - enterprise value proxy
   - survival
   - trust/compliance
   - capital efficiency
   - stakeholder quality
2. Add hard constraints:
   - bankruptcy
   - legal violation thresholds
   - severe trust collapse
   - catastrophic collateral damage
3. Add collateral-damage penalties for:
   - unnecessary layoffs
   - support backlog explosions
   - harmful pricing moves
   - customer trust damage
4. Add evaluator reports that explain why a run failed.
5. Add expert calibration studies comparing score outputs to operator judgments.
6. Use semantic judges only for narrow artifacts:
   - board memo
   - customer incident response
   - hiring rationale

### Exit criteria

- score decomposition is inspectable
- expert reviewers broadly agree that high-scoring runs are actually strong operating behavior

## Workstream 6. Human And Baseline Calibration

### Objective

Make benchmark difficulty and ranking interpretable.

### Tasks

1. Add stronger scripted baselines by track.
2. Add operator-inspired baseline families:
   - conservative CFO-style
   - aggressive growth-style
   - crisis specialist
   - product-led optimizer
3. Run human/operator baselines:
   - founders
   - PMs
   - finance operators
   - GTM leaders
4. Add human solvability review before official scenario promotion.
5. Publish model-vs-human gap reports per track.

### Exit criteria

- the benchmark clearly separates weak heuristics, strong heuristics, humans, and frontier models

## Workstream 7. Governance And Leaderboard Operations

### Objective

Turn policy docs into enforceable benchmark operations.

### Tasks

1. Add a known-issues ledger.
2. Add an exploit-report template and response SLA.
3. Define official leaderboard entry types:
   - hosted official
   - reproduced third-party
   - self-reported unofficial
4. Define retirement policy for benchmark and pack major versions.
5. Publish benchmark release notes for every versioned change.
6. Add required metadata for public leaderboard entries:
   - contamination flag
   - code availability
   - prompt policy
   - cost
   - wall-clock time
   - repeated-run count

### Exit criteria

- public results are governed by process, not only by maintainers’ judgment

## Workstream 8. Testing And Regression Hardening

### Objective

Bring the test surface closer to benchmark-grade stability.

### Tasks

1. Add evaluator regression tests for difficult tradeoff cases.
2. Add long-horizon multi-turn scenario tests.
3. Add snapshot tests for official suite statistics.
4. Add negative tests for hidden-pack integrity violations.
5. Add CI gates for:
   - no duplicate hidden scenario ids across hidden packs
   - no split-cloned fresh packs
   - required changelog updates for pack promotions
6. Add reproducibility tests for clean-shell installs and locked environments.

### Exit criteria

- benchmark changes that alter evaluation behavior are detected before release

## Workstream 9. Differentiators Needed For Category Leadership

### Objective

Make TheStartupBench not just “startup-flavored AppWorld,” but the definitive benchmark for business operating judgment.

### Tasks

1. Build multi-quarter planning scenarios, not just short crisis windows.
2. Add stakeholder conflict scenarios where no action is universally good.
3. Add board and investor communication as constrained evaluated artifacts.
4. Add “save the company” scenarios where runway, trust, and product all compete.
5. Add strategic pivot scenarios where the agent must change the company model itself.
6. Add operator-quality dashboards and incomplete information surfaces.
7. Add delayed-consequence scenarios where early vanity wins create later failures.

### Exit criteria

- the benchmark measures startup operating judgment, not just local business optimization

## Priority Order

Highest priority:

1. Hidden-eval integrity
2. Official evaluation discipline
3. Scenario corpus scale
4. Evaluator quality
5. Human and baseline calibration

Second tier:

6. Startup world realism
7. Governance and leaderboard operations
8. Testing and regression hardening

Strategic differentiator tier:

9. Category-leadership features specific to startup operation

## Definition Of SOTA Readiness

TheStartupBench should only be described as SOTA-ready if all of the following are true:

- distinct public, hidden test, and fresh packs exist at meaningful scale
- official hosted evaluation settings are locked and documented
- uncertainty metrics are published for official results
- at least one human/operator baseline exists
- score quality is calibrated against expert judgment
- benchmark governance is live
- scenario coverage spans the full startup operating surface
- no major integrity drifts remain in hidden-pack handling

## Bottom Line

TheStartupBench does not need a new philosophy. It needs execution hardening.

The path to category leadership is:

- preserve the current executable benchmark architecture
- fix hidden-eval integrity
- scale the scenario corpus
- improve evaluator quality
- calibrate against real operators
- enforce benchmark governance as process
