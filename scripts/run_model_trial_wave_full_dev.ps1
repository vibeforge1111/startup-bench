param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "gemini")]
    [string]$ModelId,

    [int]$Seed = 1
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$examplesRoot = Join-Path $repoRoot "examples"
$scriptRoot = Join-Path $repoRoot "tmp_model_trial_full_dev_scripts\$ModelId"
$runRoot = Join-Path $repoRoot "tmp_model_trial_full_dev_runs\$ModelId"
$suitePath = Join-Path $examplesRoot "dev_scenario_suite.json"

if (-not (Test-Path $suitePath)) {
    throw "Missing dev suite manifest: $suitePath"
}

$suite = Get-Content $suitePath -Raw | ConvertFrom-Json
$jobs = @()

foreach ($scenario in $suite.scenarios) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension([string]$scenario.path)
    $name = $stem -replace '^minimal_', '' -replace '_scenario$', ''
    $jobs += @{
        Name = $name
        Scenario = Join-Path $examplesRoot $scenario.path
        Script = Join-Path $scriptRoot "$name`_script.json"
        Output = Join-Path $runRoot $name
    }
}

foreach ($job in $jobs) {
    if (-not (Test-Path $job.Script)) {
        throw "Missing script file for $($job.Name): $($job.Script)"
    }

    New-Item -ItemType Directory -Force -Path $job.Output | Out-Null

    python -m thestartupbench run-script $job.Scenario $job.Script --seed $Seed --output-dir $job.Output
    if ($LASTEXITCODE -ne 0) {
        throw "run-script failed for $($job.Name) using model '$ModelId'"
    }
}

Write-Host "Completed full dev model trial for $ModelId"
Write-Host "Artifacts written under: $runRoot"
