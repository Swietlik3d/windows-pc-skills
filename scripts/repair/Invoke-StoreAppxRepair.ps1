<#
.SYNOPSIS Scan-first controlled repair wrapper for store-appx-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-StoreAppxRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-StoreAppxRepair.ps1 -Mode Repair -Apply -Target 'specified-AppX-package' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='specified-AppX-package',
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
$steps=@('resolve exact package/current user','export package metadata','register its AppxManifest only','validate events and launch')
$rollback=@('restore from Store/approved package source','use prior package version only when supported')
$plan=New-WmRepairPlan -Operation 'store-appx-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply store-appx-repair (R2)')){
 try{
  if([string]::IsNullOrWhiteSpace($PackageName)){throw '-PackageName is required for Apply.'}
  $packages=@(Get-AppxPackage -Name $PackageName -ErrorAction Stop)
  if($packages.Count -ne 1){throw "Expected exactly one package; found $($packages.Count)."}
  Write-WmJson ($packages|Select-Object Name,PackageFullName,Version,InstallLocation,Status) (Join-Path $LogRoot 'package-before.json')
  $manifest=Join-Path $packages[0].InstallLocation 'AppxManifest.xml'
  Add-AppxPackage -DisableDevelopmentMode -Register $manifest -ErrorAction Stop
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='store-appx-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='store-appx-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='store-appx-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
