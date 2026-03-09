from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


SCENARIOS = {
    "crisis": {
        "path": "examples/minimal_crisis_scenario.json",
        "goal": "trust stabilization and disciplined crisis handling",
    },
    "product": {
        "path": "examples/minimal_product_scenario.json",
        "goal": "early quality stabilization and support-capacity discipline",
    },
    "finance": {
        "path": "examples/minimal_finance_scenario.json",
        "goal": "liquidity protection, treasury risk control, and financing discipline",
    },
}


def _build_prompt(*, model_id: str, scenario_key: str, scenario: dict, repo_root: Path) -> str:
    output_path = repo_root / "tmp_model_trial_wave_001_scripts" / model_id / f"{scenario_key}_script.json"
    scenario_json = json.dumps(scenario, indent=2)
    return (
        "You are generating a static TheStartupBench tool script.\n\n"
        "Your task is to produce a valid JSON array of tool calls for exactly 4 weekly turns for one scenario.\n\n"
        "Important:\n"
        "- Return JSON only.\n"
        "- Do not use markdown fences.\n"
        "- Do not add explanation before or after the JSON.\n"
        "- Do not call tools live.\n"
        "- Do not simulate outputs.\n"
        "- You are only writing the tool-call script that will later be executed by the benchmark runner.\n\n"
        "Goal:\n"
        f"Write a high-quality startup-operator policy for this scenario that is strategically coherent, adaptive, and benchmark-valid for {SCENARIOS[scenario_key]['goal']}.\n\n"
        "Hard constraints:\n"
        "- Output must be a JSON array.\n"
        "- Each element must be an object with:\n"
        '  - "tool_name"\n'
        '  - "request_id"\n'
        '  - "arguments"\n'
        "- Use only tools declared by the scenario.\n"
        "- Use unique request_id values.\n"
        "- Plan exactly 4 weekly turns.\n"
        '- End each turn with exactly one:\n'
        '  - "tool_name": "sim.advance"\n'
        '  - "arguments": { "advance_by": 1, "unit": "week" }\n'
        "- No comments.\n"
        "- No placeholder values.\n"
        "- No invented fields.\n"
        "- No invented tools.\n"
        "- Prefer a realistic operator sequence:\n"
        "  - read state\n"
        "  - make targeted decisions\n"
        "  - communicate when appropriate\n"
        "  - advance time\n"
        "- Avoid rigid or repetitive no-op loops.\n"
        "- Make decisions that fit the scenario's actual risks and tradeoffs.\n\n"
        "Quality bar:\n"
        "- React to the scenario's core risk, not generic startup behavior.\n"
        "- Use the runtime's actual argument names instead of invented wrappers.\n"
        "- Use board updates only when they add real informational value.\n"
        "- Use notes only if they capture genuine operating intent.\n"
        "- Protect survival, trust, and strategic coherence, not just vanity metrics.\n"
        "- Avoid obviously gameable behavior like mechanical pipeline padding during trust or liquidity crises.\n\n"
        f"Target output path after generation: {output_path}\n\n"
        "Use this scenario:\n"
        "SCENARIO_JSON_START\n"
        f"{scenario_json}\n"
        "SCENARIO_JSON_END\n"
    )


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
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Tool script contains a non-object item.")
        for required_key in ("tool_name", "request_id", "arguments"):
            if required_key not in item:
                raise ValueError(f"Tool script item is missing '{required_key}'.")
    return payload


def _run_provider(*, model_id: str, prompt: str, repo_root: Path) -> str:
    prompt_path = repo_root / "tmp_model_trial_wave_001_raw" / model_id / "_prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    if model_id == "codex":
        codex_output_path = repo_root / "tmp_model_trial_wave_001_raw" / model_id / "_last_message.txt"
        command = (
            f"Get-Content -Raw '{prompt_path}' | "
            f"codex exec --sandbox read-only -C '{repo_root}' -o '{codex_output_path}' -"
        )
        result = subprocess.run(
            ["powershell", "-Command", command],
            text=True,
            capture_output=True,
            check=False,
            cwd=repo_root,
        )
    elif model_id == "claude":
        command = (
            f"Get-Content -Raw '{prompt_path}' | "
            "claude --print --permission-mode plan --output-format text -"
        )
        result = subprocess.run(
            ["powershell", "-Command", command],
            text=True,
            capture_output=True,
            check=False,
            cwd=repo_root,
        )
    elif model_id == "gemini":
        command = (
            f"Get-Content -Raw '{prompt_path}' | "
            "gemini --prompt - --approval-mode plan --output-format text"
        )
        result = subprocess.run(
            ["powershell", "-Command", command],
            text=True,
            capture_output=True,
            check=False,
            cwd=repo_root,
        )
    else:
        raise ValueError(f"Unsupported model id: {model_id}")

    if result.returncode != 0:
        raise RuntimeError(
            f"{model_id} invocation failed with exit code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    if model_id == "codex":
        output = codex_output_path.read_text(encoding="utf-8").strip()
    else:
        output = result.stdout.strip()
    if not output:
        raise RuntimeError(f"{model_id} returned empty output.")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        default="codex,claude,gemini",
        help="Comma-separated model ids to run.",
    )
    parser.add_argument(
        "--run-wave",
        action="store_true",
        help="Run scripts/run_model_trial_wave_001.ps1 after generating scripts for each model.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    raw_root = repo_root / "tmp_model_trial_wave_001_raw"
    scripts_root = repo_root / "tmp_model_trial_wave_001_scripts"
    raw_root.mkdir(parents=True, exist_ok=True)
    scripts_root.mkdir(parents=True, exist_ok=True)

    report: dict[str, dict] = {"models": {}}
    for model_id in [item.strip() for item in args.models.split(",") if item.strip()]:
        model_raw_root = raw_root / model_id
        model_scripts_root = scripts_root / model_id
        model_raw_root.mkdir(parents=True, exist_ok=True)
        model_scripts_root.mkdir(parents=True, exist_ok=True)
        model_report = {"scenarios": {}, "run_wave": None}

        for scenario_key, scenario_config in SCENARIOS.items():
            scenario_path = repo_root / scenario_config["path"]
            scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
            prompt = _build_prompt(model_id=model_id, scenario_key=scenario_key, scenario=scenario, repo_root=repo_root)
            raw_output = _run_provider(model_id=model_id, prompt=prompt, repo_root=repo_root)

            raw_output_path = model_raw_root / f"{scenario_key}_response.txt"
            raw_output_path.write_text(raw_output, encoding="utf-8")

            script = _normalize_json_output(raw_output)
            script_path = model_scripts_root / f"{scenario_key}_script.json"
            script_path.write_text(json.dumps(script, indent=2), encoding="utf-8")
            model_report["scenarios"][scenario_key] = {
                "scenario_path": str(scenario_path),
                "raw_output_path": str(raw_output_path),
                "script_path": str(script_path),
                "tool_call_count": len(script),
            }

        if args.run_wave:
            cmd = [
                "powershell",
                "-File",
                "scripts/run_model_trial_wave_001.ps1",
                "-ModelId",
                model_id,
            ]
            result = subprocess.run(
                cmd,
                text=True,
                capture_output=True,
                check=False,
                cwd=repo_root,
            )
            model_report["run_wave"] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
            if result.returncode != 0:
                raise RuntimeError(
                    f"Wave run failed for {model_id}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
                )

        report["models"][model_id] = model_report

    report_path = repo_root / "tmp_model_trial_wave_001_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "report_path": str(report_path), "models": list(report["models"].keys())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
