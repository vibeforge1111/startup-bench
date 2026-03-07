# TheStartupBench SOTA Benchmark Audit

Last updated: 2026-03-07

## Executive Verdict

TheStartupBench is methodologically closer to serious agent benchmarks than to toy simulations, but it is not yet a state-of-the-art benchmark.

Current label:

- strong benchmark prototype
- credible benchmark architecture
- not yet benchmark-standard
- not yet SOTA for startup/business evaluation

The main reason is not architectural failure. The main reason is missing benchmark depth:

- corpus scale is too small
- human/operator calibration is missing
- evaluator rigor is still early
- hidden-eval integrity is only partially operational
- governance is more specified than enforced

## What SOTA Benchmarks Consistently Do Well

Across benchmarks such as SWE-bench, SWE-bench Verified, SWE-rebench, Terminal-Bench, OSWorld, WebArena, WorkArena, AppWorld, tau-bench, tau2-bench, and MLE-bench, several recurring patterns appear.

### 1. They evaluate real execution, not essays

The strongest benchmarks do not mainly rely on free-form judging. They evaluate:

- code patches against tests
- browser interactions against state checks
- app/API changes against unit tests
- submission files against grading scripts

TheStartupBench is aligned here. Its runtime, tools, traces, and programmatic evaluators are the right structural choice.

### 2. They constrain the environment

Top benchmarks define a bounded operating environment with:

- fixed tools
- known APIs
- sandboxed state
- versioned scaffolds

This is why scores are comparable.

TheStartupBench is aligned here too. The benchmark is built around a business operating system rather than unconstrained prose roleplay.

### 3. They use hidden evaluation and contamination discipline

SOTA benchmarks increasingly assume that static public sets become compromised over time. The strongest current pattern is:

- public dev split
- hidden test split
- fresh or rolling evaluation tasks
- contamination notes or retirement rules

TheStartupBench is directionally aligned, but not fully mature in execution.

### 4. They standardize evaluation conditions

SWE-rebench is especially strong here:

- fixed scaffolding
- fixed prompts
- fixed hyperparameter defaults
- centralized evaluation
- repeated runs
- SEM or similar uncertainty reporting

TheStartupBench only partially matches this today.

### 5. They have enough task volume to resist leaderboard noise

AppWorld, WorkArena, OSWorld, and MLE-bench all push scale much harder than TheStartupBench currently does.

Small suites are useful for prototyping, but they do not establish benchmark authority.

### 6. They have either strong human validation or strong external grading

The strongest benchmarks reduce ambiguity by using one or both of:

- human validation of task quality and solvability
- externally checkable grading scripts

Startup evaluation is inherently more ambiguous than coding, so TheStartupBench needs this even more than many other benchmarks.

### 7. They publish governance, not just scores

SOTA benchmarks increasingly include:

- leaderboard rules
- contamination policy
- version boundaries
- dataset refresh policy
- changelogs
- known-issues handling

TheStartupBench has started this, but governance is not yet operationally complete.

## Where TheStartupBench Is Already Strong

### 1. Benchmark framing is correct

The project is not making the common mistake of building a startup roleplay benchmark. It is building:

- explicit state
- explicit tools
- explicit transitions
- explicit evaluation artifacts

That is the correct design family.

### 2. Domain focus is differentiated

There is no widely accepted startup/business operating benchmark with strong executable evaluation. That gives TheStartupBench a genuine opportunity to define the category.

### 3. Real-world crisis grounding is a strong differentiator

The real-world-derived startup crisis scenarios are a good methodological differentiator because they:

- anchor the benchmark in believable business failure modes
- force cross-functional reasoning
- reduce arbitrary game mechanics

### 4. Infrastructure quality is ahead of the corpus

The repo already has:

- schemas
- manifests
- traces
- submission artifacts
- redaction logic
- suite packaging
- validation
- CI

That is real benchmark infrastructure.

### 5. Hidden-eval thinking exists early

Many benchmarks only address contamination once it is already a problem. TheStartupBench is already thinking in terms of:

- `dev`
- `test`
- `fresh`
- pack lifecycle

That is the right instinct.

## Where TheStartupBench Is Weak Relative To SOTA Benchmarks

### 1. Corpus scale

This is the largest gap.

Current repository state is still small:

- 5-scenario dev suite
- 10-scenario real-world pack
- 5-scenario hidden real-world test pack

This is not enough to support robust leaderboard claims.

### 2. Human calibration

There are no:

- founder/operator baselines
- human solvability reviews
- rubric calibration sessions
- model-vs-human gap reports

For startup benchmarking, this is a major deficiency because many “correct” choices are tradeoff-sensitive rather than binary.

### 3. Evaluator maturity

TheStartupBench has programmatic scoring, which is good, but it still lacks:

- richer constraint semantics
- harder long-horizon tradeoff accounting
- track-specific evaluator bundles
- calibration against expert judgments
- limited semantic evaluation for communication artifacts

### 4. Standardization discipline

The benchmark has specs, but it does not yet have full centralized evaluation discipline in the SWE-rebench sense:

- locked official scaffold
- locked prompt bundle
- locked hyperparameter policy
- hosted official runs
- uniform reporting across models

### 5. World realism breadth

Current startup mechanics are promising but narrow. Missing areas include:

- detailed hiring funnels
- deeper cap-table and financing mechanics
- market competition
- product adoption/retention heterogeneity
- customer segmentation
- multi-quarter strategic drift
- legal and compliance progression

### 6. Governance maturity

There are policies and changelogs, but not yet:

- full submission review workflow
- exploit review process
- known-issues ledger
- adjudication process
- scenario promotion committee or review rubric

## Places Where TheStartupBench Has Drifted

### Drift 1. Fresh-pack semantics are not yet true fresh evaluation

The biggest concrete drift in the current repository is that the checked-in `fresh` pack is a split/version clone of the hidden `test` suite, not a genuinely distinct set of new hidden scenarios.

This weakens one of the benchmark’s most important integrity claims.

### Drift 2. Packaging maturity exceeds evaluation maturity

TheStartupBench currently has benchmark-grade packaging in several places:

- manifests
- CLI flows
- submission assembly
- changelog artifacts

But the empirical core is still small. This creates a risk that the project looks more benchmark-complete than it actually is.

### Drift 3. Baseline maturity is too narrow

Two heuristic baselines are enough to test plumbing, but not enough to establish difficulty, separability, or robustness.

### Drift 4. Scenario growth has favored crisis realism over breadth

The real-world crisis pack is valuable, but if the benchmark becomes overly crisis-weighted, it drifts away from “running a startup” and toward “handling emergencies at a startup.”

A SOTA startup benchmark needs strong coverage in:

- strategy
- GTM
- product
- finance
- people
- board communication
- crisis

## Comparison Against Major Benchmark Families

### SWE-bench / SWE-bench Verified

What they do well:

- executable evaluation
- real-world tasks
- human task validation
- containerized harness

What TheStartupBench should learn:

- human solvability review before official promotion
- better separation between prototype tasks and official benchmark tasks

### SWE-rebench

What it does especially well:

- fixed scaffold
- centralized evaluation
- repeated runs
- SEM and pass@k reporting
- explicit contamination framing

What TheStartupBench should learn:

- lock official evaluation settings much harder
- publish uncertainty metrics as first-class outputs
- standardize official run conditions across all model submissions

### Terminal-Bench

What it does well:

- task plus environment plus test harness plus oracle framing
- versioned benchmark structure
- canary-style contamination awareness

What TheStartupBench should learn:

- scenario should be treated more like `world + validator + oracle policy notes`
- add stronger canary and exploit-detection mechanics

### OSWorld

What it does well:

- realistic persistent environment
- difficult open-ended interaction
- broad task coverage

What TheStartupBench should learn:

- broader environment breadth matters
- scale and realism together create legitimacy

### WebArena / WorkArena

What they do well:

- state-based programmatic validation
- realistic enterprise workflows
- large task volume
- compositionality

What TheStartupBench should learn:

- startup workflows should be composed from reusable atomic business operations
- validation should focus on state correctness and collateral damage, not just final score

### AppWorld

What it does especially well:

- persistent world
- rich APIs
- many tasks
- collateral-damage-aware evaluation
- contamination-aware release posture

What TheStartupBench should learn:

- startup worlds should have richer stakeholder state
- “unexpected bad side effects” should be explicitly penalized
- scenario generation should scale from primitives, not just hand-authored cases

### tau-bench / tau2-bench

What they do well:

- multi-turn interaction
- policy-constrained domains
- simulation of counterparties or users

What TheStartupBench should learn:

- add stronger stakeholder simulation:
  - customers
  - board members
  - candidates
  - regulators
  - employees

### MLE-bench

What it does well:

- externally checkable scoring
- leaderboard hygiene
- grading artifacts

What TheStartupBench should learn:

- make score decomposition more auditable
- expose official grading reports for every scenario run

## What Would Make TheStartupBench Genuinely SOTA

To become the SOTA startup benchmark, TheStartupBench needs to become strong in all five dimensions below at the same time.

### 1. Integrity

Needs:

- truly distinct hidden `test` and `fresh` packs
- canary scenarios
- contamination adjudication
- retirement and replacement process

### 2. Coverage

Needs:

- far more scenarios
- balanced tracks
- difficulty tiers
- broader startup lifecycle coverage

### 3. Realism

Needs:

- more realistic causal dynamics
- richer stakeholders
- delayed and nonlinear consequences
- collateral-damage accounting

### 4. Evaluation quality

Needs:

- stronger constraints
- uncertainty metrics
- expert calibration
- human/operator baselines

### 5. Governance

Needs:

- formal promotion rules
- official run policy
- known-issues handling
- benchmark-version boundaries
- reproducible leaderboard operations

## Honest Bottom Line

TheStartupBench has not drifted away from the right benchmark philosophy. It is still fundamentally aligned with the most credible modern agent benchmarks.

However, it has not yet earned SOTA status.

The current state is best described as:

- architecturally promising
- methodologically aware
- stronger than a toy benchmark
- weaker than benchmark-standard leaders on corpus scale, calibration, and integrity operations

If the next phase focuses on:

- true hidden-eval integrity
- scenario scale
- operator calibration
- track-balanced realism
- centralized evaluation discipline

then TheStartupBench has a credible path to become the leading benchmark in its category.
