<#
.SYNOPSIS Generates a service-media plan; it never downloads assets or writes a USB device.
.EXAMPLE .\New-ServiceMediaPlan.ps1 -ManifestPath .\tools\manifests\service-media.yaml -OutputPath .\dist\service-media-plan.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$ManifestPath,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$manifest=Get-Content -LiteralPath (Resolve-Path -LiteralPath $ManifestPath) -Raw|ConvertFrom-Json
$adkRoots=@(@("${env:ProgramFiles(x86)}\Windows Kits\10\Assessment and Deployment Kit","$env:ProgramFiles\Windows Kits\10\Assessment and Deployment Kit")|Where-Object{$_ -and(Test-Path -LiteralPath $_)})
$plan=[ordered]@{created_utc=[DateTime]::UtcNow.ToString('o');mode='plan-only';adk_detected=@($adkRoots);winpe_build_allowed=($adkRoots.Count -gt 0);architectures=@('x64','ARM64');directories=$manifest.directories;items=$manifest.items;gates=@('review ADK page and security patch','exact USB UniqueId before R4 write','license acceptance','hash/signature verification');downloads_performed=0;usb_writes_performed=0}
$plan|ConvertTo-Json -Depth 12|Set-Content -LiteralPath $OutputPath -Encoding utf8
$plan
