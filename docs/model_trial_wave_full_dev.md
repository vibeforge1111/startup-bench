# Model Trial Wave Full Dev

This is the full public dev-suite version of the first model-comparison workflow.

Use it after `model_trial_wave_001` is already working. The goal is to compare `Codex`, `Claude`, and `Gemini` across the full visible dev benchmark without touching hidden packs.

## Scope

This wave uses all `9` public dev scenarios from [dev_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/dev_scenario_suite.json).

Tracks covered:

- `0to1`
- `b2b_saas`
- `board`
- `crisis`
- `scale`
- `gtm`
- `finance`
- `people`
- `product`

## Recommended Usage

Use this as a research comparison, not as an official leaderboard claim.

Recommended order:

1. confirm `model_trial_wave_001` works
2. generate `9` tool scripts for one model
3. run the full public dev wave for that model
4. repeat for the other models
5. compare score reports and traces

## Output Layout

Each model should produce one tool-script JSON per scenario under:

- `tmp_model_trial_full_dev_scripts/<model_id>/`

The runner will write artifacts under:

- `tmp_model_trial_full_dev_runs/<model_id>/`

## Shared Prompt Template

Use this for `Codex`, `Claude`, or `Gemini`.

If the model cannot read local files directly, paste the full scenario JSON where indicated.

```text
You are generating a static TheStartupBench tool script.

Your task is to produce a valid JSON array of tool calls for exactly 4 weekly turns for one scenario.

Important:
- Return JSON only.
- Do not use markdown fences.
- Do not add explanation before or after the JSON.
- Do not call tools live.
- Do not simulate outputs.
- You are only writing the tool-call script that will later be executed by the benchmark runner.

Goal:
Write a high-quality startup-operator policy for this scenario that is strategically coherent, adaptive, and benchmark-valid.

Hard constraints:
- Output must be a JSON array.
- Each element must be an object with:
  - "tool_name"
  - "request_id"
  - "arguments"
- Use only tools declared by the scenario.
- Use unique request_id values.
- Plan exactly 4 weekly turns.
- End each turn with exactly one:
  - "tool_name": "sim.advance"
  - "arguments": { "advance_by": 1, "unit": "week" }
- No comments.
- No placeholder values.
- No invented fields.
- No invented tools.
- Prefer a realistic operator sequence:
  - read state
  - make targeted decisions
  - communicate when appropriate
  - advance time
- Avoid rigid or repetitive no-op loops.
- Make decisions that fit the scenario's actual risks and tradeoffs.

Quality bar:
- React to the scenario's core risk, not generic startup behavior.
- Use the runtime's actual argument names instead of invented business-language wrappers.
- Use board updates only when they add real informational value.
- Use notes only if they capture genuine operating intent.
- Protect survival, trust, and strategic coherence, not just vanity metrics.
- Avoid obviously gameable behavior like mechanical pipeline padding during trust or liquidity crises.

Output path:
OUTPUT_PATH_HERE

Use this scenario:
SCENARIO_JSON_START
PASTE_SCENARIO_JSON_HERE
SCENARIO_JSON_END
```

## Scenario Matrix

For each model, use the same scenario file but change the output path folder.

| Key | Scenario file | Track | Output file |
| --- | --- | --- | --- |
| `0to1` | `examples/minimal_0to1_scenario.json` | `0to1` | `tmp_model_trial_full_dev_scripts/<model_id>/0to1_script.json` |
| `b2b_saas` | `examples/minimal_b2b_saas_scenario.json` | `b2b_saas` | `tmp_model_trial_full_dev_scripts/<model_id>/b2b_saas_script.json` |
| `board` | `examples/minimal_board_scenario.json` | `board` | `tmp_model_trial_full_dev_scripts/<model_id>/board_script.json` |
| `crisis` | `examples/minimal_crisis_scenario.json` | `crisis` | `tmp_model_trial_full_dev_scripts/<model_id>/crisis_script.json` |
| `scale` | `examples/minimal_scale_scenario.json` | `scale` | `tmp_model_trial_full_dev_scripts/<model_id>/scale_script.json` |
| `gtm` | `examples/minimal_gtm_scenario.json` | `gtm` | `tmp_model_trial_full_dev_scripts/<model_id>/gtm_script.json` |
| `finance` | `examples/minimal_finance_scenario.json` | `finance` | `tmp_model_trial_full_dev_scripts/<model_id>/finance_script.json` |
| `people` | `examples/minimal_people_scenario.json` | `people` | `tmp_model_trial_full_dev_scripts/<model_id>/people_script.json` |
| `product` | `examples/minimal_product_scenario.json` | `product` | `tmp_model_trial_full_dev_scripts/<model_id>/product_script.json` |

Replace `<model_id>` with:

- `codex`
- `claude`
- `gemini`

## Run The Full Dev Wave

After one model has all `9` script files, run:

```powershell
powershell -File scripts/run_model_trial_wave_full_dev.ps1 -ModelId codex
powershell -File scripts/run_model_trial_wave_full_dev.ps1 -ModelId claude
powershell -File scripts/run_model_trial_wave_full_dev.ps1 -ModelId gemini
```

Optional seed override:

```powershell
powershell -File scripts/run_model_trial_wave_full_dev.ps1 -ModelId claude -Seed 1
```

## What The Runner Emits

Per scenario it writes:

- `trace.json`
- `score_report.json`

under:

- `tmp_model_trial_full_dev_runs/<model_id>/<scenario_key>/`

## Compare Results

Start with:

- scenario-level `score_report.json`
- final `pass` / `fail`
- component subscores
- obvious runtime alignment problems

Pay special attention to:

- whether a model uses actual runtime argument names
- whether board/governance scenarios get real communication updates
- whether finance scenarios include treasury and financing follow-through
- whether product/people scenarios avoid passive quality-debt accumulation

## Interpretation

This is the right next step for public, visible comparison.

It is not the same as:

- hidden-pack benchmarking
- official evaluation
- leaderboard-quality model ranking

Use it to learn:

- which models are more benchmark-native
- which models adapt better across tracks
- whether some models need stricter prompting before any serious broader run
