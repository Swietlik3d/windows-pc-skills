<#
.SYNOPSIS Scan-first controlled repair wrapper for vss-backup-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-VssBackupRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-VssBackupRepair.ps1 -Mode Repair -Apply -Target 'specified-VSS-writer-service' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='specified-VSS-writer-service',
 [Parameter(Mandatory)][string]$LogRoot,
 [string]$Confirmation,
 [string]$PackageName,
 [string]$ProfileSid,
 [string]$PublishedName,
 [string]$ServiceName,
 [switch]$Synthetic
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$steps=@('capture writers/providers/events','restart only mapped failed writer service','run application-aware backup','restore one file')
$rollback=@('restore original service start state','re-enable vendor provider','do not delete existing shadows')
$plan=New-WmRepairPlan -Operation 'vss-backup-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply vss-backup-repair (R2)')){
 try{
  if([string]::IsNullOrWhiteSpace($ServiceName)){throw '-ServiceName is required for Apply.'}
  $allowed=@('VSS','swprv','SQLWriter','CryptSvc')
  if($ServiceName -notin $allowed){throw "ServiceName is not in reviewed allow-list: $($allowed -join ', ')"}
  $before=Get-Service -Name $ServiceName|Select-Object Name,Status,StartType
  Write-WmJson $before (Join-Path $LogRoot 'vss-service-before.json')
  Restart-Service -Name $ServiceName -Force -ErrorAction Stop
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='vss-backup-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='vss-backup-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='vss-backup-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
