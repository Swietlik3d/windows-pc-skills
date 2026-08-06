<#
.SYNOPSIS Scan-first controlled repair wrapper for windows-update-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-WindowsUpdateRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-WindowsUpdateRepair.ps1 -Mode Repair -Apply -Target 'online-Windows-Update-components' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='online-Windows-Update-components',
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
$steps=@('capture update health and policy','stop exact update services','rename cache to dated backup','start services','scan update')
$rollback=@('stop services','restore renamed SoftwareDistribution/Catroot2 only if new cache is removed and target matches','start services')
$plan=New-WmRepairPlan -Operation 'windows-update-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply windows-update-repair (R2)')){
 try{
  $stamp=Get-Date -Format 'yyyyMMddHHmmss'
  $services=@('bits','wuauserv','cryptsvc')
  $serviceState=Get-Service -Name $services|Select-Object Name,Status,StartType
  Write-WmJson $serviceState (Join-Path $LogRoot 'services-before.json')
  foreach($service in $services){Stop-Service -Name $service -Force -ErrorAction Stop}
  $sd=Join-Path $env:SystemRoot 'SoftwareDistribution'
  $cr=Join-Path $env:SystemRoot 'System32\catroot2'
  if(Test-Path -LiteralPath $sd){Rename-Item -LiteralPath $sd -NewName "SoftwareDistribution.wmbackup.$stamp"}
  if(Test-Path -LiteralPath $cr){Rename-Item -LiteralPath $cr -NewName "catroot2.wmbackup.$stamp"}
  foreach($service in @('cryptsvc','wuauserv','bits')){Start-Service -Name $service -ErrorAction Stop}
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-update-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='windows-update-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-update-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
