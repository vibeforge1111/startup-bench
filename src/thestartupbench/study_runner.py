"""Calibration study execution helpers."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from .calibration import build_calibration_report
from .baseline_runner import run_baseline
from .paths import repo_root
from .scenario_loader import load_json, load_scenario
from .suite_runner import load_scenario_suite, run_suite
from .validation import raise_if_invalid, validate_instance


def _round_metric(value: float) -> float:
    return round(value, 4)


def _resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return repo_root() / path


def _load_study_manifest(path: Path) -> dict:
    manifest = load_json(path)
    raise_if_invalid(artifact_type="calibration-study", instance=manifest, path=path)
    return manifest


def _write_scenario_run_artifacts(
    *,
    scenario_path: Path,
    baseline_runner_id: str,
    seed: int,
    max_turns: int | None,
    output_dir: Path,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run_baseline(
        scenario_path=scenario_path,
        baseline_id=baseline_runner_id,
        seed=seed,
        max_turns=max_turns,
    )
    trace_path = output_dir / "trace.json"
    score_report_path = output_dir / "score_report.json"
    trace_path.write_text(json.dumps(result["trace"], indent=2), encoding="utf-8")
    score_report_path.write_text(json.dumps(result["score_report"], indent=2), encoding="utf-8")
    return {
        "trace_path": str(trace_path),
        "score_report_path": str(score_report_path),
    }


def run_calibration_study(*, study_manifest_path: Path, output_dir: Path) -> dict:
    manifest = _load_study_manifest(study_manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    targets_dir = output_dir / "targets"
    targets_dir.mkdir(parents=True, exist_ok=True)

    target_runs = []
    for target in manifest["review_targets"]:
        suite_path = _resolve_path(target["suite_path"])
        suite = load_scenario_suite(suite_path)
        target_dir = targets_dir / target["target_id"]
        target_dir.mkdir(parents=True, exist_ok=True)

        suite_result = run_suite(
            suite_path=suite_path,
            runner_type="baseline",
            seeds=[int(target["seed"])],
            baseline_id=target["baseline_runner_id"],
            max_turns=target.get("max_turns"),
        )
        suite_report = suite_result["suite_report"]
        suite_report_path = target_dir / "suite_report.json"
        suite_report_path.write_text(json.dumps(suite_report, indent=2), encoding="utf-8")

        scenario_entries = []
        for entry in suite["scenarios"]:
            scenario_path = (suite_path.parent / entry["path"]).resolve()
            scenario = load_scenario(scenario_path)
            scenario_run_artifacts = _write_scenario_run_artifacts(
                scenario_path=scenario_path,
                baseline_runner_id=target["baseline_runner_id"],
                seed=int(target["seed"]),
                max_turns=target.get("max_turns"),
                output_dir=target_dir / "scenarios" / scenario["metadata"]["scenario_id"],
            )
            scenario_entries.append(
                {
                    "scenario_id": scenario["metadata"]["scenario_id"],
                    "track": scenario["metadata"]["track"],
                    "title": scenario["metadata"]["title"],
                    "summary": scenario["metadata"]["summary"],
                    "trace_path": scenario_run_artifacts["trace_path"],
                    "score_report_path": scenario_run_artifacts["score_report_path"],
                }
            )

        packet = {
            "packet_version": "0.1.0",
            "benchmark_version": manifest["benchmark_version"],
            "study_id": manifest["study_id"],
            "target_id": target["target_id"],
            "focus": target["focus"],
            "suite_path": str(suite_path),
            "suite_report_path": str(suite_report_path),
            "scenario_pack_version": suite_report["scenario_pack_version"],
            "split": suite_report["split"],
            "runner_type": suite_report["runner_type"],
            "runner_id": target["baseline_runner_id"],
            "seed": int(target["seed"]),
            "required_scenarios": target.get(
                "required_scenarios",
                [item["scenario_id"] for item in scenario_entries],
            ),
            "rubric_keys": [
                "survival_and_risk",
                "capital_allocation",
                "customer_trust",
                "people_leadership",
                "strategic_quality",
            ],
            "scenarios": scenario_entries,
        }
        packet_path = target_dir / "review_packet.json"
        packet_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")

        packet_validation = validate_instance(
            artifact_type="review-packet",
            instance=packet,
            path=packet_path,
        )
        target_runs.append(
            {
                "target_id": target["target_id"],
                "suite_report_path": str(suite_report_path),
                "review_packet_path": str(packet_path),
                "scenario_count": len(scenario_entries),
                "validation": {
                    "suite_report": suite_result["validation"],
                    "review_packet": packet_validation.to_dict(),
                },
            }
        )

    study_run = {
        "run_version": "0.1.0",
        "benchmark_version": manifest["benchmark_version"],
        "study_id": manifest["study_id"],
        "target_count": len(target_runs),
        "target_runs": target_runs,
    }
    validation = validate_instance(
        artifact_type="calibration-study-run",
        instance=study_run,
        path=output_dir / "calibration_study_run.json",
    )
    (output_dir / "calibration_study_run.json").write_text(json.dumps(study_run, indent=2), encoding="utf-8")
    return {
        "study_run": study_run,
        "validation": validation.to_dict(),
    }


def compile_calibration_study(
    *,
    study_manifest_path: Path,
    study_run_dir: Path,
    review_paths: list[Path],
    output_dir: Path,
) -> dict:
    manifest = _load_study_manifest(study_manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    study_run = load_json(study_run_dir / "calibration_study_run.json")
    raise_if_invalid(
        artifact_type="calibration-study-run",
        instance=study_run,
        path=study_run_dir / "calibration_study_run.json",
    )

    loaded_reviews = []
    for review_path in review_paths:
        review = load_json(review_path)
        raise_if_invalid(artifact_type="operator-review", instance=review, path=review_path)
        loaded_reviews.append((review_path, review))

    target_reports = []
    completed_reports = []
    target_output_dir = output_dir / "targets"
    target_output_dir.mkdir(parents=True, exist_ok=True)

    for target in manifest["review_targets"]:
        suite_report_path = study_run_dir / "targets" / target["target_id"] / "suite_report.json"
        suite_report = load_json(suite_report_path)
        scenario_ids = {item["scenario_id"] for item in suite_report["scenario_reports"]}
        target_review_paths = [
            path for path, review in loaded_reviews if review["scenario"]["scenario_id"] in scenario_ids
        ]
        if not target_review_paths:
            target_reports.append(
                {
                    "target_id": target["target_id"],
                    "focus": target["focus"],
                    "status": "pending",
                    "review_count": 0,
                    "matched_scenario_count": 0,
                    "mean_absolute_rubric_gap": 0.0,
                    "recommendation_agreement_rate": 0.0,
                }
            )
            continue

        target_dir = target_output_dir / target["target_id"]
        target_dir.mkdir(parents=True, exist_ok=True)
        calibration_result = build_calibration_report(
            suite_report_path=suite_report_path,
            review_paths=target_review_paths,
        )
        report = calibration_result["report"]
        if report is None:
            raise ValueError(f"Calibration report failed for target '{target['target_id']}'.")
        report_path = target_dir / "calibration_report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        target_report = {
            "target_id": target["target_id"],
            "focus": target["focus"],
            "status": "completed",
            "review_count": report["review_count"],
            "matched_scenario_count": report["matched_scenario_count"],
            "mean_absolute_rubric_gap": report["overall"]["mean_absolute_rubric_gap"],
            "recommendation_agreement_rate": report["overall"]["recommendation_agreement_rate"],
            "calibration_report_path": str(report_path),
        }
        target_reports.append(target_report)
        completed_reports.append(target_report)

    overall_gap = mean(item["mean_absolute_rubric_gap"] for item in completed_reports) if completed_reports else 0.0
    overall_agreement = (
        mean(item["recommendation_agreement_rate"] for item in completed_reports) if completed_reports else 0.0
    )
    gates = manifest["promotion_gates"]
    study_report = {
        "report_version": "0.1.0",
        "benchmark_version": manifest["benchmark_version"],
        "study_id": manifest["study_id"],
        "target_count": len(manifest["review_targets"]),
        "completed_target_count": len(completed_reports),
        "pending_target_count": len(manifest["review_targets"]) - len(completed_reports),
        "overall": {
            "mean_absolute_rubric_gap": _round_metric(overall_gap),
            "recommendation_agreement_rate": _round_metric(overall_agreement),
        },
        "promotion_gate_status": {
            "minimum_reviewers_per_target_met": all(
                item["review_count"] >= gates["minimum_reviewers_per_target"] for item in completed_reports
            ) if completed_reports else False,
            "mean_absolute_rubric_gap_met": overall_gap <= float(gates["maximum_mean_absolute_rubric_gap"]),
            "recommendation_agreement_rate_met": overall_agreement >= float(gates["minimum_recommendation_agreement_rate"]),
            "ready_for_promotion": bool(completed_reports)
            and len(completed_reports) == len(manifest["review_targets"])
            and all(item["review_count"] >= gates["minimum_reviewers_per_target"] for item in completed_reports)
            and overall_gap <= float(gates["maximum_mean_absolute_rubric_gap"])
            and overall_agreement >= float(gates["minimum_recommendation_agreement_rate"]),
        },
        "target_reports": target_reports,
    }
    validation = validate_instance(
        artifact_type="calibration-study-report",
        instance=study_report,
        path=output_dir / "calibration_study_report.json",
    )
    (output_dir / "calibration_study_report.json").write_text(json.dumps(study_report, indent=2), encoding="utf-8")
    return {
        "study_report": study_report,
        "validation": validation.to_dict(),
    }
