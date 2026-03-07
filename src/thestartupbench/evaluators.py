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
    treasury_concentration = float(finance.get("treasury_concentration", 0))
    liquid_cash_usd = float(finance.get("liquid_cash_usd", finance.get("cash_usd", 0)))
    cash_usd = float(finance.get("cash_usd", 0))
    dilution_index = float(finance.get("dilution_index", 0))

    runway_score = _clamp(runway_weeks / 52.0)
    if monthly_burn_usd <= 0:
        burn_quality = 1.0
    elif net_burn_usd <= 0:
        burn_quality = 1.0
    else:
        burn_quality = _clamp(1.0 - (net_burn_usd / monthly_burn_usd))
    concentration_score = _clamp(1.0 - (treasury_concentration / 1.2))
    if cash_usd <= 0:
        liquidity_score = 0.0
    else:
        liquidity_score = _clamp(liquid_cash_usd / cash_usd)
    dilution_score = _clamp(1.0 - dilution_index)

    score = _round_score(
        runway_score * 0.42
        + burn_quality * 0.23
        + concentration_score * 0.13
        + liquidity_score * 0.12
        + dilution_score * 0.1
    )
    details = {
        "runway_weeks": round(runway_weeks, 2),
        "net_burn_usd": round(net_burn_usd, 2),
        "runway_score": _round_score(runway_score),
        "burn_quality_score": _round_score(burn_quality),
        "treasury_concentration": round(treasury_concentration, 4),
        "concentration_score": _round_score(concentration_score),
        "liquid_cash_usd": round(liquid_cash_usd, 2),
        "liquidity_score": _round_score(liquidity_score),
        "dilution_index": round(dilution_index, 4),
        "dilution_score": _round_score(dilution_score),
    }
    return score, details


def _score_revenue_quality(world_state: dict) -> tuple[float, dict]:
    finance = world_state.get("finance", {})
    sales = world_state.get("sales", {})
    market = world_state.get("market", {})
    customers = world_state.get("customers", {})
    monthly_revenue_usd = float(finance.get("monthly_revenue_usd", 0))
    monthly_burn_usd = float(finance.get("monthly_burn_usd", 0))
    weighted_pipeline_usd = float(sales.get("weighted_pipeline_usd", 0))
    current_price_index = float(sales.get("pricing", {}).get("current_price_index", 1.0))
    demand_index = float(market.get("demand_index", 0.85))
    competitor_pressure = float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.3)))
    segment_mix_index = float(customers.get("segment_mix_index", customers.get("health_index", 0.6)))

    if monthly_burn_usd <= 0:
        revenue_coverage = 1.0
    else:
        revenue_coverage = _clamp((monthly_revenue_usd / monthly_burn_usd) / 1.2)

    expected_pipeline_floor = max(monthly_burn_usd * 6.0, 1.0)
    pipeline_coverage = _clamp(weighted_pipeline_usd / expected_pipeline_floor)
    pricing_signal = _clamp(current_price_index / 1.2)
    demand_signal = _clamp(demand_index / 1.1)
    competitor_signal = _clamp(1.0 - competitor_pressure)
    segment_signal = _clamp(segment_mix_index)

    score = _round_score(
        revenue_coverage * 0.36
        + pipeline_coverage * 0.28
        + pricing_signal * 0.12
        + demand_signal * 0.1
        + competitor_signal * 0.07
        + segment_signal * 0.07
    )
    details = {
        "monthly_revenue_usd": round(monthly_revenue_usd, 2),
        "weighted_pipeline_usd": round(weighted_pipeline_usd, 2),
        "price_index": round(current_price_index, 4),
        "revenue_coverage_score": _round_score(revenue_coverage),
        "pipeline_coverage_score": _round_score(pipeline_coverage),
        "pricing_signal_score": _round_score(pricing_signal),
        "demand_index": round(demand_index, 4),
        "demand_signal_score": _round_score(demand_signal),
        "competitor_pressure_index": round(competitor_pressure, 4),
        "competitor_signal_score": _round_score(competitor_signal),
        "segment_mix_index": round(segment_mix_index, 4),
        "segment_signal_score": _round_score(segment_signal),
    }
    return score, details


def _score_customer_health(world_state: dict) -> tuple[float, dict]:
    customers = world_state.get("customers", {})
    operations = world_state.get("operations", {})
    team = world_state.get("team", {})
    market = world_state.get("market", {})
    trust_score = float(customers.get("trust_score", 0))
    churn_rate = float(customers.get("monthly_churn_rate", 0))
    health_index = float(customers.get("health_index", 0))
    segment_mix_index = float(customers.get("segment_mix_index", health_index))
    support_backlog = float(operations.get("support_backlog", 0))
    morale = float(team.get("morale", 0.7))
    delivery_capacity = float(team.get("delivery_capacity_index", 0.6))
    competitor_pressure = float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.3)))

    trust_component = _clamp(trust_score)
    churn_component = _clamp(1.0 - (churn_rate / 0.12))
    health_component = _clamp(health_index)
    support_component = _clamp(1.0 - (support_backlog / 120.0))
    morale_component = _clamp(morale)
    segment_component = _clamp(segment_mix_index)
    delivery_component = _clamp(delivery_capacity)
    market_component = _clamp(1.0 - competitor_pressure)

    score = _round_score(
        trust_component * 0.24
        + churn_component * 0.2
        + health_component * 0.2
        + support_component * 0.08
        + morale_component * 0.08
        + segment_component * 0.1
        + delivery_component * 0.06
        + market_component * 0.04
    )
    details = {
        "trust_score": round(trust_score, 4),
        "monthly_churn_rate": round(churn_rate, 4),
        "health_index": round(health_index, 4),
        "trust_component_score": _round_score(trust_component),
        "churn_component_score": _round_score(churn_component),
        "health_component_score": _round_score(health_component),
        "support_backlog": round(support_backlog, 2),
        "support_component_score": _round_score(support_component),
        "morale": round(morale, 4),
        "morale_component_score": _round_score(morale_component),
        "segment_mix_index": round(segment_mix_index, 4),
        "segment_component_score": _round_score(segment_component),
        "delivery_capacity_index": round(delivery_capacity, 4),
        "delivery_component_score": _round_score(delivery_component),
        "market_pressure_index": round(competitor_pressure, 4),
        "market_component_score": _round_score(market_component),
    }
    return score, details


def _score_strategic_coherence(world_state: dict, *, scenario: dict) -> tuple[float, dict]:
    governance = world_state.get("governance", {})
    finance = world_state.get("finance", {})
    operations = world_state.get("operations", {})
    product = world_state.get("product", {})
    team = world_state.get("team", {})
    risk = world_state.get("risk", {})
    market = world_state.get("market", {})
    hiring = team.get("hiring", {})

    board_update_count = int(governance.get("board_update_count", 0))
    has_latest_update = bool(governance.get("latest_board_update"))
    has_finance_plan = bool(finance.get("last_plan_update"))
    incident_response_count = int(operations.get("incident_response_count", 0))
    major_incidents_open = int(product.get("major_incidents_open", 0))
    support_actions_taken = int(operations.get("support_actions_taken", 0))
    org_changes_count = int(team.get("org_changes_count", 0))
    legal_responses_count = int(risk.get("legal_responses_count", 0))
    regulatory_pressure = float(risk.get("regulatory_pressure", 0.0))
    runway_weeks = float(finance.get("runway_weeks", 0.0))
    has_raise_plan = bool(finance.get("last_raise_plan"))
    financing_events_count = int(finance.get("financing_events_count", 0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))
    market_reads_count = int(market.get("market_reads_count", 0))
    hiring_actions_count = int(hiring.get("hiring_actions_count", 0))
    open_roles = int(hiring.get("open_roles", team.get("open_roles", 0)))
    hiring_capacity_index = float(hiring.get("hiring_capacity_index", 0.0))
    track = scenario["metadata"]["track"]

    board_signal = _clamp(board_update_count / 2.0)
    base_score = (
        board_signal * 0.4
        + (0.25 if has_latest_update else 0.0)
        + (0.15 if has_finance_plan else 0.0)
    )
    if track == "crisis":
        incident_signal = _clamp(incident_response_count / 2.0)
        resolution_signal = 1.0 if major_incidents_open == 0 else _clamp(1.0 - (major_incidents_open / 3.0))
        support_signal = _clamp(support_actions_taken / 2.0)
        legal_signal = _clamp(legal_responses_count / 2.0)
        compliance_signal = _clamp(1.0 - regulatory_pressure)
        fundraising_signal = 1.0 if runway_weeks >= 18 else (_clamp(financing_events_count / 1.0) if has_raise_plan else 0.0)
        score = _round_score(
            base_score * 0.35
            + incident_signal * 0.15
            + resolution_signal * 0.15
            + support_signal * 0.1
            + legal_signal * 0.1
            + compliance_signal * 0.1
            + fundraising_signal * 0.05
        )
    else:
        org_signal = _clamp(org_changes_count / 1.0)
        compliance_signal = _clamp(1.0 - regulatory_pressure)
        fundraising_signal = 1.0 if runway_weeks >= 20 else (_clamp(financing_events_count / 1.0) if has_raise_plan else 0.0)
        market_signal = _clamp(market_reads_count / 1.0)
        hiring_signal = (
            1.0
            if open_roles == 0
            else _clamp((hiring_actions_count / 2.0) * 0.6 + hiring_capacity_index * 0.4)
        )
        if track == "gtm":
            score = _round_score(
                base_score * 0.38
                + compliance_signal * 0.12
                + fundraising_signal * 0.12
                + market_signal * 0.2
                + hiring_signal * 0.08
                + _clamp(1.0 - float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.3)))) * 0.1
            )
        elif track == "people":
            score = _round_score(
                base_score * 0.28
                + org_signal * 0.18
                + hiring_signal * 0.22
                + compliance_signal * 0.08
                + fundraising_signal * 0.08
                + _clamp(float(team.get("delivery_capacity_index", 0.6))) * 0.16
            )
        elif track == "finance":
            score = _round_score(
                base_score * 0.3
                + compliance_signal * 0.12
                + fundraising_signal * 0.28
                + market_signal * 0.12
                + hiring_signal * 0.06
                + _clamp(1.0 - financing_pressure) * 0.12
            )
        else:
            score = _round_score(
                base_score * 0.43
                + org_signal * 0.1
                + compliance_signal * 0.13
                + fundraising_signal * 0.16
                + market_signal * 0.1
                + hiring_signal * 0.08
            )
    details = {
        "board_update_count": board_update_count,
        "has_latest_board_update": has_latest_update,
        "has_finance_plan_update": has_finance_plan,
        "has_raise_plan": has_raise_plan,
        "board_signal_score": _round_score(board_signal),
        "incident_response_count": incident_response_count,
        "major_incidents_open": major_incidents_open,
        "support_actions_taken": support_actions_taken,
        "org_changes_count": org_changes_count,
        "legal_responses_count": legal_responses_count,
        "regulatory_pressure": round(regulatory_pressure, 4),
        "financing_events_count": financing_events_count,
        "financing_pressure": round(financing_pressure, 4),
        "market_reads_count": market_reads_count,
        "hiring_actions_count": hiring_actions_count,
        "open_roles": open_roles,
        "hiring_capacity_index": round(hiring_capacity_index, 4),
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
    liquid_cash_usd = float(finance.get("liquid_cash_usd", cash_usd))
    trust_score = float(customers.get("trust_score", 0))
    regulatory_pressure = float(world_state.get("risk", {}).get("regulatory_pressure", 0.0))
    financing_pressure = float(world_state.get("risk", {}).get("financing_pressure", 0.0))

    violations = []
    bankrupt = cash_usd < 0 or liquid_cash_usd <= 0 or runway_weeks <= 0
    severe_trust_breach = trust_score < 0.45
    severe_compliance_breach = regulatory_pressure > 0.9
    severe_financing_failure = runway_weeks < 8 and financing_pressure > 0.8
    if bankrupt:
        violations.append({"violation_id": "bankruptcy", "severity": "critical"})
    if severe_trust_breach:
        violations.append({"violation_id": "severe_trust_breach", "severity": "high"})
    if severe_compliance_breach:
        violations.append({"violation_id": "severe_compliance_breach", "severity": "high"})
    if severe_financing_failure:
        violations.append({"violation_id": "severe_financing_failure", "severity": "high"})

    if bankrupt:
        constraint_score = 0.0
    elif sum(int(flag) for flag in (severe_trust_breach, severe_compliance_breach, severe_financing_failure)) >= 2:
        constraint_score = 0.35
    elif severe_trust_breach or severe_compliance_breach or severe_financing_failure:
        constraint_score = 0.5
    else:
        constraint_score = 1.0
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
                "liquid_cash_usd": round(liquid_cash_usd, 2),
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
        EvaluatorResult(
            evaluator_id="tsb_constraint_compliance_v1",
            evaluator_version="0.1.0",
            status="ok",
            outputs={
                "severe_compliance_breach": severe_compliance_breach,
                "regulatory_pressure": round(regulatory_pressure, 4),
            },
            violations=[violation for violation in violations if violation["violation_id"] == "severe_compliance_breach"],
            rationale_metadata={"kind": "programmatic_constraint"},
            referenced_artifact_ids=[],
        ).to_dict(),
        EvaluatorResult(
            evaluator_id="tsb_constraint_financing_v1",
            evaluator_version="0.1.0",
            status="ok",
            outputs={
                "severe_financing_failure": severe_financing_failure,
                "financing_pressure": round(financing_pressure, 4),
                "runway_weeks": round(runway_weeks, 2),
            },
            violations=[violation for violation in violations if violation["violation_id"] == "severe_financing_failure"],
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
