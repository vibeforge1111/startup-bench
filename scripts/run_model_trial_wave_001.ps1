param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "gemini")]
    [string]$ModelId
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptRoot = Join-Path $repoRoot "tmp_model_trial_wave_001_scripts\$ModelId"
$runRoot = Join-Path $repoRoot "tmp_model_trial_wave_001_runs\$ModelId"

$jobs = @(
    @{
        Name = "crisis"
        Scenario = Join-Path $repoRoot "examples\minimal_crisis_scenario.json"
        Script = Join-Path $scriptRoot "crisis_script.json"
        Output = Join-Path $runRoot "crisis"
    },
    @{
        Name = "product"
        Scenario = Join-Path $repoRoot "examples\minimal_product_scenario.json"
        Script = Join-Path $scriptRoot "product_script.json"
        Output = Join-Path $runRoot "product"
    },
    @{
        Name = "finance"
        Scenario = Join-Path $repoRoot "examples\minimal_finance_scenario.json"
        Script = Join-Path $scriptRoot "finance_script.json"
        Output = Join-Path $runRoot "finance"
    }
)

foreach ($job in $jobs) {
    if (-not (Test-Path $job.Script)) {
        throw "Missing script file for $($job.Name): $($job.Script)"
    }

    New-Item -ItemType Directory -Force -Path $job.Output | Out-Null

    python -m thestartupbench run-script $job.Scenario $job.Script --seed 1 --output-dir $job.Output
    if ($LASTEXITCODE -ne 0) {
        throw "run-script failed for $($job.Name) using model '$ModelId'"
    }
}

Write-Host "Completed model trial wave 001 for $ModelId"
Write-Host "Artifacts written under: $runRoot"
