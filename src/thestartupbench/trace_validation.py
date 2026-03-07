"""Trace integrity validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class IntegrityIssue:
    severity: str
    message: str
    path: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class TraceIntegrityResult:
    ok: bool
    issues: list[IntegrityIssue]

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_trace_integrity(trace: dict) -> TraceIntegrityResult:
    issues: list[IntegrityIssue] = []

    turns = trace.get("turns", [])
    expected_turn_index = 0
    previous_after = None
    for idx, turn in enumerate(turns):
        turn_index = turn.get("turn_index")
        if turn_index != expected_turn_index:
            issues.append(
                IntegrityIssue(
                    severity="error",
                    message=f"Turn index {turn_index} does not match expected {expected_turn_index}",
                    path=["turns", str(idx), "turn_index"],
                )
            )
        expected_turn_index += 1

        before = _parse_time(turn["sim_time_before"])
        after = _parse_time(turn["sim_time_after"])
        if after < before:
            issues.append(
                IntegrityIssue(
                    severity="error",
                    message="sim_time_after precedes sim_time_before",
                    path=["turns", str(idx)],
                )
            )
        if previous_after is not None and before < previous_after:
            issues.append(
                IntegrityIssue(
                    severity="error",
                    message="Turn sim time moved backwards relative to prior turn",
                    path=["turns", str(idx), "sim_time_before"],
                )
            )
        previous_after = after

        actions = turn.get("actions", [])
        for action_idx, action in enumerate(actions):
            request_id = action.get("request_id")
            response = action.get("response", {})
            if response and response.get("request_id") != request_id:
                issues.append(
                    IntegrityIssue(
                        severity="error",
                        message="Tool response request_id does not match action request_id",
                        path=["turns", str(idx), "actions", str(action_idx)],
                    )
                )

    snapshots = trace.get("state_snapshots", [])
    if len(snapshots) < 2:
        issues.append(
            IntegrityIssue(
                severity="error",
                message="Trace must contain at least initial and final state snapshots",
                path=["state_snapshots"],
            )
        )

    return TraceIntegrityResult(ok=not issues, issues=issues)


__all__ = ["IntegrityIssue", "TraceIntegrityResult", "validate_trace_integrity"]

