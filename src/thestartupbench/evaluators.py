"""Programmatic evaluators for TheStartupBench reference scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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


def _score_product_health(world_state: dict) -> tuple[float, dict]:
    product = world_state.get("product", {})
    operations = world_state.get("operations", {})
    growth = world_state.get("growth", {})
    customers = world_state.get("customers", {})

    onboarding_quality = float(product.get("onboarding_quality", 0.5))
    major_incidents_open = int(product.get("major_incidents_open", 0))
    roadmap_items = float(product.get("roadmap_items", 0))
    support_sla_breach_risk = float(operations.get("support_sla_breach_risk", 0.0))
    activation_index = float(growth.get("activation_index", onboarding_quality))
    trust_score = float(customers.get("trust_score", 0.7))

    onboarding_component = _clamp(onboarding_quality)
    reliability_component = 1.0 if major_incidents_open == 0 else _clamp(1.0 - (major_incidents_open / 3.0))
    roadmap_focus_component = _clamp(1.0 - max(0.0, roadmap_items - 4.0) / 8.0)
    support_component = _clamp(1.0 - support_sla_breach_risk)
    activation_component = _clamp(activation_index)
    trust_component = _clamp(trust_score)

    score = _round_score(
        onboarding_component * 0.26
        + reliability_component * 0.24
        + roadmap_focus_component * 0.12
        + support_component * 0.14
        + activation_component * 0.16
        + trust_component * 0.08
    )
    details = {
        "onboarding_quality": round(onboarding_quality, 4),
        "major_incidents_open": major_incidents_open,
        "roadmap_items": round(roadmap_items, 2),
        "support_sla_breach_risk": round(support_sla_breach_risk, 4),
        "activation_index": round(activation_index, 4),
        "trust_score": round(trust_score, 4),
        "onboarding_component_score": _round_score(onboarding_component),
        "reliability_component_score": _round_score(reliability_component),
        "roadmap_focus_component_score": _round_score(roadmap_focus_component),
        "support_component_score": _round_score(support_component),
        "activation_component_score": _round_score(activation_component),
        "trust_component_score": _round_score(trust_component),
    }
    return score, details


def _score_team_health(world_state: dict) -> tuple[float, dict]:
    team = world_state.get("team", {})
    hiring = team.get("hiring", {})

    morale = float(team.get("morale", 0.7))
    attrition_risk = float(team.get("attrition_risk", 0.2))
    bandwidth_load = float(team.get("bandwidth_load", 0.7))
    delivery_capacity = float(team.get("delivery_capacity_index", 0.6))
    hiring_capacity = float(hiring.get("hiring_capacity_index", 0.0))
    open_roles = int(hiring.get("open_roles", team.get("open_roles", 0)))
    headcount = int(team.get("headcount", 0))

    morale_component = _clamp(morale)
    attrition_component = _clamp(1.0 - attrition_risk)
    bandwidth_component = _clamp(1.0 - (bandwidth_load / 1.2))
    delivery_component = _clamp(delivery_capacity)
    hiring_component = _clamp(hiring_capacity)
    open_role_burden = _clamp(1.0 - (open_roles / max(headcount + open_roles, 1)))

    score = _round_score(
        morale_component * 0.28
        + attrition_component * 0.24
        + bandwidth_component * 0.18
        + delivery_component * 0.18
        + hiring_component * 0.07
        + open_role_burden * 0.05
    )
    details = {
        "morale": round(morale, 4),
        "attrition_risk": round(attrition_risk, 4),
        "bandwidth_load": round(bandwidth_load, 4),
        "delivery_capacity_index": round(delivery_capacity, 4),
        "hiring_capacity_index": round(hiring_capacity, 4),
        "open_roles": open_roles,
        "headcount": headcount,
        "morale_component_score": _round_score(morale_component),
        "attrition_component_score": _round_score(attrition_component),
        "bandwidth_component_score": _round_score(bandwidth_component),
        "delivery_component_score": _round_score(delivery_component),
        "hiring_component_score": _round_score(hiring_component),
        "open_role_burden_score": _round_score(open_role_burden),
    }
    return score, details


def _score_risk_management(world_state: dict) -> tuple[float, dict]:
    finance = world_state.get("finance", {})
    risk = world_state.get("risk", {})
    product = world_state.get("product", {})
    operations = world_state.get("operations", {})

    financing_pressure = float(risk.get("financing_pressure", 0.0))
    regulatory_pressure = float(risk.get("regulatory_pressure", 0.0))
    counterparty_risk = float(risk.get("counterparty_risk", 0.0))
    treasury_concentration = float(finance.get("treasury_concentration", 0.0))
    major_incidents_open = int(product.get("major_incidents_open", 0))
    active_legal_matters = int(risk.get("active_legal_matters", 0))
    support_sla_breach_risk = float(operations.get("support_sla_breach_risk", 0.0))

    financing_component = _clamp(1.0 - financing_pressure)
    regulatory_component = _clamp(1.0 - regulatory_pressure)
    counterparty_component = _clamp(1.0 - counterparty_risk)
    concentration_component = _clamp(1.0 - (treasury_concentration / 1.2))
    incident_component = 1.0 if major_incidents_open == 0 else _clamp(1.0 - (major_incidents_open / 3.0))
    legal_component = _clamp(1.0 - (active_legal_matters / 4.0))
    support_component = _clamp(1.0 - support_sla_breach_risk)

    score = _round_score(
        financing_component * 0.26
        + regulatory_component * 0.22
        + counterparty_component * 0.16
        + concentration_component * 0.12
        + incident_component * 0.12
        + legal_component * 0.06
        + support_component * 0.06
    )
    details = {
        "financing_pressure": round(financing_pressure, 4),
        "regulatory_pressure": round(regulatory_pressure, 4),
        "counterparty_risk": round(counterparty_risk, 4),
        "treasury_concentration": round(treasury_concentration, 4),
        "major_incidents_open": major_incidents_open,
        "active_legal_matters": active_legal_matters,
        "support_sla_breach_risk": round(support_sla_breach_risk, 4),
        "financing_component_score": _round_score(financing_component),
        "regulatory_component_score": _round_score(regulatory_component),
        "counterparty_component_score": _round_score(counterparty_component),
        "concentration_component_score": _round_score(concentration_component),
        "incident_component_score": _round_score(incident_component),
        "legal_component_score": _round_score(legal_component),
        "support_component_score": _round_score(support_component),
    }
    return score, details


def _extract_alerts(turn: dict) -> list[str]:
    alerts: list[str] = []
    for action in turn.get("actions", []):
        if action.get("tool_name") != "metrics.report":
            continue
        report = action.get("response", {}).get("result", {}).get("report", {})
        raw_alerts = report.get("alerts", [])
        if isinstance(raw_alerts, list):
            alerts.extend(str(item) for item in raw_alerts)
    return alerts


def _extract_metrics_report(turn: dict) -> dict:
    for action in turn.get("actions", []):
        if action.get("tool_name") != "metrics.report":
            continue
        report = action.get("response", {}).get("result", {}).get("report", {})
        if isinstance(report, dict):
            return report
    return {}


def _extract_board_update_summaries(turns: list[dict]) -> list[str]:
    summaries: list[str] = []
    for turn in turns:
        for action in turn.get("actions", []):
            if action.get("tool_name") != "board.update":
                continue
            arguments = action.get("arguments", {})
            summary = arguments.get("summary")
            if isinstance(summary, str) and summary.strip():
                summaries.append(summary.strip())
    return summaries


def _behavioral_penalty(
    *,
    world_state: dict,
    trace_evidence: dict[str, Any] | None,
    scenario: dict,
) -> tuple[float, dict]:
    track = scenario["metadata"]["track"]
    if trace_evidence is None:
        return 0.0, {
            "behavioral_penalty": 0.0,
            "adverse_event_count": 0,
            "unanswered_adverse_events": 0,
            "support_alert_turn_count": 0,
            "support_actions_after_adverse_event": 0,
            "trust_decline": 0.0,
            "soft_demand_alert_turn_count": 0,
            "demand_decline": 0.0,
            "pipeline_decline_ratio": 0.0,
            "hiring_response_count": 0,
            "finance_response_count": 0,
            "unresolved_hiring_pressure": False,
            "rigid_loop_penalty_applied": False,
        }

    turns = trace_evidence.get("turns", [])
    if not isinstance(turns, list) or not turns:
        return 0.0, {
            "behavioral_penalty": 0.0,
            "adverse_event_count": 0,
            "unanswered_adverse_events": 0,
            "support_alert_turn_count": 0,
            "support_actions_after_adverse_event": 0,
            "trust_decline": 0.0,
            "soft_demand_alert_turn_count": 0,
            "demand_decline": 0.0,
            "pipeline_decline_ratio": 0.0,
            "hiring_response_count": 0,
            "finance_response_count": 0,
            "unresolved_hiring_pressure": False,
            "rigid_loop_penalty_applied": False,
        }

    normalized_sequences = [
        tuple(str(action.get("tool_name", "")) for action in turn.get("actions", []))
        for turn in turns
    ]
    dominant_sequence_count = max((normalized_sequences.count(sequence) for sequence in set(normalized_sequences)), default=0)
    rigid_loop_penalty_applied = dominant_sequence_count >= 3 and len(set(normalized_sequences)) <= 2

    if track == "gtm":
        adverse_event_types = {"pricing_backlash", "customer_backlash", "trust_backlash", "retention_shock"}
        substantive_response_tools = {
            "ops.support.resolve",
            "sales.pricing.propose",
            "product.roadmap.write",
            "people.hiring.update",
            "finance.plan.write",
            "notes.write",
        }
        adverse_turn_indices = [
            index
            for index, turn in enumerate(turns)
            if any(event.get("event_type") in adverse_event_types for event in turn.get("events", []))
        ]
        response_tools_after_adverse_event: list[str] = []
        if adverse_turn_indices:
            first_adverse_turn = adverse_turn_indices[0]
            for turn in turns[first_adverse_turn + 1 :]:
                for action in turn.get("actions", []):
                    response_tools_after_adverse_event.append(str(action.get("tool_name", "")))
        support_actions_after_adverse_event = sum(
            1 for tool_name in response_tools_after_adverse_event if tool_name == "ops.support.resolve"
        )
        unanswered_adverse_events = (
            len(adverse_turn_indices)
            if adverse_turn_indices and not any(tool in substantive_response_tools for tool in response_tools_after_adverse_event)
            else 0
        )

        support_alert_turn_count = sum(1 for turn in turns if "support_backlog_above_50" in _extract_alerts(turn))
        has_any_support_action = any(
            action.get("tool_name") == "ops.support.resolve"
            for turn in turns
            for action in turn.get("actions", [])
        )
        first_report = _extract_metrics_report(turns[0])
        initial_trust = float(first_report.get("customers", {}).get("trust_score", 0.0) or 0.0)
        final_trust = float(world_state.get("customers", {}).get("trust_score", 0.0))
        trust_decline = max(0.0, initial_trust - final_trust)

        penalty = 0.0
        if unanswered_adverse_events > 0:
            penalty += 0.4
        if support_alert_turn_count >= 2 and not has_any_support_action:
            penalty += 0.15
        if trust_decline >= 0.1 and unanswered_adverse_events > 0:
            penalty += 0.1
        if rigid_loop_penalty_applied and unanswered_adverse_events > 0:
            penalty += 0.05

        penalty = _round_score(penalty)
        return penalty, {
            "behavioral_penalty": penalty,
            "adverse_event_count": len(adverse_turn_indices),
            "unanswered_adverse_events": unanswered_adverse_events,
            "support_alert_turn_count": support_alert_turn_count,
            "support_actions_after_adverse_event": support_actions_after_adverse_event,
            "trust_decline": round(trust_decline, 4),
            "soft_demand_alert_turn_count": 0,
            "demand_decline": 0.0,
            "pipeline_decline_ratio": 0.0,
            "hiring_response_count": 0,
            "finance_response_count": 0,
            "unresolved_hiring_pressure": False,
            "rigid_loop_penalty_applied": rigid_loop_penalty_applied,
        }

    if track == "people":
        soft_demand_alert_turn_count = sum(1 for turn in turns if "market_demand_softening" in _extract_alerts(turn))
        first_report = _extract_metrics_report(turns[0])
        initial_demand = float(first_report.get("market", {}).get("demand_index", 0.0) or 0.0)
        initial_pipeline = float(first_report.get("sales", {}).get("weighted_pipeline_usd", 0.0) or 0.0)
        final_demand = float(world_state.get("market", {}).get("demand_index", 0.0))
        final_pipeline = float(world_state.get("sales", {}).get("weighted_pipeline_usd", 0.0))
        demand_decline = max(0.0, initial_demand - final_demand)
        if initial_pipeline <= 0:
            pipeline_decline_ratio = 0.0
        else:
            pipeline_decline_ratio = max(0.0, (initial_pipeline - final_pipeline) / initial_pipeline)

        hiring_response_tools = {"people.hiring.update", "people.org.adjust"}
        finance_response_tools = {"finance.plan.write", "finance.raise.propose"}
        hiring_response_count = sum(
            1
            for turn in turns
            for action in turn.get("actions", [])
            if action.get("tool_name") in hiring_response_tools
        )
        finance_response_count = sum(
            1
            for turn in turns
            for action in turn.get("actions", [])
            if action.get("tool_name") in finance_response_tools
        )
        open_roles = int(world_state.get("team", {}).get("hiring", {}).get("open_roles", 0))
        financing_pressure = float(world_state.get("risk", {}).get("financing_pressure", 0.0))
        unresolved_hiring_pressure = open_roles > 0 and financing_pressure >= 0.55
        no_response = hiring_response_count == 0 and finance_response_count == 0

        penalty = 0.0
        if soft_demand_alert_turn_count >= 3 and unresolved_hiring_pressure and hiring_response_count == 0:
            penalty += 0.02
        if soft_demand_alert_turn_count >= 3 and financing_pressure >= 0.55 and finance_response_count == 0:
            penalty += 0.02
        if demand_decline >= 0.03 and pipeline_decline_ratio >= 0.2 and no_response:
            penalty += 0.02
        if rigid_loop_penalty_applied and no_response and soft_demand_alert_turn_count >= 3:
            penalty += 0.01

        penalty = _round_score(penalty)
        return penalty, {
            "behavioral_penalty": penalty,
            "adverse_event_count": 0,
            "unanswered_adverse_events": 0,
            "support_alert_turn_count": 0,
            "support_actions_after_adverse_event": 0,
            "trust_decline": 0.0,
            "soft_demand_alert_turn_count": soft_demand_alert_turn_count,
            "demand_decline": round(demand_decline, 4),
            "pipeline_decline_ratio": round(pipeline_decline_ratio, 4),
            "hiring_response_count": hiring_response_count,
            "finance_response_count": finance_response_count,
            "unresolved_hiring_pressure": unresolved_hiring_pressure,
            "rigid_loop_penalty_applied": rigid_loop_penalty_applied,
        }

    if track == "board":
        governance_event_types = {"board_growth_push", "narrative_pressure", "board_pressure", "growth_ultimatum"}
        customer_event_types = {"customer_pushback", "customer_reference_loss", "renewal_escalation"}

        governance_turn_indices = [
            index
            for index, turn in enumerate(turns)
            if any(event.get("event_type") in governance_event_types for event in turn.get("events", []))
        ]
        customer_turn_indices = [
            index
            for index, turn in enumerate(turns)
            if any(event.get("event_type") in customer_event_types for event in turn.get("events", []))
        ]

        board_update_after_governance_count = 0
        support_follow_up_count = 0
        incident_follow_up_count = 0
        finance_follow_up_count = 0
        market_read_count = 0
        board_read_count = 0
        if governance_turn_indices or customer_turn_indices:
            first_follow_up_turn = min(governance_turn_indices + customer_turn_indices)
            for turn in turns[first_follow_up_turn + 1 :]:
                for action in turn.get("actions", []):
                    tool_name = str(action.get("tool_name", ""))
                    if tool_name == "board.read":
                        board_read_count += 1
                    if tool_name == "board.update":
                        board_update_after_governance_count += 1
                    elif tool_name == "ops.support.resolve":
                        support_follow_up_count += 1
                    elif tool_name in {"ops.incident.respond", "product.roadmap.write"}:
                        incident_follow_up_count += 1
                    elif tool_name in {"finance.plan.write", "finance.raise.propose"}:
                        finance_follow_up_count += 1
                    elif tool_name == "research.market.read":
                        market_read_count += 1

        board_summaries = _extract_board_update_summaries(turns)
        unique_board_summaries = len(set(board_summaries))
        repeated_board_update = len(board_summaries) >= 2 and unique_board_summaries <= 1

        first_report = _extract_metrics_report(turns[0])
        initial_trust = float(first_report.get("customers", {}).get("trust_score", 0.0) or 0.0)
        final_trust = float(world_state.get("customers", {}).get("trust_score", 0.0))
        trust_decline = max(0.0, initial_trust - final_trust)
        final_major_incidents_open = int(world_state.get("product", {}).get("major_incidents_open", 0))
        final_support_backlog = float(world_state.get("operations", {}).get("support_backlog", 0.0))
        final_financing_pressure = float(world_state.get("risk", {}).get("financing_pressure", 0.0))

        penalty = 0.0
        if governance_turn_indices and board_update_after_governance_count == 0:
            penalty += 0.06
        if governance_turn_indices and board_read_count == 0:
            penalty += 0.03
        if customer_turn_indices and support_follow_up_count == 0:
            penalty += 0.05
        if repeated_board_update:
            penalty += 0.04
        if final_major_incidents_open > 0:
            penalty += 0.04
        if final_major_incidents_open > 0 and incident_follow_up_count == 0:
            penalty += 0.04
        if trust_decline >= 0.04 and customer_turn_indices and support_follow_up_count == 0:
            penalty += 0.03
        if final_financing_pressure >= 0.75 and finance_follow_up_count == 0:
            penalty += 0.03
        if market_read_count == 0:
            penalty += 0.02
        if rigid_loop_penalty_applied and repeated_board_update:
            penalty += 0.02
        if final_support_backlog >= 26 and customer_turn_indices and support_follow_up_count == 0:
            penalty += 0.02

        penalty = _round_score(penalty)
        return penalty, {
            "behavioral_penalty": penalty,
            "adverse_event_count": len(governance_turn_indices) + len(customer_turn_indices),
            "unanswered_adverse_events": 0,
            "support_alert_turn_count": 0,
            "support_actions_after_adverse_event": support_follow_up_count,
            "trust_decline": round(trust_decline, 4),
            "soft_demand_alert_turn_count": 0,
            "demand_decline": 0.0,
            "pipeline_decline_ratio": 0.0,
            "hiring_response_count": 0,
            "finance_response_count": finance_follow_up_count,
            "unresolved_hiring_pressure": False,
            "board_event_count": len(governance_turn_indices),
            "customer_event_count": len(customer_turn_indices),
            "board_update_after_governance_count": board_update_after_governance_count,
            "support_follow_up_count": support_follow_up_count,
            "incident_follow_up_count": incident_follow_up_count,
            "board_read_count": board_read_count,
            "market_read_count": market_read_count,
            "repeated_board_update": repeated_board_update,
            "unique_board_summaries": unique_board_summaries,
            "final_major_incidents_open": final_major_incidents_open,
            "final_support_backlog": round(final_support_backlog, 2),
            "final_financing_pressure": round(final_financing_pressure, 4),
            "rigid_loop_penalty_applied": rigid_loop_penalty_applied,
        }

    if track == "crisis":
        security_event_types = {"trust_shock", "security_backlash", "privacy_backlash"}
        liquidity_event_types = {"bank_freeze", "treasury_freeze", "counterparty_freeze"}
        crisis_turn_indices = [
            index
            for index, turn in enumerate(turns)
            if any(
                event.get("event_type") in security_event_types.union(liquidity_event_types)
                for event in turn.get("events", [])
            )
        ]
        first_crisis_turn = crisis_turn_indices[0] if crisis_turn_indices else None
        security_crisis_detected = any(
            event.get("event_type") in security_event_types
            for turn in turns
            for event in turn.get("events", [])
        )
        liquidity_crisis_detected = any(
            event.get("event_type") in liquidity_event_types
            for turn in turns
            for event in turn.get("events", [])
        )

        product_response_count = sum(
            1
            for turn in turns
            for action in turn.get("actions", [])
            if action.get("tool_name") == "product.roadmap.write"
        )
        board_update_after_crisis_count = 0
        legal_follow_up_count = 0
        finance_follow_up_count = 0
        pipeline_actions_during_trust_crisis = 0
        pipeline_actions_during_liquidity_crisis = 0
        market_read_count = 0
        if first_crisis_turn is not None:
            for turn in turns[first_crisis_turn + 1 :]:
                report = _extract_metrics_report(turn)
                current_trust = float(report.get("customers", {}).get("trust_score", 0.0) or 0.0)
                current_financing_pressure = float(report.get("risk", {}).get("financing_pressure", 0.0) or 0.0)
                for action in turn.get("actions", []):
                    tool_name = str(action.get("tool_name", ""))
                    if tool_name == "board.update":
                        board_update_after_crisis_count += 1
                    elif tool_name == "legal.compliance.respond":
                        legal_follow_up_count += 1
                    elif tool_name in {"finance.plan.write", "finance.raise.propose", "finance.treasury.rebalance"}:
                        finance_follow_up_count += 1
                    elif tool_name == "research.market.read":
                        market_read_count += 1
                    elif tool_name == "sales.pipeline.update" and current_trust <= 0.62:
                        pipeline_actions_during_trust_crisis += 1
                    elif tool_name == "sales.pipeline.update" and current_financing_pressure >= 0.8:
                        pipeline_actions_during_liquidity_crisis += 1

        first_report = _extract_metrics_report(turns[0])
        initial_trust = float(first_report.get("customers", {}).get("trust_score", 0.0) or 0.0)
        final_trust = float(world_state.get("customers", {}).get("trust_score", 0.0))
        trust_recovery = max(0.0, final_trust - initial_trust)
        final_regulatory_pressure = float(world_state.get("risk", {}).get("regulatory_pressure", 0.0))
        final_financing_pressure = float(world_state.get("risk", {}).get("financing_pressure", 0.0))
        final_counterparty_risk = float(world_state.get("risk", {}).get("counterparty_risk", 0.0))
        finance_state = world_state.get("finance", {})
        monthly_burn_usd = float(finance_state.get("monthly_burn_usd", 0.0))
        liquid_cash_usd = float(finance_state.get("liquid_cash_usd", finance_state.get("cash_usd", 0.0)))
        liquid_cash_months = liquid_cash_usd / monthly_burn_usd if monthly_burn_usd > 0 else 0.0

        penalty = 0.0
        if security_crisis_detected and product_response_count == 0:
            penalty += 0.18
        if first_crisis_turn is not None and board_update_after_crisis_count == 0:
            penalty += 0.12
        if security_crisis_detected and final_regulatory_pressure >= 0.5 and legal_follow_up_count == 0:
            penalty += 0.08
        if security_crisis_detected and pipeline_actions_during_trust_crisis >= 1 and product_response_count == 0:
            penalty += 0.08
        if security_crisis_detected and market_read_count == 0:
            penalty += 0.04
        if rigid_loop_penalty_applied and first_crisis_turn is not None:
            penalty += 0.04
        if security_crisis_detected and trust_recovery < 0.12 and product_response_count == 0:
            penalty += 0.04
        if liquidity_crisis_detected and finance_follow_up_count == 0:
            penalty += 0.12
        if liquidity_crisis_detected and final_financing_pressure >= 0.85 and finance_follow_up_count == 0:
            penalty += 0.08
        if liquidity_crisis_detected and final_counterparty_risk >= 0.9 and finance_follow_up_count == 0:
            penalty += 0.05
        if liquidity_crisis_detected and liquid_cash_months <= 4.0 and finance_follow_up_count == 0:
            penalty += 0.04
        if liquidity_crisis_detected and pipeline_actions_during_liquidity_crisis >= 1 and finance_follow_up_count == 0:
            penalty += 0.03

        penalty = _round_score(penalty)
        return penalty, {
            "behavioral_penalty": penalty,
            "adverse_event_count": len(crisis_turn_indices),
            "unanswered_adverse_events": 0,
            "support_alert_turn_count": 0,
            "support_actions_after_adverse_event": 0,
            "trust_decline": 0.0,
            "soft_demand_alert_turn_count": 0,
            "demand_decline": 0.0,
            "pipeline_decline_ratio": 0.0,
            "hiring_response_count": 0,
            "finance_response_count": 0,
            "unresolved_hiring_pressure": False,
            "trust_recovery": round(trust_recovery, 4),
            "product_response_count": product_response_count,
            "board_update_after_crisis_count": board_update_after_crisis_count,
            "legal_follow_up_count": legal_follow_up_count,
            "finance_follow_up_count": finance_follow_up_count,
            "pipeline_actions_during_trust_crisis": pipeline_actions_during_trust_crisis,
            "pipeline_actions_during_liquidity_crisis": pipeline_actions_during_liquidity_crisis,
            "market_read_count": market_read_count,
            "security_crisis_detected": security_crisis_detected,
            "liquidity_crisis_detected": liquidity_crisis_detected,
            "final_financing_pressure": round(final_financing_pressure, 4),
            "final_counterparty_risk": round(final_counterparty_risk, 4),
            "liquid_cash_months": round(liquid_cash_months, 4),
            "rigid_loop_penalty_applied": rigid_loop_penalty_applied,
        }

    return 0.0, {
        "behavioral_penalty": 0.0,
        "adverse_event_count": 0,
        "unanswered_adverse_events": 0,
        "support_alert_turn_count": 0,
        "support_actions_after_adverse_event": 0,
        "trust_decline": 0.0,
        "soft_demand_alert_turn_count": 0,
        "demand_decline": 0.0,
        "pipeline_decline_ratio": 0.0,
        "hiring_response_count": 0,
        "finance_response_count": 0,
        "unresolved_hiring_pressure": False,
        "trust_recovery": 0.0,
        "product_response_count": 0,
        "board_update_after_crisis_count": 0,
        "legal_follow_up_count": 0,
        "finance_follow_up_count": 0,
        "pipeline_actions_during_trust_crisis": 0,
        "pipeline_actions_during_liquidity_crisis": 0,
        "market_read_count": 0,
        "security_crisis_detected": False,
        "liquidity_crisis_detected": False,
        "final_financing_pressure": 0.0,
        "final_counterparty_risk": 0.0,
        "liquid_cash_months": 0.0,
        "rigid_loop_penalty_applied": rigid_loop_penalty_applied,
    }


def _score_strategic_coherence(
    world_state: dict,
    *,
    scenario: dict,
    trace_evidence: dict[str, Any] | None = None,
) -> tuple[float, dict]:
    governance = world_state.get("governance", {})
    finance = world_state.get("finance", {})
    operations = world_state.get("operations", {})
    product = world_state.get("product", {})
    customers = world_state.get("customers", {})
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
        elif track == "board":
            org_signal = _clamp(org_changes_count / 1.0)
            market_signal = _clamp(market_reads_count / 1.0)
            incident_signal = _clamp(incident_response_count / 2.0)
            resolution_signal = 1.0 if major_incidents_open == 0 else _clamp(1.0 - (major_incidents_open / 3.0))
            support_signal = _clamp(support_actions_taken / 2.0)
            trust_signal = _clamp(float(customers.get("trust_score", 0.0)))
            score = _round_score(
                base_score * 0.28
                + org_signal * 0.08
                + compliance_signal * 0.08
                + fundraising_signal * 0.12
                + market_signal * 0.08
                + incident_signal * 0.12
                + resolution_signal * 0.12
                + support_signal * 0.1
                + trust_signal * 0.1
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
    behavioral_penalty, behavioral_details = _behavioral_penalty(
        world_state=world_state,
        trace_evidence=trace_evidence,
        scenario=scenario,
    )
    score = _round_score(score - behavioral_penalty)
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
        **behavioral_details,
    }
    return score, details


def evaluate_dry_run(*, scenario: dict, world_state: dict, trace_evidence: dict[str, Any] | None = None) -> dict:
    finance = world_state.get("finance", {})
    customers = world_state.get("customers", {})
    weights = _weight_map(scenario)

    cash_efficiency, cash_details = _score_cash_efficiency(world_state)
    revenue_quality, revenue_details = _score_revenue_quality(world_state)
    customer_health, customer_details = _score_customer_health(world_state)
    product_health, product_details = _score_product_health(world_state)
    team_health, team_details = _score_team_health(world_state)
    risk_management, risk_details = _score_risk_management(world_state)
    strategic_coherence, strategy_details = _score_strategic_coherence(
        world_state,
        scenario=scenario,
        trace_evidence=trace_evidence,
    )

    component_scores = {
        "cash_efficiency": cash_efficiency,
        "revenue_quality": revenue_quality,
        "customer_health": customer_health,
        "product_health": product_health,
        "team_health": team_health,
        "risk_management": risk_management,
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
                    "product_health": product_details,
                    "team_health": team_details,
                    "risk_management": risk_details,
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
