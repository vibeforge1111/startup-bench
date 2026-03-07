"""Heuristic baseline runners for TheStartupBench."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from .artifacts import build_score_report, build_trace
from .evaluators import evaluate_dry_run
from .runner import initialize_world_state
from .scenario_loader import load_scenario
from .runtime import RuntimeSession, execute_tool_call
from .tool_registry import tool_manifest_for_names
from .trace_validation import validate_trace_integrity
from .validation import validate_instance


_BASELINE_IDS = {
    "heuristic_b2b_operator",
    "heuristic_governance_operator",
    "heuristic_liquidity_operator",
    "heuristic_long_horizon_operator",
    "heuristic_market_aware_operator",
    "heuristic_resilient_operator",
}


def list_baselines() -> list[str]:
    return sorted(_BASELINE_IDS)


def _next_request_id(turn_index: int, action_index: int) -> str:
    return f"baseline_req_{turn_index:03d}_{action_index:02d}"


def _long_horizon_board_update_payload(session: RuntimeSession) -> dict:
    finance = session.world_state.get("finance", {})
    customers = session.world_state.get("customers", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    product = session.world_state.get("product", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    board_update_count = int(governance.get("board_update_count", 0))

    summary = "Protected long-horizon trust, delivery capacity, and financing optionality ahead of short-term narrative wins."
    asks = ["support sequencing quality and capacity investments before aggressive expansion"]

    if board_update_count == 0 and (
        int(product.get("major_incidents_open", 0)) > 0 or float(operations.get("support_backlog", 0.0)) >= 34
    ):
        summary = "Prioritized immediate reliability recovery and support stabilization before making new growth promises to the board."
        asks = ["support incident recovery and service-quality sequencing before acceleration"]
    elif float(risk.get("financing_pressure", 0.0)) >= 0.72 or float(finance.get("runway_weeks", 999.0)) < 24:
        summary = "Grounded the board in liquidity reality, kept financing optionality open, and prioritized operating resilience over narrative expansion."
        asks = ["support a conservative financing posture and transparent runway planning"]
    elif board_update_count >= 1 and (
        float(customers.get("trust_score", 0.0)) < 0.7
        or float(operations.get("support_backlog", 0.0)) >= 24
        or float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0))) > 0.58
    ):
        summary = "Sequenced customer trust recovery ahead of headline growth commitments and kept the roadmap aligned with buyer reality."
        asks = ["support a trust-first operating plan until customer signals strengthen"]
    elif float(team.get("morale", 1.0)) < 0.6 or float(team.get("attrition_risk", 0.0)) > 0.52:
        summary = "Protected team durability and delivery capacity so growth targets stay believable rather than aspirational."
        asks = ["support selective hiring and org relief before expanding commitments"]

    return {
        "summary": summary,
        "forecast": {
            "runway_weeks": finance.get("runway_weeks"),
            "support_backlog": operations.get("support_backlog"),
            "delivery_capacity_index": team.get("delivery_capacity_index"),
            "trust_score": customers.get("trust_score"),
            "major_incidents_open": product.get("major_incidents_open"),
            "financing_pressure": risk.get("financing_pressure"),
        },
        "asks": asks,
    }


def _liquidity_board_update_payload(session: RuntimeSession) -> dict:
    finance = session.world_state.get("finance", {})
    customers = session.world_state.get("customers", {})
    governance = session.world_state.get("governance", {})
    risk = session.world_state.get("risk", {})
    team = session.world_state.get("team", {})

    board_update_count = int(governance.get("board_update_count", 0))
    runway = float(finance.get("runway_weeks", 999.0))
    liquid_cash = float(finance.get("liquid_cash_usd", finance.get("cash_usd", 0.0)))
    burn = max(1.0, float(finance.get("monthly_burn_usd", 1.0)))
    treasury_concentration = float(finance.get("treasury_concentration", 0.0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))
    counterparty_risk = float(risk.get("counterparty_risk", 0.0))

    summary = "Protected liquidity first, preserved payroll continuity, and kept bridge-financing options open while avoiding narrative overreach."
    asks = ["support a liquidity-first operating plan until cash access and financing pressure normalize"]

    if treasury_concentration > 0.72 or counterparty_risk > 0.72:
        summary = "Reduced treasury concentration, prioritized cash access, and treated payroll continuity as the primary operating constraint."
        asks = ["support treasury diversification and short-horizon cash controls before new growth commitments"]
    elif runway < 18 or liquid_cash < burn * 2.0:
        summary = "Reset the board on immediate survival math, paired burn control with bridge financing, and avoided cosmetic growth narratives."
        asks = ["support emergency financing and hard spend discipline until liquidity stabilizes"]
    elif board_update_count >= 1 and financing_pressure > 0.78:
        summary = "Shifted the board conversation from pipeline optics to financing risk, cash access, and downside protection."
        asks = ["support transparent liquidity reporting and fast contingency planning"]
    elif float(customers.get("trust_score", 1.0)) < 0.68:
        summary = "Balanced liquidity actions with customer trust protection so a financing fix does not become a retention failure."
        asks = ["support retention-preserving cuts and selective trust repair work"]
    elif float(team.get("morale", 1.0)) < 0.55:
        summary = "Stabilized cash and team durability together so the company can survive the reset without a hidden execution collapse."
        asks = ["support morale-protecting changes tied to the financial reset"]

    return {
        "summary": summary,
        "forecast": {
            "runway_weeks": finance.get("runway_weeks"),
            "liquid_cash_usd": finance.get("liquid_cash_usd"),
            "restricted_cash_usd": finance.get("restricted_cash_usd"),
            "treasury_concentration": finance.get("treasury_concentration"),
            "financing_pressure": risk.get("financing_pressure"),
            "counterparty_risk": risk.get("counterparty_risk"),
        },
        "asks": asks,
    }


def _heuristic_b2b_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if float(finance.get("runway_weeks", 0)) < 32 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -25000}},
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.5)) < 0.68:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": -1,
                    "budget_change_monthly_burn_usd": 8000,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) > 0.68
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.08
    ):
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.08},
            }
        )
        action_index += 1

    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * 7.0:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 60000,
                },
            }
        )
        action_index += 1

    if int(governance.get("board_update_count", 0)) == 0 or (turn_index > 0 and turn_index % 4 == 0):
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "summary": "Tightened burn, improved onboarding focus, and monitored pricing elasticity.",
                    "forecast": {
                        "runway_weeks": finance.get("runway_weeks"),
                        "monthly_revenue_usd": finance.get("monthly_revenue_usd"),
                    },
                    "asks": ["maintain current hiring pace"],
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_resilient_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    hiring = team.get("hiring", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0))) > 0.55 or float(market.get("demand_index", 1.0)) < 0.78:
        actions.append(
            {
                "tool_name": "research.market.read",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {},
            }
        )
        action_index += 1

    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append(
            {
                "tool_name": "ops.incident.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.06,
                    "churn_reduction": 0.01,
                    "monthly_burn_increase_usd": 9000,
                },
            }
        )
        action_index += 1

    if float(operations.get("support_backlog", 0.0)) > 35 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.45:
        actions.append(
            {
                "tool_name": "ops.support.resolve",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "backlog_reduction": 16,
                    "sla_risk_reduction": 0.16,
                    "trust_recovery": 0.025,
                    "churn_reduction": 0.004,
                    "monthly_burn_increase_usd": 7000,
                },
            }
        )
        action_index += 1

    if float(risk.get("regulatory_pressure", 0.0)) > 0.55 or int(risk.get("active_legal_matters", 0)) > 0:
        actions.append(
            {
                "tool_name": "legal.compliance.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pressure_reduction": 0.2,
                    "matters_reduction": 1,
                    "compliance_backlog_reduction": 6,
                    "trust_recovery": 0.02,
                    "monthly_burn_increase_usd": 11000,
                },
            }
        )
        action_index += 1

    if float(finance.get("treasury_concentration", 0.0)) > 0.78:
        actions.append(
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "target_concentration": 0.45,
                    "rebalance_cost_usd": 8000,
                },
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 18 or float(finance.get("liquid_cash_usd", finance.get("cash_usd", 0.0))) < float(finance.get("monthly_burn_usd", 0.0)) * 2.0:
        if not finance.get("last_raise_plan"):
            actions.append(
                {
                    "tool_name": "finance.raise.propose",
                    "request_id": _next_request_id(turn_index, action_index),
                    "arguments": {
                        "raise_amount_usd": max(600000.0, float(finance.get("monthly_burn_usd", 0.0)) * 6.0),
                        "dilution_pct": 0.12,
                        "monthly_burn_change_usd": 0,
                        "financing_risk_reduction": 0.28,
                        "transaction_cost_usd": 30000,
                    },
                }
            )
            action_index += 1

    if int(hiring.get("open_roles", team.get("open_roles", 0))) > 0 and (
        float(team.get("bandwidth_load", 0.0)) > 0.78
        or float(team.get("delivery_capacity_index", 1.0)) < 0.58
        or int(hiring.get("critical_roles_open", 0)) > 0
    ):
        actions.append(
            {
                "tool_name": "people.hiring.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "sourced_candidates_delta": 6 if int(hiring.get("sourced_candidates", 0)) < 8 else 0,
                    "onsite_candidates_delta": 2 if int(hiring.get("sourced_candidates", 0)) >= 6 else 0,
                    "offers_out_delta": 1 if int(hiring.get("onsite_candidates", 0)) >= 2 else 0,
                    "accepted_hires": 1 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "monthly_burn_change_usd": 16000 if int(hiring.get("offers_out", 0)) >= 1 else 4500,
                    "morale_delta": 0.03 if int(hiring.get("offers_out", 0)) >= 1 else 0.01,
                    "bandwidth_load_delta": -0.06 if int(hiring.get("offers_out", 0)) >= 1 else -0.01,
                    "support_backlog_delta": -4 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "onboarding_quality_delta": 0.015 if int(hiring.get("offers_out", 0)) >= 1 else 0.0,
                },
            }
        )
        action_index += 1

    if float(team.get("morale", 0.7)) < 0.58 or float(team.get("attrition_risk", 0.0)) > 0.5:
        actions.append(
            {
                "tool_name": "people.org.adjust",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "morale_delta": 0.08,
                    "attrition_risk_delta": -0.1,
                    "bandwidth_load_delta": -0.08,
                    "monthly_burn_change_usd": 9000,
                    "onboarding_quality_delta": 0.02,
                },
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 0)) < 34 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -18000}},
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.5)) < 0.7 and int(product.get("major_incidents_open", 0)) <= 1:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.07,
                    "major_incidents_delta": 0,
                    "budget_change_monthly_burn_usd": 5000,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) >= 0.72
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.05
        and float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0))) < 0.6
    ):
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.04},
            }
        )
        action_index += 1

    pipeline_threshold = 5.5 if float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0))) < 0.6 else 6.5
    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * pipeline_threshold:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 65000 if float(market.get("demand_index", 1.0)) >= 0.8 else 45000,
                },
            }
        )
        action_index += 1

    if turn_index % 3 == 0 or int(governance.get("board_update_count", 0)) < 2:
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "summary": "Stabilized incidents first, protected trust, and tightened spend while recovering pipeline quality.",
                    "forecast": {
                        "runway_weeks": finance.get("runway_weeks"),
                        "major_incidents_open": product.get("major_incidents_open"),
                        "trust_score": customers.get("trust_score"),
                    },
                    "asks": ["support temporary incident-focused resource allocation"],
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_market_aware_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    market = session.world_state.get("market", {})
    team = session.world_state.get("team", {})
    hiring = team.get("hiring", {})
    risk = session.world_state.get("risk", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    actions.append(
        {
            "tool_name": "research.market.read",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    competitor_pressure = float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0)))
    pricing_pressure = float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0)))
    demand_index = float(market.get("demand_index", 0.85))

    if float(finance.get("treasury_concentration", 0.0)) > 0.78:
        actions.append(
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"target_concentration": 0.42, "rebalance_cost_usd": 7000},
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 20 or float(risk.get("financing_pressure", 0.0)) > 0.72:
        if not finance.get("last_raise_plan"):
            actions.append(
                {
                    "tool_name": "finance.raise.propose",
                    "request_id": _next_request_id(turn_index, action_index),
                    "arguments": {
                        "raise_amount_usd": max(750000.0, float(finance.get("monthly_burn_usd", 0.0)) * 5.5),
                        "dilution_pct": 0.11,
                        "monthly_burn_change_usd": 0,
                        "financing_risk_reduction": 0.24,
                        "transaction_cost_usd": 26000,
                    },
                }
            )
            action_index += 1

    if float(finance.get("runway_weeks", 0.0)) < 30 and not finance.get("last_plan_update"):
        burn_cut = -22000 if demand_index < 0.78 else -14000
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": burn_cut}},
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.0)) < 0.69 and competitor_pressure > 0.55:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": 0,
                    "budget_change_monthly_burn_usd": 5000,
                },
            }
        )
        action_index += 1

    if int(hiring.get("open_roles", team.get("open_roles", 0))) > 0 and float(team.get("bandwidth_load", 0.0)) > 0.76:
        actions.append(
            {
                "tool_name": "people.hiring.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "sourced_candidates_delta": 5 if int(hiring.get("sourced_candidates", 0)) < 6 else 0,
                    "onsite_candidates_delta": 2 if int(hiring.get("sourced_candidates", 0)) >= 5 else 0,
                    "offers_out_delta": 1 if int(hiring.get("onsite_candidates", 0)) >= 2 else 0,
                    "accepted_hires": 1 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "monthly_burn_change_usd": 14500 if int(hiring.get("offers_out", 0)) >= 1 else 3500,
                    "morale_delta": 0.03 if int(hiring.get("offers_out", 0)) >= 1 else 0.008,
                    "bandwidth_load_delta": -0.05 if int(hiring.get("offers_out", 0)) >= 1 else -0.01,
                    "support_backlog_delta": -3 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "onboarding_quality_delta": 0.012 if int(hiring.get("offers_out", 0)) >= 1 else 0.0,
                },
            }
        )
        action_index += 1

    pipeline_threshold = float(finance.get("monthly_burn_usd", 0.0)) * (6.8 if competitor_pressure > 0.65 else 5.8)
    if float(sales.get("weighted_pipeline_usd", 0.0)) < pipeline_threshold:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1 if demand_index >= 0.72 else 0,
                    "weighted_pipeline_usd_delta": 70000 if demand_index >= 0.8 else 50000,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) >= 0.74
        and pricing_pressure < 0.52
        and competitor_pressure < 0.62
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.04
    ):
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.03},
            }
        )
        action_index += 1

    if turn_index % 3 == 0 or int(governance.get("board_update_count", 0)) == 0:
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "summary": "Adjusted to market pressure, protected distribution quality, and kept financing optionality open.",
                    "forecast": {
                        "runway_weeks": finance.get("runway_weeks"),
                        "competitor_pressure_index": market.get("competitor_pressure_index"),
                        "demand_index": market.get("demand_index"),
                    },
                    "asks": ["support selective hiring and GTM focus shifts"],
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_liquidity_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    track = session.scenario["metadata"]["track"]
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    actions: list[dict] = []
    action_index = 0

    runway = float(finance.get("runway_weeks", 999.0))
    monthly_burn = float(finance.get("monthly_burn_usd", 0.0))
    liquid_cash = float(finance.get("liquid_cash_usd", finance.get("cash_usd", 0.0)))
    treasury_concentration = float(finance.get("treasury_concentration", 0.0))
    restricted_cash = float(finance.get("restricted_cash_usd", 0.0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))
    counterparty_risk = float(risk.get("counterparty_risk", 0.0))

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if treasury_concentration > 0.55 or restricted_cash > 0 or financing_pressure > 0.7:
        actions.append(
            {
                "tool_name": "finance.treasury.read",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {},
            }
        )
        action_index += 1

    if financing_pressure > 0.68 or runway < 26:
        actions.append(
            {
                "tool_name": "finance.plan.read",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {},
            }
        )
        action_index += 1

    if track in {"board", "crisis", "finance"} and (turn_index == 0 or turn_index % 2 == 0):
        actions.append(
            {
                "tool_name": "board.read",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {},
            }
        )
        action_index += 1

    if treasury_concentration > 0.72 or counterparty_risk > 0.74:
        actions.append(
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "target_concentration": 0.32 if treasury_concentration > 0.88 else 0.4,
                    "rebalance_cost_usd": 9000,
                },
            }
        )
        action_index += 1

    if (runway < 26 or financing_pressure > 0.7 or liquid_cash < monthly_burn * 2.5) and not finance.get("last_plan_update"):
        burn_cut = -32000 if runway < 18 or financing_pressure > 0.82 else -22000
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": burn_cut}},
            }
        )
        action_index += 1

    if (
        not finance.get("last_raise_plan")
        and (financing_pressure > 0.82 or liquid_cash < monthly_burn * 2.0 or restricted_cash > float(finance.get("cash_usd", 0.0)) * 0.25)
    ):
        actions.append(
            {
                "tool_name": "finance.raise.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "raise_amount_usd": max(900000.0, monthly_burn * 7.0),
                    "dilution_pct": 0.13,
                    "monthly_burn_change_usd": 0,
                    "financing_risk_reduction": 0.34,
                    "transaction_cost_usd": 28000,
                },
            }
        )
        action_index += 1

    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append(
            {
                "tool_name": "ops.incident.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.04,
                    "churn_reduction": 0.006,
                    "monthly_burn_increase_usd": 7000,
                },
            }
        )
        action_index += 1

    if float(operations.get("support_backlog", 0.0)) > 34 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.42:
        actions.append(
            {
                "tool_name": "ops.support.resolve",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "backlog_reduction": 16,
                    "sla_risk_reduction": 0.16,
                    "trust_recovery": 0.025,
                    "churn_reduction": 0.004,
                    "monthly_burn_increase_usd": 5500,
                },
            }
        )
        action_index += 1

    if float(risk.get("regulatory_pressure", 0.0)) > 0.55 or int(risk.get("active_legal_matters", 0)) > 0:
        actions.append(
            {
                "tool_name": "legal.compliance.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pressure_reduction": 0.2,
                    "matters_reduction": 1,
                    "compliance_backlog_reduction": 6,
                    "trust_recovery": 0.02,
                    "monthly_burn_increase_usd": 9000,
                },
            }
        )
        action_index += 1

    if (
        (float(team.get("morale", 1.0)) < 0.52 or float(team.get("attrition_risk", 0.0)) > 0.62)
        and runway > 14
        and financing_pressure < 0.9
    ):
        actions.append(
            {
                "tool_name": "people.org.adjust",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "morale_delta": 0.05,
                    "attrition_risk_delta": -0.07,
                    "bandwidth_load_delta": -0.06,
                    "monthly_burn_change_usd": 4000,
                    "onboarding_quality_delta": 0.015,
                },
            }
        )
        action_index += 1

    if (
        financing_pressure < 0.72
        and runway > 22
        and float(market.get("demand_index", 0.8)) > 0.74
        and float(sales.get("weighted_pipeline_usd", 0.0)) < monthly_burn * 4.5
    ):
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 45000,
                },
            }
        )
        action_index += 1

    if turn_index % 2 == 0 or int(governance.get("board_update_count", 0)) == 0:
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": _liquidity_board_update_payload(session),
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_governance_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    team = session.world_state.get("team", {})
    hiring = team.get("hiring", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    actions.append(
        {
            "tool_name": "board.read",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    actions.append(
        {
            "tool_name": "research.market.read",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append(
            {
                "tool_name": "ops.incident.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.05,
                    "churn_reduction": 0.006,
                    "monthly_burn_increase_usd": 7000,
                },
            }
        )
        action_index += 1

    if float(operations.get("support_backlog", 0.0)) > 26 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.32:
        actions.append(
            {
                "tool_name": "ops.support.resolve",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "backlog_reduction": 16,
                    "sla_risk_reduction": 0.16,
                    "trust_recovery": 0.028,
                    "churn_reduction": 0.004,
                    "monthly_burn_increase_usd": 6000,
                },
            }
        )
        action_index += 1

    if (
        float(team.get("morale", 1.0)) < 0.58
        or float(team.get("attrition_risk", 0.0)) > 0.52
        or float(team.get("bandwidth_load", 0.0)) > 0.84
    ):
        actions.append(
            {
                "tool_name": "people.org.adjust",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "morale_delta": 0.07,
                    "attrition_risk_delta": -0.09,
                    "bandwidth_load_delta": -0.08,
                    "monthly_burn_change_usd": 7000,
                    "onboarding_quality_delta": 0.02,
                },
            }
        )
        action_index += 1

    if int(hiring.get("open_roles", team.get("open_roles", 0))) > 0 and (
        int(hiring.get("critical_roles_open", 0)) > 0 or float(team.get("bandwidth_load", 0.0)) > 0.8
    ):
        actions.append(
            {
                "tool_name": "people.hiring.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "sourced_candidates_delta": 5 if int(hiring.get("sourced_candidates", 0)) < 7 else 0,
                    "onsite_candidates_delta": 2 if int(hiring.get("sourced_candidates", 0)) >= 5 else 0,
                    "offers_out_delta": 1 if int(hiring.get("onsite_candidates", 0)) >= 2 else 0,
                    "accepted_hires": 1 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "monthly_burn_change_usd": 13000 if int(hiring.get("offers_out", 0)) >= 1 else 3000,
                    "morale_delta": 0.03 if int(hiring.get("offers_out", 0)) >= 1 else 0.01,
                    "bandwidth_load_delta": -0.05 if int(hiring.get("offers_out", 0)) >= 1 else -0.01,
                    "support_backlog_delta": -4 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "onboarding_quality_delta": 0.015 if int(hiring.get("offers_out", 0)) >= 1 else 0.0,
                },
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 28 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -22000}},
            }
        )
        action_index += 1

    if float(risk.get("financing_pressure", 0.0)) > 0.8 and not finance.get("last_raise_plan"):
        actions.append(
            {
                "tool_name": "finance.raise.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "raise_amount_usd": max(850000.0, float(finance.get("monthly_burn_usd", 0.0)) * 5.5),
                    "dilution_pct": 0.11,
                    "monthly_burn_change_usd": 0,
                    "financing_risk_reduction": 0.28,
                    "transaction_cost_usd": 26000,
                },
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.0)) < 0.7 or int(product.get("roadmap_items", 0)) > 7:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": 0,
                    "budget_change_monthly_burn_usd": 3500,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) > 0.74
        and float(operations.get("support_backlog", 0.0)) < 24
        and float(risk.get("financing_pressure", 0.0)) < 0.7
        and float(finance.get("monthly_revenue_usd", 0.0)) > 0
        and float(finance.get("runway_weeks", 999.0)) > 22
    ):
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 50000,
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "board.update",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": _long_horizon_board_update_payload(session),
        }
    )
    action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_long_horizon_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    track = session.scenario["metadata"]["track"]
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    team = session.world_state.get("team", {})
    hiring = team.get("hiring", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    actions.append(
        {
            "tool_name": "research.market.read",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if track == "board" and (turn_index == 0 or turn_index % 2 == 0):
        actions.append(
            {
                "tool_name": "board.read",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {},
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 28 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -20000}},
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 18 or float(risk.get("financing_pressure", 0.0)) > 0.75:
        if not finance.get("last_raise_plan"):
            actions.append(
                {
                    "tool_name": "finance.raise.propose",
                    "request_id": _next_request_id(turn_index, action_index),
                    "arguments": {
                        "raise_amount_usd": max(850000.0, float(finance.get("monthly_burn_usd", 0.0)) * 5.0),
                        "dilution_pct": 0.1,
                        "monthly_burn_change_usd": 0,
                        "financing_risk_reduction": 0.26,
                        "transaction_cost_usd": 24000,
                    },
                }
            )
            action_index += 1

    if float(finance.get("treasury_concentration", 0.0)) > 0.8:
        actions.append(
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"target_concentration": 0.4, "rebalance_cost_usd": 7000},
            }
        )
        action_index += 1

    if (
        float(product.get("onboarding_quality", 0.0)) < 0.7
        or int(product.get("roadmap_items", 0)) > 7
        or float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0))) > 0.58
    ):
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": 0,
                    "budget_change_monthly_burn_usd": 4000,
                },
            }
        )
        action_index += 1

    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append(
            {
                "tool_name": "ops.incident.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.05,
                    "churn_reduction": 0.008,
                    "monthly_burn_increase_usd": 8500,
                },
            }
        )
        action_index += 1

    if float(operations.get("support_backlog", 0.0)) > 34 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.38:
        actions.append(
            {
                "tool_name": "ops.support.resolve",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "backlog_reduction": 18,
                    "sla_risk_reduction": 0.18,
                    "trust_recovery": 0.03,
                    "churn_reduction": 0.005,
                    "monthly_burn_increase_usd": 6500,
                },
            }
        )
        action_index += 1

    if int(hiring.get("open_roles", team.get("open_roles", 0))) > 0 and (
        float(team.get("bandwidth_load", 0.0)) > 0.74
        or float(team.get("delivery_capacity_index", 1.0)) < 0.62
        or int(hiring.get("critical_roles_open", 0)) > 0
    ):
        actions.append(
            {
                "tool_name": "people.hiring.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "sourced_candidates_delta": 5 if int(hiring.get("sourced_candidates", 0)) < 7 else 0,
                    "onsite_candidates_delta": 2 if int(hiring.get("sourced_candidates", 0)) >= 5 else 0,
                    "offers_out_delta": 1 if int(hiring.get("onsite_candidates", 0)) >= 2 else 0,
                    "accepted_hires": 1 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "monthly_burn_change_usd": 14000 if int(hiring.get("offers_out", 0)) >= 1 else 3200,
                    "morale_delta": 0.03 if int(hiring.get("offers_out", 0)) >= 1 else 0.01,
                    "bandwidth_load_delta": -0.06 if int(hiring.get("offers_out", 0)) >= 1 else -0.01,
                    "support_backlog_delta": -4 if int(hiring.get("offers_out", 0)) >= 1 else 0,
                    "onboarding_quality_delta": 0.015 if int(hiring.get("offers_out", 0)) >= 1 else 0.0,
                },
            }
        )
        action_index += 1

    if float(team.get("morale", 0.7)) < 0.58 or float(team.get("attrition_risk", 0.0)) > 0.52:
        actions.append(
            {
                "tool_name": "people.org.adjust",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "morale_delta": 0.07,
                    "attrition_risk_delta": -0.1,
                    "bandwidth_load_delta": -0.08,
                    "monthly_burn_change_usd": 8000,
                    "onboarding_quality_delta": 0.02,
                },
            }
        )
        action_index += 1

    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * 5.8:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 55000 if float(market.get("demand_index", 1.0)) >= 0.76 else 40000,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) >= 0.76
        and float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0))) < 0.48
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.03
    ):
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.02},
            }
        )
        action_index += 1

    if turn_index % 2 == 0 or int(governance.get("board_update_count", 0)) == 0:
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": _long_horizon_board_update_payload(session),
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _proposed_actions_for_baseline(session: RuntimeSession, *, baseline_id: str, turn_index: int) -> list[dict]:
    if baseline_id == "heuristic_b2b_operator":
        return _heuristic_b2b_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_governance_operator":
        return _heuristic_governance_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_liquidity_operator":
        return _heuristic_liquidity_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_long_horizon_operator":
        return _heuristic_long_horizon_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_market_aware_operator":
        return _heuristic_market_aware_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_resilient_operator":
        return _heuristic_resilient_actions(session, turn_index=turn_index)
    raise ValueError(f"Unknown baseline_id '{baseline_id}'.")


def run_baseline(*, scenario_path: Path, baseline_id: str, seed: int, max_turns: int | None = None) -> dict:
    if baseline_id not in _BASELINE_IDS:
        raise ValueError(f"Unknown baseline_id '{baseline_id}'. Available baselines: {', '.join(list_baselines())}")

    scenario = load_scenario(scenario_path)
    declared_tools = set(scenario["tools"])
    horizon_length = int(scenario["metadata"]["time_horizon"]["length"])
    total_turns = max_turns if max_turns is not None else horizon_length
    total_turns = max(1, min(total_turns, horizon_length))

    world_state = initialize_world_state(scenario, seed=seed)
    session = RuntimeSession(scenario=scenario, world_state=world_state)
    turns: list[dict] = []
    snapshots: list[dict] = [
        {"snapshot_id": "initial", "kind": "initial", "state": deepcopy(session.world_state)}
    ]
    total_tool_calls = 0

    for turn_index in range(total_turns):
        before_time = session.world_state["sim"]["current_time"]
        observations = session.visible_observations()
        proposed_actions = _proposed_actions_for_baseline(session, baseline_id=baseline_id, turn_index=turn_index)
        events: list[dict] = []
        actions: list[dict] = []

        for tool_call in proposed_actions:
            if tool_call["tool_name"] not in declared_tools:
                continue
            response = execute_tool_call(session, tool_call)
            total_tool_calls += 1
            events.extend(response.get("result", {}).get("events_processed", []))
            actions.append(
                {
                    "tool_name": tool_call["tool_name"],
                    "request_id": tool_call["request_id"],
                    "arguments": tool_call.get("arguments", {}),
                    "response": response,
                    "status": "ok" if response.get("ok", False) else "error",
                }
            )

        after_time = session.world_state["sim"]["current_time"]
        turns.append(
            {
                "turn_index": turn_index,
                "sim_time_before": before_time,
                "sim_time_after": after_time,
                "observations": observations,
                "actions": actions,
                "events": events,
                "notes": [],
            }
        )
        snapshots.append(
            {
                "snapshot_id": f"turn_{turn_index}",
                "kind": "milestone",
                "state": deepcopy(session.world_state),
            }
        )

    run_id = f"baseline-{uuid4()}"
    final_snapshots = snapshots + [{"snapshot_id": "final", "kind": "final", "state": deepcopy(session.world_state)}]
    evaluation = evaluate_dry_run(
        scenario=scenario,
        world_state=session.world_state,
        trace_evidence={
            "turns": turns,
            "state_snapshots": final_snapshots,
        },
    )
    trace = build_trace(
        scenario=scenario,
        seed=seed,
        run_id=run_id,
        model_id=baseline_id,
        evaluation=evaluation,
        world_state=session.world_state,
    )
    trace["turns"] = turns
    trace["state_snapshots"] = final_snapshots
    trace["runtime"]["total_tool_calls"] = total_tool_calls
    trace["agent"]["provider"] = "baseline"
    trace["agent"]["agent_name"] = baseline_id

    score_report = build_score_report(scenario=scenario, run_id=run_id, evaluation=evaluation)
    return {
        "run_id": run_id,
        "baseline_id": baseline_id,
        "tool_manifest": tool_manifest_for_names(scenario["tools"]),
        "trace": trace,
        "score_report": score_report,
        "artifact_validation": {
            "trace": validate_instance(artifact_type="trace", instance=trace, path=Path("trace.json")).to_dict(),
            "trace_integrity": validate_trace_integrity(trace).to_dict(),
            "score_report": validate_instance(
                artifact_type="score-report",
                instance=score_report,
                path=Path("score_report.json"),
            ).to_dict(),
        },
    }


__all__ = ["list_baselines", "run_baseline"]
