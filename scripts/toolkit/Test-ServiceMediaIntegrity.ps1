<#
.SYNOPSIS Verifies files against a provenance manifest without executing them.
.EXAMPLE .\Test-ServiceMediaIntegrity.ps1 -Root .\staging -ManifestPath .\staging\provenance.json
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$ManifestPath)
Set-StrictMode -Version Latest;$ErrorActionPreference='Stop'
$resolved=(Resolve-Path -LiteralPath $Root).Path;$manifest=Get-Content -LiteralPath (Resolve-Path -LiteralPath $ManifestPath) -Raw|ConvertFrom-Json
$results=@()
foreach($entry in @($manifest.files)){
 $path=Join-Path $resolved $entry.path
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){$results+=[pscustomobject]@{Path=$entry.path;Status='missing'};continue}
 $hash=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
 $status=if($hash -ceq $entry.sha256.ToLowerInvariant()){'ok'}else{'hash-mismatch'}
 $results+=[pscustomobject]@{Path=$entry.path;Status=$status;Sha256=$hash}
}
$results
if(@($results|Where-Object Status -ne 'ok').Count){exit 2}else{exit 0}
