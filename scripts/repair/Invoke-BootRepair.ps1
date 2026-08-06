<#
.SYNOPSIS Plans or applies an exact BCDBoot repair after UEFI/BIOS layout identification.
.DESCRIPTION R3. Apply requires exact OS/System volumes, backup, elevation, ShouldProcess and typed confirmation.
.EXAMPLE .\Invoke-BootRepair.ps1 -Mode Plan -OsVolume D: -SystemVolume S: -Firmware UEFI -LogRoot E:\case\logs
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param(
 [ValidateSet('Plan','Repair')][string]$Mode='Plan',
 [Parameter(Mandatory)][ValidatePattern('^[A-Za-z]:$')][string]$OsVolume,
 [Parameter(Mandatory)][ValidatePattern('^[A-Za-z]:$')][string]$SystemVolume,
 [Parameter(Mandatory)][ValidateSet('UEFI','BIOS','ALL')][string]$Firmware,
 [Parameter(Mandatory)][string]$LogRoot,
 [switch]$Apply,
 [string]$Confirmation,
 [switch]$Synthetic
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot);Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$target="$OsVolume->$SystemVolume/$Firmware"
$steps=@('verify disk UniqueId/partition roles/BitLocker','export existing BCD','run BCDBoot with explicit /s and /f','enumerate and cold-boot validate')
$rollback=@('restore exported BCD store','restore ESP file backup','restore firmware boot entry through supported OEM/BCDEdit path')
$plan=New-WmRepairPlan -Operation 'boot-files-bcd' -RiskClass R3 -Target $target -Steps $steps -Rollback $rollback -LogRoot $LogRoot -Synthetic:$Synthetic
if(-not $Apply -or $Mode -eq 'Plan'){$plan;exit 0}
Assert-WmApplyGate -Apply $true -RiskClass R3 -Target $target -Confirmation $Confirmation -RequireElevated
if($Synthetic){throw 'Apply forbidden in synthetic mode.'}
$windows=Join-Path $OsVolume 'Windows'
if(-not(Test-Path -LiteralPath (Join-Path $windows 'System32'))){throw "Verified Windows directory missing: $windows"}
if(-not(Test-Path -LiteralPath "$SystemVolume\")){throw "System volume missing: $SystemVolume"}
if($PSCmdlet.ShouldProcess($target,'Back up BCD and rebuild boot files')){
 $backup=Join-Path $LogRoot 'bcd-before'
 & "$env:SystemRoot\System32\bcdedit.exe" /export $backup
 if($LASTEXITCODE -ne 0){throw 'BCD export failed; repair stopped.'}
 & "$env:SystemRoot\System32\bcdboot.exe" $windows /s $SystemVolume /f $Firmware
 if($LASTEXITCODE -ne 0){throw "BCDBoot failed: $LASTEXITCODE"}
 [pscustomobject]@{Target=$target;Status='applied-pending-cold-boot-validation';Backup=$backup}
}
