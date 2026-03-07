"""Authoring-time lint checks for TSB scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .scenario_loader import load_scenario


@dataclass(frozen=True)
class LintIssue:
    message: str
    path: list[str]

    def to_dict(self) -> dict:
        return {"message": self.message, "path": self.path}


@dataclass(frozen=True)
class LintResult:
    ok: bool
    issues: list[LintIssue]

    def to_dict(self) -> dict:
        return {"ok": self.ok, "issues": [issue.to_dict() for issue in self.issues]}


def lint_scenario_instance(scenario: dict) -> LintResult:
    issues: list[LintIssue] = []
    event_model = scenario.get("event_model", {})
    primitive_catalog = event_model.get("primitive_catalog", {})
    scheduled_events = event_model.get("scheduled_events", [])

    seen_event_ids: set[str] = set()
    for index, event in enumerate(scheduled_events):
        event_id = event.get("event_id")
        path_prefix = ["event_model", "scheduled_events", str(index)]
        if event_id in seen_event_ids:
            issues.append(LintIssue(message=f"Duplicate event_id '{event_id}'", path=path_prefix + ["event_id"]))
        elif isinstance(event_id, str):
            seen_event_ids.add(event_id)

        at_turn = event.get("at_turn")
        if not isinstance(at_turn, int) or at_turn < 1:
            issues.append(LintIssue(message="Scheduled events must use at_turn >= 1", path=path_prefix + ["at_turn"]))

        primitive_id = event.get("primitive_id")
        if primitive_id and primitive_id not in primitive_catalog:
            issues.append(
                LintIssue(
                    message=f"Unknown primitive_id '{primitive_id}'",
                    path=path_prefix + ["primitive_id"],
                )
            )

        if "primitive_id" not in event and "effects" not in event and "operations" not in event:
            issues.append(
                LintIssue(
                    message="Scheduled event must define primitive_id, effects, or operations",
                    path=path_prefix,
                )
            )

    tools = scenario.get("tools", [])
    if len(tools) != len(set(tools)):
        issues.append(LintIssue(message="Scenario tools must be unique", path=["tools"]))

    return LintResult(ok=not issues, issues=issues)


def lint_scenario_file(path: Path) -> LintResult:
    return lint_scenario_instance(load_scenario(path))


__all__ = ["LintIssue", "LintResult", "lint_scenario_file", "lint_scenario_instance"]
