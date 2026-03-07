"""Minimal evaluator registry and dry-run evaluators."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluatorResult:
    evaluator_id: str
    evaluator_version: str
    status: str
    outputs: dict
    violations: list[dict]
    rationale_metadata: dict
    referenced_artifact_ids: list[str]

    def to_dict(self) -> dict:
        return {
            "evaluator_id": self.evaluator_id,
            "evaluator_version": self.evaluator_version,
            "status": self.status,
            "outputs": self.outputs,
            "violations": self.violations,
            "rationale_metadata": self.rationale_metadata,
            "referenced_artifact_ids": self.referenced_artifact_ids,
        }


def evaluate_dry_run(*, scenario: dict, world_state: dict) -> dict:
    cash_usd = float(world_state.get("finance", {}).get("cash_usd", 0))
    bankrupt = cash_usd < 0
    violations = []
    if bankrupt:
        violations.append({"violation_id": "bankruptcy", "severity": "critical"})

    component_scores = {
        component["component_id"]: 0.0
        for component in scenario["evaluation"]["outcome_components"]
    }
    outcome_score = 0.0
    constraint_score = 0.0 if bankrupt else 1.0
    scenario_score = outcome_score * constraint_score

    evaluator_results = [
        EvaluatorResult(
            evaluator_id="dry_run_constraint_bankruptcy",
            evaluator_version="0.1.0",
            status="ok",
            outputs={"bankrupt": bankrupt},
            violations=violations,
            rationale_metadata={},
            referenced_artifact_ids=[],
        ).to_dict()
    ]

    return {
        "scenario_score": scenario_score,
        "outcome_score": outcome_score,
        "constraint_score": constraint_score,
        "subscores": component_scores,
        "violations": violations,
        "pass": (not bankrupt) and bool(scenario_score > 0),
        "evaluator_results": evaluator_results,
    }


__all__ = ["EvaluatorResult", "evaluate_dry_run"]

