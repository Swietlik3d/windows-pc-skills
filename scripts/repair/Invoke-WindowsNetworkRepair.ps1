<#
.SYNOPSIS Scan-first controlled repair wrapper for windows-network-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-WindowsNetworkRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-WindowsNetworkRepair.ps1 -Mode Repair -Apply -Target 'online-Windows-network-stack' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='online-Windows-network-stack',
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
$steps=@('export adapters/routes/DNS/proxy','reset Winsock catalog','reset TCP/IP with log','reboot gate','layered validation')
$rollback=@('restore static IP/DNS/proxy/routes from snapshot','reinstall approved VPN/filter client if required')
$plan=New-WmRepairPlan -Operation 'windows-network-repair' -RiskClass 'R2' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R2' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply windows-network-repair (R2)')){
 try{
  Get-NetIPConfiguration|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $LogRoot 'ip-before.json') -Encoding utf8
  & "$env:SystemRoot\System32\netsh.exe" winsock reset
  if($LASTEXITCODE -ne 0){throw "Winsock reset failed: $LASTEXITCODE"}
  & "$env:SystemRoot\System32\netsh.exe" int ip reset (Join-Path $LogRoot 'netsh-ip-reset.log')
  if($LASTEXITCODE -ne 0){throw "TCP/IP reset failed: $LASTEXITCODE"}
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-network-repair';target=$Target;risk='R2';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='windows-network-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='windows-network-repair';target=$Target;risk='R2';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
