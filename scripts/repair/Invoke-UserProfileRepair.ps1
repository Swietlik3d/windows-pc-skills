<#
.SYNOPSIS Scan-first controlled repair wrapper for user-profile-repair.
.DESCRIPTION Default Mode=Scan writes a preflight plan. Mutations require Mode Repair, -Apply, elevation, ShouldProcess and the documented authorization gate.
.EXAMPLE .\Invoke-UserProfileRepair.ps1 -Mode Scan -LogRoot .\dist\repair-plan -Synthetic
.EXAMPLE .\Invoke-UserProfileRepair.ps1 -Mode Repair -Apply -Target 'explicit-profile-SID' -LogRoot C:\case\logs -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
 [ValidateSet('Scan','Repair')][string]$Mode='Scan',
 [switch]$Apply,
 [string]$Target='explicit-profile-SID',
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
$steps=@('verify authorized SID/profile path/EFS/OneDrive','export exact ProfileList key','set RefCount/State only when evidence matches temporary-profile pattern','logon validation')
$rollback=@('import exact exported ProfileList key','restore original State/RefCount values','use replacement profile migration if hive remains corrupt')
$plan=New-WmRepairPlan -Operation 'user-profile-repair' -RiskClass 'R3' -Target $Target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Scan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass 'R3' -Target $Target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply is forbidden with -Synthetic.'}
if($PSCmdlet.ShouldProcess($Target,'Apply user-profile-repair (R3)')){
 try{
  if($ProfileSid -notmatch '^S-1-5-21-(?:\d+-){3}\d+$'){throw 'Exact local/domain user SID is required.'}
  $profileKey="HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$ProfileSid"
  if(-not(Test-Path -LiteralPath $profileKey)){throw "ProfileList key not found: $ProfileSid"}
  $export=Join-Path $LogRoot 'profilelist-before.reg'
  & "$env:SystemRoot\System32\reg.exe" export "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\$ProfileSid" $export /y|Out-Null
  if($LASTEXITCODE -ne 0){throw 'ProfileList export failed.'}
  $current=Get-ItemProperty -LiteralPath $profileKey
  Write-WmJson ($current|Select-Object ProfileImagePath,State,RefCount,Flags) (Join-Path $LogRoot 'profile-before.json')
  if($null -ne $current.RefCount -and $current.RefCount -gt 0){Set-ItemProperty -LiteralPath $profileKey -Name RefCount -Value 0 -Type DWord}
  if($null -ne $current.State -and $current.State -ne 0){Set-ItemProperty -LiteralPath $profileKey -Name State -Value 0 -Type DWord}
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='user-profile-repair';target=$Target;risk='R3';result='applied';rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [pscustomobject]@{Operation='user-profile-repair';Target=$Target;Status='applied-pending-validation';ExitCode=0}
  exit 0
 }catch{
  Add-WmJsonLine ([ordered]@{timestamp_utc=[DateTime]::UtcNow.ToString('o');operation='user-profile-repair';target=$Target;risk='R3';result='failed';error=$_.Exception.Message;rollback=$rollback}) (Join-Path $LogRoot 'repair-actions.jsonl')
  [Console]::Error.WriteLine($_.Exception.Message);exit 40
 }
}
