<#
.SYNOPSIS Scan-first controlled repair wrapper for print-spooler-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-PrintSpoolerRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-PrintSpoolerRepair.ps1 -Mode Repair -Apply -Target 'local-print-spooler' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='local-print-spooler',
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
$steps=@('export queue/driver/port state','stop Spooler','move stuck spool files to quarantine','start Spooler','test page')
$rollback=@('stop Spooler','move quarantined files back only when compatible','start Spooler')
$plan=New-WmRepairPlan -Operation 'print-spooler-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply print-spooler-repair (R2)')){
 try{
  $queue=Get-Printer -ErrorAction SilentlyContinue|Select-Object Name,DriverName,PortName,PrinterStatus
  Write-WmJson $queue (Join-Path $LogRoot 'printers-before.json')
  Stop-Service -Name Spooler -Force -ErrorAction Stop
  $spool=Join-Path $env:SystemRoot 'System32\spool\PRINTERS'
  $quarantine=Join-Path $LogRoot ('spool-quarantine-'+(Get-Date -Format 'yyyyMMddHHmmss'))
  New-Item -ItemType Directory -Path $quarantine -Force|Out-Null
  Get-ChildItem -LiteralPath $spool -File -ErrorAction SilentlyContinue|Move-Item -Destination $quarantine
  Start-Service -Name Spooler -ErrorAction Stop
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='print-spooler-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='print-spooler-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='print-spooler-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
