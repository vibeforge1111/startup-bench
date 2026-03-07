"""Benchmark-to-operator calibration helpers."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean

from .human_eval import RECOMMENDATION_ORDER, RUBRIC_KEYS, aggregate_operator_reviews
from .scenario_loader import load_json
from .validation import validate_instance


def _round_metric(value: float) -> float:
    return round(value, 4)


def _benchmark_score_to_rubric(score: float) -> float:
    return 1.0 + (4.0 * float(score))


def _recommendation_from_rubric(score: float) -> str:
    if score >= 3.5:
        return "pass"
    if score >= 2.5:
        return "borderline"
    return "fail"


def _top_recommendation(distribution: dict[str, int]) -> str:
    return sorted(
        RECOMMENDATION_ORDER,
        key=lambda item: (-distribution.get(item, 0), RECOMMENDATION_ORDER.index(item)),
    )[0]


def build_calibration_report(*, suite_report_path: Path, review_paths: list[Path]) -> dict:
    if not review_paths:
        raise ValueError("At least one operator review is required.")

    suite_report = load_json(suite_report_path)
    suite_validation = validate_instance(
        artifact_type="suite-report",
        instance=suite_report,
        path=suite_report_path,
    )
    if not suite_validation.ok:
        return {
            "report": None,
            "validation": {
                "artifact_type": "calibration-report",
                "path": "calibration_report.json",
                "schema_name": "tsb_calibration_report.schema.json",
                "ok": False,
                "issues": suite_validation.to_dict()["issues"],
            },
            "suite_validation": suite_validation.to_dict(),
            "review_summary_validation": None,
        }

    review_result = aggregate_operator_reviews(review_paths)
    if not review_result["validation"]["ok"] or review_result["summary"] is None:
        return {
            "report": None,
            "validation": review_result["validation"],
            "suite_validation": suite_validation.to_dict(),
            "review_summary_validation": review_result["validation"],
        }

    review_summary = review_result["summary"]
    suite_scenarios = {item["scenario_id"]: item for item in suite_report["scenario_reports"]}
    track_groups: dict[str, list[dict]] = defaultdict(list)
    scenario_alignments: list[dict] = []
    matched_count = 0

    for scenario_summary in review_summary["scenario_summaries"]:
        scenario_id = scenario_summary["scenario_id"]
        suite_entry = suite_scenarios.get(scenario_id)
        if suite_entry is None:
            continue
        matched_count += 1
        operator_mean_rubric = mean(float(scenario_summary["mean_scores"][key]) for key in RUBRIC_KEYS)
        benchmark_rubric = _benchmark_score_to_rubric(suite_entry["scenario_score_mean"])
        operator_recommendation = _top_recommendation(scenario_summary["recommendation_distribution"])
        benchmark_recommendation = _recommendation_from_rubric(benchmark_rubric)
        alignment = {
            "scenario_id": scenario_id,
            "track": scenario_summary["track"],
            "review_count": scenario_summary["review_count"],
            "benchmark_score": _round_metric(float(suite_entry["scenario_score_mean"])),
            "benchmark_rubric_equivalent": _round_metric(benchmark_rubric),
            "operator_mean_rubric": _round_metric(operator_mean_rubric),
            "operator_recommendation": operator_recommendation,
            "benchmark_recommendation": benchmark_recommendation,
            "recommendation_agreement": operator_recommendation == benchmark_recommendation,
            "absolute_rubric_gap": _round_metric(abs(benchmark_rubric - operator_mean_rubric)),
            "disagreement_flag": bool(scenario_summary["disagreement_flag"]),
        }
        scenario_alignments.append(alignment)
        track_groups[alignment["track"]].append(alignment)

    track_alignments = []
    for track, rows in sorted(track_groups.items()):
        track_alignments.append(
            {
                "track": track,
                "scenario_count": len(rows),
                "mean_benchmark_rubric_equivalent": _round_metric(mean(row["benchmark_rubric_equivalent"] for row in rows)),
                "mean_operator_rubric": _round_metric(mean(row["operator_mean_rubric"] for row in rows)),
                "mean_absolute_rubric_gap": _round_metric(mean(row["absolute_rubric_gap"] for row in rows)),
                "recommendation_agreement_rate": _round_metric(
                    mean(1.0 if row["recommendation_agreement"] else 0.0 for row in rows)
                ),
            }
        )

    report = {
        "report_version": "0.1.0",
        "benchmark_version": suite_report["benchmark_version"],
        "scenario_pack_version": suite_report["scenario_pack_version"],
        "split": suite_report["split"],
        "runner_type": suite_report["runner_type"],
        "runner_id": suite_report["runner_id"],
        "review_count": review_summary["review_count"],
        "reviewer_count": review_summary["reviewer_count"],
        "matched_scenario_count": matched_count,
        "unmatched_review_scenario_count": review_summary["scenario_count"] - matched_count,
        "overall": {
            "mean_benchmark_rubric_equivalent": _round_metric(
                mean(item["benchmark_rubric_equivalent"] for item in scenario_alignments)
            ) if scenario_alignments else 0.0,
            "mean_operator_rubric": _round_metric(
                mean(item["operator_mean_rubric"] for item in scenario_alignments)
            ) if scenario_alignments else 0.0,
            "mean_absolute_rubric_gap": _round_metric(
                mean(item["absolute_rubric_gap"] for item in scenario_alignments)
            ) if scenario_alignments else 0.0,
            "recommendation_agreement_rate": _round_metric(
                mean(1.0 if item["recommendation_agreement"] else 0.0 for item in scenario_alignments)
            ) if scenario_alignments else 0.0,
        },
        "track_alignments": track_alignments,
        "scenario_alignments": scenario_alignments,
    }
    validation = validate_instance(
        artifact_type="calibration-report",
        instance=report,
        path=Path("calibration_report.json"),
    )
    return {
        "report": report,
        "validation": validation.to_dict(),
        "suite_validation": suite_validation.to_dict(),
        "review_summary_validation": review_result["validation"],
    }
