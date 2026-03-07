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
- repeated-run campaign aggregation implemented
- generic primitive/event operation engine implemented

Key documents:

- `THE_STARTUP_BENCH_RFC.md`
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
- `schemas/tsb_trace.schema.json`
- `schemas/tsb_submission.schema.json`
- `examples/minimal_b2b_saas_scenario.json`
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
python -m thestartupbench run-baseline examples/minimal_b2b_saas_scenario.json heuristic_b2b_operator --seed 1 --max-turns 6 --output-dir tmp_out
python -m thestartupbench run-campaign examples/minimal_b2b_saas_scenario.json baseline --baseline-id heuristic_b2b_operator --seeds 1,2,3 --max-turns 6 --output-dir tmp_out
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
- `finance.plan.read`
- `finance.plan.write`
- `board.read`
- `board.update`
- `notes.read`
- `notes.write`
- `sim.advance`

Current state-transition coverage:

- tool handlers now route core mutations through a shared operation engine
- scheduled events may reference reusable `event_model.primitive_catalog` entries
- primitive operations currently support `set`, `increment`, `multiply`, `clamp`, and `append_unique`
