"""Reviewer assignment, form export, and import helpers."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from .paths import repo_root
from .scenario_loader import load_json
from .validation import raise_if_invalid, validate_instance

REVIEW_FORM_COLUMNS = [
    "reviewer_id",
    "role",
    "functional_domain",
    "startup_stage_focus",
    "years_experience",
    "scenario_id",
    "track",
    "split",
    "scenario_pack_version",
    "runner_type",
    "runner_id",
    "seed",
    "trace_path",
    "score_report_path",
    "survival_and_risk",
    "capital_allocation",
    "customer_trust",
    "people_leadership",
    "strategic_quality",
    "overall_recommendation",
    "strengths",
    "weaknesses",
    "recommended_actions",
    "benchmark_gaming_signals",
]


def _resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return repo_root() / path


def _load_study_manifest(path: Path) -> dict:
    manifest = load_json(path)
    raise_if_invalid(artifact_type="calibration-study", instance=manifest, path=path)
    return manifest


def _load_study_run(path: Path) -> dict:
    study_run = load_json(path)
    raise_if_invalid(artifact_type="calibration-study-run", instance=study_run, path=path)
    return study_run


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def _write_csv_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _split_notes(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def assign_reviewer_taskforce(
    *,
    study_manifest_path: Path,
    study_run_dir: Path,
    roster_path: Path,
    output_dir: Path,
) -> dict:
    manifest = _load_study_manifest(study_manifest_path)
    study_run = _load_study_run(study_run_dir / "calibration_study_run.json")
    roster_rows = _load_csv_rows(roster_path)
    active_reviewers = [row for row in roster_rows if row.get("status", "").lstrip("@").lower() in {"invited", "active"}]
    if not active_reviewers:
        raise ValueError("No active or invited reviewers found in roster.")

    target_lookup = {item["target_id"]: item for item in manifest["review_targets"]}
    assignments: list[dict] = []
    assignment_rows: list[dict[str, object]] = []
    reviewer_cursor = 0

    def pick_reviewers(target_count: int) -> list[dict[str, str]]:
        selected: list[dict[str, str]] = []
        nonlocal reviewer_cursor
        max_iterations = len(active_reviewers) * max(1, target_count)
        iterations = 0
        while len(selected) < target_count and iterations < max_iterations:
            reviewer = active_reviewers[reviewer_cursor % len(active_reviewers)]
            reviewer_cursor += 1
            iterations += 1
            if reviewer["reviewer_id"] in {item["reviewer_id"] for item in selected}:
                continue
            selected.append(reviewer)
        return selected

    for target_run in study_run["target_runs"]:
        target = target_lookup[target_run["target_id"]]
        requested_reviewers = int(manifest["promotion_gates"]["minimum_reviewers_per_target"])
        selected_reviewers = pick_reviewers(requested_reviewers)
        review_packet_path = Path(target_run["review_packet_path"])
        review_packet = load_json(review_packet_path)
        for reviewer in selected_reviewers:
            assignment_id = f"{target_run['target_id']}__{reviewer['reviewer_id']}"
            assignment = {
                "assignment_id": assignment_id,
                "reviewer_id": reviewer["reviewer_id"],
                "reviewer_role": reviewer.get("role", ""),
                "functional_domain": reviewer.get("functional_domain", ""),
                "target_id": target_run["target_id"],
                "focus": target["focus"],
                "review_packet_path": str(review_packet_path),
                "suite_report_path": target_run["suite_report_path"],
                "scenario_count": target_run["scenario_count"],
            }
            assignments.append(assignment)
            assignment_rows.append(assignment)

    assignment_manifest = {
        "assignment_version": "0.1.0",
        "benchmark_version": manifest["benchmark_version"],
        "study_id": manifest["study_id"],
        "assignment_count": len(assignments),
        "assignments": assignments,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "review_assignments.json"
    manifest_path.write_text(json.dumps(assignment_manifest, indent=2), encoding="utf-8")
    _write_csv_rows(
        output_dir / "review_assignments.csv",
        assignment_rows,
        ["assignment_id", "reviewer_id", "reviewer_role", "functional_domain", "target_id", "focus", "review_packet_path", "suite_report_path", "scenario_count"],
    )
    validation = validate_instance(
        artifact_type="review-assignments",
        instance=assignment_manifest,
        path=manifest_path,
    )
    return {
        "assignment_manifest": assignment_manifest,
        "validation": validation.to_dict(),
    }


def export_review_forms(
    *,
    assignment_manifest_path: Path,
    output_dir: Path,
) -> dict:
    assignment_manifest = load_json(assignment_manifest_path)
    raise_if_invalid(artifact_type="review-assignments", instance=assignment_manifest, path=assignment_manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported_forms: list[dict] = []
    by_reviewer: dict[str, list[dict]] = defaultdict(list)
    for assignment in assignment_manifest["assignments"]:
        by_reviewer[assignment["reviewer_id"]].append(assignment)

    for reviewer_id, assignments in sorted(by_reviewer.items()):
        reviewer_dir = output_dir / reviewer_id
        reviewer_dir.mkdir(parents=True, exist_ok=True)
        markdown_lines = [
            f"# Review Packet Assignments for {reviewer_id}",
            "",
            f"Study id: `{assignment_manifest['study_id']}`",
            "",
            "Assigned targets:",
        ]
        csv_rows: list[dict[str, object]] = []

        for assignment in assignments:
            packet = load_json(Path(assignment["review_packet_path"]))
            markdown_lines.extend(
                [
                    f"- `{assignment['target_id']}`: {assignment['focus']}",
                    f"  - review packet: `{assignment['review_packet_path']}`",
                    f"  - suite report: `{assignment['suite_report_path']}`",
                ]
            )
            scenario_lookup = {item["scenario_id"]: item for item in packet["scenarios"]}
            for scenario_id in packet["required_scenarios"]:
                scenario = scenario_lookup[scenario_id]
                csv_rows.append(
                    {
                        "reviewer_id": reviewer_id,
                        "role": assignment["reviewer_role"],
                        "functional_domain": assignment["functional_domain"],
                        "startup_stage_focus": "",
                        "years_experience": "",
                        "scenario_id": scenario["scenario_id"],
                        "track": scenario["track"],
                        "split": packet["split"],
                        "scenario_pack_version": packet["scenario_pack_version"],
                        "runner_type": packet["runner_type"],
                        "runner_id": packet["runner_id"],
                        "seed": packet["seed"],
                        "trace_path": "",
                        "score_report_path": "",
                        "survival_and_risk": "",
                        "capital_allocation": "",
                        "customer_trust": "",
                        "people_leadership": "",
                        "strategic_quality": "",
                        "overall_recommendation": "",
                        "strengths": "",
                        "weaknesses": "",
                        "recommended_actions": "",
                        "benchmark_gaming_signals": "",
                    }
                )

        markdown_path = reviewer_dir / "review_instructions.md"
        markdown_path.write_text("\n".join(markdown_lines) + "\n", encoding="utf-8")
        csv_path = reviewer_dir / "review_form.csv"
        _write_csv_rows(csv_path, csv_rows, REVIEW_FORM_COLUMNS)
        exported_forms.append(
            {
                "reviewer_id": reviewer_id,
                "markdown_path": str(markdown_path),
                "csv_path": str(csv_path),
                "scenario_count": len(csv_rows),
            }
        )

    result = {
        "export_version": "0.1.0",
        "study_id": assignment_manifest["study_id"],
        "reviewer_count": len(exported_forms),
        "exports": exported_forms,
    }
    validation = validate_instance(
        artifact_type="review-form-export",
        instance=result,
        path=output_dir / "review_form_export.json",
    )
    (output_dir / "review_form_export.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return {
        "export": result,
        "validation": validation.to_dict(),
    }


def import_review_forms(*, forms_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    imported_reviews: list[dict] = []
    review_paths: list[str] = []

    for csv_path in sorted(forms_dir.rglob("review_form.csv")):
        for row in _load_csv_rows(csv_path):
            if not row.get("scenario_id") or not row.get("overall_recommendation"):
                continue
            review = {
                "review_version": "0.1.0",
                "benchmark_version": "0.2.0-draft",
                "reviewer": {
                    "reviewer_id": row["reviewer_id"],
                    "role": row["role"],
                    "functional_domain": row["functional_domain"],
                    **({"years_experience": float(row["years_experience"])} if row.get("years_experience") else {}),
                    **({"startup_stage_focus": row["startup_stage_focus"]} if row.get("startup_stage_focus") else {}),
                },
                "scenario": {
                    "scenario_id": row["scenario_id"],
                    "track": row["track"],
                    "split": row["split"],
                    "scenario_pack_version": row["scenario_pack_version"],
                },
                "run": {
                    "runner_type": row["runner_type"],
                    "runner_id": row["runner_id"],
                    "seed": int(row["seed"]),
                    **({"trace_path": row["trace_path"]} if row.get("trace_path") else {}),
                    **({"score_report_path": row["score_report_path"]} if row.get("score_report_path") else {}),
                },
                "rubric": {
                    "survival_and_risk": int(row["survival_and_risk"]),
                    "capital_allocation": int(row["capital_allocation"]),
                    "customer_trust": int(row["customer_trust"]),
                    "people_leadership": int(row["people_leadership"]),
                    "strategic_quality": int(row["strategic_quality"]),
                    "overall_recommendation": row["overall_recommendation"],
                },
                "notes": {
                    "strengths": _split_notes(row.get("strengths", "")),
                    "weaknesses": _split_notes(row.get("weaknesses", "")),
                    "recommended_actions": _split_notes(row.get("recommended_actions", "")),
                    "benchmark_gaming_signals": _split_notes(row.get("benchmark_gaming_signals", "")),
                },
            }
            review_filename = f"{row['reviewer_id']}__{row['scenario_id']}.json"
            review_path = output_dir / review_filename
            raise_if_invalid(artifact_type="operator-review", instance=review, path=review_path)
            review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
            imported_reviews.append(review)
            review_paths.append(str(review_path))

    result = {
        "import_version": "0.1.0",
        "review_count": len(imported_reviews),
        "review_paths": review_paths,
    }
    validation = validate_instance(
        artifact_type="review-form-import",
        instance=result,
        path=output_dir / "review_form_import.json",
    )
    (output_dir / "review_form_import.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return {
        "import_result": result,
        "validation": validation.to_dict(),
    }
