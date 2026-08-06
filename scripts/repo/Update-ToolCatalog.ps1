<#
.SYNOPSIS Checks official tool pages as metadata and writes a review-only diff report.
.EXAMPLE .\Update-ToolCatalog.ps1 -WhatIf
.EXAMPLE .\Update-ToolCatalog.ps1 -Fetch -OutputPath .\dist\research\tool-diff.json
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([switch]$Fetch,[string]$OutputPath,[int]$MaxTools=20)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$catalog=Get-Content -LiteralPath (Join-Path $repo 'tools\catalog.yaml') -Raw|ConvertFrom-Json
$targets=@($catalog|Where-Object status -in @('active','unknown')|Select-Object -First $MaxTools)
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');count=$targets.Count;mode='metadata-diff-only';auto_accept=$false;tool_ids=@($targets.id)}
if(-not $Fetch){[pscustomobject]$plan;return}
if(-not $OutputPath){throw '-OutputPath is required with -Fetch.'}
if(-not $PSCmdlet.ShouldProcess($OutputPath,'Check official pages and write review report')){return [pscustomobject]$plan}
$report=[ordered]@{metadata=$plan;checks=@()}
foreach($tool in $targets){
 try{$response=Invoke-WebRequest -Uri $tool.official_home -Method Head -MaximumRedirection 5 -TimeoutSec 30;$report.checks+=[ordered]@{id=$tool.id;url=$tool.official_home;status=[int]$response.StatusCode;checked_utc=[DateTime]::UtcNow.ToString('o');catalog_version=$tool.current_version}}
 catch{$report.checks+=[ordered]@{id=$tool.id;url=$tool.official_home;status='error';message=$_.Exception.Message}}
}
New-Item -ItemType Directory -Path (Split-Path -Parent $OutputPath) -Force|Out-Null
$report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $OutputPath -Encoding utf8
[pscustomobject]$report
