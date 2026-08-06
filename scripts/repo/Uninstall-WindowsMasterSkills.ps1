<#
.SYNOPSIS Removes only files recorded by the installer manifest; modified files are preserved.
.EXAMPLE .\Uninstall-WindowsMasterSkills.ps1 -Scope User -RestoreBackup
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='High')]
param([ValidateSet('Repo','User')][string]$Scope='User',[string]$Destination,[switch]$RestoreBackup)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if(-not $Destination){$Destination=if($Scope -eq 'User'){Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'}else{Join-Path $repo '.agents\skills-installed'}}
$dest=[IO.Path]::GetFullPath($Destination);$manifestPath=Join-Path $dest '.windows-master-installed.json'
if(-not(Test-Path -LiteralPath $manifestPath)){throw "Install manifest not found: $manifestPath"}
$manifest=Get-Content -LiteralPath $manifestPath -Raw|ConvertFrom-Json
if([IO.Path]::GetFullPath($manifest.destination).TrimEnd('\') -ne $dest.TrimEnd('\')){throw 'Manifest destination mismatch.'}
$removed=0;$preserved=@()
foreach($entry in @($manifest.entries)){
 $target=[IO.Path]::GetFullPath($entry.target)
 if(-not $target.StartsWith($dest.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Unsafe target in manifest: $target"}
 if(-not(Test-Path -LiteralPath $target)){continue}
 if($entry.mode -eq 'Junction'){
  $item=Get-Item -LiteralPath $target -Force
  if(-not($item.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "Expected junction but found regular directory: $target"}
  if($PSCmdlet.ShouldProcess($target,'Remove installed junction')){Remove-Item -LiteralPath $target -Force;$removed++}
 }else{
  $changed=$false
  foreach($file in @($entry.files)){
   $path=Join-Path $dest $file.path
   if(Test-Path -LiteralPath $path){$hash=(Get-FileHash $path -Algorithm SHA256).Hash.ToLowerInvariant();if($hash -cne $file.sha256){$changed=$true;$preserved+=$path}}
  }
  if(-not $changed -and $PSCmdlet.ShouldProcess($target,'Remove unchanged installed skill directory')){Remove-Item -LiteralPath $target -Recurse -Force;$removed++}
 }
 if($RestoreBackup -and $entry.backup -and (Test-Path -LiteralPath $entry.backup) -and -not(Test-Path -LiteralPath $target)){
  if($PSCmdlet.ShouldProcess($entry.backup,"Restore backup to $target")){Move-Item -LiteralPath $entry.backup -Destination $target}
 }
}
if($preserved.Count -eq 0 -and $PSCmdlet.ShouldProcess($manifestPath,'Remove install manifest')){Remove-Item -LiteralPath $manifestPath -Force}
[pscustomobject]@{Destination=$dest;Removed=$removed;PreservedModified=@($preserved);BackupRestoreRequested=[bool]$RestoreBackup}
