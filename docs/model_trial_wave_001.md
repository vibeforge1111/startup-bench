# Model Trial Wave 001

This is the recommended first cross-model benchmark trial for `TheStartupBench`.

It is intentionally smaller than a full suite run. The goal is to compare behavior cleanly across `Codex`, `Claude`, and `Gemini` before running broader packs.

## Trial Design

Use these three public scenarios:

- `examples/minimal_crisis_scenario.json`
- `examples/minimal_product_scenario.json`
- `examples/minimal_finance_scenario.json`

These cover:

- crisis response and trust recovery
- product quality and delayed consequences
- runway, treasury, and financing tradeoffs

## Output Layout

Ask each model to create exactly one tool-script JSON file per scenario:

- `tmp_model_trial_wave_001_scripts/codex/crisis_script.json`
- `tmp_model_trial_wave_001_scripts/codex/product_script.json`
- `tmp_model_trial_wave_001_scripts/codex/finance_script.json`
- `tmp_model_trial_wave_001_scripts/claude/crisis_script.json`
- `tmp_model_trial_wave_001_scripts/claude/product_script.json`
- `tmp_model_trial_wave_001_scripts/claude/finance_script.json`
- `tmp_model_trial_wave_001_scripts/gemini/crisis_script.json`
- `tmp_model_trial_wave_001_scripts/gemini/product_script.json`
- `tmp_model_trial_wave_001_scripts/gemini/finance_script.json`

Each script must be a JSON array of tool calls in the same format as `examples/minimal_tool_script.json`.

## Hard Rules For All Models

Each prompt below assumes these constraints:

- output valid JSON only
- do not wrap output in markdown fences
- write a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique `request_id` values
- plan exactly `4` weekly turns
- end each turn with one `sim.advance` call
- use `{"advance_by": 1, "unit": "week"}` for each `sim.advance`
- avoid placeholder text and comments
- do not invent tools or fields

## Codex Prompts

### Crisis

```text
Read the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_crisis_scenario.json

Create a valid TheStartupBench tool-script JSON array for exactly 4 weekly turns and write it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\codex\crisis_script.json

Requirements:
- output must be a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like codex_crisis_001
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, trust stabilization, and disciplined crisis handling
- no markdown fences
- no prose explanation
- overwrite the output file with the final JSON only
```

### Product

```text
Read the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_product_scenario.json

Create a valid TheStartupBench tool-script JSON array for exactly 4 weekly turns and write it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\codex\product_script.json

Requirements:
- output must be a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like codex_product_001
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, early quality stabilization, and support-capacity discipline
- no markdown fences
- no prose explanation
- overwrite the output file with the final JSON only
```

### Finance

```text
Read the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_finance_scenario.json

Create a valid TheStartupBench tool-script JSON array for exactly 4 weekly turns and write it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\codex\finance_script.json

Requirements:
- output must be a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like codex_finance_001
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, liquidity protection, treasury risk control, and financing discipline
- no markdown fences
- no prose explanation
- overwrite the output file with the final JSON only
```

## Claude Prompts

### Crisis

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_crisis_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\claude\crisis_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like claude_crisis_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, trust stabilization, and disciplined crisis handling
```

### Product

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_product_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\claude\product_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like claude_product_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, early quality stabilization, and support-capacity discipline
```

### Finance

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_finance_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\claude\finance_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like claude_finance_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, liquidity protection, treasury risk control, and financing discipline
```

## Gemini Prompts

### Crisis

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_crisis_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\gemini\crisis_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like gemini_crisis_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, trust stabilization, and disciplined crisis handling
```

### Product

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_product_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\gemini\product_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like gemini_product_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, early quality stabilization, and support-capacity discipline
```

### Finance

```text
Read and follow the scenario file at:
C:\Users\USER\Desktop\startup-bench\examples\minimal_finance_scenario.json

Return only the final JSON tool script and save it to:
C:\Users\USER\Desktop\startup-bench\tmp_model_trial_wave_001_scripts\gemini\finance_script.json

Requirements:
- output valid JSON only
- do not wrap it in markdown fences
- output a JSON array of tool-call objects
- use only tools declared by the scenario
- use unique request_id values like gemini_finance_001
- plan exactly 4 weekly turns
- end each turn with one sim.advance call using {"advance_by": 1, "unit": "week"}
- optimize for long-horizon company outcomes, liquidity protection, treasury risk control, and financing discipline
```

## Run The Trial

After each model writes its three scripts, run:

```powershell
powershell -File scripts/run_model_trial_wave_001.ps1 -ModelId codex
powershell -File scripts/run_model_trial_wave_001.ps1 -ModelId claude
powershell -File scripts/run_model_trial_wave_001.ps1 -ModelId gemini
```

This writes run artifacts to:

- `tmp_model_trial_wave_001_runs/codex`
- `tmp_model_trial_wave_001_runs/claude`
- `tmp_model_trial_wave_001_runs/gemini`

Each model gets:

- `crisis/trace.json`
- `crisis/score_report.json`
- `product/trace.json`
- `product/score_report.json`
- `finance/trace.json`
- `finance/score_report.json`

## Compare Results

Start with:

- final recommendation in each `score_report.json`
- whether the tool script stayed on-policy and scenario-relevant
- where the models differ in crisis prioritization, product discipline, and financing posture

Do not over-interpret one trial wave. Use this as the first controlled model comparison before running larger suites.
