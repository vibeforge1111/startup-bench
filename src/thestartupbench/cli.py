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
    suite_parser.add_argument("--profile-path", help="Optional official evaluation profile path; emits a run manifest when used with --output-dir")
    suite_parser.add_argument("--output-dir", help="Optional directory to write the suite report artifact")

    official_profile_parser = subparsers.add_parser("show-official-profile", help="Print a validated official evaluation profile")
    official_profile_parser.add_argument("path", nargs="?", default="examples/official_eval_profile.json", help="Path to the official evaluation profile JSON file")

    run_manifest_parser = subparsers.add_parser("emit-run-manifest", help="Emit a validated run manifest for an official evaluation")
    run_manifest_parser.add_argument("suite_path", help="Path to the scenario suite JSON file")
    run_manifest_parser.add_argument("runner_type", help="Runner type: baseline or script")
    run_manifest_parser.add_argument("--seeds", required=True, help="Comma-separated seed list, e.g. 1,2,3,4,5")
    run_manifest_parser.add_argument("--baseline-id", help="Baseline id when runner_type=baseline")
    run_manifest_parser.add_argument("--tool-calls-path", help="Tool script path when runner_type=script")
    run_manifest_parser.add_argument("--max-turns", type=int, help="Optional turn cap; defaults to the profile default")
    run_manifest_parser.add_argument("--profile-path", default="examples/official_eval_profile.json", help="Official evaluation profile JSON path")
    run_manifest_parser.add_argument("--output-dir", help="Optional directory to write the run manifest artifact")

    redact_parser = subparsers.add_parser("redact-suite", help="Emit a public redacted manifest from a private suite")
    redact_parser.add_argument("suite_path", help="Path to the private scenario suite JSON file")
    redact_parser.add_argument("--output-dir", help="Optional directory to write the public manifest artifact")

    promote_parser = subparsers.add_parser("promote-suite", help="Clone a suite into a new split/pack version")
    promote_parser.add_argument("suite_path", help="Path to the source scenario suite JSON file")
    promote_parser.add_argument("--split", required=True, choices=["dev", "test", "fresh"], help="Target split")
    promote_parser.add_argument("--scenario-pack-version", required=True, help="Target scenario pack version")
    promote_parser.add_argument(
        "--allow-split-clone",
        action="store_true",
        help="Allow draft-only cloning into hidden splits. Official hidden packs should use distinct scenarios instead.",
    )
    promote_parser.add_argument("--output-dir", help="Optional directory to write the promoted suite artifact")

    family_parser = subparsers.add_parser("check-suite-family", help="Check hidden suite families for duplicated ids or files")
    family_parser.add_argument("suite_paths", nargs="+", help="Two or more scenario suite JSON paths")

    changelog_parser = subparsers.add_parser("check-pack-changelog", help="Validate a public pack lifecycle changelog")
    changelog_parser.add_argument("path", help="Path to the pack changelog JSON file")

    submission_parser = subparsers.add_parser("build-submission", help="Build a leaderboard submission from suite reports")
    submission_parser.add_argument("--suite-report-paths", required=True, help="Comma-separated suite report paths")
    submission_parser.add_argument("--model-id", required=True, help="Model id for the submission")
    submission_parser.add_argument("--provider", required=True, help="Model provider")
    submission_parser.add_argument("--contamination-flag", required=True, help="clean, possible_contamination, or known_contamination")
    submission_parser.add_argument("--contamination-notes", default="", help="Optional contamination notes")
    submission_parser.add_argument("--release-date", help="Optional model release date")
    submission_parser.add_argument("--source-url", help="Optional source or trace manifest URL")
    submission_parser.add_argument("--output-dir", help="Optional directory to write the submission artifact")

    review_parser = subparsers.add_parser("aggregate-operator-reviews", help="Aggregate operator review artifacts into a calibration summary")
    review_parser.add_argument("review_paths", help="Comma-separated operator review JSON paths")
    review_parser.add_argument("--output-dir", help="Optional directory to write the operator review summary artifact")

    calibration_parser = subparsers.add_parser("build-calibration-report", help="Compare operator reviews against a suite report")
    calibration_parser.add_argument("--suite-report-path", required=True, help="Path to a suite report JSON artifact")
    calibration_parser.add_argument("--review-paths", required=True, help="Comma-separated operator review JSON paths")
    calibration_parser.add_argument("--output-dir", help="Optional directory to write the calibration report artifact")

    study_run_parser = subparsers.add_parser("run-calibration-study", help="Run all calibration-study targets and emit review packets")
    study_run_parser.add_argument("study_manifest_path", help="Path to a calibration-study JSON manifest")
    study_run_parser.add_argument("--output-dir", required=True, help="Directory to write study run artifacts")

    study_compile_parser = subparsers.add_parser("compile-calibration-study", help="Compile operator reviews into a study-level calibration report")
    study_compile_parser.add_argument("study_manifest_path", help="Path to a calibration-study JSON manifest")
    study_compile_parser.add_argument("--study-run-dir", required=True, help="Directory containing calibration study run artifacts")
    study_compile_parser.add_argument("--review-paths", required=True, help="Comma-separated operator review JSON paths")
    study_compile_parser.add_argument("--output-dir", required=True, help="Directory to write calibration study report artifacts")

    assign_parser = subparsers.add_parser("assign-reviewers", help="Assign reviewers from a roster to a calibration study run")
    assign_parser.add_argument("study_manifest_path", help="Path to a calibration-study JSON manifest")
    assign_parser.add_argument("--study-run-dir", required=True, help="Directory containing calibration study run artifacts")
    assign_parser.add_argument("--roster-path", required=True, help="CSV roster path")
    assign_parser.add_argument("--output-dir", required=True, help="Directory to write assignment artifacts")

    export_forms_parser = subparsers.add_parser("export-review-forms", help="Export reviewer-facing markdown and CSV forms from assignments")
    export_forms_parser.add_argument("assignment_manifest_path", help="Path to a review assignment manifest JSON file")
    export_forms_parser.add_argument("--output-dir", required=True, help="Directory to write reviewer-facing forms")

    import_forms_parser = subparsers.add_parser("import-review-forms", help="Import completed reviewer CSV forms into operator-review JSON artifacts")
    import_forms_parser.add_argument("forms_dir", help="Directory containing completed review_form.csv files")
    import_forms_parser.add_argument("--output-dir", required=True, help="Directory to write imported operator-review JSON artifacts")

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
    profile_path: str | None,
    output_dir: str | None,
) -> int:
    from .campaign_runner import _parse_seeds
    from .official_eval import build_run_manifest
    from .suite_runner import run_suite

    parsed_seeds = _parse_seeds(seeds)
    result = run_suite(
        suite_path=Path(suite_path),
        runner_type=runner_type,
        seeds=parsed_seeds,
        baseline_id=baseline_id,
        tool_calls_path=Path(tool_calls_path) if tool_calls_path else None,
        max_turns=max_turns,
    )
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "suite_report.json").write_text(json.dumps(result["suite_report"], indent=2), encoding="utf-8")
        if profile_path:
            try:
                manifest_result = build_run_manifest(
                    suite_path=Path(suite_path),
                    profile_path=Path(profile_path),
                    runner_type=runner_type,
                    seeds=parsed_seeds,
                    baseline_id=baseline_id,
                    tool_calls_path=Path(tool_calls_path) if tool_calls_path else None,
                    max_turns=max_turns,
                )
            except ValueError as exc:
                print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
                return 1
            (out_dir / "run_manifest.json").write_text(json.dumps(manifest_result["run_manifest"], indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_show_official_profile(path: str) -> int:
    from .official_eval import load_official_eval_profile
    from .validation import validate_instance

    profile = load_official_eval_profile(Path(path))
    validation = validate_instance(
        artifact_type="official-eval-profile",
        instance=profile,
        path=Path(path),
    )
    print(json.dumps({"profile": profile, "validation": validation.to_dict()}, indent=2))
    return 0 if validation.ok else 1


def _cmd_emit_run_manifest(
    suite_path: str,
    runner_type: str,
    seeds: str,
    baseline_id: str | None,
    tool_calls_path: str | None,
    max_turns: int | None,
    profile_path: str,
    output_dir: str | None,
) -> int:
    from .campaign_runner import _parse_seeds
    from .official_eval import build_run_manifest

    try:
        result = build_run_manifest(
            suite_path=Path(suite_path),
            profile_path=Path(profile_path),
            runner_type=runner_type,
            seeds=_parse_seeds(seeds),
            baseline_id=baseline_id,
            tool_calls_path=Path(tool_calls_path) if tool_calls_path else None,
            max_turns=max_turns,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "run_manifest.json").write_text(json.dumps(result["run_manifest"], indent=2), encoding="utf-8")
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


def _cmd_promote_suite(
    suite_path: str,
    split: str,
    scenario_pack_version: str,
    allow_split_clone: bool,
    output_dir: str | None,
) -> int:
    from .pack_ops import promote_suite_pack

    try:
        result = promote_suite_pack(
            Path(suite_path),
            split=split,
            scenario_pack_version=scenario_pack_version,
            allow_split_clone=allow_split_clone,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "scenario_suite.json").write_text(json.dumps(result["suite"], indent=2), encoding="utf-8")
        if "public_manifest" in result:
            (out_dir / "public_suite_manifest.json").write_text(
                json.dumps(result["public_manifest"], indent=2),
                encoding="utf-8",
            )
    print(json.dumps(result, indent=2))
    suite_ok = result["validation"]["ok"]
    manifest_ok = result.get("public_manifest_validation", {}).get("ok", True)
    return 0 if suite_ok and manifest_ok else 1


def _cmd_check_suite_family(suite_paths: list[str]) -> int:
    from .pack_ops import validate_suite_family

    result = validate_suite_family([Path(path) for path in suite_paths])
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def _cmd_check_pack_changelog(path: str) -> int:
    from .pack_ops import validate_pack_changelog

    result = validate_pack_changelog(Path(path))
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


def _cmd_aggregate_operator_reviews(review_paths: str, output_dir: str | None) -> int:
    from .human_eval import aggregate_operator_reviews

    result = aggregate_operator_reviews(
        [Path(path.strip()) for path in review_paths.split(",") if path.strip()]
    )
    if output_dir and result["summary"] is not None:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "operator_review_summary.json").write_text(
            json.dumps(result["summary"], indent=2),
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_build_calibration_report(
    suite_report_path: str,
    review_paths: str,
    output_dir: str | None,
) -> int:
    from .calibration import build_calibration_report

    result = build_calibration_report(
        suite_report_path=Path(suite_report_path),
        review_paths=[Path(path.strip()) for path in review_paths.split(",") if path.strip()],
    )
    if output_dir and result["report"] is not None:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "calibration_report.json").write_text(
            json.dumps(result["report"], indent=2),
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_run_calibration_study(study_manifest_path: str, output_dir: str) -> int:
    from .study_runner import run_calibration_study

    result = run_calibration_study(
        study_manifest_path=Path(study_manifest_path),
        output_dir=Path(output_dir),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_compile_calibration_study(
    study_manifest_path: str,
    study_run_dir: str,
    review_paths: str,
    output_dir: str,
) -> int:
    from .study_runner import compile_calibration_study

    result = compile_calibration_study(
        study_manifest_path=Path(study_manifest_path),
        study_run_dir=Path(study_run_dir),
        review_paths=[Path(path.strip()) for path in review_paths.split(",") if path.strip()],
        output_dir=Path(output_dir),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_assign_reviewers(
    study_manifest_path: str,
    study_run_dir: str,
    roster_path: str,
    output_dir: str,
) -> int:
    from .reviewer_ops import assign_reviewer_taskforce

    result = assign_reviewer_taskforce(
        study_manifest_path=Path(study_manifest_path),
        study_run_dir=Path(study_run_dir),
        roster_path=Path(roster_path),
        output_dir=Path(output_dir),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_export_review_forms(assignment_manifest_path: str, output_dir: str) -> int:
    from .reviewer_ops import export_review_forms

    result = export_review_forms(
        assignment_manifest_path=Path(assignment_manifest_path),
        output_dir=Path(output_dir),
    )
    print(json.dumps(result, indent=2))
    return 0 if result["validation"]["ok"] else 1


def _cmd_import_review_forms(forms_dir: str, output_dir: str) -> int:
    from .reviewer_ops import import_review_forms

    result = import_review_forms(
        forms_dir=Path(forms_dir),
        output_dir=Path(output_dir),
    )
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
            args.profile_path,
            args.output_dir,
        )
    if args.command == "show-official-profile":
        return _cmd_show_official_profile(args.path)
    if args.command == "emit-run-manifest":
        return _cmd_emit_run_manifest(
            args.suite_path,
            args.runner_type,
            args.seeds,
            args.baseline_id,
            args.tool_calls_path,
            args.max_turns,
            args.profile_path,
            args.output_dir,
        )
    if args.command == "redact-suite":
        return _cmd_redact_suite(args.suite_path, args.output_dir)
    if args.command == "promote-suite":
        return _cmd_promote_suite(
            args.suite_path,
            args.split,
            args.scenario_pack_version,
            args.allow_split_clone,
            args.output_dir,
        )
    if args.command == "check-suite-family":
        return _cmd_check_suite_family(args.suite_paths)
    if args.command == "check-pack-changelog":
        return _cmd_check_pack_changelog(args.path)
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
    if args.command == "aggregate-operator-reviews":
        return _cmd_aggregate_operator_reviews(args.review_paths, args.output_dir)
    if args.command == "build-calibration-report":
        return _cmd_build_calibration_report(
            args.suite_report_path,
            args.review_paths,
            args.output_dir,
        )
    if args.command == "run-calibration-study":
        return _cmd_run_calibration_study(args.study_manifest_path, args.output_dir)
    if args.command == "compile-calibration-study":
        return _cmd_compile_calibration_study(
            args.study_manifest_path,
            args.study_run_dir,
            args.review_paths,
            args.output_dir,
        )
    if args.command == "assign-reviewers":
        return _cmd_assign_reviewers(
            args.study_manifest_path,
            args.study_run_dir,
            args.roster_path,
            args.output_dir,
        )
    if args.command == "export-review-forms":
        return _cmd_export_review_forms(args.assignment_manifest_path, args.output_dir)
    if args.command == "import-review-forms":
        return _cmd_import_review_forms(args.forms_dir, args.output_dir)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
