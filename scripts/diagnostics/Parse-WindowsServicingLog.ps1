<#
.SYNOPSIS Parses CBS/DISM text metadata from a copied log or synthetic fixture.
.EXAMPLE .\Parse-WindowsServicingLog.ps1 -Path .\tests\fixtures\logs\CBS.log -OutputPath .\dist\cbs.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $Path).Path;$lines=[IO.File]::ReadAllLines($resolved)
$matchedLines=@($lines|Where-Object{$_ -match '(?i)error|corrupt|failed|0x[0-9a-f]{8}|repair'})
$summary=[ordered]@{path=(Split-Path -Leaf $resolved);sha256=(Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash.ToLowerInvariant();line_count=$lines.Count;matched_count=$matchedLines.Count;matches=@($matchedLines|Select-Object -First 250);limitations='Text triage only; context and matched source are required.'}
Write-WmJson $summary $OutputPath;$summary
