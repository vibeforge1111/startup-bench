param(
    [Parameter(Mandatory = $true)]
    [string]$CompletedFormsDir,

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

$reviewJsonPaths = Get-ChildItem -Path $ImportDir -Filter *.json -File | ForEach-Object { $_.FullName }

if (-not $reviewJsonPaths -or $reviewJsonPaths.Count -eq 0) {
    throw "No imported review JSON files found in $ImportDir"
}

$compileArgs = @(
    "-m", "thestartupbench", "compile-calibration-study",
    "$StudyRunDir\calibration_study_run.json",
    "--output-dir", $ReportDir,
    "--review-paths"
) + $reviewJsonPaths

python @compileArgs

Write-Host ""
Write-Host "Completed human review wave 002 compilation."
Write-Host "Imported reviews: $ImportDir"
Write-Host "Study report: $ReportDir"
