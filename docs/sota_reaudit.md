# TheStartupBench SOTA Re-Audit

Last updated: 2026-03-07

## Executive Verdict

Current decision: `defer`

Current label:

- strong benchmark prototype
- strong reference implementation
- not yet SOTA
- on the right methodological track

Current stability score: `7.4/10`

TheStartupBench has not drifted off the benchmark path. In fact, it has moved closer to the methodology used by strong agent benchmarks:

- executable environment
- constrained tools
- hidden `test` and `fresh` packs
- redacted public manifests
- versioned run artifacts
- uncertainty-aware reporting
- canary packs for anti-gaming pressure
- human and synthetic review calibration lanes

The benchmark is now structurally serious. The remaining gap is not framing. The remaining gap is benchmark depth, corpus scale, calibration evidence, and operations.

## What Improved Since The Earlier Audit

The earlier audit is now partially stale. The following benchmark weaknesses have materially improved:

- hidden `fresh` pack integrity is no longer a clone problem; hidden suite-family checks now enforce distinct `test` and `fresh` packs
- official evaluation settings now exist as first-class artifacts
- suite, campaign, and submission outputs now include SEM and 95 percent confidence intervals
- hidden canary packs now exist for exploit and overfit detection
- human/operator calibration is no longer just a policy idea; it now has executable study runs, packet generation, assignment workflows, import flows, and study compilation
- synthetic reviewer support now has real prompt-bundle export and raw review import workflows
- the benchmark is broader than crisis response alone; it now covers `0to1`, `b2b_saas`, `board`, `crisis`, `finance`, `gtm`, `people`, `product`, and `scale`

These are meaningful benchmark-hardening improvements, not cosmetic additions.

## What TheStartupBench Now Does Well Relative To SOTA Patterns

### 1. Execution-first evaluation

Like `SWE-bench`, `Terminal-Bench`, `WebArena`, `WorkArena`, and `AppWorld`, TheStartupBench evaluates behavior inside a constrained executable environment rather than scoring startup essays.

This remains one of its strongest properties.

### 2. Hidden-eval awareness exists early

Top benchmarks increasingly assume public static corpora will be contaminated. TheStartupBench now has:

- public dev packs
- hidden `test` packs
- hidden `fresh` packs
- public redacted manifests
- public lifecycle changelog
- hidden suite-family integrity checks

This is aligned with the right benchmark logic.

### 3. Auditability is strong

The repo has:

- schemas
- manifests
- traces
- score reports
- run manifests
- suite reports
- calibration reports
- review packets
- submission artifacts

That makes benchmark behavior inspectable, which is essential for credibility.

### 4. Anti-gaming pressure is no longer absent

The canary hidden pack family is a real methodological strength. It means the benchmark is not only checking whether a model scores well, but also whether it is falling into exploit-shaped behavior.

### 5. Startup-specific differentiation is real

The benchmark now has a legitimate domain identity:

- resource allocation under runway pressure
- trust/compliance and incident tradeoffs
- board and stakeholder conflict
- GTM, finance, product, people, and scale choices
- real-world-derived startup crisis patterns

That gives it a genuine chance to define the startup benchmark category.

## Where It Still Falls Short Of SOTA

### 1. Corpus scale is still too small

This is the biggest blocker.

The repo now has meaningful breadth, but it still does not have a benchmark-scale corpus. It has:

- a 9-track dev suite
- multiple small hidden pack families
- a 10-scenario real-world pack

That is enough for a strong prototype, not enough for benchmark authority.

What SOTA requires:

- larger per-track scenario families
- enough scenario count to reduce leaderboard noise
- scenario diversity that prevents one heuristic family from generalizing too easily

### 2. Human calibration machinery exists, but human evidence does not

This is the second biggest blocker.

The repo now has:

- operator review schemas
- reviewer manual
- taskforce strategy
- study manifests
- review assignments
- CSV review workflows
- synthetic panel tooling

But it still does not have real collected multi-review operator data in the repository process.

Until real founder/operator review waves are run, calibration remains procedural rather than empirical.

### 3. Evaluator depth is still early

The benchmark has programmatic scoring, which is necessary, but not yet sufficient.

Remaining evaluator gaps:

- richer track-specific scoring
- harder penalties for collateral damage and second-order effects
- stronger treatment of delayed strategy errors
- more explicit survival/trust/compliance constraint logic
- calibrated semantic judging for board/customer/people communication artifacts

### 4. Official benchmark operations are still thin

The benchmark now has official profile artifacts, but not yet full benchmark operations comparable to stronger evaluation ecosystems.

Still missing:

- official hosted run policy in practice
- adjudication process for disputed scenarios
- known-issues ledger
- exploit-retirement workflow
- submission review and acceptance protocol with humans in the loop

### 5. Baseline ecosystem is still small

TheStartupBench has several heuristic baselines, which is good for internal pressure testing, but it still lacks:

- stronger scripted baselines
- intentionally narrow specialist baselines by track
- weak baselines and medium baselines published together
- real human/operator baseline runs

Without that, it is hard to show difficulty separation the way stronger benchmarks do.

### 6. World realism is broader, but still incomplete

The runtime is now materially better than before, but still not benchmark-complete.

Important missing realism:

- detailed cap-table and financing structure
- deeper enterprise sales and renewal cycles
- hiring pipeline lag and backfill friction
- more realistic retention/churn heterogeneity
- competitor response loops
- deeper legal/regulatory progression
- multi-quarter compounding on org design and management debt

## Anti-Pattern Sweep

### `ghost_improvement`

Severity: `warn`

Evidence:

- infrastructure quality is improving faster than corpus and human evidence
- the benchmark looks more complete than its empirical coverage really is

Status: `open`

### `golden_demo_collapse`

Severity: `warn`

Evidence:

- multiple small hidden packs still pass cleanly with built-in heuristics
- current difficulty may still be too compressible into a narrow strategy family

Status: `open`

### `schema_wall`

Severity: `info`

Evidence:

- schema discipline is strong
- validation coverage is broad
- trace and artifact contracts are stable

Status: `contained`

### `comfort_zone_optimization`

Severity: `warn`

Evidence:

- recent work has been strong on workflow, docs, and calibration plumbing
- the next bottleneck is corpus depth and empirical calibration, not more meta-tooling

Status: `open`

## Guardrail Status

- `schema_gate`: `pass`
- `lineage_gate`: `warn`
- `complexity_gate`: `warn`
- `transfer_gate`: `warn`
- `memory_hygiene_gate`: `pass`
- `human_gate`: `warn`

Why:

- `schema_gate` passes because the repo has strong schema validation and broad artifact coverage
- `lineage_gate` is only a warning because the benchmark has an evolving roadmap, but the mutation log from weakness to fix to benchmark gain is still not formalized enough
- `complexity_gate` is a warning because tooling and documentation are growing faster than benchmark evidence
- `transfer_gate` is a warning because the benchmark still needs proof that improvements generalize across tracks rather than overfitting the existing packs
- `human_gate` is a warning because the human calibration lane exists, but real review waves are not yet embedded into benchmark promotion

## Pillar Assessment

### Causal Anchor

Status: `warn`

Evidence:

- several earlier weaknesses were addressed with concrete fixes
- however, the benchmark still needs a more explicit weakness-to-fix-to-measured-outcome loop for major benchmark mutations

### Cross-Pollination

Status: `warn`

Evidence:

- multiple tracks now exist
- but many evaluator and runtime assumptions still need stronger cross-track pressure testing

### Entropy Filter

Status: `warn`

Evidence:

- the benchmark now has many strong operational surfaces
- however, the next phase should prioritize corpus and evidence over more control-plane complexity

### Surprise Priority

Status: `pass`

Evidence:

- the current highest-surprise bottlenecks are correctly visible
- the benchmark no longer appears stuck optimizing only its strongest area
- the real bottlenecks are obvious: scale, calibration, evaluator realism, and governance

## The Hard Truth Right Now

TheStartupBench is now good enough that the main danger is not conceptual drift. The main danger is false completion.

In plain terms:

- it already looks like a benchmark
- parts of it behave like a benchmark
- but it does not yet have enough corpus, calibration evidence, or operational authority to *be* a SOTA benchmark

That means the repo should now bias toward:

- more hard scenarios
- more hidden scenarios
- more expert review evidence
- stricter promotion and retirement rules

and away from:

- more documentation layers
- more meta-workflow layers
- more packaging polish without new empirical pressure

## Top Bottleneck

Top bottleneck: `benchmark evidence density`

This combines:

- scenario count
- scenario difficulty
- human/operator calibration evidence
- baseline separation
- evaluator-vs-operator agreement evidence

That is now the limiting factor more than architecture.

## Required Fixes Before SOTA Claims

1. Run real operator calibration waves on canary, strategy, and real-world hidden packs.
2. Expand hidden scenario families substantially across all major startup tracks.
3. Publish stronger baseline families, including intentionally weak, medium, and specialist baselines.
4. Harden evaluator logic for delayed damage, collateral damage, and trust/compliance constraints.
5. Formalize benchmark operations: adjudication, known issues, exploit retirement, and promotion gates.
6. Add more realistic long-horizon mechanics in finance, people, GTM, and product.

## Next Experiments

1. Run a synthetic panel wave across Gemini, Opus, and GPT on one hidden target family and compare agreement rates.
2. Run a real operator wave with at least two reviewers per target family on the same family.
3. Measure benchmark-vs-operator gap by track and use that to prioritize evaluator fixes.
4. Add one new hidden family focused on enterprise sales, one on fundraising/cap-table decisions, and one on management/org debt.
5. Add specialist baselines that are strong on one track and weak on others to measure scenario separability.

## Risk If Ignored

If the repo keeps optimizing structure without increasing benchmark evidence density, TheStartupBench will drift into the worst middle state:

- too polished to be treated as a prototype
- too small and weakly calibrated to be treated as a benchmark authority

That is the main failure mode to avoid now.
