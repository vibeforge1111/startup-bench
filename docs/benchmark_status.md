# TheStartupBench Status Map

Last updated: 2026-03-07

## Current Snapshot

TheStartupBench is no longer just an RFC. It now has:

- a benchmark charter and methodology package
- machine-readable artifact schemas
- a reference Python package and CLI
- a stateful startup runtime with core operator tools
- built-in heuristic baselines
- a multi-scenario dev suite
- private/test suite packaging and redacted public manifest generation
- unit tests and executable smoke paths

The project is in the `reference implementation + benchmark hardening` phase, not the `fully benchmark-complete` phase.

## What Is Done

### 1. Benchmark framing and methodology

Completed:

- benchmark charter and high-level RFC in [THE_STARTUP_BENCH_RFC.md](/C:/Users/USER/Desktop/startup-bench/THE_STARTUP_BENCH_RFC.md)
- implementation-oriented spec package in [spec/README.md](/C:/Users/USER/Desktop/startup-bench/spec/README.md)
- explicit benchmark, scenario, tool, scoring, trace, runner, evaluator, validation, and leaderboard contracts under [spec](/C:/Users/USER/Desktop/startup-bench/spec)
- methodology direction aligned with stateful, executable, anti-gaming benchmark practices rather than static toy-sim evaluation

### 2. Artifact schemas and examples

Completed:

- JSON schemas for scenarios, world state, primitives, tool calls/responses, traces, score reports, batch reports, suite reports, manifests, and submissions under [schemas](/C:/Users/USER/Desktop/startup-bench/schemas)
- example artifacts for individual scenarios, suites, manifests, score reports, and submissions under [examples](/C:/Users/USER/Desktop/startup-bench/examples)

### 3. Reference tooling and runtime

Completed:

- Python package in [src/thestartupbench](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench)
- schema validation and trace integrity checks
- scenario loading and authoring linting
- dry-run, scripted-run, baseline-run, campaign-run, and suite-run flows
- hidden-eval packaging helpers:
  - `redact-suite`
  - `build-submission`
- stateful runtime support for:
  - finance planning
  - sales pipeline updates
  - pricing changes
  - product roadmap changes
  - board updates
  - note taking
  - incident reading/response
  - time advancement

### 4. Primitive/event execution

Completed:

- shared primitive operation engine in [primitive_engine.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/primitive_engine.py)
- support for:
  - `set`
  - `increment`
  - `multiply`
  - `clamp`
  - `append_unique`
- scheduled events can reference reusable primitive templates from scenario `event_model.primitive_catalog`

### 5. Scoring and baselines

Completed:

- programmatic evaluator layer in [evaluators.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/evaluators.py)
- built-in baselines in [baseline_runner.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/baseline_runner.py):
  - `heuristic_b2b_operator`
  - `heuristic_resilient_operator`
- repeated-run aggregation in [campaign_runner.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/campaign_runner.py)

### 6. Suite packaging

Completed:

- dev suite manifest in [dev_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/dev_scenario_suite.json)
- private test suite manifest in [private_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_test_scenario_suite.json)
- redacted public manifest generation in [suite_manifest.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/suite_manifest.py)
- submission assembly in [submission_builder.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/submission_builder.py)

### 7. Current scenario coverage

Completed example tracks:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `scale`

These are example-scale scenarios, not yet a production benchmark corpus.

## What Is Partially Done

### 1. World realism

Partially done:

- there is a usable world-state model and executable runtime
- there are early business mechanics for finance, sales, product, governance, and incident handling
- the current mechanics are still narrow relative to real startup operation

What remains inside this category:

- richer hiring funnel dynamics
- morale and attrition propagation
- deeper customer segmentation and churn mechanisms
- fundraising, debt, and cap-table mechanics
- competitor and market-shift systems
- regulatory and legal state transitions

### 2. Evaluator sophistication

Partially done:

- there is a real programmatic scoring path
- crisis-aware behavior is now distinguishable from generic heuristics

What remains inside this category:

- stronger multi-objective scoring weights
- explicit constraint scoring for compliance/trust/survival
- better calibration around delayed effects
- track-specific evaluator bundles
- limited semantic-judge use for memos, board updates, and stakeholder communication

### 3. Benchmark integrity

Partially done:

- private/test suite format exists
- public redacted suite manifest exists
- suite and submission artifacts exist

What remains inside this category:

- true held-out scenario inventory at meaningful scale
- benchmark refresh cadence
- contamination policy and disclosure workflow
- canary scenarios and exploit review pipeline
- leaderboard operations and review procedures

### 4. Baseline depth

Partially done:

- two heuristic baselines exist and are measurably different
- one baseline now passes the current 5-scenario dev suite

What remains inside this category:

- stronger scripted baselines
- domain-specific baseline families by track
- human/operator baselines
- frontier-model adapters and locked eval harnesses

## What Is Not Done Yet

### 1. Benchmark-scale scenario library

Not done:

- a large public dev set
- a large hidden official test set
- broad scenario coverage across product, GTM, finance, people, legal, and crisis operations
- difficulty tiering and refresh lineages

This is the biggest gap between the current repo and an industry-standard benchmark.

### 2. Full benchmark governance

Not done:

- official submission review workflow
- contamination adjudication process
- benchmark version retirement policy
- known-issues ledger
- evaluator drift review
- third-party scenario contribution process

### 3. CI and release hardening

Not done:

- automated CI for validation, smoke runs, and tests
- release packaging
- clean-shell CLI installation path from a fresh checkout
- benchmark data freeze process
- signed release artifacts
- reproducible runner environments

### 4. Human calibration

Not done:

- operator baselines from founders or startup functional leads
- rubric calibration sessions
- human solvability review for promoted scenarios
- model-vs-human gap reporting

## Highest-Priority Remaining Work

If the goal is to make TheStartupBench materially stronger, the next steps should be:

1. Build a larger scenario corpus with track-balanced dev and hidden test suites.
2. Add richer state transitions for people, fundraising, legal/compliance, and market dynamics.
3. Strengthen evaluator design so survival, trust, compliance, and capital efficiency are explicit constraints rather than soft side effects.
4. Add more baseline families, especially human-inspired scripted policies and crisis-specialist heuristics.
5. Add benchmark governance artifacts: contamination policy, version policy, exploit review, and refresh cadence.
6. Add CI so schema validation, smoke runs, and unit tests are automatic on every change.

## Definition Of “Done Enough” For A Credible v1

TheStartupBench should not be presented as a benchmark-standard v1 until all of the following are true:

- at least one public dev suite and one hidden official test suite exist at meaningful scale
- scenario coverage spans multiple startup functions, not just runtime mechanics
- repeated-run reporting is standard
- at least one human/operator baseline exists
- submission and leaderboard rules are documented and enforced
- contamination and refresh policies are live
- smoke and unit checks run in CI

## Bottom Line

What is already built is substantial and real. What remains is mostly benchmark hardening, scenario scale, governance, and calibration. The main risk is not that the current project is empty; it is that it could be mistaken for benchmark-complete before the hidden-eval corpus, evaluator depth, and governance are mature enough.
