# Scoring Contract

## 1. Scoring principles

Scoring SHOULD reward durable business performance under constraints.

Scoring MUST:

- prefer state-based evaluation over free-form text judgment
- separate outcomes from constraints
- expose subscores
- report uncertainty

## 2. Scenario score

Each scenario produces:

- `outcome_score`
- `constraint_score`
- `scenario_score`
- `subscores`
- `violations`

Recommended formula:

`scenario_score = outcome_score * constraint_score`

Where:

- `outcome_score` is normalized to `[0, 100]`
- `constraint_score` is normalized to `[0, 1]`

## 3. Outcome score

Outcome score SHOULD aggregate weighted components such as:

- revenue quality
- cash efficiency
- product health
- customer health
- team health
- strategic coherence
- risk management

Each component MUST declare:

- `component_id`
- `weight`
- `normalization`
- `higher_is_better`

## 4. Constraint score

Constraint score SHOULD encode hard or semi-hard penalties.

Constraint examples:

- bankruptcy
- severe compliance breach
- catastrophic trust loss
- severe morale collapse

Constraint score MAY use multiplicative penalties or minimum caps.

## 5. Semantic scoring

Semantic scoring MAY be used for artifacts such as:

- board updates
- customer responses
- hiring plans

Semantic scoring MUST:

- use rubric-bound evaluators
- preserve evaluator version
- be a minority share of total score
- emit rationale metadata for audits

## 6. Run-level aggregation

A run is one scenario-seed execution.

For each run, report:

- `scenario_score`
- `outcome_score`
- `constraint_score`
- `subscores`
- `violations`
- `api_cost_usd`
- `wall_clock_seconds`

## 7. Submission-level aggregation

A submission SHOULD report:

- mean score
- median score
- pass@1
- pass@k where relevant
- standard error or confidence interval
- per-track score
- cost-adjusted score

## 8. Pass criteria

Each scenario MAY define a pass threshold.

Pass criteria SHOULD be reserved for:

- flagship completion statistics
- `pass@k` reporting

Ranking SHOULD still use continuous scores.

## 9. Calibration policy

Scoring weights SHOULD be calibrated against:

- human operator baselines
- scripted baselines
- expert review

Weight changes MUST trigger at least a minor benchmark version bump.

