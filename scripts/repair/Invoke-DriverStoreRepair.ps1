<#
.SYNOPSIS Scan-first controlled repair wrapper for driver-store-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-DriverStoreRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-DriverStoreRepair.ps1 -Mode Repair -Apply -Target 'explicit-published-OEM-INF' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='explicit-published-OEM-INF',
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
$steps=@('verify device/hardware ID/provider/version','export driver package','check boot-critical dependency','remove exact published name','install matched OEM package')
$rollback=@('reinstall exported/matched signed OEM INF','boot Safe Mode/WinRE if boot regression')
$plan=New-WmRepairPlan -Operation 'driver-store-repair' -RiskClass 'R3' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R3' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply driver-store-repair (R3)')){
 try{
  if($PublishedName -notmatch '^oem\d+\.inf$'){throw 'PublishedName must be exact oemNN.inf.'}
  & "$env:SystemRoot\System32\pnputil.exe" /enum-drivers|Set-Content -LiteralPath (Join-Path $LogRoot 'drivers-before.txt') -Encoding utf8
  & "$env:SystemRoot\System32\pnputil.exe" /delete-driver $PublishedName /uninstall
  if($LASTEXITCODE -ne 0){throw "PnPUtil delete-driver failed: $LASTEXITCODE"}
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='driver-store-repair';target=$Target;risk='R3';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='driver-store-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='driver-store-repair';target=$Target;risk='R3';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
