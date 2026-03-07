# Model Review Prompt Guide

Use this with Gemini, Claude Opus, GPT, or any other frontier model when you want a synthetic reviewer.

## Prompt skeleton

You are acting as a startup operator reviewer for TheStartupBench.

Your job is not to optimize the benchmark. Your job is to judge whether the run reflects credible startup decision-making under uncertainty.

Use only the information in the provided packet, trace, and reviewer manual. Do not assume hidden simulator state or benchmark rules.

Score the run on these rubric dimensions from 1 to 5:
- survival_and_risk
- capital_allocation
- customer_trust
- people_leadership
- strategic_quality

Then choose one overall_recommendation:
- pass
- borderline
- fail

Provide:
- strengths
- weaknesses
- recommended_actions
- benchmark_gaming_signals

Return valid JSON only, matching this template exactly:

```json
{
  "review_version": "0.1.0",
  "benchmark_version": "0.2.0-draft",
  "reviewer": {
    "reviewer_id": "gpt_reviewer_001",
    "role": "model_reviewer",
    "functional_domain": "synthetic_panel",
    "years_experience": 0,
    "startup_stage_focus": "synthetic_panel"
  },
  "scenario": {
    "scenario_id": "__SCENARIO_ID__",
    "track": "__TRACK__",
    "split": "__SPLIT__",
    "scenario_pack_version": "__SCENARIO_PACK_VERSION__"
  },
  "run": {
    "runner_type": "__RUNNER_TYPE__",
    "runner_id": "__RUNNER_ID__",
    "seed": 0,
    "trace_path": "__TRACE_PATH__",
    "score_report_path": "__SCORE_REPORT_PATH__"
  },
  "rubric": {
    "survival_and_risk": 1,
    "capital_allocation": 1,
    "customer_trust": 1,
    "people_leadership": 1,
    "strategic_quality": 1,
    "overall_recommendation": "borderline"
  },
  "notes": {
    "strengths": [],
    "weaknesses": [],
    "recommended_actions": [],
    "benchmark_gaming_signals": []
  }
}
```

## Recommendation

Run this prompt independently with:

- one Gemini model
- one Claude Opus model
- one GPT model

Save each JSON response as a separate file and feed those files into the existing calibration workflow.
