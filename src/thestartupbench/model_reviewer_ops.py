"""Synthetic reviewer prompt export and raw-review import helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .paths import repo_root
from .scenario_loader import load_json
from .validation import raise_if_invalid, validate_instance

PROMPT_TEMPLATE = """# TheStartupBench Synthetic Reviewer Prompt

You are acting as a startup operator reviewer for TheStartupBench.

Your job is not to optimize the benchmark. Your job is to judge whether the run reflects credible startup decision-making under uncertainty.

Use only the information in the provided context. Do not assume hidden simulator state or benchmark rules.

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

Return valid JSON only. Do not wrap the JSON in explanation.

Recommended synthetic reviewer ids:
- codex_reviewer_001
- claude_reviewer_001
- gemini_reviewer_001

## Review rules

- Judge the run as a sober startup operator, not as a benchmark optimizer.
- Reward disciplined survival, trust protection, and coherent tradeoffs.
- Penalize brittle growth hacking, unrealistic assumptions, or obvious benchmark gaming.
- If evidence is missing, score conservatively and note the missing evidence in `weaknesses`.

## Scenario context and evidence

```json
{context_json}
```

## Return this exact JSON shape

```json
{template_json}
```
"""


def _resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return repo_root() / path


def _extract_json_object(text: str) -> dict:
    stripped = text.strip()
    fenced_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.DOTALL)
    candidate = fenced_match.group(1) if fenced_match else stripped
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        start_index = candidate.find("{")
        if start_index == -1:
            raise
        parsed, _ = decoder.raw_decode(candidate[start_index:])
        if not isinstance(parsed, dict):
            raise json.JSONDecodeError("Expected a JSON object.", candidate, start_index)
        return parsed


def _load_study_run(path: Path) -> dict:
    study_run = load_json(path)
    raise_if_invalid(artifact_type="calibration-study-run", instance=study_run, path=path)
    return study_run


def _build_template(*, packet: dict, scenario: dict) -> dict:
    return {
        "review_version": "0.1.0",
        "benchmark_version": packet["benchmark_version"],
        "reviewer": {
            "reviewer_id": "__REVIEWER_ID__",
            "role": "model_reviewer",
            "functional_domain": "synthetic_panel",
            "years_experience": 0,
            "startup_stage_focus": "synthetic_panel",
        },
        "scenario": {
            "scenario_id": scenario["scenario_id"],
            "track": scenario["track"],
            "split": packet["split"],
            "scenario_pack_version": packet["scenario_pack_version"],
        },
        "run": {
            "runner_type": packet["runner_type"],
            "runner_id": packet["runner_id"],
            "seed": packet["seed"],
            "trace_path": scenario["trace_path"],
            "score_report_path": scenario["score_report_path"],
        },
        "rubric": {
            "survival_and_risk": 1,
            "capital_allocation": 1,
            "customer_trust": 1,
            "people_leadership": 1,
            "strategic_quality": 1,
            "overall_recommendation": "borderline",
        },
        "notes": {
            "strengths": [],
            "weaknesses": [],
            "recommended_actions": [],
            "benchmark_gaming_signals": [],
        },
    }


def export_model_review_bundles(*, study_run_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    study_run = _load_study_run(study_run_dir / "calibration_study_run.json")

    bundles: list[dict] = []
    for target_run in study_run["target_runs"]:
        packet_path = _resolve_path(target_run["review_packet_path"])
        suite_report_path = _resolve_path(target_run["suite_report_path"])
        packet = load_json(packet_path)
        raise_if_invalid(artifact_type="review-packet", instance=packet, path=packet_path)
        suite_report = load_json(suite_report_path)
        raise_if_invalid(artifact_type="suite-report", instance=suite_report, path=suite_report_path)

        scenario_lookup = {item["scenario_id"]: item for item in packet["scenarios"]}
        report_lookup = {item["scenario_id"]: item for item in suite_report["scenario_reports"]}

        for scenario_id in packet["required_scenarios"]:
            if scenario_id not in scenario_lookup:
                raise ValueError(f"Scenario '{scenario_id}' is required by review packet but missing from packet scenarios.")
            if scenario_id not in report_lookup:
                raise ValueError(f"Scenario '{scenario_id}' is required by review packet but missing from suite report.")

            scenario = scenario_lookup[scenario_id]
            scenario_report = report_lookup[scenario_id]
            trace_path = _resolve_path(scenario["trace_path"])
            score_report_path = _resolve_path(scenario["score_report_path"])
            trace = load_json(trace_path)
            raise_if_invalid(artifact_type="trace", instance=trace, path=trace_path)
            score_report = load_json(score_report_path)
            raise_if_invalid(artifact_type="score-report", instance=score_report, path=score_report_path)
            template = _build_template(packet=packet, scenario=scenario)
            context = {
                "benchmark_version": packet["benchmark_version"],
                "study_id": packet["study_id"],
                "target_id": packet["target_id"],
                "focus": packet["focus"],
                "scenario": scenario,
                "run": {
                    "runner_type": packet["runner_type"],
                    "runner_id": packet["runner_id"],
                    "seed": packet["seed"],
                    "trace_path": scenario["trace_path"],
                    "score_report_path": scenario["score_report_path"],
                },
                "suite_report_path": packet["suite_report_path"],
                "scenario_report": scenario_report,
                "score_report": score_report,
                "trace": trace,
                "rubric_keys": packet["rubric_keys"],
            }

            bundle_dir = output_dir / packet["target_id"] / scenario_id
            bundle_dir.mkdir(parents=True, exist_ok=True)
            prompt_path = bundle_dir / "prompt.md"
            context_path = bundle_dir / "context.json"
            template_path = bundle_dir / "review_template.json"
            trace_bundle_path = bundle_dir / "trace.json"
            score_bundle_path = bundle_dir / "score_report.json"

            context_json = json.dumps(context, indent=2)
            template_json = json.dumps(template, indent=2)
            prompt_path.write_text(
                PROMPT_TEMPLATE.format(context_json=context_json, template_json=template_json),
                encoding="utf-8",
            )
            context_path.write_text(context_json + "\n", encoding="utf-8")
            template_path.write_text(template_json + "\n", encoding="utf-8")
            trace_bundle_path.write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")
            score_bundle_path.write_text(json.dumps(score_report, indent=2) + "\n", encoding="utf-8")

            bundles.append(
                {
                    "bundle_id": f"{packet['target_id']}__{scenario_id}",
                    "target_id": packet["target_id"],
                    "scenario_id": scenario_id,
                    "track": scenario["track"],
                    "split": packet["split"],
                    "scenario_pack_version": packet["scenario_pack_version"],
                    "prompt_path": str(prompt_path),
                    "context_path": str(context_path),
                    "template_path": str(template_path),
                    "trace_path": str(trace_bundle_path),
                    "score_report_path": str(score_bundle_path),
                }
            )

    result = {
        "export_version": "0.1.0",
        "study_id": study_run["study_id"],
        "bundle_count": len(bundles),
        "bundles": bundles,
    }
    manifest_path = output_dir / "model_review_prompt_export.json"
    manifest_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    validation = validate_instance(
        artifact_type="model-review-prompt-export",
        instance=result,
        path=manifest_path,
    )
    return {
        "export": result,
        "validation": validation.to_dict(),
    }


def import_model_reviews(*, raw_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    imported_review_paths: list[str] = []
    rejected_files: list[dict[str, str]] = []

    for path in sorted(raw_dir.rglob("*")):
        if path.is_dir() or path.name == "model_review_import.json":
            continue
        if path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        try:
            review = _extract_json_object(path.read_text(encoding="utf-8"))
            raise_if_invalid(artifact_type="operator-review", instance=review, path=path)
        except Exception as exc:  # noqa: BLE001
            rejected_files.append({"path": str(path), "message": str(exc)})
            continue

        review_filename = f"{review['reviewer']['reviewer_id']}__{review['scenario']['scenario_id']}.json"
        review_path = output_dir / review_filename
        review_path.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
        imported_review_paths.append(str(review_path))

    result = {
        "import_version": "0.1.0",
        "imported_review_count": len(imported_review_paths),
        "imported_review_paths": imported_review_paths,
        "rejected_count": len(rejected_files),
        "rejected_files": rejected_files,
    }
    manifest_path = output_dir / "model_review_import.json"
    manifest_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    validation = validate_instance(
        artifact_type="model-review-import",
        instance=result,
        path=manifest_path,
    )
    return {
        "import_result": result,
        "validation": validation.to_dict(),
    }


__all__ = ["export_model_review_bundles", "import_model_reviews"]
