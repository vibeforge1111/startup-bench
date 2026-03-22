"""Doctrine-augmented agent for TheStartupBench.

Uses startup-yc doctrine packets to guide operational decisions.
Builds on the heuristic_long_horizon_operator baseline but injects
doctrine-based reasoning for board updates, pricing decisions,
hiring plans, and crisis responses.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

# Add startup-bench src to path
BENCH_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BENCH_ROOT / "src"))

from thestartupbench.artifacts import build_score_report, build_trace
from thestartupbench.evaluators import evaluate_dry_run
from thestartupbench.runner import initialize_world_state
from thestartupbench.scenario_loader import load_scenario
from thestartupbench.runtime import RuntimeSession, execute_tool_call
from thestartupbench.tool_registry import tool_manifest_for_names


# ---------------------------------------------------------------------------
# Doctrine loading (from domain-chip-startup-yc)
# ---------------------------------------------------------------------------

STARTUP_YC_ROOT = Path(r"C:\Users\USER\Desktop\domain-chip-startup-yc")
PACKETS_ROOT = STARTUP_YC_ROOT / "docs" / "research-packets"


def _parse_packet_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("- ") and ":" in stripped:
            key, _, value = stripped[2:].partition(":")
            metadata[key.strip()] = value.strip().strip("`")
    return metadata


def _parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = ""
    lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current and lines:
                sections[current] = " ".join(l.strip() for l in lines if l.strip())
            current = line[3:].strip().lower()
            lines = []
        elif current:
            lines.append(line)
    if current and lines:
        sections[current] = " ".join(l.strip() for l in lines if l.strip())
    return sections


def load_doctrine_packets() -> list[dict]:
    """Load promoted + candidate packets from startup-yc."""
    packets = []
    for path in sorted(PACKETS_ROOT.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        text = path.read_text(encoding="utf-8")
        meta = _parse_packet_metadata(text)
        promo = meta.get("promotion_status", "")
        if promo not in ("promoted", "candidate_doctrine"):
            continue
        sections = _parse_sections(text)
        packets.append({
            "packet_id": meta.get("packet_id", path.stem),
            "claim": sections.get("claim", ""),
            "mechanism": sections.get("mechanism", ""),
            "boundary": sections.get("boundary", ""),
            "doctrine_tags": [t.strip() for t in meta.get("doctrine_tags", "").split(",") if t.strip()],
            "coverage_areas": [a.strip() for a in meta.get("coverage_areas", "").split(",") if a.strip()],
        })
    return packets


# ---------------------------------------------------------------------------
# Doctrine context selection for startup-bench scenarios
# ---------------------------------------------------------------------------

TRACK_DOCTRINE_MAP: dict[str, list[str]] = {
    "finance": ["failure_survival_and_capital_discipline", "fundraising_and_investor_dynamics", "pricing_and_sales_execution"],
    "board": ["operating_cadence_and_org_design", "failure_survival_and_capital_discipline", "founder_and_cofounder_fit"],
    "crisis": ["failure_survival_and_capital_discipline", "operating_cadence_and_org_design"],
    "people": ["hiring_and_talent_quality", "operating_cadence_and_org_design", "founder_and_cofounder_fit"],
    "gtm": ["pricing_and_sales_execution", "user_truth_and_distribution", "pivoting_and_experiment_quality"],
    "product": ["product_taste_and_user_empathy", "problem_and_wedge_selection", "pmf_and_positioning_truth"],
    "growth": ["user_truth_and_distribution", "pivoting_and_experiment_quality"],
    "hiring": ["hiring_and_talent_quality", "operating_cadence_and_org_design"],
    "scale": ["operating_cadence_and_org_design", "pricing_and_sales_execution"],
    "0to1": ["pmf_and_positioning_truth", "problem_and_wedge_selection", "idea_quality_and_validation"],
    "b2b_saas": ["pricing_and_sales_execution", "pmf_and_positioning_truth"],
    "real_world": ["failure_survival_and_capital_discipline", "operating_cadence_and_org_design"],
    "launch": ["user_truth_and_distribution", "product_taste_and_user_empathy"],
}


def select_doctrine_for_track(packets: list[dict], track: str, max_packets: int = 5) -> list[dict]:
    """Select relevant doctrine packets based on scenario track."""
    relevant_tags = TRACK_DOCTRINE_MAP.get(track, [])
    if not relevant_tags:
        return packets[:max_packets]

    scored = []
    for p in packets:
        score = 0
        for tag in p["doctrine_tags"]:
            tag_core = tag.replace("doctrine:", "")
            if tag_core in relevant_tags:
                score += 3
            for rt in relevant_tags:
                # Partial match on tag words
                rt_words = set(rt.split("_"))
                tag_words = set(tag_core.split("_"))
                overlap = rt_words & tag_words
                if len(overlap) >= 2:
                    score += 1
        scored.append((score, p))

    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:max_packets]]


def format_doctrine_guidance(packets: list[dict]) -> str:
    """Format doctrine packets into operational guidance for the agent."""
    if not packets:
        return ""
    parts = ["STARTUP DOCTRINE GUIDANCE:"]
    for p in packets:
        parts.append(f"\n[{p['packet_id'].split('-')[-1] if '-' in p['packet_id'] else p['packet_id']}]")
        if p["claim"]:
            parts.append(f"  Principle: {p['claim'][:200]}")
        if p["mechanism"]:
            parts.append(f"  How: {p['mechanism'][:150]}")
        if p["boundary"]:
            parts.append(f"  Warning: {p['boundary'][:150]}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Doctrine-enhanced decision logic
# Uses baseline's calibrated thresholds + doctrine-informed reasoning
# ---------------------------------------------------------------------------

def _next_request_id(turn_index: int, action_index: int) -> str:
    return f"doctrine_req_{turn_index:03d}_{action_index:02d}"


def _doctrine_board_update(session: RuntimeSession, doctrine: list[dict]) -> dict:
    """Board update: baseline structure + doctrine-informed summaries."""
    finance = session.world_state.get("finance", {})
    customers = session.world_state.get("customers", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    product = session.world_state.get("product", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    board_update_count = int(governance.get("board_update_count", 0))

    # Default (from baseline)
    summary = "Protected long-horizon trust, delivery capacity, and financing optionality ahead of short-term narrative wins."
    asks = ["support sequencing quality and capacity investments before aggressive expansion"]

    # Doctrine-enhanced: inject YC wisdom into board framing
    if board_update_count == 0 and (
        int(product.get("major_incidents_open", 0)) > 0
        or float(operations.get("support_backlog", 0.0)) >= 34
    ):
        summary = "Doctrine: trust compounds, negligence compounds faster. Prioritized immediate reliability recovery and support stabilization before making new growth promises."
        asks = ["support incident recovery and service-quality sequencing before acceleration"]
    elif float(risk.get("financing_pressure", 0.0)) >= 0.72 or float(finance.get("runway_weeks", 999.0)) < 24:
        summary = "Doctrine: default alive or default dead. Grounded the board in liquidity reality, kept financing optionality open, and prioritized operating resilience over narrative expansion."
        asks = ["support a conservative financing posture and transparent runway planning"]
    elif board_update_count >= 1 and (
        float(customers.get("trust_score", 0.0)) < 0.7
        or float(operations.get("support_backlog", 0.0)) >= 24
        or float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0))) > 0.58
    ):
        summary = "Doctrine: you cannot grow your way out of a trust deficit. Sequenced customer trust recovery ahead of headline growth commitments."
        asks = ["support a trust-first operating plan until customer signals strengthen"]
    elif float(team.get("morale", 1.0)) < 0.6 or float(team.get("attrition_risk", 0.0)) > 0.52:
        summary = "Doctrine: startups die from internal dysfunction more often than external competition. Protected team durability so growth targets stay believable."
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


def _doctrine_incident_comms(session: RuntimeSession) -> dict:
    """Incident comms: baseline structure + doctrine insight."""
    customers = session.world_state.get("customers", {})
    operations = session.world_state.get("operations", {})
    product = session.world_state.get("product", {})
    risk = session.world_state.get("risk", {})

    trust_score = float(customers.get("trust_score", 1.0))
    support_backlog = float(operations.get("support_backlog", 0.0))
    major_incidents_open = int(product.get("major_incidents_open", 0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))

    summary = "Acknowledge the incident directly, explain the immediate containment path, and commit to a concrete next customer update."
    affected_segments = ["enterprise", "mid_market"]
    delivery_channels = ["status_page", "email"]
    support_path = "route priority accounts through the incident queue and customer success follow-up"
    next_update_hours = 6

    if trust_score < 0.62 or support_backlog >= 42:
        summary = "Doctrine: trust is rebuilt through over-communication, not silence. Direct customer-facing communication explaining the issue, current mitigation, and concrete support path."
        next_update_hours = 4
    elif major_incidents_open == 0 and financing_pressure > 0.8:
        summary = "Keep customer messaging factual and narrow so financial stress does not distort the external incident response."
        affected_segments = ["enterprise"]
        delivery_channels = ["email", "account_outreach"]
        next_update_hours = 8

    return {
        "summary": summary,
        "affected_segments": affected_segments,
        "delivery_channels": delivery_channels,
        "support_path": support_path,
        "next_update_hours": next_update_hours,
    }


def _doctrine_org_proposal(session: RuntimeSession) -> dict:
    """Org proposal: baseline structure + doctrine reasoning."""
    operations = session.world_state.get("operations", {})
    product = session.world_state.get("product", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})

    support_backlog = float(operations.get("support_backlog", 0.0))
    onboarding_quality = float(product.get("onboarding_quality", 1.0))
    bandwidth_load = float(team.get("bandwidth_load", 0.0))
    morale = float(team.get("morale", 1.0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))

    summary = "Doctrine: consolidate ownership before expanding scope. Single accountable manager for onboarding and support while leadership bench resets."
    target_function = "customer_ops"
    expected_morale_delta = 0.03
    expected_bandwidth_load_delta = -0.05
    expected_monthly_burn_change_usd = 4000.0

    if onboarding_quality < 0.58 and support_backlog < 52:
        summary = "Doctrine: fix the product before fixing the org. Reset product-delivery ownership so onboarding quality recovers before new roadmap commitments."
        target_function = "product"
        expected_morale_delta = 0.02
        expected_bandwidth_load_delta = -0.04
    elif financing_pressure > 0.72 and bandwidth_load > 0.88:
        summary = "Doctrine: don't add headcount to solve management problems. Clarify operating ownership and escalation paths so the company can stabilize without a costly reorg spiral."
        target_function = "operations"
        expected_morale_delta = 0.02
        expected_bandwidth_load_delta = -0.04
        expected_monthly_burn_change_usd = 0.0
    elif morale < 0.5 and bandwidth_load > 0.92:
        summary = "Doctrine: protect the builders. Create a temporary leadership bench rotation so manager load becomes explicit instead of leaking across the org."

    return {
        "summary": summary,
        "target_function": target_function,
        "expected_morale_delta": expected_morale_delta,
        "expected_bandwidth_load_delta": expected_bandwidth_load_delta,
        "expected_monthly_burn_change_usd": expected_monthly_burn_change_usd,
    }


def _doctrine_hiring_plan(session: RuntimeSession) -> dict:
    """Hiring plan: baseline calibration + doctrine wisdom."""
    team = session.world_state.get("team", {})
    hiring = team.get("hiring", {})
    operations = session.world_state.get("operations", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})

    open_roles = int(hiring.get("open_roles", team.get("open_roles", 0)))
    critical_roles_open = int(hiring.get("critical_roles_open", 0))
    bandwidth_load = float(team.get("bandwidth_load", 0.0))
    financing_pressure = float(risk.get("financing_pressure", 0.0))
    demand_index = float(market.get("demand_index", 1.0))
    support_backlog = float(operations.get("support_backlog", 0.0))

    summary = "Doctrine: hire for leverage, not headcount. Prioritize the most leveraged roles, keep pace tied to delivery relief."
    priority_roles = ["customer_ops_lead", "senior_engineer"]
    owner = "vp_ops"
    success_metrics = ["time_to_fill_under_8_weeks", "delivery_capacity_index_up", "support_backlog_down"]
    hiring_pace = "stage sourcing first, then move offers only on the top one or two roles"
    risk_guardrail = "do not add new noncritical roles until delivery capacity and cash visibility improve"

    if critical_roles_open > 1 or support_backlog >= 38:
        priority_roles = ["customer_ops_lead", "support_manager", "senior_engineer"]
        owner = "head_of_customer_ops"
    elif demand_index < 0.76 or financing_pressure >= 0.55:
        priority_roles = ["senior_engineer"]
        owner = "ceo"
        success_metrics = ["critical_role_filled", "bandwidth_load_down", "runway_weeks_stable"]
        hiring_pace = "advance one critical role at a time and defer broader expansion"
        risk_guardrail = "Doctrine: premature hiring burns cash and creates coordination overhead. Freeze discretionary hiring until demand and financing signals recover."
    elif bandwidth_load > 0.9:
        priority_roles = ["product_engineer", "customer_ops_lead"]
        owner = "vp_product"

    return {
        "summary": summary,
        "priority_roles": priority_roles,
        "owner": owner,
        "success_metrics": success_metrics,
        "hiring_pace": hiring_pace,
        "risk_guardrail": risk_guardrail,
        "open_roles": open_roles,
    }


def _doctrine_actions(session: RuntimeSession, doctrine: list[dict], *, turn_index: int) -> list[dict]:
    """Generate actions using baseline's calibrated thresholds + doctrine reasoning.

    Mirrors _heuristic_long_horizon_actions exactly but with doctrine-enhanced
    board updates, hiring plans, incident comms, and org proposals.
    """
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
    ai = 0

    # Always read metrics first
    actions.append({
        "tool_name": "metrics.report",
        "request_id": _next_request_id(turn_index, ai),
        "arguments": {},
    })
    ai += 1

    # Always read market
    actions.append({
        "tool_name": "research.market.read",
        "request_id": _next_request_id(turn_index, ai),
        "arguments": {},
    })
    ai += 1

    # Board track: read board state early
    if track == "board" and (turn_index == 0 or turn_index % 2 == 0):
        actions.append({
            "tool_name": "board.read",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {},
        })
        ai += 1

    # Finance: burn cut at runway < 28 (baseline calibration)
    if float(finance.get("runway_weeks", 999.0)) < 28 and not finance.get("last_plan_update"):
        actions.append({
            "tool_name": "finance.plan.write",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {"budget_changes": {"monthly_burn_usd": -20000}},
        })
        ai += 1

    # Finance: raise at runway < 18 or financing_pressure > 0.75 (baseline calibration)
    if float(finance.get("runway_weeks", 999.0)) < 18 or float(risk.get("financing_pressure", 0.0)) > 0.75:
        if not finance.get("last_raise_plan"):
            actions.append({
                "tool_name": "finance.raise.propose",
                "request_id": _next_request_id(turn_index, ai),
                "arguments": {
                    "raise_amount_usd": max(850000.0, float(finance.get("monthly_burn_usd", 0.0)) * 5.0),
                    "dilution_pct": 0.1,
                    "monthly_burn_change_usd": 0,
                    "financing_risk_reduction": 0.26,
                    "transaction_cost_usd": 24000,
                },
            })
            ai += 1

    # Treasury rebalance at concentration > 0.8 (baseline calibration)
    if float(finance.get("treasury_concentration", 0.0)) > 0.8:
        actions.append({
            "tool_name": "finance.treasury.rebalance",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {"target_concentration": 0.4, "rebalance_cost_usd": 7000},
        })
        ai += 1

    # Product: roadmap focus (baseline calibration)
    if (
        float(product.get("onboarding_quality", 0.0)) < 0.7
        or int(product.get("roadmap_items", 0)) > 7
        or float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0))) > 0.58
    ):
        actions.append({
            "tool_name": "product.roadmap.write",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {
                "roadmap_items_delta": -1,
                "onboarding_quality_delta": 0.08,
                "major_incidents_delta": 0,
                "budget_change_monthly_burn_usd": 4000,
            },
        })
        ai += 1

    # Incident response (baseline calibration + doctrine comms)
    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append({
            "tool_name": "ops.incident.respond",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {
                "incident_reduction": 1,
                "trust_recovery": 0.05,
                "churn_reduction": 0.008,
                "monthly_burn_increase_usd": 8500,
                "customer_comms_plan": _doctrine_incident_comms(session),
            },
        })
        ai += 1

    # Support backlog (baseline calibration)
    if float(operations.get("support_backlog", 0.0)) > 34 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.38:
        actions.append({
            "tool_name": "ops.support.resolve",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {
                "backlog_reduction": 18,
                "sla_risk_reduction": 0.18,
                "trust_recovery": 0.03,
                "churn_reduction": 0.005,
                "monthly_burn_increase_usd": 6500,
            },
        })
        ai += 1

    # Hiring (baseline calibration + doctrine plan)
    if int(hiring.get("open_roles", team.get("open_roles", 0))) > 0 and (
        float(team.get("bandwidth_load", 0.0)) > 0.74
        or float(team.get("delivery_capacity_index", 1.0)) < 0.62
        or int(hiring.get("critical_roles_open", 0)) > 0
    ):
        hp = _doctrine_hiring_plan(session)
        actions.append({
            "tool_name": "people.hiring.update",
            "request_id": _next_request_id(turn_index, ai),
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
                "hiring_plan": hp,
            },
        })
        ai += 1

    # Org proposal (doctrine-enhanced)
    if (
        "people.org.propose" in session.scenario.get("tools", [])
        and not team.get("last_org_proposal")
        and (
            track == "people"
            or float(team.get("morale", 1.0)) < 0.5
            or float(team.get("attrition_risk", 0.0)) > 0.6
            or float(team.get("bandwidth_load", 0.0)) > 0.9
        )
    ):
        actions.append({
            "tool_name": "people.org.propose",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": _doctrine_org_proposal(session),
        })
        ai += 1

    # Org adjust for morale/attrition (baseline calibration)
    if float(team.get("morale", 0.7)) < 0.58 or float(team.get("attrition_risk", 0.0)) > 0.52:
        actions.append({
            "tool_name": "people.org.adjust",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {
                "morale_delta": 0.07,
                "attrition_risk_delta": -0.1,
                "bandwidth_load_delta": -0.08,
                "monthly_burn_change_usd": 8000,
                "onboarding_quality_delta": 0.02,
            },
        })
        ai += 1

    # Sales pipeline maintenance (baseline calibration)
    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * 5.8:
        actions.append({
            "tool_name": "sales.pipeline.update",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {
                "pipeline_count_delta": 1,
                "weighted_pipeline_usd_delta": 55000 if float(market.get("demand_index", 1.0)) >= 0.76 else 40000,
            },
        })
        ai += 1

    # Pricing (baseline calibration)
    if (
        float(customers.get("trust_score", 0.0)) >= 0.76
        and float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0))) < 0.48
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.03
    ):
        actions.append({
            "tool_name": "sales.pricing.propose",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": {"price_change_pct": 0.02},
        })
        ai += 1

    # Board update (doctrine-enhanced)
    if turn_index % 2 == 0 or int(governance.get("board_update_count", 0)) == 0:
        actions.append({
            "tool_name": "board.update",
            "request_id": _next_request_id(turn_index, ai),
            "arguments": _doctrine_board_update(session, doctrine),
        })
        ai += 1

    # Advance sim
    actions.append({
        "tool_name": "sim.advance",
        "request_id": _next_request_id(turn_index, ai),
        "arguments": {"advance_by": 1, "unit": "week"},
    })

    return actions


# ---------------------------------------------------------------------------
# Main run function
# ---------------------------------------------------------------------------

def run_doctrine_agent(
    *,
    scenario_path: Path,
    seed: int = 1,
    max_turns: int | None = None,
    track: str = "",
) -> dict:
    """Run a doctrine-augmented agent on a startup-bench scenario."""
    scenario = load_scenario(scenario_path)
    declared_tools = set(scenario["tools"])
    horizon = int(scenario["metadata"]["time_horizon"]["length"])
    total_turns = max_turns if max_turns is not None else horizon
    total_turns = max(1, min(total_turns, horizon))

    # Load and select doctrine
    all_packets = load_doctrine_packets()
    if not track:
        track = scenario.get("metadata", {}).get("track", "general")
    doctrine = select_doctrine_for_track(all_packets, track)
    print(f"  Loaded {len(all_packets)} doctrine packets, selected {len(doctrine)} for track '{track}'")

    world_state = initialize_world_state(scenario, seed=seed)
    session = RuntimeSession(scenario=scenario, world_state=world_state)
    turns: list[dict] = []
    snapshots = [{"snapshot_id": "initial", "kind": "initial", "state": deepcopy(session.world_state)}]
    total_tool_calls = 0

    for turn_index in range(total_turns):
        before_time = session.world_state["sim"]["current_time"]
        observations = session.visible_observations()
        proposed = _doctrine_actions(session, doctrine, turn_index=turn_index)
        events: list[dict] = []
        actions: list[dict] = []

        for tool_call in proposed:
            if tool_call["tool_name"] not in declared_tools:
                continue
            response = execute_tool_call(session, tool_call)
            total_tool_calls += 1
            events.extend(response.get("result", {}).get("events_processed", []))
            actions.append({
                "tool_name": tool_call["tool_name"],
                "request_id": tool_call["request_id"],
                "arguments": tool_call.get("arguments", {}),
                "response": response,
                "status": "ok" if response.get("ok", False) else "error",
            })

        after_time = session.world_state["sim"]["current_time"]
        turns.append({
            "turn_index": turn_index,
            "sim_time_before": before_time,
            "sim_time_after": after_time,
            "observations": observations,
            "actions": actions,
            "events": events,
            "notes": [],
        })
        snapshots.append({
            "snapshot_id": f"turn_{turn_index}",
            "kind": "milestone",
            "state": deepcopy(session.world_state),
        })

    run_id = f"doctrine-{uuid4()}"
    final_snapshots = snapshots + [{"snapshot_id": "final", "kind": "final", "state": deepcopy(session.world_state)}]
    evaluation = evaluate_dry_run(
        scenario=scenario,
        world_state=session.world_state,
        trace_evidence={"turns": turns, "state_snapshots": final_snapshots},
    )
    trace = build_trace(
        scenario=scenario,
        seed=seed,
        run_id=run_id,
        model_id="doctrine_augmented_agent_v1",
        evaluation=evaluation,
        world_state=session.world_state,
    )
    trace["turns"] = turns

    score_report = build_score_report(
        scenario=scenario,
        evaluation=evaluation,
        run_id=run_id,
    )

    return {
        "trace": trace,
        "score_report": score_report,
        "evaluation": evaluation,
        "total_tool_calls": total_tool_calls,
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="run_doctrine_agent")
    parser.add_argument("scenario", type=Path, help="Path to scenario JSON")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--max-turns", type=int, default=None)
    parser.add_argument("--track", default="", help="Override scenario track")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    scenario_path = args.scenario
    if not scenario_path.is_absolute() and not scenario_path.exists():
        scenario_path = BENCH_ROOT / scenario_path

    result = run_doctrine_agent(
        scenario_path=scenario_path,
        seed=args.seed,
        max_turns=args.max_turns,
        track=args.track,
    )

    score = result["score_report"]
    print(f"\nScenario: {score.get('scenario_id', '?')}")
    print(f"Score: {score.get('scenario_score', 0):.2%}")
    print(f"Outcome: {score.get('outcome_score', 0):.2%}")
    print(f"Constraints: {score.get('constraint_score', 0):.2%}")
    print(f"Pass: {score.get('pass', False)}")
    print(f"Violations: {len(score.get('violations', []))}")
    print(f"Tool calls: {result['total_tool_calls']}")

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        sid = score.get("scenario_id", "unknown")
        (args.output_dir / f"{sid}_score.json").write_text(
            json.dumps(score, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (args.output_dir / f"{sid}_trace.json").write_text(
            json.dumps(result["trace"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    # Print subscore breakdown
    subscores = score.get("subscores", {})
    if subscores:
        print("\nSubscores:")
        for name, val in sorted(subscores.items()):
            if isinstance(val, (int, float)):
                print(f"  {name}: {val:.3f}")

    sys.stdout.flush()


if __name__ == "__main__":
    main()
