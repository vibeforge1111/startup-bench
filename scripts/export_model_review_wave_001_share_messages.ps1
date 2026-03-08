param(
    [ValidateSet("claude", "gemini")]
    [string]$Provider,

    [string]$ProviderPacketsDir = "tmp_model_review_wave_001_provider_packets",

    [string]$OutputDir = "tmp_model_review_wave_001_share_messages"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$packetsRoot = Join-Path $repoRoot $ProviderPacketsDir
$shareRoot = Join-Path $repoRoot $OutputDir

$providers = @()
if ($Provider) {
    $providers = @($Provider)
} else {
    $providers = @("claude", "gemini")
}

foreach ($activeProvider in $providers) {
    $providerManifestPath = Join-Path $packetsRoot "$activeProvider\provider_prompt_export.json"
    if (-not (Test-Path $providerManifestPath)) {
        throw "Provider packet manifest not found: $providerManifestPath"
    }

    $providerManifest = Get-Content $providerManifestPath -Raw | ConvertFrom-Json
    $providerOutputDir = Join-Path $shareRoot $activeProvider
    New-Item -ItemType Directory -Force -Path $providerOutputDir | Out-Null

    $shareEntries = @()

    foreach ($bundle in $providerManifest.bundles) {
        $promptPath = Join-Path $repoRoot $bundle.prompt_path
        if (-not (Test-Path $promptPath)) {
            throw "Prompt file not found: $promptPath"
        }

        $shareFileName = "{0}__{1}__share_prompt.txt" -f $activeProvider, $bundle.scenario_id
        $shareFilePath = Join-Path $providerOutputDir $shareFileName

        $header = @"
Paste everything below into $activeProvider as a single message.

Scenario: $($bundle.scenario_id)
Track: $($bundle.track)
Reviewer ID: $($bundle.reviewer_id)

----- BEGIN COPY -----

"@

        $body = Get-Content $promptPath -Raw
        $footer = @"

----- END COPY -----
"@

        Set-Content -Path $shareFilePath -Value ($header + $body + $footer) -Encoding utf8

        $shareEntries += [ordered]@{
            scenario_id = $bundle.scenario_id
            track = $bundle.track
            reviewer_id = $bundle.reviewer_id
            share_prompt_path = $shareFilePath
        }
    }

    $shareManifest = [ordered]@{
        export_version = "0.1.0"
        study_id = $providerManifest.study_id
        provider = $activeProvider
        reviewer_id = $providerManifest.reviewer_id
        bundle_count = $shareEntries.Count
        share_messages = $shareEntries
    }

    $shareManifestPath = Join-Path $providerOutputDir "share_prompt_export.json"
    $shareManifest | ConvertTo-Json -Depth 6 | Set-Content -Path $shareManifestPath -Encoding utf8

    Write-Host "Share messages exported to: $providerOutputDir"
    Write-Host "Manifest: $shareManifestPath"
}
