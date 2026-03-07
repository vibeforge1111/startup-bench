param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "gemini")]
    [string]$ModelId,

    [int]$Seed = 1
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptRoot = Join-Path $repoRoot "tmp_model_trial_full_dev_scripts\$ModelId"
$runRoot = Join-Path $repoRoot "tmp_model_trial_full_dev_runs\$ModelId"

$jobs = @(
    @{
        Name = "0to1"
        Scenario = Join-Path $repoRoot "examples\minimal_0to1_scenario.json"
        Script = Join-Path $scriptRoot "0to1_script.json"
        Output = Join-Path $runRoot "0to1"
    },
    @{
        Name = "b2b_saas"
        Scenario = Join-Path $repoRoot "examples\minimal_b2b_saas_scenario.json"
        Script = Join-Path $scriptRoot "b2b_saas_script.json"
        Output = Join-Path $runRoot "b2b_saas"
    },
    @{
        Name = "board"
        Scenario = Join-Path $repoRoot "examples\minimal_board_scenario.json"
        Script = Join-Path $scriptRoot "board_script.json"
        Output = Join-Path $runRoot "board"
    },
    @{
        Name = "crisis"
        Scenario = Join-Path $repoRoot "examples\minimal_crisis_scenario.json"
        Script = Join-Path $scriptRoot "crisis_script.json"
        Output = Join-Path $runRoot "crisis"
    },
    @{
        Name = "scale"
        Scenario = Join-Path $repoRoot "examples\minimal_scale_scenario.json"
        Script = Join-Path $scriptRoot "scale_script.json"
        Output = Join-Path $runRoot "scale"
    },
    @{
        Name = "gtm"
        Scenario = Join-Path $repoRoot "examples\minimal_gtm_scenario.json"
        Script = Join-Path $scriptRoot "gtm_script.json"
        Output = Join-Path $runRoot "gtm"
    },
    @{
        Name = "finance"
        Scenario = Join-Path $repoRoot "examples\minimal_finance_scenario.json"
        Script = Join-Path $scriptRoot "finance_script.json"
        Output = Join-Path $runRoot "finance"
    },
    @{
        Name = "people"
        Scenario = Join-Path $repoRoot "examples\minimal_people_scenario.json"
        Script = Join-Path $scriptRoot "people_script.json"
        Output = Join-Path $runRoot "people"
    },
    @{
        Name = "product"
        Scenario = Join-Path $repoRoot "examples\minimal_product_scenario.json"
        Script = Join-Path $scriptRoot "product_script.json"
        Output = Join-Path $runRoot "product"
    }
)

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
