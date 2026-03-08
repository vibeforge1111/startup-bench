"""Artifact validation utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from jsonschema.exceptions import ValidationError

from .schema_store import build_validator

SCHEMA_BY_ARTIFACT_TYPE = {
    "scenario": "tsb_scenario.schema.json",
    "scenario-suite": "tsb_scenario_suite.schema.json",
    "public-suite-manifest": "tsb_public_suite_manifest.schema.json",
    "pack-changelog": "tsb_pack_changelog.schema.json",
    "official-eval-profile": "tsb_official_eval_profile.schema.json",
    "official-eval-window": "tsb_official_eval_window.schema.json",
    "leaderboard-governance-pack": "tsb_leaderboard_governance_pack.schema.json",
    "hidden-pack-rotation-policy": "tsb_hidden_pack_rotation_policy.schema.json",
    "run-manifest": "tsb_run_manifest.schema.json",
    "trace": "tsb_trace.schema.json",
    "submission": "tsb_submission.schema.json",
    "operator-review": "tsb_operator_review.schema.json",
    "operator-review-summary": "tsb_operator_review_summary.schema.json",
    "calibration-report": "tsb_calibration_report.schema.json",
    "calibration-study": "tsb_calibration_study.schema.json",
    "review-packet": "tsb_review_packet.schema.json",
    "calibration-study-run": "tsb_calibration_study_run.schema.json",
    "calibration-study-report": "tsb_calibration_study_report.schema.json",
    "review-assignments": "tsb_review_assignments.schema.json",
    "review-form-export": "tsb_review_form_export.schema.json",
    "review-form-import": "tsb_review_form_import.schema.json",
    "model-review-prompt-export": "tsb_model_review_prompt_export.schema.json",
    "model-review-import": "tsb_model_review_import.schema.json",
    "world-state": "tsb_world_state.schema.json",
    "primitives": "tsb_primitives.schema.json",
    "tool-manifest": "tsb_tool_manifest.schema.json",
    "tool-call": "tsb_tool_call.schema.json",
    "tool-response": "tsb_tool_response.schema.json",
    "evaluator-result": "tsb_evaluator_result.schema.json",
    "score-report": "tsb_score_report.schema.json",
    "batch-report": "tsb_batch_report.schema.json",
    "suite-report": "tsb_suite_report.schema.json",
}


@dataclass(frozen=True)
class ValidationIssue:
    message: str
    path: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"message": self.message, "path": self.path}


@dataclass(frozen=True)
class ValidationResult:
    artifact_type: str
    path: str
    schema_name: str
    ok: bool
    issues: list[ValidationIssue]

    def to_dict(self) -> dict:
        return {
            "artifact_type": self.artifact_type,
            "path": self.path,
            "schema_name": self.schema_name,
            "ok": self.ok,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_instance(*, artifact_type: str, instance: dict, path: Path) -> ValidationResult:
    if artifact_type not in SCHEMA_BY_ARTIFACT_TYPE:
        known = sorted(SCHEMA_BY_ARTIFACT_TYPE)
        raise KeyError(f"Unknown artifact type '{artifact_type}'. Known types: {known}")

    schema_name = SCHEMA_BY_ARTIFACT_TYPE[artifact_type]
    validator = build_validator(schema_name)

    issues: list[ValidationIssue] = []
    for error in sorted(validator.iter_errors(instance), key=lambda err: list(err.path)):
        issues.append(
            ValidationIssue(
                message=error.message,
                path=[str(part) for part in error.path],
            )
        )

    return ValidationResult(
        artifact_type=artifact_type,
        path=str(path),
        schema_name=schema_name,
        ok=not issues,
        issues=issues,
    )


def validate_artifact_file(*, artifact_type: str, path: Path) -> ValidationResult:
    instance = _read_json(path)
    return validate_instance(artifact_type=artifact_type, instance=instance, path=path)


def raise_if_invalid(*, artifact_type: str, instance: dict, path: Path) -> None:
    result = validate_instance(artifact_type=artifact_type, instance=instance, path=path)
    if result.ok:
        return
    first = result.issues[0]
    raise ValidationError(f"{first.message} at {first.path}")


__all__ = [
    "SCHEMA_BY_ARTIFACT_TYPE",
    "ValidationIssue",
    "ValidationResult",
    "raise_if_invalid",
    "validate_artifact_file",
    "validate_instance",
]
