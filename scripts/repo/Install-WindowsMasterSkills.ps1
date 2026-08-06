<#
.SYNOPSIS Installs Windows Master skills using Copy (default) or Junction with collision backup and a file manifest.
.EXAMPLE .\Install-WindowsMasterSkills.ps1 -Scope User -Mode Copy
.EXAMPLE .\Install-WindowsMasterSkills.ps1 -Destination C:\Temp\skills -Mode Copy
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Medium')]
param(
 [ValidateSet('Repo','User')][string]$Scope='User',
 [ValidateSet('Copy','Junction')][string]$Mode='Copy',
 [string]$Destination,
 [string]$Source
)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
if(-not $Source){
 $packaged=Join-Path $repo 'dist\skills'
 if(Test-Path -LiteralPath (Join-Path $packaged 'packages.json')){$Source=$packaged}else{$Source=Join-Path $repo '.agents\skills'}
}
if(-not $Destination){
 if($Scope -eq 'User'){$Destination=Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'}
 else{throw "Repo scope requires -Destination '<TARGET_REPO>\.agents\skills'. This repository already exposes .agents\skills directly."}
}
$sourceRoot=(Resolve-Path -LiteralPath $Source).Path;$dest=[IO.Path]::GetFullPath($Destination)
if([IO.Path]::GetFullPath($sourceRoot).TrimEnd('\') -eq $dest.TrimEnd('\')){throw 'Source and destination must differ.'}
$skills=@(Get-ChildItem -LiteralPath $sourceRoot -Directory|Where-Object Name -ne '_shared'|Sort-Object Name)
if($WhatIfPreference){
 [pscustomobject]@{Destination=$dest;Installed=0;Planned=$skills.Count;Mode=$Mode;Manifest=(Join-Path $dest '.windows-master-installed.json');Mutation=$false}
 return
}
New-Item -ItemType Directory -Path $dest -Force|Out-Null
$stamp=Get-Date -Format 'yyyyMMddHHmmss';$backupRoot=Join-Path $dest ".windows-master-backup-$stamp";$entries=@()
foreach($skill in $skills){
 $target=Join-Path $dest $skill.Name;$backup=$null
 if(Test-Path -LiteralPath $target){
  New-Item -ItemType Directory -Path $backupRoot -Force|Out-Null;$backup=Join-Path $backupRoot $skill.Name
  if($PSCmdlet.ShouldProcess($target,"Back up collision to $backup")){Move-Item -LiteralPath $target -Destination $backup}
 }
 if($PSCmdlet.ShouldProcess($target,"Install skill using $Mode")){
  if($Mode -eq 'Copy'){Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse}
  else{New-Item -ItemType Junction -Path $target -Target $skill.FullName|Out-Null}
 }
 $files=@()
 if($Mode -eq 'Copy'){foreach($file in Get-ChildItem -LiteralPath $target -File -Recurse){$files+=[ordered]@{path=(Get-WmRelativePath -BasePath $dest -Path $file.FullName);sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}}}
 $entries+=[ordered]@{name=$skill.Name;target=$target;mode=$Mode;source=$skill.FullName;backup=$backup;files=$files}
}
$manifest=[ordered]@{schema_version='1.0.0';installed_utc=[DateTime]::UtcNow.ToString('o');scope=$Scope;destination=$dest;source=$sourceRoot;entries=$entries}
$manifestPath=Join-Path $dest '.windows-master-installed.json'
$manifest|ConvertTo-Json -Depth 20|Set-Content -LiteralPath $manifestPath -Encoding utf8
[pscustomobject]@{Destination=$dest;Installed=$entries.Count;Mode=$Mode;Manifest=$manifestPath;Backup=$backupRoot}
