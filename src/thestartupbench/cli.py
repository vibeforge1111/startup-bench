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

    inspect_parser = subparsers.add_parser("inspect-scenario", help="Print selected scenario metadata")
    inspect_parser.add_argument("path", help="Path to the scenario JSON file")

    run_parser = subparsers.add_parser("run-dry", help="Run a zero-action dry execution for a scenario")
    run_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    run_parser.add_argument("--seed", type=int, default=0, help="Seed used for the dry run")
    run_parser.add_argument("--output-dir", help="Optional directory to write trace and score report artifacts")

    script_parser = subparsers.add_parser("run-script", help="Execute a scripted sequence of tool calls")
    script_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    script_parser.add_argument("tool_calls_path", help="Path to the tool-call JSON array")
    script_parser.add_argument("--seed", type=int, default=0, help="Seed used for the scripted run")
    script_parser.add_argument("--output-dir", help="Optional directory to write trace and score report artifacts")

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
    if args.command == "inspect-scenario":
        return _cmd_inspect_scenario(args.path)
    if args.command == "run-dry":
        return _cmd_run_dry(args.scenario_path, args.seed, args.output_dir)
    if args.command == "run-script":
        return _cmd_run_script(args.scenario_path, args.tool_calls_path, args.seed, args.output_dir)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
