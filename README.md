# TheStartupBench

TheStartupBench is a benchmark design project for evaluating AI agents on startup and business decision-making under uncertainty.

Current status:

- benchmark RFC drafted
- implementation-oriented spec package drafted
- machine-readable schemas added
- example scenario added
- reference CLI and validation runtime implemented
- stateful business transition runtime implemented for core startup tools
- programmatic scoring and runtime tests implemented
- heuristic baseline runner implemented
- multiple heuristic baseline families implemented
- repeated-run campaign aggregation implemented
- generic primitive/event operation engine implemented
- multi-scenario suite packaging and reporting implemented
- private/public suite packaging and submission assembly implemented
- SOTA benchmark audit and task roadmap documented
- distinct hidden fresh pack variants and hidden-suite integrity enforcement implemented
- uncertainty-aware reporting implemented for batch, suite, and submission artifacts
- official evaluation profile and run-manifest support implemented
- expanded benchmark coverage across GTM, finance, and people tracks
- added a second hidden pack family for operator-style GTM, finance, and people evaluation
- added first-pass hiring funnel, customer segmentation, and market/competitor mechanics to the reference runtime
- added a product track plus a hidden strategy pack family for long-horizon board, product, and scale evaluation
- added a long-horizon baseline family for multi-quarter startup planning behavior

Key documents:

- `THE_STARTUP_BENCH_RFC.md`
- `docs/benchmark_status.md`
- `docs/sota_benchmark_audit.md`
- `docs/sota_task_roadmap.md`
- `docs/testing_coverage.md`
- `docs/pack_lifecycle_changelog.md`
- `spec/README.md`
- `spec/benchmark_contract.md`
- `spec/scenario_spec.md`
- `spec/state_model.md`
- `spec/scenario_primitives.md`
- `spec/tool_contract.md`
- `spec/tool_schema_catalog.md`
- `spec/scoring_contract.md`
- `spec/trace_spec.md`
- `spec/runner_contract.md`
- `spec/evaluator_contract.md`
- `spec/validation_contract.md`
- `spec/leaderboard_protocol.md`
- `spec/hidden_eval_policy.md`

Artifacts:

- `schemas/tsb_scenario.schema.json`
- `schemas/tsb_world_state.schema.json`
- `schemas/tsb_primitives.schema.json`
- `schemas/tsb_tool_manifest.schema.json`
- `schemas/tsb_tool_call.schema.json`
- `schemas/tsb_tool_response.schema.json`
- `schemas/tsb_evaluator_result.schema.json`
- `schemas/tsb_score_report.schema.json`
- `schemas/tsb_batch_report.schema.json`
- `schemas/tsb_scenario_suite.schema.json`
- `schemas/tsb_public_suite_manifest.schema.json`
- `schemas/tsb_official_eval_profile.schema.json`
- `schemas/tsb_run_manifest.schema.json`
- `schemas/tsb_suite_report.schema.json`
- `schemas/tsb_trace.schema.json`
- `schemas/tsb_submission.schema.json`
- `examples/minimal_b2b_saas_scenario.json`
- `examples/minimal_crisis_scenario.json`
- `examples/minimal_0to1_scenario.json`
- `examples/minimal_board_scenario.json`
- `examples/minimal_gtm_scenario.json`
- `examples/minimal_finance_scenario.json`
- `examples/minimal_people_scenario.json`
- `examples/minimal_product_scenario.json`
- `examples/minimal_scale_scenario.json`
- `examples/dev_scenario_suite.json`
- `examples/private_test_scenario_suite.json`
- `examples/private_operator_test_scenario_suite.json`
- `examples/private_operator_fresh_scenario_suite.json`
- `examples/private_strategy_test_scenario_suite.json`
- `examples/private_strategy_fresh_scenario_suite.json`
- `examples/official_eval_profile.json`
- `examples/minimal_run_manifest.json`
- `examples/minimal_public_suite_manifest.json`
- `examples/minimal_submission.json`
- `examples/minimal_world_state.json`
- `examples/minimal_primitives.json`
- `examples/minimal_tool_manifest.json`
- `examples/minimal_score_report.json`
- `examples/minimal_tool_script.json`

Implementation package:

- `pyproject.toml`
- `src/thestartupbench/`
- `tests/`

Current CLI examples:

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
python -m thestartupbench check-suite-family examples/private_real_world_test_scenario_suite.json examples/private_real_world_fresh_scenario_suite.json
python -m thestartupbench build-submission --suite-report-paths tmp_out/suite_report.json --model-id heuristic_resilient_operator --provider baseline --contamination-flag clean --output-dir tmp_out
python -m unittest discover -s tests -p "test_*.py"
```

Current reference runtime coverage:

- `metrics.query`
- `metrics.report`
- `product.roadmap.read`
- `product.roadmap.write`
- `sales.pipeline.read`
- `sales.pipeline.update`
- `sales.pricing.propose`
- `research.market.read`
- `finance.plan.read`
- `finance.plan.write`
- `finance.treasury.read`
- `finance.treasury.rebalance`
- `finance.raise.propose`
- `ops.incident.read`
- `ops.incident.respond`
- `ops.support.read`
- `ops.support.resolve`
- `people.hiring.read`
- `people.hiring.update`
- `people.org.read`
- `people.org.adjust`
- `legal.compliance.read`
- `legal.compliance.respond`
- `board.read`
- `board.update`
- `notes.read`
- `notes.write`
- `sim.advance`

Current state-transition coverage:

- tool handlers now route core mutations through a shared operation engine
- scheduled events may reference reusable `event_model.primitive_catalog` entries
- primitive operations currently support `set`, `increment`, `multiply`, `clamp`, and `append_unique`

Current built-in baselines:

- `heuristic_b2b_operator`
- `heuristic_long_horizon_operator`
- `heuristic_market_aware_operator`
- `heuristic_resilient_operator`

Current dev suite coverage:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `finance`
- `gtm`
- `people`
- `product`
- `scale`
