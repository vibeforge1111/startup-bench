from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


MISSING_SCENARIOS = [
    "minimal_launch_distribution_scenario.json",
    "minimal_growth_experiment_scenario.json",
    "minimal_finance_fundraise_reset_scenario.json",
    "minimal_people_leadership_scenario.json",
]


TOOL_GUIDE = {
    "metrics.query": 'Use arguments like {"metric_ids": ["cash_usd", "runway_weeks"]}.',
    "metrics.report": "Use empty arguments: {}.",
    "product.roadmap.read": "Use empty arguments: {}.",
    "product.roadmap.write": 'Use arguments like {"roadmap_items_delta": -1, "onboarding_quality_delta": 0.05, "major_incidents_delta": 0, "monthly_burn_change_usd": 8000}.',
    "product.launch": 'Use arguments like {"launch_name": "Focused partner launch", "monthly_revenue_delta_usd": 4000, "pipeline_count_delta": 1, "weighted_pipeline_usd_delta": 30000, "demand_index_delta": 0.03, "trust_delta": 0.01, "onboarding_quality_delta": 0.02, "support_backlog_delta": 8, "monthly_burn_change_usd": 6000, "major_incidents_delta": 0, "activation_delta": 0.03}.',
    "growth.experiment.create": 'Use arguments like {"experiment_id": "exp_launch_001", "experiment_name": "Guided launch cohort", "channel": "partners", "budget_change_monthly_burn_usd": 5000, "monthly_revenue_delta_usd": 1500, "pipeline_count_delta": 1, "weighted_pipeline_usd_delta": 20000, "demand_index_delta": 0.02, "trust_delta": 0.0, "activation_delta": 0.04}.',
    "growth.experiment.review": "Use empty arguments: {}.",
    "sales.pipeline.read": "Use empty arguments: {}.",
    "sales.pipeline.update": 'Use arguments like {"pipeline_count_delta": 1, "weighted_pipeline_usd_delta": 25000, "closed_won_revenue_delta_usd": 0}.',
    "ops.support.read": "Use empty arguments: {}.",
    "ops.support.resolve": 'Use arguments like {"backlog_reduction": 12, "sla_risk_reduction": 0.12, "trust_recovery": 0.03, "churn_reduction": 0.004, "monthly_burn_increase_usd": 7000}.',
    "finance.plan.read": "Use empty arguments: {}.",
    "finance.plan.write": 'Use arguments like {"budget_changes": {"monthly_burn_usd": -12000}}.',
    "finance.treasury.read": "Use empty arguments: {}.",
    "finance.treasury.rebalance": 'Use arguments like {"target_concentration": 0.4, "rebalance_cost_usd": 8000}.',
    "finance.raise.propose": 'Use arguments like {"raise_amount_usd": 700000, "dilution_pct": 0.05, "monthly_burn_change_usd": 0, "financing_risk_reduction": 0.24, "transaction_cost_usd": 14000, "trust_delta": 0.0}.',
    "people.hiring.read": "Use empty arguments: {}.",
    "people.hiring.update": 'Use arguments like {"sourced_candidates_delta": 2, "onsite_candidates_delta": 1, "offers_out_delta": 0, "accepted_hires": 0, "open_roles_delta": 1, "critical_roles_delta": 1, "monthly_burn_change_usd": 4000, "morale_delta": 0.0, "bandwidth_load_delta": 0.0, "support_backlog_delta": 0, "onboarding_quality_delta": 0.0, "hiring_plan": {"summary": "Backfill manager gap", "roles": ["support_manager"], "priority": "high"}}.',
    "people.org.read": "Use empty arguments: {}.",
    "people.org.propose": 'Use arguments like {"summary": "Clarify ownership and manager span", "target_function": "customer_success", "expected_morale_delta": 0.03, "expected_bandwidth_load_delta": -0.04, "expected_monthly_burn_change_usd": 6000}.',
    "people.org.adjust": 'Use arguments like {"morale_delta": 0.06, "attrition_risk_delta": -0.08, "bandwidth_load_delta": -0.07, "monthly_burn_change_usd": 9000, "onboarding_quality_delta": 0.03}.',
    "research.market.read": "Use empty arguments: {}.",
    "board.read": "Use empty arguments: {}.",
    "board.update": 'Use arguments like {"summary": "Tight launch sequencing until onboarding is stronger.", "forecast": {"monthly_burn_usd": 180000, "trust_score": 0.74}, "asks": ["Support the focused plan over broad rollout."]}.',
    "notes.read": "Use empty arguments: {}.",
    "notes.write": 'Use arguments like {"content": "Focused launch only after onboarding and support readiness improve."}.',
    "sim.advance": 'Use exactly {"advance_by": 1, "unit": "week"}.',
}


def _scenario_key(path_str: str) -> str:
    stem = Path(path_str).stem
    if stem.startswith("minimal_"):
        stem = stem[len("minimal_") :]
    if stem.endswith("_scenario"):
        stem = stem[: -len("_scenario")]
    return stem


def _normalize_json_output(raw_text: str) -> list[dict]:
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    payload = json.loads(text)
    if not isinstance(payload, list):
        raise ValueError("Provider output is not a JSON array.")
    return payload


def _build_prompt(*, scenario: dict, scenario_path: Path, repo_root: Path) -> str:
    key = _scenario_key(scenario_path.name)
    tools = scenario["tools"]
    guide_lines = "\n".join(f"- `{tool}`: {TOOL_GUIDE[tool]}" for tool in tools if tool in TOOL_GUIDE)
    scenario_json = json.dumps(scenario, indent=2)
    output_path = repo_root / "tmp_model_trial_full_dev_scripts" / "codex" / f"{key}_script.json"
    return (
        "You are generating a static TheStartupBench tool script.\n\n"
        "Return JSON only. Do not use markdown fences. Do not add explanation. Do not inspect any local repository files. "
        "Use only the scenario JSON and tool guide below.\n\n"
        "Task:\n"
        "Produce a valid JSON array of tool calls for exactly 4 weekly turns.\n\n"
        "Hard constraints:\n"
        "- Output must be a JSON array.\n"
        '- Each item must contain only "tool_name", "request_id", and "arguments".\n'
        "- Use only the tools declared by the scenario.\n"
        "- Use unique request_id values.\n"
        '- End each turn with one `sim.advance` call using {"advance_by": 1, "unit": "week"}.\n'
        "- No comments, no placeholders, no invented fields, no invented tools.\n"
        "- Prefer realistic sequencing: read state, make focused decisions, communicate if useful, then advance time.\n"
        "- Avoid rigid loops and avoid generic vanity-metric optimization.\n\n"
        "Tool guide:\n"
        f"{guide_lines}\n\n"
        f"Write the final JSON so it is valid to save at: {output_path}\n\n"
        "Scenario JSON:\n"
        "SCENARIO_JSON_START\n"
        f"{scenario_json}\n"
        "SCENARIO_JSON_END\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "scenario_files",
        nargs="*",
        help="Optional scenario filenames from examples/. Defaults to the four missing full-dev scenarios.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    examples_root = repo_root / "examples"
    scripts_root = repo_root / "tmp_model_trial_full_dev_scripts" / "codex"
    raw_root = repo_root / "tmp_model_trial_full_dev_raw" / "codex"
    sandbox_root = repo_root / "tmp_codex_prompt_only"
    scripts_root.mkdir(parents=True, exist_ok=True)
    raw_root.mkdir(parents=True, exist_ok=True)
    sandbox_root.mkdir(parents=True, exist_ok=True)

    report: dict[str, dict] = {"generated": {}}
    filenames = args.scenario_files or MISSING_SCENARIOS
    for filename in filenames:
        scenario_path = examples_root / filename
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        key = _scenario_key(filename)
        prompt = _build_prompt(scenario=scenario, scenario_path=scenario_path, repo_root=repo_root)
        prompt_path = raw_root / f"{key}_prompt.txt"
        output_path = raw_root / f"{key}_response.txt"
        prompt_path.write_text(prompt, encoding="utf-8")

        command = (
            f"Get-Content -Raw '{prompt_path}' | "
            f"codex exec --skip-git-repo-check --sandbox read-only -C '{sandbox_root}' -o '{output_path}' -"
        )
        result = subprocess.run(
            ["powershell", "-Command", command],
            text=True,
            capture_output=True,
            check=False,
            cwd=repo_root,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"codex invocation failed for {key} with exit code {result.returncode}.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )
        raw_output = output_path.read_text(encoding="utf-8")
        script = _normalize_json_output(raw_output)
        script_path = scripts_root / f"{key}_script.json"
        script_path.write_text(json.dumps(script, indent=2), encoding="utf-8")
        report["generated"][key] = {
            "scenario_id": scenario["metadata"]["scenario_id"],
            "script_path": str(script_path),
            "tool_call_count": len(script),
        }

    report_path = repo_root / "tmp_model_trial_full_dev_missing_codex_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "report_path": str(report_path), "generated": list(report["generated"].keys())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
