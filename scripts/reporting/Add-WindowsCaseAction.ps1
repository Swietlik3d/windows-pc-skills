<#
.SYNOPSIS Appends an immutable-style JSONL action record to a service case.
.EXAMPLE .\Add-WindowsCaseAction.ps1 -CasePath .\cases\x -Purpose inventory -RiskClass R0 -Result observed -Rollback not-applicable
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Low')]
param(
    [Parameter(Mandatory)][string]$CasePath,
    [Parameter(Mandatory)][string]$Purpose,
    [Parameter(Mandatory)][ValidateSet('R0','R1','R2','R3','R4')][string]$RiskClass,
    [string]$Operator=$env:USERNAME,
    [string]$CommandOrTool='manual-observation',
    [string]$Target='case',
    [Parameter(Mandatory)][ValidateSet('observed','not-observed','inconclusive','blocked','success','failed')][string]$Result,
    [Parameter(Mandatory)][string]$Rollback,
    [string[]]$Artifacts=@()
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$resolved=(Resolve-Path -LiteralPath $CasePath).Path
if(-not(Test-Path -LiteralPath (Join-Path $resolved 'intake.yaml'))){throw 'Not a service case.'}
$hashes=@()
foreach($artifact in $Artifacts){if(Test-Path -LiteralPath $artifact){$h=Get-FileHash -LiteralPath $artifact -Algorithm SHA256;$hashes+=[ordered]@{path=$artifact;sha256=$h.Hash.ToLowerInvariant()}}}
$record=[ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operator=$Operator;purpose=$Purpose;risk_class=$RiskClass;command_or_tool=$CommandOrTool;target=$Target;result=$Result;rollback=$Rollback;artifacts=$hashes}
if($PSCmdlet.ShouldProcess((Join-Path $resolved 'actions.jsonl'),'Append case action')){Add-WmJsonLine $record (Join-Path $resolved 'actions.jsonl');Add-WmJsonLine ([ordered]@{timestamp_utc=$record.timestamp_utc;event='action-recorded';purpose=$Purpose}) (Join-Path $resolved 'timeline.jsonl')}
$record
