<#
.SYNOPSIS Reads identity from an offline Windows SOFTWARE hive and always unloads it.
.EXAMPLE .\Get-OfflineWindowsIdentity.ps1 -WindowsPath D:\Windows -WhatIf
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Medium')]
param([Parameter(Mandatory)][ValidateScript({Test-Path -LiteralPath $_ -PathType Container})][string]$WindowsPath)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$hive=Join-Path $WindowsPath 'System32\config\SOFTWARE'
if(-not(Test-Path -LiteralPath $hive -PathType Leaf)){throw "SOFTWARE hive not found under: $WindowsPath"}
$mount='HKLM\WM_OFFLINE_{0}' -f ([guid]::NewGuid().ToString('N'))
$loaded=$false
try{
 if($PSCmdlet.ShouldProcess($hive,"Temporarily load read-only query hive at $mount")){
  & "$env:SystemRoot\System32\reg.exe" load $mount $hive|Out-Null
  if($LASTEXITCODE -ne 0){throw 'reg load failed'};$loaded=$true
  $path="Registry::$mount\Microsoft\Windows NT\CurrentVersion"
  Get-ItemProperty -LiteralPath $path|Select-Object ProductName,EditionID,CurrentBuild,CurrentBuildNumber,UBR,DisplayVersion,InstallationType
 }
}finally{if($loaded){& "$env:SystemRoot\System32\reg.exe" unload $mount|Out-Null}}
