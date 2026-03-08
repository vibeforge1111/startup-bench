param(
    [string]$StudyManifestPath = "examples/operator_model_review_wave_001_manifest.json",

    [string]$OutputDir = "tmp_model_review_wave_001",

    [string]$BundleDir = "tmp_model_review_wave_001_bundles"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

python -m thestartupbench run-calibration-study $StudyManifestPath --output-dir $OutputDir
python -m thestartupbench export-model-review-bundles $OutputDir --output-dir $BundleDir

Write-Host ""
Write-Host "Model review wave 001 launch complete."
Write-Host "Study run: $OutputDir\calibration_study_run.json"
Write-Host "Prompt export: $BundleDir\model_review_prompt_export.json"
