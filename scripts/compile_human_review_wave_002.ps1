param(
    [Parameter(Mandatory = $true)]
    [string]$CompletedFormsDir,

    [string]$StudyManifestPath = "examples/operator_human_review_wave_002_manifest.json",

    [string]$StudyRunDir = "tmp_human_wave_002",

    [string]$ImportDir = "tmp_human_wave_002_results/import",

    [string]$ReportDir = "tmp_human_wave_002_results/report"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $CompletedFormsDir)) {
    throw "Completed forms directory not found: $CompletedFormsDir"
}

if (-not (Test-Path $StudyRunDir)) {
    throw "Study run directory not found: $StudyRunDir"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

python -m thestartupbench import-review-forms $CompletedFormsDir --output-dir $ImportDir

$reviewJsonPaths = Get-ChildItem -Path $ImportDir -Filter *.json -File |
    Where-Object { $_.Name -ne "review_form_import.json" } |
    ForEach-Object { $_.FullName }

if (-not $reviewJsonPaths -or $reviewJsonPaths.Count -eq 0) {
    throw "No imported review JSON files found in $ImportDir"
}

$reviewPathBlock = ($reviewJsonPaths | ForEach-Object { $_ }) -join "`n"
$pythonScript = @"
import json
from pathlib import Path
from thestartupbench.study_runner import compile_calibration_study

review_paths = [Path(path) for path in r'''$reviewPathBlock'''.splitlines() if path.strip()]
result = compile_calibration_study(
    study_manifest_path=Path(r'''$StudyManifestPath'''),
    study_run_dir=Path(r'''$StudyRunDir'''),
    review_paths=review_paths,
    output_dir=Path(r'''$ReportDir'''),
)
print(json.dumps(result, indent=2))
"@

python -c $pythonScript

Write-Host ""
Write-Host "Completed human review wave 002 compilation."
Write-Host "Imported reviews: $ImportDir"
Write-Host "Study report: $ReportDir"
