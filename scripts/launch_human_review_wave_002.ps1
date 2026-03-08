param(
    [string]$StudyManifestPath = "examples/operator_human_review_wave_002_manifest.json",

    [string]$RosterPath = "examples/reviewer_roster_template.csv",

    [string]$OutputDir = "tmp_human_wave_002"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

python -m thestartupbench run-calibration-study $StudyManifestPath --output-dir $OutputDir
python -m thestartupbench assign-reviewers $StudyManifestPath --study-run-dir $OutputDir --roster-path $RosterPath --output-dir $OutputDir
python -m thestartupbench export-review-forms "$OutputDir\review_assignments.json" --output-dir $OutputDir

Write-Host ""
Write-Host "Human review wave 002 launch complete."
Write-Host "Study run: $OutputDir\calibration_study_run.json"
Write-Host "Assignments: $OutputDir\review_assignments.json"
Write-Host "Exports: $OutputDir\review_form_export.json"
