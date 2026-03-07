"""CLI entrypoint for TheStartupBench tooling."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .paths import examples_dir, repo_root, schemas_dir, spec_dir


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tsb", description="TheStartupBench reference tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the installed package version")
    subparsers.add_parser("paths", help="Print important repository paths")

    validate_parser = subparsers.add_parser("validate", help="Validate an artifact against a benchmark schema")
    validate_parser.add_argument("artifact_type", help="Artifact type, e.g. scenario, trace, submission")
    validate_parser.add_argument("path", help="Path to the JSON artifact")

    check_trace_parser = subparsers.add_parser("check-trace", help="Run structural integrity checks on a trace")
    check_trace_parser.add_argument("path", help="Path to the trace JSON file")

    manifest_parser = subparsers.add_parser("manifest", help="Generate the active tool manifest for a scenario")
    manifest_parser.add_argument("path", help="Path to the scenario JSON file")

    subparsers.add_parser("list-baselines", help="List built-in heuristic baselines")

    inspect_parser = subparsers.add_parser("inspect-scenario", help="Print selected scenario metadata")
    inspect_parser.add_argument("path", help="Path to the scenario JSON file")

    lint_parser = subparsers.add_parser("lint-scenario", help="Run authoring-time lint checks on a scenario")
    lint_parser.add_argument("path", help="Path to the scenario JSON file")

    run_parser = subparsers.add_parser("run-dry", help="Run a zero-action dry execution for a scenario")
    run_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    run_parser.add_argument("--seed", type=int, default=0, help="Seed used for the dry run")
    run_parser.add_argument("--output-dir", help="Optional directory to write trace and score report artifacts")

    script_parser = subparsers.add_parser("run-script", help="Execute a scripted sequence of tool calls")
    script_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    script_parser.add_argument("tool_calls_path", help="Path to the tool-call JSON array")
    script_parser.add_argument("--seed", type=int, default=0, help="Seed used for the scripted run")
    script_parser.add_argument("--output-dir", help="Optional directory to write trace and score report artifacts")

    baseline_parser = subparsers.add_parser("run-baseline", help="Execute a built-in heuristic baseline")
    baseline_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    baseline_parser.add_argument("baseline_id", help="Baseline id, e.g. heuristic_b2b_operator")
    baseline_parser.add_argument("--seed", type=int, default=0, help="Seed used for the baseline run")
    baseline_parser.add_argument("--max-turns", type=int, help="Optional cap on the number of simulated turns")
    baseline_parser.add_argument("--output-dir", help="Optional directory to write trace and score report artifacts")

    campaign_parser = subparsers.add_parser("run-campaign", help="Run repeated evaluations and aggregate results")
    campaign_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    campaign_parser.add_argument("runner_type", help="Runner type: dry, baseline, or script")
    campaign_parser.add_argument("--seeds", required=True, help="Comma-separated seed list, e.g. 1,2,3")
    campaign_parser.add_argument("--baseline-id", help="Baseline id when runner_type=baseline")
    campaign_parser.add_argument("--tool-calls-path", help="Tool script path when runner_type=script")
    campaign_parser.add_argument("--max-turns", type=int, help="Optional turn cap when runner_type=baseline")
    campaign_parser.add_argument("--output-dir", help="Optional directory to write the batch report artifact")

    suite_parser = subparsers.add_parser("run-suite", help="Run a scenario suite and aggregate across scenarios")
    suite_parser.add_argument("suite_path", help="Path to the scenario suite JSON file")
    suite_parser.add_argument("runner_type", help="Runner type: dry, baseline, or script")
    suite_parser.add_argument("--seeds", required=True, help="Comma-separated seed list, e.g. 1,2,3")
    suite_parser.add_argument("--baseline-id", help="Baseline id when runner_type=baseline")
    suite_parser.add_argument("--tool-calls-path", help="Tool script path when runner_type=script")
    suite_parser.add_argument("--max-turns", type=int, help="Optional turn cap when runner_type=baseline")
    suite_parser.add_argument("--output-dir", help="Optional directory to write the suite report artifact")

    redact_parser = subparsers.add_parser("redact-suite", help="Emit a public redacted manifest from a private suite")
    redact_parser.add_argument("suite_path", help="Path to the private scenario suite JSON file")
    redact_parser.add_argument("--output-dir", help="Optional directory to write the public manifest artifact")

    submission_parser = subparsers.add_parser("build-submission", help="Build a leaderboard submission from suite reports")
    submission_parser.add_argument("--suite-report-paths", required=True, help="Comma-separated suite report paths")
    submission_parser.add_argument("--model-id", required=True, help="Model id for the submission")
    submission_parser.add_argument("--provider", required=True, help="Model provider")
    submission_parser.add_argument("--contamination-flag", required=True, help="clean, possible_contamination, or known_contamination")
    submission_parser.add_argument("--contamination-notes", default="", help="Optional contamination notes")
    submission_parser.add_argument("--release-date", help="Optional model release date")
    submission_parser.add_argument("--source-url", help="Optional source or trace manifest URL")
    submission_parser.add_argument("--output-dir", help="Optional directory to write the submission artifact")

    return parser


def _cmd_paths() -> int:
    payload = {
        "repo_root": str(repo_root()),
        "schemas_dir": str(schemas_dir()),
        "examples_dir": str(examples_dir()),
        "spec_dir": str(spec_dir()),
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_validate(artifact_type: str, path: str) -> int:
    from .validation import validate_artifact_file

    result = validate_artifact_file(artifact_type=artifact_type, path=Path(path))
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_inspect_scenario(path: str) -> int:
    from .scenario_loader import load_scenario

    scenario = load_scenario(Path(path))
    metadata = scenario["metadata"]
    payload = {
        "scenario_id": metadata["scenario_id"],
        "scenario_version": metadata["scenario_version"],
        "benchmark_version": metadata["benchmark_version"],
        "track": metadata["track"],
        "mode": metadata["mode"],
        "title": metadata["title"],
        "summary": metadata["summary"],
        "tools": scenario["tools"],
        "observation_surface_count": len(scenario["observation_surfaces"]),
        "terminal_condition_count": len(scenario["terminal_conditions"]),
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_lint_scenario(path: str) -> int:
    from .scenario_lint import lint_scenario_file

    result = lint_scenario_file(Path(path))
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_check_trace(path: str) -> int:
    from .scenario_loader import load_json
    from .trace_validation import validate_trace_integrity
    from .validation import validate_instance

    trace = load_json(Path(path))
    schema_result = validate_instance(artifact_type="trace", instance=trace, path=Path(path))
    integrity_result = validate_trace_integrity(trace)
    payload = {
        "schema_validation": schema_result.to_dict(),
        "integrity_validation": integrity_result.to_dict(),
    }
    print(json.dumps(payload, indent=2))
    return 0 if schema_result.ok and integrity_result.ok else 1


def _cmd_manifest(path: str) -> int:
    from .scenario_loader import load_scenario
    from .tool_registry import tool_manifest_for_names
    from .validation import validate_instance

    scenario = load_scenario(Path(path))
    manifest = tool_manifest_for_names(scenario["tools"])
    validation = validate_instance(
        artifact_type="tool-manifest",
        instance=manifest,
        path=Path("tool_manifest.json"),
    )
    payload = {
        "manifest": manifest,
        "validation": validation.to_dict(),
    }
    print(json.dumps(payload, indent=2))
    return 0 if validation.ok else 1


def _cmd_list_baselines() -> int:
    from .baseline_runner import list_baselines

    print(json.dumps({"baselines": list_baselines()}, indent=2))
    return 0


def _cmd_run_dry(scenario_path: str, seed: int, output_dir: str | None) -> int:
    from .runner import run_dry_scenario

    result = run_dry_scenario(Path(scenario_path), seed=seed)
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "trace.json").write_text(json.dumps(result["trace"], indent=2), encoding="utf-8")
        (out_dir / "score_report.json").write_text(json.dumps(result["score_report"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_run_script(scenario_path: str, tool_calls_path: str, seed: int, output_dir: str | None) -> int:
    from .script_runner import run_tool_script

    result = run_tool_script(
        scenario_path=Path(scenario_path),
        tool_calls_path=Path(tool_calls_path),
        seed=seed,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "trace.json").write_text(json.dumps(result["trace"], indent=2), encoding="utf-8")
        (out_dir / "score_report.json").write_text(json.dumps(result["score_report"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_run_baseline(
    scenario_path: str,
    baseline_id: str,
    seed: int,
    max_turns: int | None,
    output_dir: str | None,
) -> int:
    from .baseline_runner import run_baseline

    result = run_baseline(
        scenario_path=Path(scenario_path),
        baseline_id=baseline_id,
        seed=seed,
        max_turns=max_turns,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "trace.json").write_text(json.dumps(result["trace"], indent=2), encoding="utf-8")
        (out_dir / "score_report.json").write_text(json.dumps(result["score_report"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_run_campaign(
    scenario_path: str,
    runner_type: str,
    seeds: str,
    baseline_id: str | None,
    tool_calls_path: str | None,
    max_turns: int | None,
    output_dir: str | None,
) -> int:
    from .campaign_runner import _parse_seeds, run_campaign

    result = run_campaign(
        scenario_path=Path(scenario_path),
        runner_type=runner_type,
        seeds=_parse_seeds(seeds),
        baseline_id=baseline_id,
        tool_calls_path=Path(tool_calls_path) if tool_calls_path else None,
        max_turns=max_turns,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "batch_report.json").write_text(json.dumps(result["batch_report"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_run_suite(
    suite_path: str,
    runner_type: str,
    seeds: str,
    baseline_id: str | None,
    tool_calls_path: str | None,
    max_turns: int | None,
    output_dir: str | None,
) -> int:
    from .campaign_runner import _parse_seeds
    from .suite_runner import run_suite

    result = run_suite(
        suite_path=Path(suite_path),
        runner_type=runner_type,
        seeds=_parse_seeds(seeds),
        baseline_id=baseline_id,
        tool_calls_path=Path(tool_calls_path) if tool_calls_path else None,
        max_turns=max_turns,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "suite_report.json").write_text(json.dumps(result["suite_report"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_redact_suite(suite_path: str, output_dir: str | None) -> int:
    from .suite_manifest import redact_suite_manifest

    result = redact_suite_manifest(Path(suite_path))
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "public_suite_manifest.json").write_text(json.dumps(result["manifest"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_build_submission(
    suite_report_paths: str,
    model_id: str,
    provider: str,
    contamination_flag: str,
    contamination_notes: str,
    release_date: str | None,
    source_url: str | None,
    output_dir: str | None,
) -> int:
    from .submission_builder import build_submission

    result = build_submission(
        suite_report_paths=[Path(path.strip()) for path in suite_report_paths.split(",") if path.strip()],
        model_id=model_id,
        provider=provider,
        contamination_flag=contamination_flag,
        contamination_notes=contamination_notes,
        release_date=release_date,
        source_url=source_url,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "submission.json").write_text(json.dumps(result["submission"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "paths":
        return _cmd_paths()
    if args.command == "validate":
        return _cmd_validate(args.artifact_type, args.path)
    if args.command == "check-trace":
        return _cmd_check_trace(args.path)
    if args.command == "manifest":
        return _cmd_manifest(args.path)
    if args.command == "list-baselines":
        return _cmd_list_baselines()
    if args.command == "inspect-scenario":
        return _cmd_inspect_scenario(args.path)
    if args.command == "lint-scenario":
        return _cmd_lint_scenario(args.path)
    if args.command == "run-dry":
        return _cmd_run_dry(args.scenario_path, args.seed, args.output_dir)
    if args.command == "run-script":
        return _cmd_run_script(args.scenario_path, args.tool_calls_path, args.seed, args.output_dir)
    if args.command == "run-baseline":
        return _cmd_run_baseline(
            args.scenario_path,
            args.baseline_id,
            args.seed,
            args.max_turns,
            args.output_dir,
        )
    if args.command == "run-campaign":
        return _cmd_run_campaign(
            args.scenario_path,
            args.runner_type,
            args.seeds,
            args.baseline_id,
            args.tool_calls_path,
            args.max_turns,
            args.output_dir,
        )
    if args.command == "run-suite":
        return _cmd_run_suite(
            args.suite_path,
            args.runner_type,
            args.seeds,
            args.baseline_id,
            args.tool_calls_path,
            args.max_turns,
            args.output_dir,
        )
    if args.command == "redact-suite":
        return _cmd_redact_suite(args.suite_path, args.output_dir)
    if args.command == "build-submission":
        return _cmd_build_submission(
            args.suite_report_paths,
            args.model_id,
            args.provider,
            args.contamination_flag,
            args.contamination_notes,
            args.release_date,
            args.source_url,
            args.output_dir,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
