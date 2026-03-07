"""Submission aggregation helpers for leaderboard-ready artifacts."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean, median

from . import __version__
from .scenario_loader import load_json
from .validation import validate_instance


def _round_metric(value: float) -> float:
    return round(value, 4)


def build_submission(
    *,
    suite_report_paths: list[Path],
    model_id: str,
    provider: str,
    contamination_flag: str,
    contamination_notes: str = "",
    release_date: str | None = None,
    source_url: str | None = None,
) -> dict:
    if not suite_report_paths:
        raise ValueError("At least one suite report is required.")

    suite_reports = [load_json(path) for path in suite_report_paths]
    track_groups: dict[str, list[dict]] = defaultdict(list)
    benchmark_version = suite_reports[0]["benchmark_version"]
    scenario_pack_version = suite_reports[0]["scenario_pack_version"]
    repeat_count = min(report["scenario_reports"][0]["run_count"] for report in suite_reports)

    for report in suite_reports:
        for scenario_report in report["scenario_reports"]:
            track_groups[scenario_report["track"]].append(scenario_report)

    track_summaries = []
    for track, reports in sorted(track_groups.items()):
        scores = [float(report["scenario_score_mean"]) for report in reports]
        pass_rates = [float(report["pass_rate"]) for report in reports]
        if len(scores) == 1:
            sem = 0.0
        else:
            score_mean = mean(scores)
            variance = sum((score - score_mean) ** 2 for score in scores) / len(scores)
            sem = (variance ** 0.5) / (len(scores) ** 0.5)

        track_summaries.append(
            {
                "track": track,
                "mean_score": _round_metric(mean(scores)),
                "median_score": _round_metric(median(scores)),
                "pass_at_1": _round_metric(mean(pass_rates)),
                "pass_at_k": _round_metric(mean(pass_rates)),
                "sem": _round_metric(sem),
                "api_cost_usd": 0.0,
            }
        )

    submission = {
        "submission_version": "0.1.0",
        "benchmark_version": benchmark_version,
        "scenario_pack_version": scenario_pack_version,
        "scaffold_version": __version__,
        "model": {
            "model_id": model_id,
            "provider": provider,
            **({"release_date": release_date} if release_date else {}),
        },
        "evaluation": {
            "repeat_count": repeat_count,
            "track_summaries": track_summaries,
        },
        "contamination": {
            "flag": contamination_flag,
            **({"notes": contamination_notes} if contamination_notes else {}),
        },
        "artifacts": {
            **({"source_url": source_url} if source_url else {}),
        },
    }
    if not submission["artifacts"]:
        submission.pop("artifacts")

    return {
        "submission": submission,
        "validation": validate_instance(
            artifact_type="submission",
            instance=submission,
            path=Path("submission.json"),
        ).to_dict(),
    }


__all__ = ["build_submission"]
