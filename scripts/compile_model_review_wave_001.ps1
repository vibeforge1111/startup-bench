param(
    [Parameter(Mandatory = $true)]
    [string]$RawReviewsDir,

    [string]$StudyManifestPath = "examples/operator_model_review_wave_001_manifest.json",

    [string]$StudyRunDir = "tmp_model_review_wave_001",

    [string]$ImportDir = "tmp_model_review_wave_001_results/import",

    [string]$ReportDir = "tmp_model_review_wave_001_results/report"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $RawReviewsDir)) {
    throw "Raw reviews directory not found: $RawReviewsDir"
}

if (-not (Test-Path $StudyRunDir)) {
    throw "Study run directory not found: $StudyRunDir"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

python -m thestartupbench import-model-reviews $RawReviewsDir --output-dir $ImportDir

$reviewJsonPaths = Get-ChildItem -Path $ImportDir -Filter *.json -File |
    Where-Object { $_.Name -ne "model_review_import.json" } |
    ForEach-Object { $_.FullName }

if (-not $reviewJsonPaths -or $reviewJsonPaths.Count -eq 0) {
    throw "No imported operator-review JSON files found in $ImportDir"
}

$compileArgs = @(
    "-m", "thestartupbench", "compile-calibration-study",
    $StudyManifestPath,
    "--study-run-dir", $StudyRunDir,
    "--output-dir", $ReportDir,
    "--review-paths", ($reviewJsonPaths -join ",")
)

python @compileArgs

Write-Host ""
Write-Host "Completed model review wave 001 compilation."
Write-Host "Imported reviews: $ImportDir"
Write-Host "Study report: $ReportDir"
