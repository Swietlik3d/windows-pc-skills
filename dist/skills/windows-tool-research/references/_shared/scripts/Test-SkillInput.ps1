<#
.SYNOPSIS Validates a JSON input envelope against the minimum safety gates shared by packaged skills.
.EXAMPLE .\Test-SkillInput.ps1 -Path .\input.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$input=Get-Content -LiteralPath (Resolve-Path -LiteralPath $Path) -Raw|ConvertFrom-Json
$required=@('boot_state','backup_status','encryption_status','managed_status','data_value')
$missing=@($required|Where-Object{$input.PSObject.Properties.Name -notcontains $_})
[pscustomobject]@{valid=($missing.Count -eq 0);missing=$missing;rule='Do not advance to R2+ when any gate is unknown.'}
if($missing.Count){exit 2}
