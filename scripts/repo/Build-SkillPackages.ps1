<#
.SYNOPSIS Builds self-contained skill directories under dist/skills with shared resources copied in.
.EXAMPLE .\Build-SkillPackages.ps1
#>
[CmdletBinding(SupportsShouldProcess,ConfirmImpact='Low')]
param([string]$Destination)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$repo=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Import-Module (Join-Path $repo 'scripts\lib\WindowsMaster.Common.psm1') -Force
$source=Join-Path $repo '.agents\skills'
if(-not $Destination){$Destination=Join-Path $repo 'dist\skills'}
$dest=[IO.Path]::GetFullPath($Destination)
$skills=@(Get-ChildItem -LiteralPath $source -Directory|Where-Object Name -ne '_shared'|Sort-Object Name)
function Write-JsonUtf8Lf {
 param([Parameter(Mandatory)][object]$InputObject,[Parameter(Mandatory)][string]$Path)
 $json=$InputObject|ConvertTo-Json -Depth 20
 [IO.File]::WriteAllText($Path,$json.Replace("`r`n","`n")+"`n",[Text.UTF8Encoding]::new($false))
}
if($WhatIfPreference){
 [pscustomobject]@{Destination=$dest;Packages=$skills.Count;SharedCopied=$false;Planned=$true}
 return
}
if(Test-Path -LiteralPath $dest){
 $resolved=[IO.Path]::GetFullPath($dest)
 $repoResolved=[IO.Path]::GetFullPath($repo)
 if(-not $resolved.StartsWith($repoResolved,[StringComparison]::OrdinalIgnoreCase) -and -not $PSBoundParameters.ContainsKey('Destination')){throw 'Refusing to clean destination outside repository.'}
 if($PSCmdlet.ShouldProcess($resolved,'Replace package output')){Remove-Item -LiteralPath $resolved -Recurse -Force}
}
New-Item -ItemType Directory -Path $dest -Force|Out-Null
$shared=Join-Path $source '_shared'
$manifest=@()
foreach($skill in $skills){
 $target=Join-Path $dest $skill.Name
 Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse
 $sharedTarget=Join-Path $target 'references\_shared'
 Copy-Item -LiteralPath $shared -Destination $sharedTarget -Recurse
 if(Test-Path -LiteralPath (Join-Path $sharedTarget 'SKILL.md')){throw '_shared unexpectedly contains SKILL.md'}
 $files=@()
 foreach($file in Get-ChildItem -LiteralPath $target -File -Recurse|Sort-Object FullName){$files+=[ordered]@{path=(Get-WmRelativePath -BasePath $target -Path $file.FullName);sha256=(Get-FileHash $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant();bytes=$file.Length}}
 $entry=[ordered]@{skill=$skill.Name;path=(Get-WmRelativePath -BasePath $repo -Path $target);self_contained=$true;files=$files}
 Write-JsonUtf8Lf -InputObject $entry -Path (Join-Path $target 'package-manifest.json')
 $manifest+=$entry
}
Write-JsonUtf8Lf -InputObject $manifest -Path (Join-Path $dest 'packages.json')
[pscustomobject]@{Destination=$dest;Packages=$manifest.Count;SharedCopied=$true}
