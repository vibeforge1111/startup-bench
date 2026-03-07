```
  _____ _          ____  _             _               ____                  _
 |_   _| |__   ___/ ___|| |_ __ _ _ __| |_ _   _ _ __ | __ )  ___ _ __   ___| |__
   | | | '_ \ / _ \___ \| __/ _` | '__| __| | | | '_ \|  _ \ / _ \ '_ \ / __| '_ \
   | | | | | |  __/___) | || (_| | |  | |_| |_| | |_) | |_) |  __/ | | | (__| | | |
   |_| |_| |_|\___|____/ \__\__,_|_|   \__|\__,_| .__/|____/ \___|_| |_|\___|_| |_|
                                                 |_|

       Can your AI run a startup?

       +-----------+     +-----------+     +-----------+
       |  SCENARIO |---->|   AGENT   |---->|   SCORE   |
       |           |     |           |     |           |
       | cash: $2M |     | decisions |     | 0.72 pass |
       | burn:$350K|     | tradeoffs |     | subscores |
       | trust: 0.7|     | actions   |     | violations|
       +-----------+     +-----------+     +-----------+
            |                  |                 |
            v                  v                 v
       9 scenarios        27 tools         4 dimensions
       4 difficulty      board comms      cash efficiency
       hidden packs      hiring/firing    revenue quality
       real-world        fundraising      customer health
       events            incident mgmt    strategic fit
```

# TheStartupBench

**A benchmark for evaluating how well AI agents operate a startup under uncertainty.**

Most AI benchmarks test coding, math, or knowledge retrieval. TheStartupBench tests something different: can an AI make the messy, multi-dimensional tradeoffs that real startup operators face every week? Budget cuts vs. quality investment. Incident response vs. roadmap velocity. Honest board communication vs. optimistic forecasting. Hiring under pressure vs. burn discipline.

The agent is dropped into a simulated startup with real financial state, customer metrics, team dynamics, and a board to report to. Events happen -- customers churn, infrastructure costs spike, key people leave, deals slip. The agent must respond using the same levers a real operator would: adjusting burn, resolving incidents, hiring, updating the board, managing pipeline, and deciding what to build next.

Scoring is programmatic across four dimensions (cash efficiency, revenue quality, customer health, strategic coherence) with hard constraint checks (bankruptcy, trust collapse, compliance breach). No vibes. No LLM-as-judge on the outcome score.

## Early Results

### Full Public Dev Benchmark (9 scenarios)

| Model | Overall | Passes | 0to1 | b2b | Board | Crisis | Scale | GTM | Finance | People | Product |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Codex 5.4 High | **0.7203** | 9/9 | 0.578 | 0.685 | 0.700 | 0.687 | 0.811 | 0.720 | 0.835 | 0.712 | 0.754 |
| Gemini 3.0 | 0.6614 | 8/9 | 0.547 | 0.634 | 0.632 | 0.676 | 0.790 | 0.603 | 0.772 | 0.665 | 0.634 |
| Claude Opus 4.6 | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |

### Initial 3-Scenario Trial Wave

| Model | Mean | Crisis | Product | Finance |
|---|---:|---:|---:|---:|
| Claude Opus 4.6 | **0.7637** | 0.684 | 0.775 | 0.832 |
| Codex 5.4 High | 0.7587 | 0.687 | 0.754 | 0.835 |
| Gemini 3.0 | 0.7161 | 0.670 | 0.705 | 0.774 |

Claude full-dev scripts are prepared but not yet scored. Codex leads on completed full-suite runs. Gemini failed the 0to1 scenario (bankruptcy constraint).

## How It Works

1. **Pick a scenario.** Each scenario defines a startup at a specific stage with realistic financials, product state, customer metrics, team health, and a set of events that will fire at specific turns.

2. **Run an agent.** The agent gets the initial state and a set of tools. Each turn, it reads metrics, makes decisions (hire, cut burn, resolve incidents, update the board, invest in quality...), then advances the simulation by one week. Events fire during advances -- cost shocks, customer escalations, deal closures, team departures.

3. **Score the outcome.** After all turns complete, programmatic evaluators score the final world state across four weighted dimensions. Hard constraints (did the company go bankrupt? did trust collapse?) gate pass/fail. Each scenario weights the dimensions differently -- a board governance scenario weights strategic coherence at 0.45, while a crisis scenario weights customer health at 0.35.

## Scenarios

| Track | Scenario | Stage | Core Challenge |
|---|---|---|---|
| 0to1 | Design Partner Conversion | Pre-seed | Activation gap at 0.42 onboarding quality blocks pipeline conversion |
| b2b_saas | Runway and Pricing Reset | Seed | Infrastructure cost shock hits mid-recovery from a major incident |
| board | Board Reforecast Pressure | Series A | Credible reforecast after missing plan, with procurement delays |
| crisis | Trust Recovery | Seed | Two open incidents, 4.1% churn, and a renewal escalation incoming |
| scale | Capacity Balance | Growth | Revenue growth strains reliability -- each surge creates new incidents |
| gtm | Channel Mix Reset | Series A | Outbound is dying, a competitor is bundling, pipeline is softening |
| finance | Treasury Tradeoff | Series A | 83% treasury concentration, rising financing pressure, payment delays |
| people | Org Stability | Series B | Morale at 0.48, attrition risk at 0.64, a key manager about to leave |
| product | Quality Debt | Series A | Launch bump drives demand but deferred quality bill hits support/trust |

Additional hidden packs (test, fresh, canary, real-world, strategy) exist for anti-gaming and leaderboard integrity.

## Quick Start

```bash
# Install
python -m pip install -e .
python -m thestartupbench version

# Run a single baseline
python -m thestartupbench run-baseline \
  examples/minimal_crisis_scenario.json \
  heuristic_resilient_operator \
  --seed 1 --max-turns 6 --output-dir tmp_out

# Run the full public dev suite
python -m thestartupbench run-suite \
  examples/dev_scenario_suite.json baseline \
  --baseline-id heuristic_resilient_operator \
  --seeds 1,2 --max-turns 4 \
  --profile-path examples/official_eval_profile.json \
  --output-dir tmp_out

# Run a pre-generated tool script (e.g. from an LLM)
python -m thestartupbench run-script \
  examples/minimal_crisis_scenario.json \
  examples/minimal_tool_script.json \
  --seed 1 --output-dir tmp_out
```

## Tools

The agent interacts with the simulated startup through 27 tools across 8 domains:

| Domain | Tools | What They Do |
|---|---|---|
| **Metrics** | `metrics.query`, `metrics.report` | Read current state and KPIs |
| **Product** | `product.roadmap.read`, `product.roadmap.write` | Ship features, improve quality, resolve incidents |
| **Sales** | `sales.pipeline.read`, `sales.pipeline.update`, `sales.pricing.propose` | Manage deals and pricing |
| **Finance** | `finance.plan.read/write`, `finance.treasury.read/rebalance`, `finance.raise.propose` | Burn control, treasury, fundraising |
| **Ops** | `ops.incident.read/respond`, `ops.support.read/resolve` | Incident response and support backlog |
| **People** | `people.hiring.read/update`, `people.org.read/adjust` | Hiring and org changes |
| **Governance** | `board.read`, `board.update`, `legal.compliance.read/respond` | Board comms and compliance |
| **General** | `research.market.read`, `notes.read/write`, `sim.advance` | Market intel, notes, advance time |

## Scoring

Each scenario defines weights across four outcome dimensions:

- **Cash efficiency** -- runway, burn quality, treasury concentration, dilution
- **Revenue quality** -- revenue coverage, pipeline strength, pricing signals, demand
- **Customer health** -- trust, churn, support backlog, morale, delivery capacity
- **Strategic coherence** -- board communication, crisis response, hiring decisions, behavioral consistency

Hard constraints gate pass/fail: bankruptcy, severe trust breach, compliance failure, financing collapse.

## Baselines

Six built-in heuristic operators for comparison:

| Baseline | Strategy |
|---|---|
| `heuristic_resilient_operator` | Incident-first, trust recovery, defensive |
| `heuristic_market_aware_operator` | Market-reading, demand-responsive |
| `heuristic_long_horizon_operator` | Runway-preserving, conservative |
| `heuristic_b2b_operator` | Pipeline and pricing focused |
| `heuristic_governance_operator` | Board-communication heavy |
| `heuristic_liquidity_operator` | Treasury and cash management |

## Release State

- **Freeze label:** `v0.9-precalibration`
- **Package version:** `0.9.0`
- **Maturity:** pre-human-calibration benchmark prototype

What this means:
- Ready for technical contributors and early volunteers
- Ready for research benchmarking
- Not yet a finished public leaderboard benchmark

## Project Structure

```
thestartupbench/
  src/thestartupbench/     # Runtime, evaluators, baselines, CLI
  tests/                   # Unit and integration tests
  examples/                # Scenarios, suites, profiles, manifests
  schemas/                 # JSON schemas for all data contracts
  spec/                    # Formal specifications
  scripts/                 # Trial and calibration automation
  docs/                    # Guides, audits, calibration logs
```

## Documentation

**Getting started:**
- [Getting started guide](docs/getting_started.md)
- [Evaluation modes](docs/evaluation_modes.md)
- [Contribution guide](CONTRIBUTING.md)

**Model trials:**
- [Initial 3-scenario trial](docs/model_trial_wave_001.md)
- [Full public dev trial](docs/model_trial_wave_full_dev.md)

**Benchmark design:**
- [RFC](THE_STARTUP_BENCH_RFC.md)
- [Benchmark status](docs/benchmark_status.md)
- [Known issues](docs/benchmark_known_issues.md)
- [SOTA audit](docs/sota_benchmark_audit.md) | [Re-audit](docs/sota_reaudit.md)

**Calibration:**
- [Calibration outcomes](docs/calibration_outcomes.md)
- [Calibration strategy](docs/calibration_taskforce_strategy.md)
- [Evaluator adjudication log](docs/evaluator_adjudication_log.md)
- [Human review wave 001](docs/human_review_wave_001.md)
- [Reviewer manual](docs/reviewer_manual.md)

**Community:**
- [Volunteer call](docs/volunteer_call.md)
- [Founder/operator outreach](docs/founder_operator_outreach.md)
- [X post kit](docs/x_post_kit.md)

<details>
<summary><strong>Specifications</strong></summary>

- [Benchmark contract](spec/benchmark_contract.md)
- [Scenario spec](spec/scenario_spec.md)
- [State model](spec/state_model.md)
- [Scenario primitives](spec/scenario_primitives.md)
- [Tool contract](spec/tool_contract.md)
- [Tool schema catalog](spec/tool_schema_catalog.md)
- [Scoring contract](spec/scoring_contract.md)
- [Trace spec](spec/trace_spec.md)
- [Runner contract](spec/runner_contract.md)
- [Evaluator contract](spec/evaluator_contract.md)
- [Validation contract](spec/validation_contract.md)
- [Leaderboard protocol](spec/leaderboard_protocol.md)
- [Hidden eval policy](spec/hidden_eval_policy.md)
- [Operator eval protocol](spec/operator_eval_protocol.md)

</details>

<details>
<summary><strong>All CLI commands</strong></summary>

```bash
python -m thestartupbench version
python -m thestartupbench validate scenario examples/minimal_b2b_saas_scenario.json
python -m thestartupbench manifest examples/minimal_b2b_saas_scenario.json
python -m thestartupbench list-baselines
python -m thestartupbench lint-scenario examples/minimal_b2b_saas_scenario.json
python -m thestartupbench run-dry examples/minimal_b2b_saas_scenario.json --seed 1 --output-dir tmp_out
python -m thestartupbench run-script examples/minimal_b2b_saas_scenario.json examples/minimal_tool_script.json --seed 1 --output-dir tmp_out
python -m thestartupbench run-baseline examples/minimal_crisis_scenario.json heuristic_resilient_operator --seed 1 --max-turns 6 --output-dir tmp_out
python -m thestartupbench run-campaign examples/minimal_crisis_scenario.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2,3 --max-turns 6 --output-dir tmp_out
python -m thestartupbench show-official-profile examples/official_eval_profile.json
python -m thestartupbench emit-run-manifest examples/dev_scenario_suite.json baseline --seeds 1,2,3,4,5 --baseline-id heuristic_resilient_operator --max-turns 8 --profile-path examples/official_eval_profile.json --output-dir tmp_out
python -m thestartupbench run-suite examples/dev_scenario_suite.json baseline --baseline-id heuristic_resilient_operator --seeds 1,2 --max-turns 4 --profile-path examples/official_eval_profile.json --output-dir tmp_out
python -m thestartupbench redact-suite examples/private_test_scenario_suite.json --output-dir tmp_out
python -m thestartupbench check-suite-family examples/private_canary_test_scenario_suite.json examples/private_canary_fresh_scenario_suite.json
python -m thestartupbench aggregate-operator-reviews examples/minimal_operator_review.json --output-dir tmp_out
python -m thestartupbench build-calibration-report --suite-report-path tmp_out/suite_report.json --review-paths examples/minimal_operator_review.json --output-dir tmp_out
python -m thestartupbench run-calibration-study examples/operator_calibration_study_manifest.json --output-dir tmp_out
python -m thestartupbench assign-reviewers examples/operator_calibration_study_manifest.json --study-run-dir tmp_out --roster-path examples/reviewer_roster_template.csv --output-dir tmp_out
python -m thestartupbench export-review-forms tmp_out/review_assignments.json --output-dir tmp_out
python -m thestartupbench import-review-forms tmp_out --output-dir tmp_out
python -m thestartupbench export-model-review-bundles tmp_out --output-dir tmp_model_bundles
python -m thestartupbench import-model-reviews tmp_model_outputs --output-dir tmp_model_import
python -m thestartupbench compile-calibration-study examples/operator_calibration_study_manifest.json --study-run-dir tmp_out --review-paths examples/minimal_operator_review.json --output-dir tmp_out
python -m thestartupbench build-submission --suite-report-paths tmp_out/suite_report.json --model-id heuristic_resilient_operator --provider baseline --contamination-flag clean --output-dir tmp_out
python -m unittest discover -s tests -p "test_*.py"
```

</details>

<details>
<summary><strong>Schemas and artifacts</strong></summary>

**JSON Schemas:**
`tsb_scenario`, `tsb_world_state`, `tsb_primitives`, `tsb_tool_manifest`, `tsb_tool_call`, `tsb_tool_response`, `tsb_evaluator_result`, `tsb_score_report`, `tsb_batch_report`, `tsb_scenario_suite`, `tsb_public_suite_manifest`, `tsb_official_eval_profile`, `tsb_run_manifest`, `tsb_suite_report`, `tsb_trace`, `tsb_submission`, `tsb_operator_review`, `tsb_operator_review_summary`, `tsb_calibration_report`, `tsb_calibration_study`, `tsb_review_packet`, `tsb_calibration_study_run`, `tsb_calibration_study_report`, `tsb_review_assignments`, `tsb_review_form_export`, `tsb_review_form_import`

All schemas live in `schemas/` as `tsb_*.schema.json`.

**Example files:** All in `examples/` -- scenarios, suites, profiles, manifests, review templates, calibration configs.

</details>

## State Engine

- Tool handlers route mutations through a shared operation engine
- Scheduled events reference reusable primitives from `event_model.primitive_catalog`
- Supported operations: `set`, `increment`, `multiply`, `clamp`, `append_unique`
