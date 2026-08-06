<#
.SYNOPSIS Scan-first controlled repair wrapper for windows-component-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-WindowsComponentRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-WindowsComponentRepair.ps1 -Mode Repair -Apply -Target 'online-Windows-component-store' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='online-Windows-component-store',
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
$steps=@('DISM ScanHealth','DISM RestoreHealth after source validation','SFC scannow once','parse CBS/DISM')
$rollback=@('use matched repair media/in-place repair if store cannot be restored','restore pre-change image for regression')
$plan=New-WmRepairPlan -Operation 'windows-component-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply windows-component-repair (R2)')){
 try{
  & "$env:SystemRoot\System32\dism.exe" /Online /Cleanup-Image /RestoreHealth
  if($LASTEXITCODE -ne 0){throw "DISM RestoreHealth failed: $LASTEXITCODE"}
  & "$env:SystemRoot\System32\sfc.exe" /scannow
  if($LASTEXITCODE -notin @(0,1)){throw "SFC failed: $LASTEXITCODE"}
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-component-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='windows-component-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-component-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
