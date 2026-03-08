# TheStartupBench Status Map

Last updated: 2026-03-08

## Current Snapshot

TheStartupBench is no longer just an RFC. It now has:

- a benchmark charter and methodology package
- machine-readable artifact schemas
- a reference Python package and CLI
- a stateful startup runtime with core operator tools
- built-in heuristic baselines
- a multi-scenario dev suite
- a real-world-derived crisis scenario pack
- private/test suite packaging and redacted public manifest generation
- operational `fresh` pack generation and public pack lifecycle tracking
- hidden suite family integrity enforcement and uncertainty-aware reporting
- official evaluation profile and run-manifest support
- official evaluation window and leaderboard governance pack support
- hidden pack rotation policy support
- a third hidden pack family for long-horizon startup judgment
- a fourth hidden pack family for canary exploit and overfit detection
- operator/founder calibration protocol and machine-readable review artifacts
- calibration reports and study manifests for hidden-pack operator alignment
- executable study runs, review packets, and study-level calibration compilation
- taskforce strategy and reviewer manual for organizing human calibration
- reviewer assignment, exportable review forms, and import back into benchmark artifacts
- synthetic reviewer panel guidance and fillable JSON template for LLM-based shadow review
- model-review prompt bundle export and raw model-review import for synthetic panels
- a tracked pre-human hardening plan in [pre_human_calibration_execution_plan.md](/C:/Users/USER/Desktop/startup-bench/docs/pre_human_calibration_execution_plan.md)
- a coverage expansion policy in [coverage_expansion_policy.md](/C:/Users/USER/Desktop/startup-bench/docs/coverage_expansion_policy.md) to keep future breadth growth aligned with benchmark standards
- a benchmark maturity plan in [benchmark_maturity_plan.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_maturity_plan.md) and active task system in [benchmark_task_board.md](/C:/Users/USER/Desktop/startup-bench/docs/benchmark_task_board.md)
- a known-issues ledger, evaluator adjudication log, and pre-freeze checklist for benchmark governance
- CI for tests, validation, and smoke suites
- unit tests and executable smoke paths

The project is in the `reference implementation + benchmark hardening` phase, not the `fully benchmark-complete` phase.

Freeze status:

- package/scaffold version: `0.9.0`
- benchmark freeze label: `v0.9-precalibration`
- official profile id: `official-hosted-v0.9.0`
- official window id: `official-window-v0.9.0-precalibration-2026-03-15-to-2026-04-12`
- frozen active packs are listed in [frozen_active_packs.md](/C:/Users/USER/Desktop/startup-bench/docs/frozen_active_packs.md)
- official reporting window rules are in [official_evaluation_window_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/official_evaluation_window_v0_9_0.md)
- leaderboard governance rules are in [leaderboard_governance_pack_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/leaderboard_governance_pack_v0_9_0.md)
- hidden pack rotation rules are in [hidden_pack_rotation_policy_v0_9_0.md](/C:/Users/USER/Desktop/startup-bench/docs/hidden_pack_rotation_policy_v0_9_0.md)

Synthetic calibration status:

- corrected and recommendation-aligned:
  - canary pricing trap
  - canary hiring trap
  - Zoom security backlash
  - Brex treasury shock
- healthy under synthetic calibration:
  - strategy product delayed consequence
  - strategy scale multi-quarter
- healthy but on governance watchlist:
  - strategy board stakeholder conflict
- added during pre-human hardening and not yet calibration-reviewed:
  - strategy board financing truth
  - strategy board incident truth
  - strategy board hiring truth
  - strategy product platform tax
  - strategy GTM efficiency sequencing
- queued for human review wave 002:
  - strategy platform sequencing
  - strategy product migration sequencing
  - strategy board product truth
  - strategy GTM multi-quarter sequencing
  - strategy scale-finance interaction

Human handoff artifacts now exist:

- [calibration_outcomes.md](/C:/Users/USER/Desktop/startup-bench/docs/calibration_outcomes.md)
- [human_review_wave_001.md](/C:/Users/USER/Desktop/startup-bench/docs/human_review_wave_001.md)
- [operator_human_review_wave_001_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_001_manifest.json)
- [human_review_wave_002.md](/C:/Users/USER/Desktop/startup-bench/docs/human_review_wave_002.md)
- [operator_human_review_wave_002_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_002_manifest.json)

Wave 002 is now launched locally with reviewer packets exported under `tmp_human_wave_002` for:

- `founder_001`
- `ops_001`
- `product_001`

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
- JSON schemas for operator reviews and review summaries under [schemas](/C:/Users/USER/Desktop/startup-bench/schemas)
- JSON schemas for calibration reports and calibration studies under [schemas](/C:/Users/USER/Desktop/startup-bench/schemas)
- example artifacts for individual scenarios, suites, manifests, score reports, submissions, operator reviews, and calibration studies under [examples](/C:/Users/USER/Desktop/startup-bench/examples)

### 3. Reference tooling and runtime

Completed:

- Python package in [src/thestartupbench](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench)
- schema validation and trace integrity checks
- scenario loading and authoring linting
- dry-run, scripted-run, baseline-run, campaign-run, and suite-run flows
- hidden-eval packaging helpers:
  - `redact-suite`
  - `build-submission`
- operator calibration helpers:
  - `aggregate-operator-reviews`
  - `build-calibration-report`
  - `run-calibration-study`
  - `compile-calibration-study`
  - `assign-reviewers`
  - `export-review-forms`
  - `import-review-forms`
  - `export-model-review-bundles`
  - `import-model-reviews`
- official evaluation helpers:
  - `show-official-profile`
  - `emit-run-manifest`
- GitHub Actions workflow in [.github/workflows/ci.yml](/C:/Users/USER/Desktop/startup-bench/.github/workflows/ci.yml#L1)
- stateful runtime support for:
  - finance planning
  - treasury concentration and liquidity rebalancing
  - sales pipeline updates
  - pricing changes
  - market and competitor research
  - product roadmap changes
  - product launch actions
  - growth experiment creation and review
  - board updates
  - note taking
  - incident reading/response
  - support backlog handling
  - legal/compliance response
  - hiring funnel and capacity updates
  - org proposal capture
  - people/org adjustment
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
  - `heuristic_governance_operator`
  - `heuristic_liquidity_operator`
  - `heuristic_long_horizon_operator`
  - `heuristic_market_aware_operator`
  - `heuristic_resilient_operator`
- repeated-run aggregation in [campaign_runner.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/campaign_runner.py)
- SEM and 95 percent confidence interval reporting in batch, suite, and submission artifacts
- official evaluation profile loader and run-manifest builder in [official_eval.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/official_eval.py)

### 6. Suite packaging

Completed:

- dev suite manifest in [dev_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/dev_scenario_suite.json)
- private test suite manifest in [private_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_test_scenario_suite.json)
- private real-world test suite manifest in [private_real_world_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_real_world_test_scenario_suite.json)
- private real-world fresh suite manifest in [private_real_world_fresh_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_real_world_fresh_scenario_suite.json)
- expanded hidden real-world coverage now includes runway-crunch finance, internal-compromise crisis, and integrity-first failover slices
- redacted public manifest generation in [suite_manifest.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/suite_manifest.py)
- suite promotion helper in [pack_ops.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/pack_ops.py)
- hidden suite family integrity checker in [pack_ops.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/pack_ops.py)
- submission assembly in [submission_builder.py](/C:/Users/USER/Desktop/startup-bench/src/thestartupbench/submission_builder.py)
- official hosted-eval profile example in [official_eval_profile.json](/C:/Users/USER/Desktop/startup-bench/examples/official_eval_profile.json)
- official run-manifest example in [minimal_run_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/minimal_run_manifest.json)
- hidden-eval policy in [hidden_eval_policy.md](/C:/Users/USER/Desktop/startup-bench/spec/hidden_eval_policy.md)
- operator calibration protocol in [operator_eval_protocol.md](/C:/Users/USER/Desktop/startup-bench/spec/operator_eval_protocol.md)
- operator study plan in [operator_study_plan.md](/C:/Users/USER/Desktop/startup-bench/docs/operator_study_plan.md)
- taskforce strategy in [calibration_taskforce_strategy.md](/C:/Users/USER/Desktop/startup-bench/docs/calibration_taskforce_strategy.md)
- reviewer manual in [reviewer_manual.md](/C:/Users/USER/Desktop/startup-bench/docs/reviewer_manual.md)
- model reviewer panel guide in [model_reviewer_panel.md](/C:/Users/USER/Desktop/startup-bench/docs/model_reviewer_panel.md)
- model review prompt guide in [model_review_prompt_guide.md](/C:/Users/USER/Desktop/startup-bench/docs/model_review_prompt_guide.md)
- public lifecycle changelog in [pack_lifecycle_changelog.md](/C:/Users/USER/Desktop/startup-bench/docs/pack_lifecycle_changelog.md)

### 7. Current scenario coverage

Completed example tracks:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `finance`
- `gtm`
- `people`
- `product`
- `scale`

These are example-scale scenarios, not yet a production benchmark corpus.

Completed real-world-derived scenario pack:

- `10` executable scenarios grounded in documented startup crises
- suite manifest in [real_world_crisis_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_crisis_scenario_suite.json)
- current pack coverage:
  - demand collapse
  - emergency financing under market shock
  - runway crunch
  - security trust crisis
  - peak-demand outage
  - phishing-led compromise
  - data-integrity recovery
  - operator-caused deletion/restoration
  - treasury concentration shock
  - peak-event readiness

Completed hidden real-world test pack:

- `8` hidden test scenarios with non-dev ids and altered operating conditions
- public redacted manifest in [real_world_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_test_manifest.json)
- current hidden pack coverage:
  - emergency financing
  - treasury concentration shock
  - runway crunch
  - phishing-led compromise
  - integrity-first failover recovery
  - security backlash
  - restoration backlog
  - peak readiness under lower headroom

Completed hidden real-world fresh pack:

- `8` fresh hidden scenarios with distinct scenario ids and distinct scenario files from the hidden `test` pack
- public redacted manifest in [real_world_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_fresh_manifest.json)
- current hidden fresh pack coverage:
  - bridge financing with harsher board terms
  - treasury freeze with payroll cascade risk
  - runway reset with harsher burn and morale drag
  - phishing compromise with deeper disclosure aftershock
  - integrity-first failover with stronger trust aftershock
  - security backlash with enterprise procurement freeze
  - restoration collapse with repeated tooling slippage
  - peak readiness with support spike and fatigue

Completed hidden operator breadth packs:

- `16` hidden `test` scenarios in [private_operator_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_operator_test_scenario_suite.json)
- `16` hidden `fresh` scenarios in [private_operator_fresh_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_operator_fresh_scenario_suite.json)
- current operator hidden coverage:
  - GTM pipeline reset
  - GTM enterprise freeze under trust fragility
  - GTM reference decay under pipeline erosion
  - GTM discount spiral under proof gaps
  - GTM partner backfire under thin onboarding
  - finance liquidity and treasury tradeoffs
  - finance margin shock under payment delay
  - finance covenant squeeze under collections drag
  - finance receivables freeze under cash-conversion drag
  - finance step-down raise under burn-credibility pressure
  - people attrition and support-load stabilization
  - people reorg drag under morale pressure
  - people manager-span overload under burnout risk
  - people exec backfill drag under ownership gaps
  - people support burnout under renewal pressure
  - people decision latency under coordination drag

Completed hidden strategy packs:

- `13` hidden `test` scenarios in [private_strategy_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_strategy_test_scenario_suite.json)
- `13` hidden `fresh` scenarios in [private_strategy_fresh_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_strategy_fresh_scenario_suite.json)
- current strategy hidden coverage:
  - board stakeholder conflict
  - board financing truth under narrative pressure
  - board incident truth under customer escalation
  - board hiring truth under leadership gap pressure
  - delayed-consequence product quality debt
  - delayed-consequence product platform tax
  - multi-quarter scale planning under capacity lag
  - platform-sequencing under expansion pull-forward
  - delayed-consequence product migration quality
  - board product truth under readiness pressure
  - GTM multi-quarter proof sequencing
  - GTM efficiency sequencing under channel expansion
  - scale-finance interaction under tightening capital quality

Completed hidden canary packs:

- `2` hidden `test` scenarios in [private_canary_test_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_canary_test_scenario_suite.json)
- `2` hidden `fresh` scenarios in [private_canary_fresh_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/private_canary_fresh_scenario_suite.json)
- current canary hidden coverage:
  - pricing hikes under trust fragility
  - hiring expansion under soft demand and thin liquidity

## What Is Partially Done

### 1. World realism

Partially done:

- there is a usable world-state model and executable runtime
- there are early business mechanics for finance, sales, product, governance, and incident handling
- there are now explicit mechanics for treasury concentration, support backlog, legal pressure, org stress, hiring funnel state, segment-aware customer health, and market/competitor drift
- the current mechanics are materially broader, but still narrow relative to real startup operation

What remains inside this category:

- deeper hiring funnel stage logic and backfill delays
- broader morale and attrition propagation
- richer customer segmentation and churn/expansion mechanisms
- fundraising, debt, and cap-table mechanics
- broader competitor and market-shift systems
- regulatory and legal state transitions

### 2. Evaluator sophistication

Partially done:

- there is a real programmatic scoring path
- crisis-aware behavior is now distinguishable from generic heuristics
- board/governance scenarios now have a dedicated trace-aware penalty path instead of fully inheriting generic non-crisis scoring

What remains inside this category:

- stronger multi-objective scoring weights
- explicit constraint scoring for compliance/trust/survival
- better calibration around delayed effects
- fuller track-specific evaluator bundles
- limited semantic-judge use for memos, board updates, and stakeholder communication

### 3. Benchmark integrity

Partially done:

- private/test suite format exists
- fresh hidden suite format exists
- hidden `test` and `fresh` suites are now distinct in ids and files
- a second hidden pack family now exists outside the crisis-heavy real-world family
- a third hidden pack family now exists for long-horizon startup judgment
- a fourth hidden pack family now exists for exploit and overfit detection
- public redacted suite manifest exists
- public lifecycle changelog exists
- known-issues, adjudication, and pre-freeze governance docs now exist
- suite and submission artifacts exist
- uncertainty-aware score reporting exists
- official evaluation profile and run-manifest artifacts exist

What remains inside this category:

- true held-out scenario inventory at meaningful scale
- benchmark refresh cadence
- contamination adjudication workflow
- exploit review pipeline tied to canary outcomes
- leaderboard operations and review procedures
- automated pack rotation pipeline

### 4. Baseline depth

Partially done:

- two heuristic baselines exist and are measurably different
- four heuristic baselines exist and are measurably different
- a long-horizon baseline now passes the expanded dev suite and the new strategy hidden packs

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
- a larger distinct hidden fresh set
- broader hidden coverage outside crisis-heavy scenarios
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

Partially done:

- automated CI for validation, smoke runs, and tests
- release packaging
- clean-shell CLI installation path from a fresh checkout
- benchmark data freeze process
- signed release artifacts
- reproducible runner environments

### 4. Human calibration

Partially done:

- operator calibration protocol now exists
- machine-readable operator review and review-summary artifacts now exist
- the reference CLI can aggregate operator reviews into a calibration summary
- calibration reports can now compare operator judgments against suite scores
- a concrete study manifest now exists for canary, strategy, and real-world hidden packs
- the reference tooling can now run a full study wave and compile partial study reports
- the repo now includes practical docs for recruiting and guiding a human calibration taskforce
- the repo now includes reviewer-facing CSV and Markdown form workflows for external operators
- the repo now includes a clear synthetic-reviewer lane for Gemini, Opus, GPT, and other model panels

What remains inside this category:

- operator baselines from founders or startup functional leads
- rubric calibration sessions
- human solvability review for promoted scenarios
- model-vs-human gap reporting

## Highest-Priority Remaining Work

If the goal is to make TheStartupBench materially stronger, the next steps should be:

1. Build a larger scenario corpus with track-balanced dev and hidden test suites.
2. Add richer state transitions for people, fundraising, legal/compliance, and market dynamics.
   Current status: first-pass hiring, segmentation, and market pressure mechanics are now live; the next gap is depth, not existence.
3. Strengthen evaluator design so survival, trust, compliance, and capital efficiency are explicit constraints rather than soft side effects.
4. Add more baseline families, especially human-inspired scripted policies and crisis-specialist heuristics.
5. Add official hosted-eval manifests and settings to model adapters beyond baselines.
6. Add benchmark governance artifacts: contamination policy, version policy, exploit review, and refresh cadence.
7. Add artifact publishing and required-branch protections on top of the new CI workflow.

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
