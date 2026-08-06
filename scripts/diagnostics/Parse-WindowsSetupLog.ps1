<#
.SYNOPSIS Extracts phases, error codes and SetupDiag-like rule lines from copied Setup/Panther logs.
.EXAMPLE .\Parse-WindowsSetupLog.ps1 -Path .\tests\fixtures\logs\setuperr.log -OutputPath .\dist\setup.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path,[Parameter(Mandatory)][string]$OutputPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $Path).Path;$lines=[IO.File]::ReadAllLines($resolved)
$hits=@($lines|Where-Object{$_ -match '(?i)error|fail|0x[0-9a-f]{8}|downlevel|safe_os|first_boot|second_boot|compat|rule'})
$result=[ordered]@{file=(Split-Path -Leaf $resolved);sha256=(Get-FileHash $resolved -Algorithm SHA256).Hash.ToLowerInvariant();hits=@($hits|Select-Object -First 300);limitations='Parser does not replace Microsoft SetupDiag or full Panther correlation.'}
Write-WmJson $result $OutputPath;$result
