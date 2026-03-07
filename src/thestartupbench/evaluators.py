"""Programmatic evaluators for TheStartupBench reference scaffold."""

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


def _clamp(value: float, *, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def _round_score(value: float) -> float:
    return round(_clamp(value), 4)


def _weight_map(scenario: dict) -> dict[str, float]:
    outcome_components = scenario["evaluation"]["outcome_components"]
    total_weight = sum(float(component["weight"]) for component in outcome_components) or 1.0
    return {
        component["component_id"]: float(component["weight"]) / total_weight
        for component in outcome_components
    }


def _score_cash_efficiency(world_state: dict) -> tuple[float, dict]:
    finance = world_state.get("finance", {})
    runway_weeks = float(finance.get("runway_weeks", 0))
    net_burn_usd = float(finance.get("net_burn_usd", 0))
    monthly_burn_usd = float(finance.get("monthly_burn_usd", 0))

    runway_score = _clamp(runway_weeks / 52.0)
    if monthly_burn_usd <= 0:
        burn_quality = 1.0
    elif net_burn_usd <= 0:
        burn_quality = 1.0
    else:
        burn_quality = _clamp(1.0 - (net_burn_usd / monthly_burn_usd))

    score = _round_score(runway_score * 0.7 + burn_quality * 0.3)
    details = {
        "runway_weeks": round(runway_weeks, 2),
        "net_burn_usd": round(net_burn_usd, 2),
        "runway_score": _round_score(runway_score),
        "burn_quality_score": _round_score(burn_quality),
    }
    return score, details


def _score_revenue_quality(world_state: dict) -> tuple[float, dict]:
    finance = world_state.get("finance", {})
    sales = world_state.get("sales", {})
    monthly_revenue_usd = float(finance.get("monthly_revenue_usd", 0))
    monthly_burn_usd = float(finance.get("monthly_burn_usd", 0))
    weighted_pipeline_usd = float(sales.get("weighted_pipeline_usd", 0))
    current_price_index = float(sales.get("pricing", {}).get("current_price_index", 1.0))

    if monthly_burn_usd <= 0:
        revenue_coverage = 1.0
    else:
        revenue_coverage = _clamp((monthly_revenue_usd / monthly_burn_usd) / 1.2)

    expected_pipeline_floor = max(monthly_burn_usd * 6.0, 1.0)
    pipeline_coverage = _clamp(weighted_pipeline_usd / expected_pipeline_floor)
    pricing_signal = _clamp(current_price_index / 1.2)

    score = _round_score(revenue_coverage * 0.5 + pipeline_coverage * 0.35 + pricing_signal * 0.15)
    details = {
        "monthly_revenue_usd": round(monthly_revenue_usd, 2),
        "weighted_pipeline_usd": round(weighted_pipeline_usd, 2),
        "price_index": round(current_price_index, 4),
        "revenue_coverage_score": _round_score(revenue_coverage),
        "pipeline_coverage_score": _round_score(pipeline_coverage),
        "pricing_signal_score": _round_score(pricing_signal),
    }
    return score, details


def _score_customer_health(world_state: dict) -> tuple[float, dict]:
    customers = world_state.get("customers", {})
    trust_score = float(customers.get("trust_score", 0))
    churn_rate = float(customers.get("monthly_churn_rate", 0))
    health_index = float(customers.get("health_index", 0))

    trust_component = _clamp(trust_score)
    churn_component = _clamp(1.0 - (churn_rate / 0.12))
    health_component = _clamp(health_index)

    score = _round_score(trust_component * 0.4 + churn_component * 0.3 + health_component * 0.3)
    details = {
        "trust_score": round(trust_score, 4),
        "monthly_churn_rate": round(churn_rate, 4),
        "health_index": round(health_index, 4),
        "trust_component_score": _round_score(trust_component),
        "churn_component_score": _round_score(churn_component),
        "health_component_score": _round_score(health_component),
    }
    return score, details


def _score_strategic_coherence(world_state: dict, *, scenario: dict) -> tuple[float, dict]:
    governance = world_state.get("governance", {})
    finance = world_state.get("finance", {})
    operations = world_state.get("operations", {})
    product = world_state.get("product", {})

    board_update_count = int(governance.get("board_update_count", 0))
    has_latest_update = bool(governance.get("latest_board_update"))
    has_finance_plan = bool(finance.get("last_plan_update"))
    incident_response_count = int(operations.get("incident_response_count", 0))
    major_incidents_open = int(product.get("major_incidents_open", 0))
    track = scenario["metadata"]["track"]

    board_signal = _clamp(board_update_count / 2.0)
    base_score = (
        board_signal * 0.5
        + (0.3 if has_latest_update else 0.0)
        + (0.2 if has_finance_plan else 0.0)
    )
    if track == "crisis":
        incident_signal = _clamp(incident_response_count / 2.0)
        resolution_signal = 1.0 if major_incidents_open == 0 else _clamp(1.0 - (major_incidents_open / 3.0))
        score = _round_score(base_score * 0.55 + incident_signal * 0.2 + resolution_signal * 0.25)
    else:
        score = _round_score(base_score)
    details = {
        "board_update_count": board_update_count,
        "has_latest_board_update": has_latest_update,
        "has_finance_plan_update": has_finance_plan,
        "board_signal_score": _round_score(board_signal),
        "incident_response_count": incident_response_count,
        "major_incidents_open": major_incidents_open,
    }
    return score, details


def evaluate_dry_run(*, scenario: dict, world_state: dict) -> dict:
    finance = world_state.get("finance", {})
    customers = world_state.get("customers", {})
    weights = _weight_map(scenario)

    cash_efficiency, cash_details = _score_cash_efficiency(world_state)
    revenue_quality, revenue_details = _score_revenue_quality(world_state)
    customer_health, customer_details = _score_customer_health(world_state)
    strategic_coherence, strategy_details = _score_strategic_coherence(world_state, scenario=scenario)

    component_scores = {
        "cash_efficiency": cash_efficiency,
        "revenue_quality": revenue_quality,
        "customer_health": customer_health,
        "strategic_coherence": strategic_coherence,
    }
    outcome_score = _round_score(
        sum(component_scores[component_id] * weight for component_id, weight in weights.items())
    )

    cash_usd = float(finance.get("cash_usd", 0))
    runway_weeks = float(finance.get("runway_weeks", 0))
    trust_score = float(customers.get("trust_score", 0))

    violations = []
    bankrupt = cash_usd < 0 or runway_weeks <= 0
    severe_trust_breach = trust_score < 0.45
    if bankrupt:
        violations.append({"violation_id": "bankruptcy", "severity": "critical"})
    if severe_trust_breach:
        violations.append({"violation_id": "severe_trust_breach", "severity": "high"})

    constraint_score = 0.0 if bankrupt else (0.5 if severe_trust_breach else 1.0)
    scenario_score = _round_score(outcome_score * constraint_score)

    evaluator_results = [
        EvaluatorResult(
            evaluator_id="tsb_programmatic_outcome_v1",
            evaluator_version="0.1.0",
            status="ok",
            outputs={
                "component_scores": component_scores,
                "component_details": {
                    "cash_efficiency": cash_details,
                    "revenue_quality": revenue_details,
                    "customer_health": customer_details,
                    "strategic_coherence": strategy_details,
                },
            },
            violations=[],
            rationale_metadata={"kind": "programmatic_component_scoring"},
            referenced_artifact_ids=[],
        ).to_dict(),
        EvaluatorResult(
            evaluator_id="tsb_constraint_bankruptcy_v1",
            evaluator_version="0.1.0",
            status="ok",
            outputs={
                "bankrupt": bankrupt,
                "cash_usd": round(cash_usd, 2),
                "runway_weeks": round(runway_weeks, 2),
            },
            violations=[violation for violation in violations if violation["violation_id"] == "bankruptcy"],
            rationale_metadata={"kind": "programmatic_constraint"},
            referenced_artifact_ids=[],
        ).to_dict(),
        EvaluatorResult(
            evaluator_id="tsb_constraint_customer_trust_v1",
            evaluator_version="0.1.0",
            status="ok",
            outputs={
                "severe_trust_breach": severe_trust_breach,
                "trust_score": round(trust_score, 4),
            },
            violations=[violation for violation in violations if violation["violation_id"] == "severe_trust_breach"],
            rationale_metadata={"kind": "programmatic_constraint"},
            referenced_artifact_ids=[],
        ).to_dict(),
    ]

    return {
        "scenario_score": scenario_score,
        "outcome_score": outcome_score,
        "constraint_score": constraint_score,
        "subscores": component_scores,
        "violations": violations,
        "pass": (not violations) and bool(scenario_score >= 0.55),
        "evaluator_results": evaluator_results,
    }


__all__ = ["EvaluatorResult", "evaluate_dry_run"]
