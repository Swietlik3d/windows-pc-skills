<#
.SYNOPSIS Stages official Windows release metadata for review; it never overwrites the accepted matrix.
.EXAMPLE .\Update-WindowsKnowledgeBase.ps1 -WhatIf
.EXAMPLE .\Update-WindowsKnowledgeBase.ps1 -Fetch -OutputPath .\dist\research\windows-candidate.json
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([switch]$Fetch,[string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$urls=@(
 'https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information',
 'https://learn.microsoft.com/en-us/windows/release-health/release-information',
 'https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install',
 'https://learn.microsoft.com/en-us/troubleshoot/windows-client/windows-security/update-secure-boot-certificates'
)
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');sources=$urls;accepted_matrix='knowledge-base/os/windows-release-matrix.yaml';mode='candidate-diff-only';auto_accept=$false}
if(-not $Fetch){[pscustomobject]$plan;return}
if(-not $OutputPath){throw '-OutputPath is required with -Fetch.'}
if(-not $PSCmdlet.ShouldProcess($OutputPath,'Fetch official HTML metadata to review candidate')){return [pscustomobject]$plan}
$candidate=[ordered]@{metadata=$plan;pages=@()}
foreach($url in $urls){
 try{$response=Invoke-WebRequest -Uri $url -MaximumRedirection 5 -TimeoutSec 45;$candidate.pages+=[ordered]@{url=$url;status=[int]$response.StatusCode;bytes=$response.RawContentLength;sha256=(Get-WmStringSha256 -Text $response.Content);retrieved_utc=[DateTime]::UtcNow.ToString('o')}}
 catch{$candidate.pages+=[ordered]@{url=$url;status='error';message=$_.Exception.Message}}
}
New-Item -ItemType Directory -Path (Split-Path -Parent $OutputPath) -Force|Out-Null
$candidate|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $OutputPath -Encoding utf8
[pscustomobject]$candidate
