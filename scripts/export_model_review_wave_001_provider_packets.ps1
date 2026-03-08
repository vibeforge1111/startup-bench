param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("claude", "gemini")]
    [string]$Provider,

    [string]$BundleManifestPath = "tmp_model_review_wave_001_bundles/model_review_prompt_export.json",

    [string]$OutputDir = "tmp_model_review_wave_001_provider_packets"
)

$ErrorActionPreference = "Stop"

$providerReviewerId = switch ($Provider) {
    "claude" { "claude_reviewer_001" }
    "gemini" { "gemini_reviewer_001" }
    default { throw "Unsupported provider: $Provider" }
}

function Get-RepoRelativePath {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    $baseUri = New-Object System.Uri((Resolve-Path $BasePath).Path + [System.IO.Path]::DirectorySeparatorChar)
    $targetUri = New-Object System.Uri((Resolve-Path $TargetPath).Path)
    $relativeUri = $baseUri.MakeRelativeUri($targetUri)
    return [System.Uri]::UnescapeDataString($relativeUri.ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot $BundleManifestPath
$rootOutputDir = Join-Path $repoRoot $OutputDir
$providerOutputDir = Join-Path $rootOutputDir $Provider

if (-not (Test-Path $manifestPath)) {
    throw "Bundle manifest not found: $manifestPath"
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path $providerOutputDir | Out-Null

$exportedBundles = @()

foreach ($bundle in $manifest.bundles) {
    $promptPath = Join-Path $repoRoot $bundle.prompt_path
    $contextPath = Join-Path $repoRoot $bundle.context_path
    $templatePath = Join-Path $repoRoot $bundle.template_path

    if (-not (Test-Path $promptPath)) {
        throw "Prompt file not found: $promptPath"
    }
    if (-not (Test-Path $contextPath)) {
        throw "Context file not found: $contextPath"
    }
    if (-not (Test-Path $templatePath)) {
        throw "Template file not found: $templatePath"
    }

    $bundleDir = Join-Path $providerOutputDir $bundle.scenario_id
    New-Item -ItemType Directory -Force -Path $bundleDir | Out-Null

    $promptText = Get-Content $promptPath -Raw
    $templateText = Get-Content $templatePath -Raw

    $assignedHeader = @"
# Assigned lane

- provider: $Provider
- reviewer_id: $providerReviewerId

Use this reviewer id in the returned JSON.

"@

    $providerPrompt = $assignedHeader + ($promptText -replace "__REVIEWER_ID__", $providerReviewerId)
    $providerTemplate = $templateText -replace "__REVIEWER_ID__", $providerReviewerId

    $providerPromptPath = Join-Path $bundleDir "prompt.md"
    $providerTemplatePath = Join-Path $bundleDir "review_template.json"
    $providerContextPath = Join-Path $bundleDir "context.json"

    Set-Content -Path $providerPromptPath -Value $providerPrompt -Encoding utf8
    Set-Content -Path $providerTemplatePath -Value $providerTemplate -Encoding utf8
    Copy-Item -Path $contextPath -Destination $providerContextPath -Force

    $exportedBundles += [ordered]@{
        bundle_id = $bundle.bundle_id
        scenario_id = $bundle.scenario_id
        track = $bundle.track
        prompt_path = Get-RepoRelativePath -BasePath $repoRoot -TargetPath $providerPromptPath
        context_path = Get-RepoRelativePath -BasePath $repoRoot -TargetPath $providerContextPath
        template_path = Get-RepoRelativePath -BasePath $repoRoot -TargetPath $providerTemplatePath
        reviewer_id = $providerReviewerId
    }
}

$result = [ordered]@{
    export_version = "0.1.0"
    study_id = $manifest.study_id
    provider = $Provider
    reviewer_id = $providerReviewerId
    bundle_count = $exportedBundles.Count
    bundles = $exportedBundles
}

$manifestOutPath = Join-Path $providerOutputDir "provider_prompt_export.json"
$result | ConvertTo-Json -Depth 6 | Set-Content -Path $manifestOutPath -Encoding utf8

Write-Host "Provider packets exported to: $providerOutputDir"
Write-Host "Manifest: $manifestOutPath"
