"""Scenario-suite evaluation helpers."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean

from .campaign_runner import _ci95, _sem, run_campaign
from .scenario_loader import load_json
from .validation import raise_if_invalid, validate_instance


def _round_metric(value: float) -> float:
    return round(value, 4)


def load_scenario_suite(path: Path) -> dict:
    suite = load_json(path)
    raise_if_invalid(artifact_type="scenario-suite", instance=suite, path=path)
    return suite


def run_suite(
    *,
    suite_path: Path,
    runner_type: str,
    seeds: list[int],
    baseline_id: str | None = None,
    tool_calls_path: Path | None = None,
    max_turns: int | None = None,
) -> dict:
    suite = load_scenario_suite(suite_path)
    suite_dir = suite_path.parent
    scenario_reports: list[dict] = []
    track_groups: dict[str, list[dict]] = defaultdict(list)

    for entry in suite["scenarios"]:
        scenario_path = suite_dir / entry["path"]
        campaign = run_campaign(
            scenario_path=scenario_path,
            runner_type=runner_type,
            seeds=seeds,
            baseline_id=baseline_id,
            tool_calls_path=tool_calls_path,
            max_turns=max_turns,
        )["batch_report"]
        report = {
            "scenario_id": campaign["campaign"]["scenario_id"],
            "track": campaign["campaign"]["track"],
            "run_count": campaign["campaign"]["run_count"],
            "scenario_score_mean": campaign["aggregate_metrics"]["scenario_score_mean"],
            "scenario_score_sem": campaign["aggregate_metrics"]["scenario_score_sem"],
            "scenario_score_ci95_low": campaign["aggregate_metrics"]["scenario_score_ci95_low"],
            "scenario_score_ci95_high": campaign["aggregate_metrics"]["scenario_score_ci95_high"],
            "pass_rate": campaign["aggregate_metrics"]["pass_rate"],
        }
        scenario_reports.append(report)
        track_groups[report["track"]].append(report)

    track_summaries = []
    for track, reports in sorted(track_groups.items()):
        score_means = [report["scenario_score_mean"] for report in reports]
        score_ci95_low, score_ci95_high = _ci95(score_means)
        track_summaries.append(
            {
                "track": track,
                "scenario_count": len(reports),
                "scenario_score_mean": _round_metric(mean(score_means)),
                "scenario_score_sem": _round_metric(_sem(score_means)),
                "scenario_score_ci95_low": _round_metric(score_ci95_low),
                "scenario_score_ci95_high": _round_metric(score_ci95_high),
                "pass_rate_mean": _round_metric(mean(report["pass_rate"] for report in reports)),
            }
        )

    overall_score_means = [report["scenario_score_mean"] for report in scenario_reports]
    overall_ci95_low, overall_ci95_high = _ci95(overall_score_means)

    suite_report = {
        "report_version": "0.1.0",
        "benchmark_version": suite["benchmark_version"],
        "scenario_pack_version": suite["scenario_pack_version"],
        "split": suite["split"],
        "runner_type": runner_type,
        "runner_id": baseline_id if runner_type == "baseline" else (tool_calls_path.name if tool_calls_path else runner_type),
        "overall": {
            "scenario_count": len(scenario_reports),
            "scenario_score_mean": _round_metric(mean(overall_score_means)),
            "scenario_score_sem": _round_metric(_sem(overall_score_means)),
            "scenario_score_ci95_low": _round_metric(overall_ci95_low),
            "scenario_score_ci95_high": _round_metric(overall_ci95_high),
            "pass_rate_mean": _round_metric(mean(report["pass_rate"] for report in scenario_reports)),
        },
        "track_summaries": track_summaries,
        "scenario_reports": scenario_reports,
    }
    return {
        "suite_report": suite_report,
        "validation": validate_instance(
            artifact_type="suite-report",
            instance=suite_report,
            path=Path("suite_report.json"),
        ).to_dict(),
    }


__all__ = ["load_scenario_suite", "run_suite"]
